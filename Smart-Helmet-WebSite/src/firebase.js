// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDwGKEPfwVE3CFtu_zJHA1TvT19UooPKj0",
  authDomain: "smarthelmet-3a072.firebaseapp.com",
  databaseURL: "https://smarthelmet-3a072-default-rtdb.firebaseio.com",
  projectId: "smarthelmet-3a072",
  storageBucket: "smarthelmet-3a072.firebasestorage.app",
  messagingSenderId: "68344745037",
  appId: "1:68344745037:web:243341a3a2c5b287c4e004",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Export firestore database
// It will be imported into your react app whenever it is needed
export const db = getFirestore(app);
