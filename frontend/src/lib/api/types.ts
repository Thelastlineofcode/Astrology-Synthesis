/**
 * TypeScript type definitions for API requests and responses
 */

// ============================================================================
// Common Types
// ============================================================================

export interface PaginationParams {
  page?: number;
  limit?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

// ============================================================================
// Authentication Types
// ============================================================================

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
  is_active: boolean;
  is_superuser?: boolean;
}

// ============================================================================
// Birth Chart Types
// ============================================================================

export interface CreateBirthChartRequest {
  name: string;
  birth_date: string; // ISO 8601
  birth_time: string; // HH:MM:SS
  latitude: number;
  longitude: number;
  timezone: string;
  birth_location: string;
  house_system?: "placidus" | "whole-sign" | "equal" | "koch";
}

export interface BirthChartResponse {
  id: number;
  user_id: number;
  name: string;
  birth_date: string;
  birth_time: string;
  latitude: number;
  longitude: number;
  timezone: string;
  birth_location: string;
  house_system: string;
  chart_data: ChartData;
  created_at: string;
  updated_at: string;
}

export interface ChartData {
  planets: Planet[];
  houses: House[];
  aspects: Aspect[];
  ascendant: number;
  midheaven: number;
}

export interface Planet {
  name: string;
  longitude: number;
  latitude: number;
  speed: number;
  sign: string;
  house: number;
  retrograde: boolean;
}

export interface House {
  number: number;
  cusp: number;
  sign: string;
}

export interface Aspect {
  planet1: string;
  planet2: string;
  type: string;
  angle: number;
  orb: number;
  applying: boolean;
}

// ============================================================================
// Prediction Types
// ============================================================================

export interface CreatePredictionRequest {
  chart_id: number;
  prediction_type: "transit" | "progression" | "solar_return";
  target_date?: string;
  options?: Record<string, unknown>;
}

export interface PredictionResponse {
  id: number;
  chart_id: number;
  prediction_type: string;
  prediction_date: string;
  content: PredictionContent;
  quality_score: number;
  created_at: string;
}

export interface PredictionContent {
  summary: string;
  detailed_analysis: string;
  key_themes: string[];
  planetary_influences: PlanetaryInfluence[];
  recommendations: string[];
}

export interface PlanetaryInfluence {
  planet: string;
  aspect: string;
  influence: string;
  strength: number;
}

// ============================================================================
// Transit Types
// ============================================================================

export interface CreateTransitRequest {
  chart_id: number;
  start_date: string;
  end_date: string;
  planets?: string[];
}

export interface TransitResponse {
  id: number;
  chart_id: number;
  transit_date: string;
  transiting_planet: string;
  natal_planet: string;
  aspect_type: string;
  orb: number;
  interpretation: string;
  intensity: number;
  created_at: string;
}

// ============================================================================
// Interpretation Types (Phase 5)
// ============================================================================

export interface InterpretationRequest {
  chart_data: ChartData;
  type: "sun" | "moon" | "ascendant" | "full" | "aspect" | "house";
  strategy?: "auto" | "llm" | "kb" | "template";
  context?: string;
}

export interface InterpretationResponse {
  interpretation: string;
  type: string;
  strategy: string;
  quality: number;
  source: string;
  cost: number;
  execution_time: number;
}

// ============================================================================
// Knowledge Base Types (Phase 5)
// ============================================================================

export interface KnowledgeSearchRequest {
  query: string;
  category?: string;
  limit?: number;
}

export interface KnowledgeSearchResponse {
  query: string;
  category?: string;
  limit: number;
  results: KnowledgeResult[];
  total_results: number;
}

export interface KnowledgeResult {
  category: string;
  text: string;
  file_path: string;
  similarity_score: number;
  weight: number;
}

export interface KnowledgeCategory {
  name: string;
  book_count: number;
  weight: number;
  path: string;
}

// ============================================================================
// LLM Budget Types (Phase 5)
// ============================================================================

export interface BudgetResponse {
  budget: {
    total: number;
    used: number;
    cost_remaining: number;
    percentage_used: number;
    estimated_monthly: number;
    calls: number;
    tokens: {
      input: number;
      output: number;
      total: number;
    };
    alert: boolean;
  };
  cache_stats: {
    cache_hits: number;
    cache_misses: number;
    total_requests: number;
    hit_rate_percentage: number;
    available: boolean;
  };
  model: string;
}

// ============================================================================
// Health Check Types
// ============================================================================

export interface HealthResponse {
  status: "healthy" | "unhealthy";
  version: string;
  timestamp: string;
  database_status: string;
  cache_status: string;
  calculation_engines_status: string;
}

// ============================================================================
// Error Types
// ============================================================================

export interface APIErrorResponse {
  error_code: string;
  error_message: string;
  errors?: Array<{
    field: string;
    message: string;
  }>;
  timestamp: string;
}
