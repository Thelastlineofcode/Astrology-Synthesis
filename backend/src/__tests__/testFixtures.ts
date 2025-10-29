/**
 * Test Utilities and Fixtures
 * Provides reusable test data and helper functions
 */

import jwt from 'jsonwebtoken';
import { config } from '../config';

export interface TestUser {
  id: string;
  email: string;
  password: string;
  name: string;
}

export interface TestChart {
  name: string;
  birthDate: string;
  birthTime: string;
  latitude: number;
  longitude: number;
}

/**
 * Generate a valid JWT token for testing
 */
export const generateTestToken = (userId: string, email: string): string => {
  return jwt.sign(
    { id: userId, email },
    config.jwt.secret,
    { expiresIn: config.jwt.expiresIn } as jwt.SignOptions
  );
};

/**
 * User fixtures for testing
 */
export const userFixtures = {
  validUser: {
    email: 'test@example.com',
    password: 'password123',
    name: 'Test User',
  },
  validUser2: {
    email: 'test2@example.com',
    password: 'password456',
    name: 'Test User Two',
  },
  invalidEmailUser: {
    email: 'invalid-email',
    password: 'password123',
    name: 'Invalid User',
  },
  shortPasswordUser: {
    email: 'short@example.com',
    password: '123',
    name: 'Short Password User',
  },
  missingNameUser: {
    email: 'noname@example.com',
    password: 'password123',
    name: '',
  },
};

/**
 * Chart fixtures for testing
 */
export const chartFixtures = {
  validChart: {
    name: 'Valid Test Chart',
    birthDate: '1990-01-01',
    birthTime: '12:00',
    latitude: 40.7128,
    longitude: -74.0060,
  },
  albertEinstein: {
    name: 'Albert Einstein',
    birthDate: '1879-03-14',
    birthTime: '11:30',
    latitude: 48.3984,
    longitude: 7.9026,
  },
  modernBirth: {
    name: 'Y2K Birth',
    birthDate: '2000-01-01',
    birthTime: '00:00',
    latitude: 40.7128,
    longitude: -74.0060,
  },
  southernHemisphere: {
    name: 'Sydney Birth',
    birthDate: '1995-07-15',
    birthTime: '14:30',
    latitude: -33.8688,
    longitude: 151.2093,
  },
  invalidDateChart: {
    name: 'Invalid Date Chart',
    birthDate: 'not-a-date',
    birthTime: '12:00',
    latitude: 40.7128,
    longitude: -74.0060,
  },
  invalidTimeChart: {
    name: 'Invalid Time Chart',
    birthDate: '1990-01-01',
    birthTime: '25:99',
    latitude: 40.7128,
    longitude: -74.0060,
  },
  invalidLatitudeChart: {
    name: 'Invalid Latitude Chart',
    birthDate: '1990-01-01',
    birthTime: '12:00',
    latitude: 91,
    longitude: -74.0060,
  },
  invalidLongitudeChart: {
    name: 'Invalid Longitude Chart',
    birthDate: '1990-01-01',
    birthTime: '12:00',
    latitude: 40.7128,
    longitude: 181,
  },
};

/**
 * BMAD Analysis test data
 */
export const bmadFixtures = {
  basicChartData: {
    planets: {
      Sun: { sign: 'Leo', degree: 15.5, house: 5 },
      Moon: { sign: 'Cancer', degree: 22.3, house: 4 },
      Mercury: { sign: 'Virgo', degree: 8.1, house: 6 },
      Venus: { sign: 'Leo', degree: 20.0, house: 5 },
      Mars: { sign: 'Aries', degree: 12.0, house: 1 },
    },
    houses: {
      house_1: { sign: 'Aries', degree: 12.0 },
      house_4: { sign: 'Cancer', degree: 12.0 },
      house_5: { sign: 'Leo', degree: 12.0 },
    },
    aspects: [
      { planet1: 'Sun', planet2: 'Venus', aspect: 'conjunction', orb: 4.5 },
    ],
  },
};

/**
 * Expected astrological calculations for known birth data
 */
export const expectedCalculations = {
  albertEinstein: {
    sunSign: 'Pisces',
    moonSign: 'Sagittarius',
    ascendant: 'Cancer',
  },
  y2kBirth: {
    sunSign: 'Capricorn',
  },
};

/**
 * Helper to create a unique email for testing
 */
export const generateUniqueEmail = (): string => {
  return `test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
};

/**
 * Helper to create a unique chart name
 */
export const generateUniqueChartName = (): string => {
  return `Test Chart ${Date.now()}`;
};

/**
 * Delay utility for async operations
 */
export const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Generate random coordinates within valid ranges
 */
export const generateRandomCoordinates = (): {
  latitude: number;
  longitude: number;
} => {
  return {
    latitude: Math.random() * 180 - 90, // -90 to 90
    longitude: Math.random() * 360 - 180, // -180 to 180
  };
};

/**
 * Generate a random birth time
 */
export const generateRandomBirthTime = (): string => {
  const hour = Math.floor(Math.random() * 24)
    .toString()
    .padStart(2, '0');
  const minute = Math.floor(Math.random() * 60)
    .toString()
    .padStart(2, '0');
  return `${hour}:${minute}`;
};

/**
 * Generate a random ISO date
 */
export const generateRandomDate = (): string => {
  const year = 1950 + Math.floor(Math.random() * 70); // 1950-2020
  const month = (1 + Math.floor(Math.random() * 12)).toString().padStart(2, '0');
  const day = (1 + Math.floor(Math.random() * 28)).toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
};
