/**
 * BMAD Pattern Recognition Engine
 * Core algorithm for identifying and scoring astrological patterns in birth data
 */

import { randomUUID } from 'crypto';
import { BirthData, BMADPattern, PatternAnalysisResult, PatternCategory } from './types';
import { patternRules } from './patternRules';

export class BMADPatternRecognizer {
  /**
   * Validate birth data
   */
  private validateBirthData(birthData: BirthData): void {
    if (!birthData.year || birthData.year < 1900 || birthData.year > 2100) {
      throw new Error('Invalid year: must be between 1900 and 2100');
    }

    if (!birthData.month || birthData.month < 1 || birthData.month > 12) {
      throw new Error('Invalid month: must be between 1 and 12');
    }

    if (!birthData.day || birthData.day < 1 || birthData.day > 31) {
      throw new Error('Invalid day: must be between 1 and 31');
    }

    // Validate day for specific month
    const daysInMonth = new Date(birthData.year, birthData.month, 0).getDate();
    if (birthData.day > daysInMonth) {
      throw new Error(
        `Invalid day: ${birthData.day} exceeds days in month ${birthData.month} (${daysInMonth} days)`
      );
    }

    if (birthData.hour !== undefined && (birthData.hour < 0 || birthData.hour > 23)) {
      throw new Error('Invalid hour: must be between 0 and 23');
    }

    if (birthData.minute !== undefined && (birthData.minute < 0 || birthData.minute > 59)) {
      throw new Error('Invalid minute: must be between 0 and 59');
    }
  }

  /**
   * Calculate pattern score based on weight and confidence
   */
  private calculateScore(weight: number, confidence: number): number {
    return Math.round(weight * confidence * 100);
  }

  /**
   * Calculate confidence based on pattern strength
   */
  private calculateConfidence(_birthData: BirthData, ruleName: string): number {
    // Base confidence
    let confidence = 0.85;

    // Adjust based on specific patterns
    if (ruleName.includes('Master')) {
      confidence = 0.95;
    } else if (ruleName.includes('Sequential')) {
      confidence = 0.9;
    } else if (ruleName.includes('Harmonic')) {
      confidence = 0.88;
    }

    return confidence;
  }

  /**
   * Detect all patterns in birth data
   */
  public detectPatterns(birthData: BirthData): BMADPattern[] {
    this.validateBirthData(birthData);

    const patterns: BMADPattern[] = [];

    for (const rule of patternRules) {
      try {
        if (rule.condition(birthData)) {
          const confidence = this.calculateConfidence(birthData, rule.name);
          const score = this.calculateScore(rule.weight, confidence);

          const pattern: BMADPattern = {
            id: randomUUID(),
            name: rule.name,
            description: rule.description(birthData),
            category: rule.category,
            score,
            weight: rule.weight,
            confidence,
            elements: rule.elements(birthData),
            interpretation: rule.interpretation(birthData),
          };

          patterns.push(pattern);
        }
      } catch (error) {
        // Skip patterns that fail evaluation
        console.warn(`Pattern ${rule.name} evaluation failed:`, error);
      }
    }

    // Sort patterns by score (highest first)
    return patterns.sort((a, b) => b.score - a.score);
  }

  /**
   * Analyze birth data and return complete analysis
   */
  public analyze(birthData: BirthData): PatternAnalysisResult {
    const patterns = this.detectPatterns(birthData);

    // Calculate total score (weighted average)
    const totalScore =
      patterns.length > 0
        ? Math.round(patterns.reduce((sum, p) => sum + p.score, 0) / patterns.length)
        : 0;

    // Find dominant categories
    const categoryScores = new Map<PatternCategory, number>();
    for (const pattern of patterns) {
      const current = categoryScores.get(pattern.category) || 0;
      categoryScores.set(pattern.category, current + pattern.score);
    }

    const dominantCategories = Array.from(categoryScores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([category]) => category);

    // Generate summary
    const summary = this.generateSummary(birthData, patterns, totalScore, dominantCategories);

    return {
      birthData,
      patterns,
      totalScore,
      dominantCategories,
      summary,
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Generate human-readable summary
   */
  private generateSummary(
    birthData: BirthData,
    patterns: BMADPattern[],
    totalScore: number,
    dominantCategories: PatternCategory[]
  ): string {
    if (patterns.length === 0) {
      return `Birth date ${birthData.month}/${birthData.day}/${birthData.year} shows standard numerological patterns with no exceptional configurations.`;
    }

    const topPattern = patterns[0];
    const categoryNames = dominantCategories.map((c) =>
      c.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase())
    );

    let summary = `Birth date ${birthData.month}/${birthData.day}/${birthData.year} reveals ${patterns.length} significant pattern${patterns.length > 1 ? 's' : ''} `;
    summary += `with an overall strength score of ${totalScore}/100. `;

    if (dominantCategories.length > 0) {
      summary += `The dominant pattern categories are ${categoryNames.join(', ')}, `;
    }

    summary += `with the most significant being "${topPattern.name}" (score: ${topPattern.score}). `;
    summary += `This configuration suggests ${topPattern.interpretation.split('.')[0].toLowerCase()}.`;

    return summary;
  }

  /**
   * Get patterns by category
   */
  public getPatternsByCategory(birthData: BirthData, category: PatternCategory): BMADPattern[] {
    const patterns = this.detectPatterns(birthData);
    return patterns.filter((p) => p.category === category);
  }

  /**
   * Get high-confidence patterns only
   */
  public getHighConfidencePatterns(
    birthData: BirthData,
    minConfidence: number = 0.9
  ): BMADPattern[] {
    const patterns = this.detectPatterns(birthData);
    return patterns.filter((p) => p.confidence >= minConfidence);
  }

  /**
   * Compare two birth dates for pattern similarities
   */
  public comparePatterns(
    birthData1: BirthData,
    birthData2: BirthData
  ): {
    commonPatterns: string[];
    uniqueTo1: string[];
    uniqueTo2: string[];
    compatibilityScore: number;
  } {
    const patterns1 = this.detectPatterns(birthData1);
    const patterns2 = this.detectPatterns(birthData2);

    const names1 = new Set(patterns1.map((p) => p.name));
    const names2 = new Set(patterns2.map((p) => p.name));

    const commonPatterns = patterns1.filter((p) => names2.has(p.name)).map((p) => p.name);

    const uniqueTo1 = patterns1.filter((p) => !names2.has(p.name)).map((p) => p.name);

    const uniqueTo2 = patterns2.filter((p) => !names1.has(p.name)).map((p) => p.name);

    // Calculate compatibility score
    const totalPatterns = names1.size + names2.size - commonPatterns.length;
    const compatibilityScore =
      totalPatterns > 0 ? Math.round((commonPatterns.length / totalPatterns) * 100) : 0;

    return {
      commonPatterns,
      uniqueTo1,
      uniqueTo2,
      compatibilityScore,
    };
  }
}
