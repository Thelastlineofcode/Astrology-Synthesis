/**
 * BMAD Pattern Rules
 * Defines the rules for detecting various astrological patterns in birth data
 */

import { BirthData, PatternCategory, PatternRule } from './types';

/**
 * Helper function to calculate digit sum (reduce to single digit)
 */
export function digitSum(num: number): number {
  while (num > 9 && num !== 11 && num !== 22 && num !== 33) {
    num = num
      .toString()
      .split('')
      .reduce((sum, digit) => sum + parseInt(digit), 0);
  }
  return num;
}

/**
 * Helper function to check if a number is a master number
 */
export function isMasterNumber(num: number): boolean {
  return num === 11 || num === 22 || num === 33;
}

/**
 * Helper function to find repeated digits
 */
export function hasRepeatedDigits(num: number): boolean {
  const digits = num.toString().split('');
  const uniqueDigits = new Set(digits);
  return digits.length > uniqueDigits.size;
}

/**
 * Helper function to check if numbers are sequential
 */
export function areSequential(nums: number[]): boolean {
  if (nums.length < 2) return false;
  const sorted = [...nums].sort((a, b) => a - b);
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i] !== sorted[i - 1] + 1) return false;
  }
  return true;
}

/**
 * Pattern detection rules
 */
export const patternRules: PatternRule[] = [
  // Master Number Day
  {
    name: 'Master Number Day',
    category: PatternCategory.MASTER_NUMBER,
    weight: 0.95,
    condition: (birthData: BirthData) => isMasterNumber(birthData.day),
    description: (birthData: BirthData) => `Birth day ${birthData.day} is a powerful master number`,
    interpretation: (birthData: BirthData) =>
      `Master number ${birthData.day} indicates heightened spiritual potential and leadership qualities. This number carries special significance in numerological and astrological traditions.`,
    elements: (birthData: BirthData) => [
      {
        type: 'day',
        value: birthData.day,
        significance: 'Master number with spiritual significance',
      },
    ],
  },

  // Repeated Digits in Day
  {
    name: 'Repeated Digit Day',
    category: PatternCategory.REPETITIVE,
    weight: 0.75,
    condition: (birthData: BirthData) => birthData.day >= 10 && hasRepeatedDigits(birthData.day),
    description: (birthData: BirthData) => `Birth day ${birthData.day} contains repeated digits`,
    interpretation: (_birthData: BirthData) =>
      `Repeated digits in the birth day suggest emphasis and intensification of certain qualities. This pattern indicates focused energy in specific life areas.`,
    elements: (birthData: BirthData) => [
      {
        type: 'day',
        value: birthData.day,
        significance: 'Repeated digits suggest intensified energy',
      },
    ],
  },

  // Sequential Birth Numbers
  {
    name: 'Sequential Pattern',
    category: PatternCategory.SEQUENTIAL,
    weight: 0.85,
    condition: (birthData: BirthData) =>
      areSequential([birthData.month, birthData.day]) ||
      areSequential([birthData.day, birthData.month]),
    description: (birthData: BirthData) =>
      `Birth month ${birthData.month} and day ${birthData.day} form a sequential pattern`,
    interpretation: (_birthData: BirthData) =>
      'Sequential numbers in birth data suggest natural progression, growth, and step-by-step development in life. This pattern indicates orderly advancement and methodical approach to goals.',
    elements: (birthData: BirthData) => [
      {
        type: 'month',
        value: birthData.month,
        significance: 'Part of sequential pattern',
      },
      {
        type: 'day',
        value: birthData.day,
        significance: 'Part of sequential pattern',
      },
    ],
  },

  // Matching Day and Month
  {
    name: 'Matching Day and Month',
    category: PatternCategory.HARMONIC,
    weight: 0.8,
    condition: (birthData: BirthData) => birthData.day === birthData.month,
    description: (birthData: BirthData) => `Birth day and month both equal ${birthData.day}`,
    interpretation: (_birthData: BirthData) =>
      'Matching day and month numbers create a harmonic resonance, suggesting balance and alignment. This pattern indicates strong focus and clarity of purpose.',
    elements: (birthData: BirthData) => [
      {
        type: 'combined',
        value: birthData.day,
        significance: 'Harmonic alignment between day and month',
      },
    ],
  },

  // Life Path Number Pattern
  {
    name: 'Life Path Harmony',
    category: PatternCategory.NUMERIC,
    weight: 0.7,
    condition: (birthData: BirthData) => {
      const lifePath = digitSum(birthData.year + birthData.month + birthData.day);
      const daySum = digitSum(birthData.day);
      return lifePath === daySum;
    },
    description: (birthData: BirthData) => {
      const lifePath = digitSum(birthData.year + birthData.month + birthData.day);
      return `Life path number ${lifePath} harmonizes with birth day`;
    },
    interpretation: (_birthData: BirthData) =>
      "When the life path number aligns with the birth day, it indicates strong self-awareness and natural alignment with one's life purpose. This pattern suggests ease in personal development.",
    elements: (birthData: BirthData) => {
      const lifePath = digitSum(birthData.year + birthData.month + birthData.day);
      return [
        {
          type: 'combined',
          value: lifePath,
          significance: 'Life path number in harmony',
        },
      ];
    },
  },

  // Cyclic Pattern (multiples)
  {
    name: 'Cyclic Multiple',
    category: PatternCategory.CYCLIC,
    weight: 0.65,
    condition: (birthData: BirthData) =>
      birthData.day % birthData.month === 0 || birthData.month % birthData.day === 0,
    description: (birthData: BirthData) =>
      `Birth day ${birthData.day} and month ${birthData.month} form a cyclic relationship`,
    interpretation: (_birthData: BirthData) =>
      'Cyclic patterns in birth numbers suggest rhythmic life cycles and recurring themes. This indicates natural timing and periodic opportunities for growth.',
    elements: (birthData: BirthData) => [
      {
        type: 'month',
        value: birthData.month,
        significance: 'Part of cyclic pattern',
      },
      {
        type: 'day',
        value: birthData.day,
        significance: 'Part of cyclic pattern',
      },
    ],
  },

  // Prime Number Day
  {
    name: 'Prime Number Day',
    category: PatternCategory.SYMBOLIC,
    weight: 0.6,
    condition: (birthData: BirthData) => {
      const primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31];
      return primes.includes(birthData.day);
    },
    description: (birthData: BirthData) => `Birth day ${birthData.day} is a prime number`,
    interpretation: (_birthData: BirthData) =>
      'Prime number birth days suggest uniqueness and indivisibility. This pattern indicates strong individuality and self-contained strength.',
    elements: (birthData: BirthData) => [
      {
        type: 'day',
        value: birthData.day,
        significance: 'Prime number symbolizing uniqueness',
      },
    ],
  },

  // Power of 2 Pattern
  {
    name: 'Power of Two',
    category: PatternCategory.SYMBOLIC,
    weight: 0.7,
    condition: (birthData: BirthData) => {
      const powersOf2 = [1, 2, 4, 8, 16];
      return powersOf2.includes(birthData.day) || powersOf2.includes(birthData.month);
    },
    description: (_birthData: BirthData) => 'Birth data contains a power of two',
    interpretation: (_birthData: BirthData) =>
      'Powers of two suggest doubling energy, expansion, and geometric growth. This pattern indicates potential for rapid development and exponential progress.',
    elements: (birthData: BirthData) => {
      const powersOf2 = [1, 2, 4, 8, 16];
      const elements = [];
      if (powersOf2.includes(birthData.day)) {
        elements.push({
          type: 'day' as const,
          value: birthData.day,
          significance: 'Power of two symbolizing growth',
        });
      }
      if (powersOf2.includes(birthData.month)) {
        elements.push({
          type: 'month' as const,
          value: birthData.month,
          significance: 'Power of two symbolizing growth',
        });
      }
      return elements;
    },
  },

  // Master Year Pattern
  {
    name: 'Master Year Energy',
    category: PatternCategory.MASTER_NUMBER,
    weight: 0.8,
    condition: (birthData: BirthData) => {
      const yearSum = digitSum(birthData.year);
      return isMasterNumber(yearSum);
    },
    description: (birthData: BirthData) => {
      const yearSum = digitSum(birthData.year);
      return `Birth year ${birthData.year} reduces to master number ${yearSum}`;
    },
    interpretation: (_birthData: BirthData) =>
      'A birth year that reduces to a master number infuses the entire lifetime with elevated spiritual energy and leadership potential. This suggests a soul purpose aligned with service and transformation.',
    elements: (birthData: BirthData) => {
      const yearSum = digitSum(birthData.year);
      return [
        {
          type: 'year',
          value: yearSum,
          significance: 'Master year energy throughout life',
        },
      ];
    },
  },

  // Perfect Balance (month + day = full year or specific number)
  {
    name: 'Numerical Balance',
    category: PatternCategory.HARMONIC,
    weight: 0.75,
    condition: (birthData: BirthData) => {
      const sum = birthData.month + birthData.day;
      return sum === 13 || sum === 21 || sum === 34; // Fibonacci-related
    },
    description: (birthData: BirthData) =>
      `Month ${birthData.month} and day ${birthData.day} create a balanced sum`,
    interpretation: (_birthData: BirthData) =>
      'When birth components sum to significant numbers, it creates numerical balance and harmony. This pattern suggests natural equilibrium and the ability to maintain balance in life.',
    elements: (birthData: BirthData) => [
      {
        type: 'combined',
        value: birthData.month + birthData.day,
        significance: 'Balanced numerical combination',
      },
    ],
  },
];
