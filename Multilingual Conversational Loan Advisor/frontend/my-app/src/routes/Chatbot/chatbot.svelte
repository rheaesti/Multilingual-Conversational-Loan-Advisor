<script>
    import { onMount, tick } from "svelte";
    import { fade, fly, scale } from "svelte/transition";
    import { backOut } from "svelte/easing";
    import { getAuth, onAuthStateChanged } from "firebase/auth";
    import { gfmPlugin } from 'svelte-exmarkdown/gfm';
    import Markdown from "svelte-exmarkdown";
    import './style.css';

    let plugins = [gfmPlugin];
    let userId = null;
    let messages = [];
    let inputText = "";
    let isTyping = false;
    let theme = "dark"; // Keeping theme functionality but both themes are retro now
    let userName = "USER";
    let botName = "CHAT-BOT";
    let showEmojis = false;
    let emojis = ["😊", "😂", "👍", "❤️", "🤔", "👀", "🎉", "🔥", "✨", "🙌"];
    
    // Animation settings
    let animationEnabled = true;
    
    // Message suggestions
    let suggestions = [
        "Loan Eligibility Check",
        "Financial Literacy Tips",
        "Document Uploader",
        "Loan Application Form"
    ];


    // Audio recording variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let audioBlob;
    let audioURL;
    
    // Audio player variable
    let currentAudio = null;


    onMount(() => {
        const auth = getAuth();
        onAuthStateChanged(auth, (user) => {
            if (user) {
                userId = user.uid;  // Store the UID
                userName = user.displayName || "USER"; // Optional: Get user's display name
            } else {
                console.log("No user logged in.");
            }
        });
        setTimeout(() => {
            messages = [...messages, { 
                text: `WELCOME! I'M YOUR BANKING ASSISTANT. HOW CAN I HELP YOU TODAY?`, 
                sender: "bot" 
            }];
        }, 500);

        setupAudioRecording();
    });

    async function setupAudioRecording() {
        try {
            // Request microphone permissions
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Create media recorder instance
            mediaRecorder = new MediaRecorder(stream);
            
            // Event handlers for the media recorder
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                // Create blob from recorded chunks
                audioBlob = new Blob(audioChunks, { 'type': 'audio/WebM' });
                audioURL = URL.createObjectURL(audioBlob);
                
                // Process the recorded audio
                await processAudioRecording();
                
                // Reset for next recording
                audioChunks = [];
            };
            
        } catch (err) {
            console.error("Error accessing microphone:", err);
            messages = [...messages, { 
                text: "ERROR! MICROPHONE ACCESS DENIED. PLEASE CHECK PERMISSIONS.", 
                sender: "bot", 
                isError: true,
                timestamp: new Date() 
            }];
        }
    }

    function startRecording() {
        if (mediaRecorder && mediaRecorder.state === "inactive") {
            isRecording = true;
            mediaRecorder.start();
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            isRecording = false;
            mediaRecorder.stop();
        }
    }

    // Function to play audio for a message
    function playAudio(url) {
    let audio = new Audio(url);
    audio.play();
}

    async function processAudioRecording() {
        try {
            isTyping = true;
            await tick();
            scrollToBottom();
            
            // Create FormData to send the audio file
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.WebM');
            formData.append('userId', userId || 'anonymous');
            console.log(audioBlob.type);
            
            // Send to backend for processing
            const response = await fetch('http://127.0.0.1:5000/process-audio', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.transcription && data.transcription.transcript) {
                // Add transcribed message to chat - using transcript field from transcription object
                messages = [...messages, { 
                    text: data.transcription.transcript, 
                    sender: "user", 
                    timestamp: new Date(),
                    isTranscribed: true,
                }];
                
                await tick();
                scrollToBottom();
                
                // Process the bot response
                setTimeout(() => {
                    isTyping = false;
                    if (data.response) {
                        // Add bot response with audio URL
                        const audioUrl = `http://127.0.0.1:5000${data.audio_url}`;
                        
                        messages = [...messages, { 
                            text: data.response, 
                            sender: "bot", 
                            timestamp: new Date(),
                            audioUrl: data.audio_url
                        }];
                        
                        tick().then(() => {
                            scrollToBottom();
                            // Automatically play the audio response
                            playAudio(audioUrl);
                        });
                    }
                }, 1000);
            } else {
                isTyping = false;
                messages = [...messages, { 
                    text: "TRANSCRIPTION ERROR. PLEASE TRY AGAIN OR TYPE YOUR MESSAGE.", 
                    sender: "bot", 
                    isError: true,
                    timestamp: new Date() 
                }];
            }
            
        } catch (error) {
            console.error("Error processing audio:", error);
            isTyping = false;
            messages = [...messages, { 
                text: "ERROR PROCESSING AUDIO. CONNECTION FAILED.", 
                sender: "bot", 
                isError: true,
                timestamp: new Date() 
            }];
        }
        
        await tick();
        scrollToBottom();
    }

    async function sendMessage(text = inputText) {
    if (!text.trim()) return; // Prevent sending empty messages

    // Add user message with animation
    messages = [...messages, { text, sender: "user", timestamp: new Date() }];
    let userMessage = text;
    inputText = "";  // Clear input after sending
    isTyping = true;
    await tick(); 

    // Auto-scroll to bottom
    scrollToBottom();

    try {
        let res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage, name: userId }),
        });

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }

        let data = await res.json();

        // Ensure `audio_url` is properly handled
        let audioUrl = data.audio_url ? `http://127.0.0.1:5000/generated_audio/${data.audio_url}` : null;

        // Simulate typing effect before showing bot response
        setTimeout(() => {
            isTyping = false;
            
            // Add bot response
            messages = [...messages, { 
                text: data.response, 
                sender: "bot", 
                timestamp: new Date(),
                audioUrl: audioUrl
            }];

            tick().then(() => {
                scrollToBottom();
                
                // Play bot response audio if available
                if (audioUrl) {
                    playAudio(audioUrl);
                }
            });
        }, 1000); // Adds a delay for a more natural typing effect

    } catch (error) {
        console.error("Error sending message:", error);
        isTyping = false;
        
        // Display error message in chat
        messages = [...messages, { 
            text: "⚠ ERROR: Connection failed. Please try again later.", 
            sender: "bot", 
            isError: true,
            timestamp: new Date() 
        }];

        await tick();
        scrollToBottom();
    }
}


    function scrollToBottom() {
        setTimeout(() => {
            let chatContainer = document.querySelector(".chat-container");
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }, 100);
    }

    function toggleTheme() {
        theme = theme === "dark" ? "light" : "dark";
        // In our retro theme, both light and dark are similar
    }

    function addEmoji(emoji) {
        inputText += emoji;
        showEmojis = false;
    }

    function formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function clearChat() {
        messages = [];
        // Add welcome message again with retro styling
        setTimeout(() => {
            messages = [...messages, { 
                text: `SYSTEM CLEARED! HOW MAY I ASSIST YOU?`, 
                sender: "bot" 
            }];
        }, 300);
    }
