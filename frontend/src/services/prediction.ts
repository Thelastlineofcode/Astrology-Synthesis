/**
 * Prediction Service
 * Handles API calls to prediction generation endpoint
 */

import authService from "./auth";

export interface PredictionEvent {
  event_type: string;
  event_date: string;
  event_window_start: string;
  event_window_end: string;
  primary_planet?: string;
  secondary_planet?: string;
  strength_score: number;
  influence_area?: string;
  description: string;
  recommendation?: string;
}

export interface PredictionRequest {
  birth_data: {
    date: string;
    time: string;
    location_name: string;
    latitude: number;
    longitude: number;
    timezone: string;
  };
  query: string;
  prediction_window_days?: number;
}

export interface PredictionResponse {
  prediction_id: string;
  user_id: string;
  query: string;
  prediction_window_start: string;
  prediction_window_end: string;
  confidence_score: number;
  events: PredictionEvent[];
  kp_contribution: number;
  dasha_contribution: number;
  transit_contribution: number;
  model_version: string;
  calculation_time_ms: number;
  created_at: string;
}

class PredictionService {
  private readonly API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

  /**
   * Generate astrological predictions
   */
  async generatePrediction(
    request: PredictionRequest
  ): Promise<PredictionResponse> {
    const accessToken = authService.getAccessToken();

    if (!accessToken) {
      throw new Error("Not authenticated. Please log in first.");
    }

    try {
      const response = await fetch(`${this.API_URL}/api/v1/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          throw new Error("Session expired. Please log in again.");
        }
        const error = await response.json();
        throw new Error(error.detail || "Prediction generation failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Prediction generation error:", error);
      if (error instanceof TypeError && error.message === "Load failed") {
        throw new Error(
          "Cannot connect to server. Please check if the backend is running on port 8001."
        );
      }
      throw error;
    }
  }

  /**
   * Get a previously generated prediction
   */
  async getPrediction(predictionId: string): Promise<PredictionResponse> {
    const accessToken = authService.getAccessToken();

    if (!accessToken) {
      throw new Error("Not authenticated. Please log in first.");
    }

    try {
      const response = await fetch(
        `${this.API_URL}/api/v1/predict/${predictionId}`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }

      return await response.json();
    } catch (error) {
      console.error("Get prediction error:", error);
      throw error;
    }
  }

  /**
   * List user's predictions
   */
  async listPredictions(): Promise<PredictionResponse[]> {
    const accessToken = authService.getAccessToken();

    if (!accessToken) {
      throw new Error("Not authenticated. Please log in first.");
    }

    try {
      const response = await fetch(`${this.API_URL}/api/v1/predict`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch predictions");
      }

      return await response.json();
    } catch (error) {
      console.error("List predictions error:", error);
      throw error;
    }
  }
}

const predictionService = new PredictionService();
export default predictionService;
