/**
 * Health Check API Service
 */

import { apiClient } from "../client";
import type { HealthResponse } from "../types";

export const healthService = {
  /**
   * Get system health status
   */
  async getHealth(): Promise<HealthResponse> {
    return apiClient.get<HealthResponse>("health");
  },

  /**
   * Get API version
   */
  async getVersion(): Promise<{ version: string }> {
    return apiClient.get<{ version: string }>("/");
  },
};
