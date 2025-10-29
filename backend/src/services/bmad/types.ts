/**
 * BMAD Pattern Recognition Types
 * Defines types for Birthday, Month, and Day pattern analysis
 */

export interface BirthData {
  year: number;
  month: number; // 1-12
  day: number; // 1-31
  hour?: number; // 0-23
  minute?: number; // 0-59
}

export interface BMADPattern {
  id: string;
  name: string;
  description: string;
  category: PatternCategory;
  score: number; // 0-100
  weight: number; // 0-1
  confidence: number; // 0-1
  elements: PatternElement[];
  interpretation: string;
}

export enum PatternCategory {
  NUMERIC = 'numeric',
  CYCLIC = 'cyclic',
  HARMONIC = 'harmonic',
  SEQUENTIAL = 'sequential',
  MASTER_NUMBER = 'master_number',
  REPETITIVE = 'repetitive',
  SYMBOLIC = 'symbolic',
}

export interface PatternElement {
  type: 'day' | 'month' | 'year' | 'combined';
  value: number;
  significance: string;
}

export interface PatternAnalysisResult {
  birthData: BirthData;
  patterns: BMADPattern[];
  totalScore: number;
  dominantCategories: PatternCategory[];
  summary: string;
  timestamp: string;
}

export interface PatternRule {
  name: string;
  category: PatternCategory;
  weight: number;
  condition: (birthData: BirthData) => boolean;
  description: (birthData: BirthData) => string;
  interpretation: (birthData: BirthData) => string;
  elements: (birthData: BirthData) => PatternElement[];
}
