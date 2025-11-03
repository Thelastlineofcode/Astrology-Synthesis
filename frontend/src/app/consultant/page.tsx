"use client";

import React, { useState, useRef, useEffect } from 'react';
import './consultant.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface Advisor {
  id: string;
  name: string;
  title: string;
  symbol: string;
  description: string;
  color: string;
}

const ADVISORS: Advisor[] = [
  {
    id: 'papa-legba',
    name: 'Papa Legba',
    title: 'The Gatekeeper',
    symbol: '🗝️',
    description: 'Crossroads guidance, new opportunities, life decisions',
    color: '#E8B598'
  },
  {
    id: 'erzulie-freda',
    name: 'Erzulie Freda',
    title: 'Goddess of Love',
    symbol: '💝',
    description: 'Love, relationships, beauty, self-care',
    color: '#E86F4D'
  },
  {
    id: 'baron-samedi',
    name: 'Baron Samedi',
    title: 'Lord of Death',
    symbol: '💀',
    description: 'Shadow work, transformation, humor, endings',
    color: '#8B6FA8'
  },
  {
    id: 'ogoun',
    name: 'Ogoun',
    title: 'Warrior Spirit',
    symbol: '⚔️',
    description: 'Career, strength, conflict resolution, victory',
    color: '#5FA9B8'
  }
];

export default function ConsultantPage() {
  const [selectedAdvisor, setSelectedAdvisor] = useState<Advisor>(ADVISORS[0]);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `Ayibobo! I am ${ADVISORS[0].name}, ${ADVISORS[0].title}. I stand at the crossroads where all paths meet. What guidance do you seek today, child?`,
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleAdvisorChange = (advisor: Advisor) => {
    setSelectedAdvisor(advisor);
    setMessages([
      {
        id: Date.now().toString(),
        role: 'assistant',
        content: `Ayibobo! I am ${advisor.name}, ${advisor.title}. ${getAdvisorGreeting(advisor.id)}`,
        timestamp: new Date()
      }
    ]);
  };

  const getAdvisorGreeting = (advisorId: string): string => {
    switch (advisorId) {
      case 'papa-legba':
        return 'I stand at the crossroads where all paths meet. What guidance do you seek today, child?';
      case 'erzulie-freda':
        return 'Love and beauty surround you. Open your heart and share what troubles your spirit.';
      case 'baron-samedi':
        return 'Death is not an end, but a transformation. What shadows do you wish to illuminate?';
      case 'ogoun':
        return 'I bring the fire of courage and strength. What battles do you face, warrior?';
      default:
        return 'How may I guide you today?';
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate API call (replace with actual backend call)
    setTimeout(() => {
      const responses: Record<string, string[]> = {
        'papa-legba': [
          'The crossroads before you hold many possibilities. Trust your intuition to choose the path that calls to your spirit.',
          'New opportunities are opening, but you must first close the door on what no longer serves you.',
          'The key to your question lies in understanding that every ending is a new beginning.'
        ],
        'erzulie-freda': [
          'Self-love is the foundation of all other love. Honor yourself first, and others will follow.',
          'Beauty is not just what you see, but what you feel within. Nurture your inner radiance.',
          'Love requires both strength and softness. Open your heart while keeping your boundaries clear.'
        ],
        'baron-samedi': [
          'What you fear most is often what you need to embrace. Dance with your shadows.',
          'Death clears the way for rebirth. Release what weighs you down, and rise renewed.',
          'Humor is the medicine for the soul. Do not take yourself too seriously in this game of life.'
        ],
        'ogoun': [
          'Victory comes to those who stand firm. Do not retreat from the battle that shapes you.',
          'Your strength is greater than you know. Channel your fire with purpose and discipline.',
          'Conflict is not your enemy—it is your teacher. Learn what it has to show you.'
        ]
      };

      const advisorResponses = responses[selectedAdvisor.id] || [];
      const response = advisorResponses[Math.floor(Math.random() * advisorResponses.length)];

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="consultant-page">
      {/* Header */}
      <div className="consultant-header">
        <button className="back-button" onClick={() => window.history.back()}>
          ← Back
        </button>
        <h1 className="consultant-title">Spiritual Consultant</h1>
        <div className="header-spacer"></div>
      </div>

      {/* Advisor Selector */}
      <div className="advisor-selector">
        <h2 className="selector-title">Choose Your Guide</h2>
        <div className="advisor-grid">
          {ADVISORS.map(advisor => (
            <button
              key={advisor.id}
              className={`advisor-card ${selectedAdvisor.id === advisor.id ? 'active' : ''}`}
              onClick={() => handleAdvisorChange(advisor)}
              style={{
                borderColor: selectedAdvisor.id === advisor.id ? advisor.color : 'transparent'
              }}
            >
              <span className="advisor-symbol">{advisor.symbol}</span>
              <h3 className="advisor-name">{advisor.name}</h3>
              <p className="advisor-description">{advisor.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Container */}
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map(message => (
            <div
              key={message.id}
              className={`message ${message.role === 'user' ? 'message-user' : 'message-assistant'}`}
            >
              {message.role === 'assistant' && (
                <div className="message-avatar" style={{ backgroundColor: selectedAdvisor.color }}>
                  {selectedAdvisor.symbol}
                </div>
              )}
              <div className="message-content">
                <p className="message-text">{message.content}</p>
                <span className="message-time">
                  {message.timestamp.toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                  })}
                </span>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message message-assistant">
              <div className="message-avatar" style={{ backgroundColor: selectedAdvisor.color }}>
                {selectedAdvisor.symbol}
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="chat-input-container">
          <textarea
            className="chat-input"
            placeholder={`Ask ${selectedAdvisor.name} for guidance...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            rows={1}
            disabled={isLoading}
          />
          <button
            className="send-button"
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            aria-label="Send message"
          >
            ↑
          </button>
        </div>
      </div>

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <button className="nav-item" onClick={() => window.location.href = '/dashboard'}>
          <span className="nav-icon">🔍</span>
          <span className="nav-label">Discover</span>
        </button>
        <button className="nav-item" onClick={() => window.location.href = '/fortune'}>
          <span className="nav-icon">🎴</span>
          <span className="nav-label">Fortune</span>
        </button>
        <button className="nav-item active">
          <span className="nav-icon">💬</span>
          <span className="nav-label">Consultant</span>
        </button>
        <button className="nav-item" onClick={() => window.location.href = '/chart-demo'}>
          <span className="nav-icon">📊</span>
          <span className="nav-label">Chart</span>
        </button>
        <button className="nav-item" onClick={() => window.location.href = '/profile'}>
          <span className="nav-icon">👤</span>
          <span className="nav-label">Profile</span>
        </button>
      </nav>
    </div>
  );
}
