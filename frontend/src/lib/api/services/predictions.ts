/**
 * Predictions API Service
 */

import { apiClient } from "../client";
import type {
  CreatePredictionRequest,
  PredictionResponse,
  PaginatedResponse,
  PaginationParams,
} from "../types";

export const predictionsService = {
  /**
   * Create a new prediction
   */
  async create(data: CreatePredictionRequest): Promise<PredictionResponse> {
    return apiClient.post<PredictionResponse>("predictions", data, {
      requiresAuth: true,
    });
  },

  /**
   * Get a specific prediction by ID
   */
  async getById(predictionId: number): Promise<PredictionResponse> {
    return apiClient.get<PredictionResponse>(`predictions/${predictionId}`, {
      requiresAuth: true,
    });
  },

  /**
   * Get all predictions for a chart
   */
  async listByChart(
    chartId: number,
    params?: PaginationParams
  ): Promise<PaginatedResponse<PredictionResponse>> {
    const queryParams = new URLSearchParams({ chart_id: chartId.toString() });
    if (params?.page) queryParams.append("page", params.page.toString());
    if (params?.limit) queryParams.append("limit", params.limit.toString());

    return apiClient.get<PaginatedResponse<PredictionResponse>>(
      `predictions?${queryParams.toString()}`,
      { requiresAuth: true }
    );
  },

  /**
   * Get all predictions for current user
   */
  async list(
    params?: PaginationParams
  ): Promise<PaginatedResponse<PredictionResponse>> {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append("page", params.page.toString());
    if (params?.limit) queryParams.append("limit", params.limit.toString());

    const query = queryParams.toString();
    const endpoint = query ? `predictions?${query}` : "predictions";

    return apiClient.get<PaginatedResponse<PredictionResponse>>(endpoint, {
      requiresAuth: true,
    });
  },

  /**
   * Delete a prediction
   */
  async delete(predictionId: number): Promise<{ message: string }> {
    return apiClient.delete<{ message: string }>(
      `predictions/${predictionId}`,
      { requiresAuth: true }
    );
  },
};
