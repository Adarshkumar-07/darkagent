import { useCallback, useEffect, useMemo, useState } from 'react';

type Props = { onError: (message: string) => void; onFinished: () => void };
export function useVoice({ onError, onFinished }: Props) {
  const [supported, setSupported] = useState(true); const [speaking, setSpeaking] = useState(false); const [paused, setPaused] = useState(false); const [enabled, setEnabled] = useState(true); const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]); const [voiceName, setVoiceName] = useState(''); const [rate, setRate] = useState(1); const [pitch, setPitch] = useState(1);
  useEffect(() => {
    if (!('speechSynthesis' in window)) { setSupported(false); return; }
    const refresh = () => setVoices(window.speechSynthesis.getVoices()); refresh(); window.speechSynthesis.addEventListener('voiceschanged', refresh); return () => window.speechSynthesis.removeEventListener('voiceschanged', refresh);
  }, []);
  const selectedVoice = useMemo(() => voices.find(item => item.name === voiceName), [voices, voiceName]);
  const speak = useCallback((text: string) => {
    if (!enabled || !supported) { onFinished(); return; }
    window.speechSynthesis.cancel(); const utterance = new SpeechSynthesisUtterance(text); utterance.voice = selectedVoice || null; utterance.rate = rate; utterance.pitch = pitch;
    utterance.onstart = () => { setSpeaking(true); setPaused(false); }; utterance.onend = () => { setSpeaking(false); onFinished(); }; utterance.onerror = () => { setSpeaking(false); onError('Speech playback failed.'); onFinished(); }; window.speechSynthesis.speak(utterance);
  }, [enabled, supported, selectedVoice, rate, pitch, onError, onFinished]);
  const stop = useCallback(() => { if (supported) window.speechSynthesis.cancel(); setSpeaking(false); setPaused(false); onFinished(); }, [supported, onFinished]);
  return { supported, speaking, paused, enabled, setEnabled, voices, voiceName, setVoiceName, rate, setRate, pitch, setPitch, speak, pause: () => { window.speechSynthesis.pause(); setPaused(true); }, resume: () => { window.speechSynthesis.resume(); setPaused(false); }, stop };
}
