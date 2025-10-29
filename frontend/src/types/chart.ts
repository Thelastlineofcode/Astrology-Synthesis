/**
 * Type definitions for astrological chart data
 */

export interface PlanetPosition {
  sign: string;
  degree: number;
  house: number;
  retrograde?: boolean;
  longitude?: number;
  latitude?: number;
  speed?: number;
}

export interface HouseCusp {
  sign: string;
  degree: number;
  longitude?: number;
}

export interface ChartData {
  planets: {
    [planetName: string]: PlanetPosition | null;
  };
  houses: {
    [houseKey: string]: HouseCusp;
  };
  ascendant?: HouseCusp;
  midheaven?: HouseCusp;
}

export interface BirthData {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  latitude: number;
  longitude: number;
  name?: string;
}

export interface Aspect {
  planet1: string;
  planet2: string;
  aspect: string;
  orb: number;
  angle?: number;
}

export interface ChartCalculationResponse {
  success: boolean;
  chart?: ChartData;
  aspects?: Aspect[];
  error?: string;
}
