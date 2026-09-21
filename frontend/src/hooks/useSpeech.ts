import { useCallback, useEffect, useRef, useState } from 'react';

type Recognition = { continuous: boolean; interimResults: boolean; lang: string; onstart: (() => void) | null; onend: (() => void) | null; onerror: ((event: { error?: string }) => void) | null; onresult: ((event: any) => void) | null; start: () => void; stop: () => void; abort: () => void };

type Props = { onFinal: (text: string) => void; onError: (message: string) => void };

export function useSpeech({ onFinal, onError }: Props) {
  const recognition = useRef<Recognition | null>(null);
  const onFinalRef = useRef(onFinal);
  const onErrorRef = useRef(onError);
  const [supported, setSupported] = useState(true);
  const [listening, setListening] = useState(false);
  const [interim, setInterim] = useState('');

  useEffect(() => { onFinalRef.current = onFinal; }, [onFinal]);
  useEffect(() => { onErrorRef.current = onError; }, [onError]);

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) { setSupported(false); return; }
    const instance = new SpeechRecognition() as Recognition;
    instance.continuous = false; instance.interimResults = true; instance.lang = 'en-US';
    instance.onstart = () => setListening(true);
    instance.onend = () => { setListening(false); setInterim(''); };
    instance.onerror = (event) => {
      setListening(false);
      const message = event.error === 'not-allowed' || event.error === 'service-not-allowed'
        ? 'Microphone permission was denied. Check your browser settings.'
        : event.error === 'no-speech' ? 'I did not hear anything. Try again.' : 'Speech recognition failed.';
      onErrorRef.current(message);
    };
    instance.onresult = (event) => {
      let finalText = ''; let interimText = '';
      for (let index = event.resultIndex; index < event.results.length; index += 1) {
        const text = event.results[index][0].transcript;
        if (event.results[index].isFinal) finalText += text; else interimText += text;
      }
      setInterim(interimText);
      if (finalText.trim()) onFinalRef.current(finalText.trim());
    };
    recognition.current = instance;
    return () => { instance.abort(); recognition.current = null; };
  }, []);

  const start = useCallback(() => {
    if (!recognition.current || listening) return;
    try { recognition.current.start(); } catch { /* browsers throw when already active */ }
  }, [listening]);
  const stop = useCallback(() => recognition.current?.stop(), []);
  return { supported, listening, interim, start, stop };
}