</script>

<style>
    .suggestion-chips {
       position: sticky;
       bottom: 60px;
       z-index: 10;
       background-color: inherit;
       padding: 10px 0;
       /* No changes to the actual button styling */
   }
   
   /* Adjust chat container to accommodate always-visible suggestions */
   .chat-container {
       max-height: calc(100vh - 180px);
   }
</style>

<div class="chat-app {theme}-theme">
    <div class="chat-header">
        <div class="logo">
            <span class="icon">💾</span>
            <h1>BANKING TERMINAL</h1>
        </div>
        <div class="controls">
            <button class="theme-toggle" on:click={toggleTheme}>
                {theme === "dark" ? "🌙" : "☀️"}
            </button>
            <button class="clear-chat" on:click={clearChat}>
                🗑️
            </button>
        </div>
    </div>

    <div class="chat-wrapper">
        <div class="chat-container">
            {#if messages.length === 0}
                <div class="empty-chat">
                    <div class="welcome" transition:scale>
                        <div class="welcome-icon">💻</div>
                        <h2>WELCOME TO BANK-OS v1.0</h2>
                        <p>INITIALIZING BANKING ASSISTANT...</p>
                        <div class="progress-bar">
                            <div class="progress-bar-filled" style="width: 35%;"></div>
                        </div>
                    </div>
                </div>
            {/if}
            
            {#each messages as msg, i (i)}
                <div 
                    class="message-wrapper {msg.sender}-wrapper"
                    in:fly={{y: 20, duration: animationEnabled ? 300 : 0, delay: animationEnabled ? 100 : 0}}
                >
                    <div class="avatar">
                        {msg.sender === "user" ? "👤" : "💾"}
                    </div>
                    <div class="message-content">
                        <div class="message-header">
                            <span class="sender-name">{msg.sender === "user" ? userName : botName}</span>
                            {#if msg.isTranscribed}
                                <span class="transcribed-tag">TRANSCRIBED</span>
                            {/if}
                            {#if msg.timestamp}
                                <span class="timestamp">{formatTime(msg.timestamp)}</span>
                            {/if}
                            
                            <!-- Add audio control button if message has audio -->
                            {#if msg.audioUrl}
                                <button 
                                    class="audio-control-button" 
                                    on:click={() => playAudio(msg.audioUrl)}
                                    title="PLAY AUDIO">
                                    🔊
                                </button>
                            {/if}
                        </div>
                        <div class="message {msg.sender} {msg.isError ? 'error' : ''}" 
                             in:fade={{duration: animationEnabled ? 200 : 0}}>
                             <Markdown md={msg.text} {plugins} />
                        </div>
                    </div>
                </div>
            {/each}

            {#if isTyping}
                <div class="message-wrapper bot-wrapper" in:fly={{y: 10, duration: 200}}>
                    <div class="avatar">💾</div>
                    <div class="typing-indicator">
                        <div class="typing-bubble"></div>
                        <div class="typing-bubble"></div>
                        <div class="typing-bubble"></div>
                    </div>
                </div>
            {/if}
        </div>

        <!-- Suggestion chips are now always visible but with original styling -->
        <div class="suggestion-chips">
            {#each suggestions as suggestion}
                {#if suggestion === "Loan Eligibility Check"}
                    <button 
                        class="suggestion-chip"
                        on:click={() => window.location.href = '/loaneligible'}
                        in:scale={{duration: 200, delay: 300, easing: backOut}}
                    >
                        {suggestion}
                    </button>
                {:else if suggestion === "Document Uploader"}
                    <button 
                        class="suggestion-chip"
                        on:click={() => window.location.href = '/document'}
                        in:scale={{duration: 200, delay: 300, easing: backOut}}
                    >
                        {suggestion}
                    </button>
                {:else if suggestion === "Loan Application Form"}
                    <button 
                        class="suggestion-chip"
                        on:click={() => window.location.href = '/from'}
                        in:scale={{duration: 200, delay: 300, easing: backOut}}
                    >
                        {suggestion}
                    </button>
                {:else}
                    <button 
                        class="suggestion-chip"
                        on:click={() => sendMessage(suggestion)}
                        in:scale={{duration: 200, delay: 300, easing: backOut}}
                    >
                        {suggestion}
                    </button>
                {/if}
            {/each}
        </div>
   \

        <div class="input-container">
            <button class="emoji-button" on:click={() => showEmojis = !showEmojis}>
                😊
            </button>
            
            {#if showEmojis}
                <div class="emoji-picker" transition:scale={{duration: 150}}>
                    {#each emojis as emoji}
                        <button class="emoji" on:click={() => addEmoji(emoji)}>
                            {emoji}
                        </button>
                    {/each}
                </div>
            {/if}

            <!-- Audio recording button -->
            <button 
                class="audio-button {isRecording ? 'recording' : ''}" 
                on:mousedown={startRecording}
                on:mouseup={stopRecording}
                on:mouseleave={isRecording ? stopRecording : null}
                title={isRecording ? "RELEASE TO STOP" : "HOLD TO RECORD"}
            >
                {isRecording ? "🔴" : "🎙️"}
            </button>
            
            <input 
                bind:value={inputText} 
                on:keydown={(e) => e.key === 'Enter' && sendMessage()} 
                placeholder="TYPE YOUR MESSAGE..." 
            />
            <button class="send-button" on:click={sendMessage} disabled={!inputText.trim()}>
                <span class="send-icon">➤</span>
            </button>
        </div>
    </div>
</div>


