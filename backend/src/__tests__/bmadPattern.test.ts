/**
 * BMAD Pattern Recognition Tests
 * Comprehensive unit tests for the BMAD pattern detection algorithm
 */

import { BMADPatternRecognizer } from '../services/bmad/patternRecognizer';
import { BirthData, PatternCategory } from '../services/bmad/types';
import { digitSum, isMasterNumber } from '../services/bmad/patternRules';

describe('BMAD Pattern Recognition', () => {
  let recognizer: BMADPatternRecognizer;

  beforeEach(() => {
    recognizer = new BMADPatternRecognizer();
  });

  describe('Helper Functions', () => {
    describe('digitSum', () => {
      it('should reduce single digit numbers correctly', () => {
        expect(digitSum(5)).toBe(5);
        expect(digitSum(9)).toBe(9);
      });

      it('should reduce double digit numbers correctly', () => {
        expect(digitSum(15)).toBe(6); // 1 + 5 = 6
        expect(digitSum(29)).toBe(11); // 2 + 9 = 11 (master number, not reduced further)
        expect(digitSum(38)).toBe(11); // 3 + 8 = 11 (master number, not reduced further)
        expect(digitSum(19)).toBe(1); // 1 + 9 = 10 -> 1 + 0 = 1
      });

      it('should preserve master numbers', () => {
        expect(digitSum(11)).toBe(11);
        expect(digitSum(22)).toBe(22);
        expect(digitSum(33)).toBe(33);
      });

      it('should handle larger numbers', () => {
        expect(digitSum(1990)).toBe(1); // 1+9+9+0 = 19 -> 1+9 = 10 -> 1+0 = 1
      });
    });

    describe('isMasterNumber', () => {
      it('should identify master numbers', () => {
        expect(isMasterNumber(11)).toBe(true);
        expect(isMasterNumber(22)).toBe(true);
        expect(isMasterNumber(33)).toBe(true);
      });

      it('should reject non-master numbers', () => {
        expect(isMasterNumber(10)).toBe(false);
        expect(isMasterNumber(12)).toBe(false);
        expect(isMasterNumber(44)).toBe(false);
      });
    });
  });

  describe('Birth Data Validation', () => {
    it('should accept valid birth data', () => {
      const validData: BirthData = {
        year: 1990,
        month: 8,
        day: 15,
      };
      expect(() => recognizer.detectPatterns(validData)).not.toThrow();
    });

    it('should reject invalid year', () => {
      const invalidData: BirthData = {
        year: 1800,
        month: 8,
        day: 15,
      };
      expect(() => recognizer.detectPatterns(invalidData)).toThrow('Invalid year');
    });

    it('should reject invalid month', () => {
      const invalidData: BirthData = {
        year: 1990,
        month: 13,
        day: 15,
      };
      expect(() => recognizer.detectPatterns(invalidData)).toThrow('Invalid month');
    });

    it('should reject invalid day', () => {
      const invalidData: BirthData = {
        year: 1990,
        month: 8,
        day: 32,
      };
      expect(() => recognizer.detectPatterns(invalidData)).toThrow('Invalid day');
    });

    it('should reject invalid day for February', () => {
      const invalidData: BirthData = {
        year: 1990,
        month: 2,
        day: 30,
      };
      expect(() => recognizer.detectPatterns(invalidData)).toThrow('exceeds days in month');
    });

    it('should accept Feb 29 in leap year', () => {
      const validData: BirthData = {
        year: 2000,
        month: 2,
        day: 29,
      };
      expect(() => recognizer.detectPatterns(validData)).not.toThrow();
    });

    it('should reject invalid hour', () => {
      const invalidData: BirthData = {
        year: 1990,
        month: 8,
        day: 15,
        hour: 24,
      };
      expect(() => recognizer.detectPatterns(invalidData)).toThrow('Invalid hour');
    });

    it('should reject invalid minute', () => {
      const invalidData: BirthData = {
        year: 1990,
        month: 8,
        day: 15,
        minute: 60,
      };
      expect(() => recognizer.detectPatterns(invalidData)).toThrow('Invalid minute');
    });
  });

  describe('Pattern Detection', () => {
    it('should detect master number day pattern', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 8,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const masterPattern = patterns.find((p) => p.name === 'Master Number Day');

      expect(masterPattern).toBeDefined();
      expect(masterPattern?.category).toBe(PatternCategory.MASTER_NUMBER);
      expect(masterPattern?.score).toBeGreaterThan(80);
    });

    it('should detect repeated digit pattern', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 8,
        day: 22,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const repeatedPattern = patterns.find((p) => p.name === 'Repeated Digit Day');

      expect(repeatedPattern).toBeDefined();
      expect(repeatedPattern?.category).toBe(PatternCategory.REPETITIVE);
    });

    it('should detect sequential pattern', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 5,
        day: 6,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const sequentialPattern = patterns.find((p) => p.name === 'Sequential Pattern');

      expect(sequentialPattern).toBeDefined();
      expect(sequentialPattern?.category).toBe(PatternCategory.SEQUENTIAL);
    });

    it('should detect matching day and month', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 7,
        day: 7,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const matchingPattern = patterns.find((p) => p.name === 'Matching Day and Month');

      expect(matchingPattern).toBeDefined();
      expect(matchingPattern?.category).toBe(PatternCategory.HARMONIC);
    });

    it('should detect prime number day', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 8,
        day: 17,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const primePattern = patterns.find((p) => p.name === 'Prime Number Day');

      expect(primePattern).toBeDefined();
      expect(primePattern?.category).toBe(PatternCategory.SYMBOLIC);
    });

    it('should detect cyclic pattern', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 3,
        day: 9, // 9 is divisible by 3
      };
      const patterns = recognizer.detectPatterns(birthData);
      const cyclicPattern = patterns.find((p) => p.name === 'Cyclic Multiple');

      expect(cyclicPattern).toBeDefined();
      expect(cyclicPattern?.category).toBe(PatternCategory.CYCLIC);
    });

    it('should detect power of two pattern', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 8,
        day: 16,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const powerPattern = patterns.find((p) => p.name === 'Power of Two');

      expect(powerPattern).toBeDefined();
      expect(powerPattern?.category).toBe(PatternCategory.SYMBOLIC);
    });

    it('should detect numerical balance', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 12,
        day: 1, // 12 + 1 = 13
      };
      const patterns = recognizer.detectPatterns(birthData);
      const balancePattern = patterns.find((p) => p.name === 'Numerical Balance');

      expect(balancePattern).toBeDefined();
      expect(balancePattern?.category).toBe(PatternCategory.HARMONIC);
    });
  });

  describe('Pattern Analysis', () => {
    it('should return complete analysis result', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const result = recognizer.analyze(birthData);

      expect(result.birthData).toEqual(birthData);
      expect(result.patterns).toBeDefined();
      expect(result.patterns.length).toBeGreaterThan(0);
      expect(result.totalScore).toBeGreaterThan(0);
      expect(result.dominantCategories).toBeDefined();
      expect(result.summary).toBeDefined();
      expect(result.timestamp).toBeDefined();
    });

    it('should sort patterns by score', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const result = recognizer.analyze(birthData);

      for (let i = 1; i < result.patterns.length; i++) {
        expect(result.patterns[i - 1].score).toBeGreaterThanOrEqual(result.patterns[i].score);
      }
    });

    it('should identify dominant categories', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 22,
      };
      const result = recognizer.analyze(birthData);

      expect(result.dominantCategories.length).toBeGreaterThan(0);
      expect(result.dominantCategories.length).toBeLessThanOrEqual(3);
    });

    it('should generate meaningful summary', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 7,
        day: 7,
      };
      const result = recognizer.analyze(birthData);

      expect(result.summary).toContain('7/7/1990');
      expect(result.summary.length).toBeGreaterThan(50);
    });

    it('should handle birth data with no special patterns', () => {
      const birthData: BirthData = {
        year: 1991,
        month: 10,
        day: 25,
      };
      const result = recognizer.analyze(birthData);

      expect(result).toBeDefined();
      expect(result.patterns).toBeDefined();
      expect(result.totalScore).toBeGreaterThanOrEqual(0);
    });
  });

  describe('Pattern Filtering', () => {
    it('should filter patterns by category', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const masterPatterns = recognizer.getPatternsByCategory(
        birthData,
        PatternCategory.MASTER_NUMBER
      );

      expect(masterPatterns.every((p) => p.category === PatternCategory.MASTER_NUMBER)).toBe(true);
    });

    it('should get high confidence patterns only', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const highConfPatterns = recognizer.getHighConfidencePatterns(birthData, 0.9);

      expect(highConfPatterns.every((p) => p.confidence >= 0.9)).toBe(true);
    });
  });

  describe('Pattern Comparison', () => {
    it('should compare two birth dates', () => {
      const birthData1: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const birthData2: BirthData = {
        year: 1992,
        month: 11,
        day: 22,
      };

      const comparison = recognizer.comparePatterns(birthData1, birthData2);

      expect(comparison.commonPatterns).toBeDefined();
      expect(comparison.uniqueTo1).toBeDefined();
      expect(comparison.uniqueTo2).toBeDefined();
      expect(comparison.compatibilityScore).toBeGreaterThanOrEqual(0);
      expect(comparison.compatibilityScore).toBeLessThanOrEqual(100);
    });

    it('should find common patterns between similar dates', () => {
      const birthData1: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const birthData2: BirthData = {
        year: 1991,
        month: 11,
        day: 11,
      };

      const comparison = recognizer.comparePatterns(birthData1, birthData2);

      expect(comparison.commonPatterns.length).toBeGreaterThan(0);
    });

    it('should calculate compatibility score', () => {
      const birthData1: BirthData = {
        year: 1990,
        month: 7,
        day: 7,
      };
      const birthData2: BirthData = {
        year: 1992,
        month: 7,
        day: 7,
      };

      const comparison = recognizer.comparePatterns(birthData1, birthData2);

      expect(comparison.compatibilityScore).toBeGreaterThan(50);
    });
  });

  describe('Edge Cases', () => {
    it('should handle edge of month days', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 1,
        day: 31,
      };
      expect(() => recognizer.analyze(birthData)).not.toThrow();
    });

    it('should handle beginning of year', () => {
      const birthData: BirthData = {
        year: 2000,
        month: 1,
        day: 1,
      };
      expect(() => recognizer.analyze(birthData)).not.toThrow();
    });

    it('should handle end of year', () => {
      const birthData: BirthData = {
        year: 1999,
        month: 12,
        day: 31,
      };
      expect(() => recognizer.analyze(birthData)).not.toThrow();
    });

    it('should handle leap year dates', () => {
      const birthData: BirthData = {
        year: 2000,
        month: 2,
        day: 29,
      };
      const result = recognizer.analyze(birthData);
      expect(result).toBeDefined();
    });

    it('should handle dates with optional time data', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 8,
        day: 15,
        hour: 14,
        minute: 30,
      };
      expect(() => recognizer.analyze(birthData)).not.toThrow();
    });

    it('should handle century edge cases', () => {
      const birthData: BirthData = {
        year: 2000,
        month: 1,
        day: 1,
      };
      const result = recognizer.analyze(birthData);
      expect(result).toBeDefined();
      expect(result.patterns.length).toBeGreaterThanOrEqual(0);
    });
  });

  describe('Pattern Scoring', () => {
    it('should assign scores within valid range', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);

      patterns.forEach((pattern) => {
        expect(pattern.score).toBeGreaterThanOrEqual(0);
        expect(pattern.score).toBeLessThanOrEqual(100);
      });
    });

    it('should assign weights within valid range', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);

      patterns.forEach((pattern) => {
        expect(pattern.weight).toBeGreaterThanOrEqual(0);
        expect(pattern.weight).toBeLessThanOrEqual(1);
      });
    });

    it('should assign confidence within valid range', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);

      patterns.forEach((pattern) => {
        expect(pattern.confidence).toBeGreaterThanOrEqual(0);
        expect(pattern.confidence).toBeLessThanOrEqual(1);
      });
    });

    it('should give higher scores to master numbers', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);
      const masterPattern = patterns.find((p) => p.category === PatternCategory.MASTER_NUMBER);

      if (masterPattern) {
        expect(masterPattern.score).toBeGreaterThan(70);
      }
    });
  });

  describe('Pattern Elements', () => {
    it('should include pattern elements in results', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);

      patterns.forEach((pattern) => {
        expect(pattern.elements).toBeDefined();
        expect(Array.isArray(pattern.elements)).toBe(true);
        expect(pattern.elements.length).toBeGreaterThan(0);
      });
    });

    it('should include proper element types', () => {
      const birthData: BirthData = {
        year: 1990,
        month: 11,
        day: 11,
      };
      const patterns = recognizer.detectPatterns(birthData);

      patterns.forEach((pattern) => {
        pattern.elements.forEach((element) => {
          expect(['day', 'month', 'year', 'combined']).toContain(element.type);
          expect(typeof element.value).toBe('number');
          expect(typeof element.significance).toBe('string');
        });
      });
    });
  });
});
