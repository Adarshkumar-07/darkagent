export type Role = 'user' | 'assistant' | 'system';
export type AssistantState = 'IDLE' | 'LISTENING' | 'PROCESSING' | 'SPEAKING' | 'ERROR';
export type Message = { role: Role; content: string; timestamp: string };
export const now = () => new Date().toISOString();
