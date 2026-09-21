import type { Message } from './types';
export type CommandContext = { clear:()=>void; newConversation:()=>void; stopSpeaking:()=>void; startListening:()=>void; openSettings:()=>void; closeSettings:()=>void; enableVoice:()=>void; disableVoice:()=>void };
type Command = { phrases: string[]; run: (context: CommandContext) => void };
export const commands: Command[] = [
 { phrases: ['clear conversation', 'clear chat'], run: c => c.clear() }, { phrases: ['new conversation', 'new chat'], run: c => c.newConversation() }, { phrases: ['stop speaking', 'stop talking'], run: c => c.stopSpeaking() }, { phrases: ['start listening'], run: c => c.startListening() }, { phrases: ['open settings'], run: c => c.openSettings() }, { phrases: ['close settings'], run: c => c.closeSettings() }, { phrases: ['enable voice'], run: c => c.enableVoice() }, { phrases: ['disable voice'], run: c => c.disableVoice() },
];
export function runLocalCommand(input: string, context: CommandContext): boolean { const normalized = input.trim().toLowerCase(); const command = commands.find(item => item.phrases.includes(normalized)); if (!command) return false; command.run(context); return true; }
export function isTimeCommand(input: string) { return ['time', 'what time is it', 'tell me the time'].includes(input.trim().toLowerCase()); }
export function timeReply() { return `It is ${new Intl.DateTimeFormat(undefined, { hour: 'numeric', minute: '2-digit' }).format(new Date())}.`; }
