import type { Message } from './types';
const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export async function chat(message: string, conversation: Message[], signal?: AbortSignal): Promise<{reply:string;conversation:Message[]}> {
 const response = await fetch(`${base}/api/chat`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message, conversation}), signal });
 let data: unknown; try { data = await response.json(); } catch { throw new Error('The server returned an invalid response.'); }
 if (!response.ok) { const detail = typeof data === 'object' && data !== null && 'detail' in data ? String((data as {detail:unknown}).detail) : 'Request failed.'; throw new Error(response.status === 429 ? 'Too many requests. Please wait a moment.' : detail); }
 if (typeof data !== 'object' || data === null || !('reply' in data) || typeof (data as {reply:unknown}).reply !== 'string') throw new Error('The server returned an invalid response.');
 return data as {reply:string;conversation:Message[]};
}
