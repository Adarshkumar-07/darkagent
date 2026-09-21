import React from 'react'; import type { Message } from './types';
export function MessageBubble({message}:{message:Message}) { return <article className={`bubble ${message.role}`}><span className="role">{message.role==='user'?'You':'Aegis'}</span><p>{message.content}</p><time>{new Date(message.timestamp).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</time></article>; }
