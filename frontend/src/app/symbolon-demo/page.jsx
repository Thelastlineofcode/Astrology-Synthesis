"use client";

import React, { useState, useEffect } from 'react';
import { SymbolonGrid } from '@/components/symbolon';

// Sample data based on the Symbolon card structure
const sampleCards = [
  {
    id: 1,
    number: 1,
    title: 'The Warrior',
    image: 'symbolon-01.jpg',
    keywords: ['Aggression', 'Conquest', 'Energy', 'New Beginning'],
    meaning: 'Underlying the problem is the anger and aggression you have not yet perceived and acknowledged. What has happened to this persona? Why do you hide its feelings?',
    interpretation: 'The task ahead of you involved becoming more instigative. You are being asked to act in order to unravel the Gordian knot holding you captive.',
    themes: ['Mars energy', 'Aries archetype', 'Initiating force', 'Warrior spirit']
  },
  {
    id: 2,
    number: 2,
    title: 'The Lover',
    image: 'symbolon-02.jpg',
    keywords: ['Worth', 'Attraction', 'Possession', 'Sociability'],
    meaning: 'You are a prisoner of your own feelings of worthlessness deep down inside. This under-estimation of your self must be allowed to come to the surface.',
    interpretation: 'The task is to develop feelings for yourself. You must learn to accept and appreciate yourself. This means seeing yourself in your entirety.',
    themes: ['Venus energy', 'Taurus archetype', 'Self-worth', 'Physical attraction']
  },
  {
    id: 3,
    number: 3,
    title: 'The Messenger',
    image: 'symbolon-03.jpg',
    keywords: ['Communication', 'Intelligence', 'Curiosity', 'Versatility'],
    meaning: 'The problem lies in your inability to understand and communicate effectively. You may be scattered or superficial in your approach to knowledge.',
    interpretation: 'The way forward involves developing your mental faculties and communication skills. Learn to listen and express yourself clearly.',
    themes: ['Mercury energy', 'Gemini archetype', 'Mental agility', 'Connection']
  },
  {
    id: 4,
    number: 4,
    title: 'The Mother',
    image: 'symbolon-04.jpg',
    keywords: ['Nurturing', 'Protection', 'Home', 'Emotions'],
    meaning: 'The challenge involves recognizing and healing your relationship with nurturing and emotional security.',
    interpretation: 'Embrace your nurturing side and create emotional safety for yourself and others. Honor your feelings and intuition.',
    themes: ['Moon energy', 'Cancer archetype', 'Maternal instinct', 'Emotional depth']
  },
  {
    id: 5,
    number: 5,
    title: 'The Hero',
    image: 'symbolon-05.jpg',
    keywords: ['Courage', 'Creativity', 'Leadership', 'Pride'],
    meaning: 'The issue relates to expressing your unique creative power and standing in your authentic light.',
    interpretation: 'Step into your power and express your creative essence. Lead with heart and courage.',
    themes: ['Sun energy', 'Leo archetype', 'Creative force', 'Self-expression']
  },
  {
    id: 6,
    number: 6,
    title: 'The Healer',
    image: 'symbolon-06.jpg',
    keywords: ['Service', 'Analysis', 'Purification', 'Health'],
    meaning: 'The challenge involves perfectionism and the need to serve or fix others at the expense of yourself.',
    interpretation: 'Learn to balance service with self-care. Develop discernment without becoming critical or judgmental.',
    themes: ['Mercury energy', 'Virgo archetype', 'Sacred service', 'Refinement']
  }
];

export default function SymbolonDemo() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{
      padding: '48px 24px',
      maxWidth: '1400px',
      margin: '0 auto',
      minHeight: '100vh'
    }}>
      <div style={{ marginBottom: '48px', textAlign: 'center' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          marginBottom: '16px',
          color: 'var(--color-primary)'
        }}>
          Symbolon Card Gallery
        </h1>
        <p style={{ 
          fontSize: '1.125rem', 
          color: 'var(--text-secondary)',
          maxWidth: '600px',
          margin: '0 auto'
        }}>
          Explore archetypal Symbolon cards for deep psychological and spiritual insights.
          Click any card to view its full interpretation.
        </p>
      </div>

      <SymbolonGrid cards={sampleCards} loading={loading} />

      <div style={{ 
        marginTop: '48px', 
        padding: '24px',
        background: 'var(--bg-secondary)',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <h2 style={{ 
          fontSize: '1.5rem', 
          marginBottom: '16px',
          color: 'var(--color-primary)'
        }}>
          About Symbolon Cards
        </h2>
        <p style={{ 
          color: 'var(--text-secondary)',
          lineHeight: '1.6',
          maxWidth: '800px',
          margin: '0 auto'
        }}>
          The Symbolon deck consists of 78 archetypal cards representing all possible 
          astrological combinations. Each card offers profound insights into personality, 
          life purpose, and psychological development through the lens of astrology and 
          depth psychology.
        </p>
      </div>
    </div>
  );
}
