/**
 * Birth Charts API Service
 */

import { apiClient } from "../client";
import type {
  CreateBirthChartRequest,
  BirthChartResponse,
  PaginatedResponse,
  PaginationParams,
} from "../types";

export const chartsService = {
  /**
   * Create a new birth chart
   */
  async create(data: CreateBirthChartRequest): Promise<BirthChartResponse> {
    return apiClient.post<BirthChartResponse>("charts", data, {
      requiresAuth: true,
    });
  },

  /**
   * Get a specific birth chart by ID
   */
  async getById(chartId: number): Promise<BirthChartResponse> {
    return apiClient.get<BirthChartResponse>(`charts/${chartId}`, {
      requiresAuth: true,
    });
  },

  /**
   * Get all birth charts for current user
   */
  async list(
    params?: PaginationParams
  ): Promise<PaginatedResponse<BirthChartResponse>> {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append("page", params.page.toString());
    if (params?.limit) queryParams.append("limit", params.limit.toString());

    const query = queryParams.toString();
    const endpoint = query ? `charts?${query}` : "charts";

    return apiClient.get<PaginatedResponse<BirthChartResponse>>(endpoint, {
      requiresAuth: true,
    });
  },

  /**
   * Update a birth chart
   */
  async update(
    chartId: number,
    data: Partial<CreateBirthChartRequest>
  ): Promise<BirthChartResponse> {
    return apiClient.put<BirthChartResponse>(`charts/${chartId}`, data, {
      requiresAuth: true,
    });
  },

  /**
   * Delete a birth chart
   */
  async delete(chartId: number): Promise<{ message: string }> {
    return apiClient.delete<{ message: string }>(`charts/${chartId}`, {
      requiresAuth: true,
    });
  },

  /**
   * Calculate chart for given data without saving
   */
  async calculate(data: CreateBirthChartRequest): Promise<BirthChartResponse> {
    return apiClient.post<BirthChartResponse>("charts/calculate", data);
  },
};
