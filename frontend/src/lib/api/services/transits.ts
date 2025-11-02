/**
 * Transits API Service
 */

import { apiClient } from "../client";
import type {
  CreateTransitRequest,
  TransitResponse,
  PaginatedResponse,
  PaginationParams,
} from "../types";

export const transitsService = {
  /**
   * Calculate transits for a chart
   */
  async calculate(data: CreateTransitRequest): Promise<TransitResponse[]> {
    return apiClient.post<TransitResponse[]>("transits/calculate", data, {
      requiresAuth: true,
    });
  },

  /**
   * Get a specific transit by ID
   */
  async getById(transitId: number): Promise<TransitResponse> {
    return apiClient.get<TransitResponse>(`transits/${transitId}`, {
      requiresAuth: true,
    });
  },

  /**
   * Get all transits for a chart
   */
  async listByChart(
    chartId: number,
    params?: PaginationParams & { start_date?: string; end_date?: string }
  ): Promise<PaginatedResponse<TransitResponse>> {
    const queryParams = new URLSearchParams({ chart_id: chartId.toString() });
    if (params?.page) queryParams.append("page", params.page.toString());
    if (params?.limit) queryParams.append("limit", params.limit.toString());
    if (params?.start_date) queryParams.append("start_date", params.start_date);
    if (params?.end_date) queryParams.append("end_date", params.end_date);

    return apiClient.get<PaginatedResponse<TransitResponse>>(
      `transits?${queryParams.toString()}`,
      { requiresAuth: true }
    );
  },

  /**
   * Get current transits for a chart
   */
  async getCurrent(chartId: number): Promise<TransitResponse[]> {
    return apiClient.get<TransitResponse[]>(`transits/current/${chartId}`, {
      requiresAuth: true,
    });
  },

  /**
   * Delete a transit
   */
  async delete(transitId: number): Promise<{ message: string }> {
    return apiClient.delete<{ message: string }>(`transits/${transitId}`, {
      requiresAuth: true,
    });
  },
};
