/**
 * Mock chart data for development and testing
 * Based on sample birth data: Metairie, LA, Dec 19, 1984
 */

export const mockChartData = {
  planets: [
    {
      name: 'Sun',
      longitude: 267.5,
      sign: 'Sagittarius',
      degree: 27.5,
      house: 10,
      retrograde: false
    },
    {
      name: 'Moon',
      longitude: 45.2,
      sign: 'Taurus',
      degree: 15.2,
      house: 3,
      retrograde: false
    },
    {
      name: 'Mercury',
      longitude: 252.8,
      sign: 'Sagittarius',
      degree: 12.8,
      house: 9,
      retrograde: true
    },
    {
      name: 'Venus',
      longitude: 290.3,
      sign: 'Capricorn',
      degree: 20.3,
      house: 11,
      retrograde: false
    },
    {
      name: 'Mars',
      longitude: 330.7,
      sign: 'Pisces',
      degree: 0.7,
      house: 1,
      retrograde: false
    },
    {
      name: 'Jupiter',
      longitude: 308.4,
      sign: 'Aquarius',
      degree: 8.4,
      house: 12,
      retrograde: false
    },
    {
      name: 'Saturn',
      longitude: 246.1,
      sign: 'Scorpio',
      degree: 26.1,
      house: 9,
      retrograde: false
    },
    {
      name: 'Uranus',
      longitude: 252.9,
      sign: 'Sagittarius',
      degree: 12.9,
      house: 9,
      retrograde: false
    },
    {
      name: 'Neptune',
      longitude: 270.5,
      sign: 'Capricorn',
      degree: 0.5,
      house: 10,
      retrograde: false
    },
    {
      name: 'Pluto',
      longitude: 214.3,
      sign: 'Scorpio',
      degree: 4.3,
      house: 8,
      retrograde: false
    }
  ],
  houses: {
    house_1: { longitude: 315.5, sign: 'Pisces' },
    house_2: { longitude: 345.2, sign: 'Aries' },
    house_3: { longitude: 15.8, sign: 'Taurus' },
    house_4: { longitude: 45.3, sign: 'Gemini' },
    house_5: { longitude: 75.7, sign: 'Cancer' },
    house_6: { longitude: 105.1, sign: 'Leo' },
    house_7: { longitude: 135.5, sign: 'Virgo' },
    house_8: { longitude: 165.2, sign: 'Libra' },
    house_9: { longitude: 195.8, sign: 'Scorpio' },
    house_10: { longitude: 225.3, sign: 'Sagittarius' },
    house_11: { longitude: 255.7, sign: 'Capricorn' },
    house_12: { longitude: 285.1, sign: 'Aquarius' }
  },
  aspects: [
    {
      planet1: 'Sun',
      planet2: 'Moon',
      type: 'trine',
      orb: 2.3,
      angle: 120
    },
    {
      planet1: 'Sun',
      planet2: 'Mars',
      type: 'square',
      orb: 3.2,
      angle: 90
    },
    {
      planet1: 'Venus',
      planet2: 'Jupiter',
      type: 'sextile',
      orb: 1.9,
      angle: 60
    },
    {
      planet1: 'Moon',
      planet2: 'Neptune',
      type: 'opposition',
      orb: 4.7,
      angle: 180
    },
    {
      planet1: 'Mercury',
      planet2: 'Uranus',
      type: 'conjunction',
      orb: 0.1,
      angle: 0
    },
    {
      planet1: 'Mars',
      planet2: 'Saturn',
      type: 'trine',
      orb: 5.4,
      angle: 120
    }
  ]
};
