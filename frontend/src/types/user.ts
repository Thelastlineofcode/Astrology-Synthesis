// Types for User Profile and Readings

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  timezone: string;
  created_at: string;
}

export interface Reading {
  id: string;
  reading_type: "fortune" | "consultation";
  data: ReadingData;
  created_at: string;
}

export interface ReadingData {
  // Fortune card data
  card_name?: string;
  card_description?: string;
  card_interpretation?: string;
  element?: string;
  planet?: string;

  // Consultation data
  advisor_name?: string;
  message_count?: number;
  messages?: Message[];
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface ReadingsResponse {
  readings: Reading[];
  total: number;
  page: number;
  total_pages: number;
}

// ReadingDetail is the same as Reading with full data populated
export type ReadingDetail = Reading;
