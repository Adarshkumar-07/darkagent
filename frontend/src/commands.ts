import type { Message } from './types';
export type CommandContext = { clear:()=>void; newConversation:()=>void; stopSpeaking:()=>void; startListening:()=>void; openSettings:()=>void; closeSettings:()=>void };
type Command = { phrases:string[]; run:(ctx:CommandContext)=>void };
export const commands: Command[] = [
 {phrases:['clear conversation'],run:c=>c.clear()}, {phrases:['new conversation'],run:c=>c.newConversation()}, {phrases:['stop speaking','stop talking'],run:c=>c.stopSpeaking()}, {phrases:['start listening'],run:c=>c.startListening()}, {phrases:['open settings'],run:c=>c.openSettings()}, {phrases:['close settings'],run:c=>c.closeSettings()},
];
export function runLocalCommand(input:string, context:CommandContext): boolean { const normalized=input.trim().toLowerCase(); const found=commands.find(c=>c.phrases.includes(normalized)); if (!found) return false; found.run(context); return true; }
export function timeReply(): string { return `It is ${new Intl.DateTimeFormat(undefined,{hour:'numeric',minute:'2-digit'}).format(new Date())}.`; }
export function isTimeCommand(input:string) { return ['what time is it','tell me the time'].includes(input.trim().toLowerCase()); }
