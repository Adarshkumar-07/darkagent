import { useEffect, useRef, useState } from 'react';
export function useSpeech(onFinal:(text:string)=>void,onError:(message:string)=>void) {
 const recognition=useRef<any>(null); const [supported,setSupported]=useState(true); const [listening,setListening]=useState(false); const [interim,setInterim]=useState('');
 useEffect(()=>{ const API=(window as any).SpeechRecognition||(window as any).webkitSpeechRecognition; if(!API){setSupported(false);return;} const r=new API(); r.continuous=false;r.interimResults=true;r.lang='en-US'; r.onstart=()=>setListening(true); r.onend=()=>{setListening(false);setInterim('')}; r.onerror=(e:any)=>{setListening(false);onError(e.error==='not-allowed'?'Microphone permission was denied.':'Speech recognition failed.')}; r.onresult=(e:any)=>{let final='';let live='';for(let i=e.resultIndex;i<e.results.length;i++){const text=e.results[i][0].transcript;if(e.results[i].isFinal)final+=text;else live+=text;}setInterim(live);if(final.trim())onFinal(final.trim())}; recognition.current=r; return()=>{r.abort()};},[onFinal,onError]);
 return {supported,listening,interim,start:()=>{try{recognition.current?.start()}catch{}},stop:()=>recognition.current?.stop()};
}
