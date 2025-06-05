from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END, MessagesState  # this is a class which stores messages in a list and has the add_messages helper function
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import sarvam_stuff
import os

temp = open('apis/api_keys.JSON')
api_keys = sarvam_stuff.json.load(temp)

Gemini_api = api_keys["GEMINI_API"]
os.environ["GOOGLE_API_KEY"] = Gemini_api #storing the API key



# Initializing the Firebase DB
cred = credentials.Certificate("apis\whatsapp-database-ca425-firebase-adminsdk-pyx9y-b4037c9675.json")
firebase_admin.initialize_app(cred)
ref = db.reference(
    'ChatHistory/', url='https://whatsapp-database-ca425-default-rtdb.asia-southeast1.firebasedatabase.app/'
)

ref.update({"THIS":"NO TOUCH"})

temp_chat_history = []  # For temporarily storing the chat history before sending it to Firebase

# Initializing the model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    max_tokens=None,
    max_retries=2
)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a helpful assistant, DO NOT USER MARKDOWN SYNTAX",
        ),
        ("human", "{input}"),
    ]
)

llm = prompt | model  # The final chain created ADD RAG LATER

#embeddings for RAG and get the saved stored vector storr
embeddings = VertexAIEmbeddings(model_name="text-embedding-005")
vector_store = FAISS.load_local("ffais_index", embeddings, allow_dangerous_deserialization=True)

#tools
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

@tool(response_format="content")
def loan(query: str):
    """click on loan eligibility to check if you are eligible for a loan"""
    res = "Click on Loan eligibility below the chat"
    return res

@tool(response_format="content")
def document(query: str):
    """click on document uploader to upload documents"""
    res = "Click on document uploader below the chat"
    return res

@tool(response_format="content")
def form(query: str):
    """click on loan application form to apply for a loan"""
    res = "Click on form application below the chat"
    return res

# Creating the GRAPH
graphbuilder = StateGraph(state_schema=MessagesState)  # Initialized da graph


# Converting to JSON serial killer
def convert_to_json(chat_history: list, session_id: str):
    Json_chat_history = {
        session_id : [
            {"role" : "human" if isinstance(msg, HumanMessage) else "ai" if isinstance(msg, AIMessage) else "tool", "content" : msg.content} for msg in chat_history.messages
        ]
    }
    return Json_chat_history


# Converting from JSON killer to InMemoryChatMessageHistory
def convert_to_inmemory(chat_history: list, session_id : str):
    notjson_list = InMemoryChatMessageHistory()
    for chat in chat_history:
        if chat["role"] == "human":
            notjson_list.add_user_message(chat["content"])
        else:
            notjson_list.add_ai_message(chat["content"])
    return notjson_list


# Getting the chat history
def get_chat_history(session_id: str):
    chats_by_session_id = ref.get()  # Getting all the session_ID with their values

    if session_id not in chats_by_session_id:
        chat_history = InMemoryChatMessageHistory()  # Getting the chat history
        json_chat = convert_to_json(chat_history , session_id)
        ref.update(json_chat)
    else:
        chat_history = chats_by_session_id.get(session_id)
        chat_history = convert_to_inmemory(chat_history, session_id)
        
    return chat_history


# Defining a function that calls the model (passing the current state as the input)
def Call_model(state: MessagesState, config: RunnableConfig):
    # Checking if there is a session ID in the config
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    history = get_chat_history(config["configurable"]["session_id"])

    model_with_tools = model.bind_tools([retrieve,loan, document, form])
    llm_with_tools = prompt|model_with_tools #making a new chain

    messages = list(history.messages) + state["messages"]
    ai_message = llm_with_tools.invoke(messages)
    history.add_messages(state["messages"] + [ai_message])
    json_history = convert_to_json(history, config["configurable"]["session_id"])
    ref.update(json_history)
    return {"messages":ai_message}

tools = ToolNode([retrieve,loan, document, form])

def generate(state: MessagesState, config: RunnableConfig):
    print("IT IS COMING HEREEE GOIWEGIOWEHGIOWEHGWEIOGIOWEH")
    """Generate answer with history storage and updating."""
    # Checking if there is a session ID in the config
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    
    session_id = config["configurable"]["session_id"]
    history = get_chat_history(session_id)
    
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]
    
    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
       "You are an assistant for question-answering tasks. "
    "Use the following retrieved context as well as your general knowledge to answer "
    "the question. If part of the answer is not found in the context, feel free to supplement with what you know. "
    "Answer in 4 to 6 sentences and add as much information as you can to it "
    "IF THERE ANY MESSAGE THAT'S RELATED TO HOW TO USE THIS MANUAL IGNORE THEM AND GIVE THEM ONLY USEFUL TIPS"
    "\n\n"
    f"{docs_content}"
    )
    
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    
    prompt = [SystemMessage(system_message_content)] + conversation_messages
    
    # Bind model with tools
    llm_with_tools = model.bind_tools([retrieve,loan, document, form])
    
    # Generate response
    ai_message = llm_with_tools.invoke(prompt)
    
    # Update history
    history.add_messages(state["messages"] + [ai_message])
    json_history = convert_to_json(history, session_id)
    ref.update(json_history)
    
    return {"messages": [ai_message]}


#creating edges and nodes
graphbuilder.add_node(Call_model)
graphbuilder.add_node(tools)
graphbuilder.add_node(generate)

graphbuilder.set_entry_point("Call_model")
graphbuilder.add_conditional_edges(
    "Call_model",
    tools_condition,
    {END: END, "tools": "tools"},
)
graphbuilder.add_edge("tools", "generate")
graphbuilder.add_edge("generate", END)

#compiling the graph
graph = graphbuilder.compile()

#sending the input to the graph and updating history an storing in DB 
def get_response(session_id: str, input_message):
    config = {"configurable": {"session_id": session_id}}
    res = graph.invoke({"messages": [input_message]}, config, stream_mode="values")
    print(res)
    return res["messages"][-1].content


def put_in_db(key,values):
    ref = db.reference(
    'loan_moment/', url='https://whatsapp-database-ca425-default-rtdb.asia-southeast1.firebasedatabase.app/')
    ref.update({"DON:T":"REMOVE"})
    ref.update({key:values})
    return 0
