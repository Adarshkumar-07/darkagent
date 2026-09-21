import type { AssistantState } from './types';
export const transitions: Record<AssistantState, AssistantState[]> = { IDLE:['LISTENING','PROCESSING','ERROR'], LISTENING:['IDLE','PROCESSING','ERROR'], PROCESSING:['SPEAKING','IDLE','ERROR'], SPEAKING:['IDLE','LISTENING','ERROR'], ERROR:['IDLE','LISTENING'] };
export function canTransition(from: AssistantState, to: AssistantState) { return transitions[from].includes(to); }
