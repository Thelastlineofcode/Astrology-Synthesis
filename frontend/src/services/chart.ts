/**
 * Chart Service
 * Handles API calls to chart generation endpoint
 */

import authService from "./auth";

export interface BirthData {
  birth_date: string; // ISO format: YYYY-MM-DD
  birth_time: string; // HH:MM format
  birth_location: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export interface ChartResponse {
  chart_id: string;
  user_id: string;
  chart_data: Record<string, unknown>;
  created_at: string;
  birth_location: string;
}

class ChartService {
  private readonly API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

  /**
   * Generate a new birth chart
   */
  async generateChart(birthData: BirthData): Promise<ChartResponse> {
    const accessToken = authService.getAccessToken();

    if (!accessToken) {
      throw new Error("Not authenticated. Please log in first.");
    }

    try {
      const response = await fetch(`${this.API_URL}/api/v1/chart`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          birth_data: {
            date: birthData.birth_date,
            time: birthData.birth_time,
            location_name: birthData.birth_location,
            latitude: birthData.latitude,
            longitude: birthData.longitude,
            timezone: birthData.timezone,
          },
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          throw new Error("Session expired. Please log in again.");
        }
        const error = await response.json();
        throw new Error(error.detail || "Chart generation failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Chart generation error:", error);
      throw error;
    }
  }

  /**
   * Get a previously generated chart
   */
  async getChart(chartId: string): Promise<ChartResponse> {
    const accessToken = authService.getAccessToken();

    if (!accessToken) {
      throw new Error("Not authenticated. Please log in first.");
    }

    try {
      const response = await fetch(`${this.API_URL}/api/v1/chart/${chartId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch chart");
      }

      return await response.json();
    } catch (error) {
      console.error("Get chart error:", error);
      throw error;
    }
  }
}

const chartService = new ChartService();
export default chartService;
