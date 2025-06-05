// Import the functions you need from the SDKs you need
import { deleteApp, getApps,getApp ,initializeApp } from "firebase/app";
import {getAuth, setPersistence , inMemoryPersistence} from 'firebase/auth';

const firebaseConfig = {
    apiKey: [Google Gemini -  API_KEY],
    authDomain: "whatsapp-database-ca425.firebaseapp.com",
    databaseURL: "https://whatsapp-database-ca425-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "whatsapp-database-ca425",
    storageBucket: "whatsapp-database-ca425.appspot.com",
    messagingSenderId: "778958316532",
    appId: "1:778958316532:web:3ecab3c81655bf7830cfa1",
    measurementId: "G-7SW4ZSV19E"
  };
  

// Initialize Firebase
let firebaseApp;
if (!getApps().length){
    firebaseApp = initializeApp (firebaseConfig)
}
else{
    firebaseApp = getApp()
    deleteApp(firebaseApp)
    firebaseApp = initializeApp(firebaseConfig)
}



export const auth = getAuth(firebaseApp)
