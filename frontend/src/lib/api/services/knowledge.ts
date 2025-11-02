/**
 * Knowledge Base API Service (Phase 5)
 */

import { apiClient } from "../client";
import type {
  KnowledgeSearchRequest,
  KnowledgeSearchResponse,
  KnowledgeCategory,
} from "../types";

export const knowledgeService = {
  /**
   * Search the knowledge base
   */
  async search(
    params: KnowledgeSearchRequest
  ): Promise<KnowledgeSearchResponse> {
    const queryParams = new URLSearchParams({ query: params.query });
    if (params.category) queryParams.append("category", params.category);
    if (params.limit) queryParams.append("limit", params.limit.toString());

    return apiClient.post<KnowledgeSearchResponse>(
      `knowledge/search?${queryParams.toString()}`
    );
  },

  /**
   * Get all knowledge base categories
   */
  async getCategories(): Promise<{
    total_categories: number;
    categories: KnowledgeCategory[];
  }> {
    return apiClient.get<{
      total_categories: number;
      categories: KnowledgeCategory[];
    }>("knowledge/categories");
  },

  /**
   * Get information about a specific category
   */
  async getCategoryInfo(
    categoryName: string
  ): Promise<KnowledgeCategory & { description?: string }> {
    return apiClient.get<KnowledgeCategory & { description?: string }>(
      `knowledge/category/${categoryName}`
    );
  },

  /**
   * Health check for knowledge service
   */
  async healthCheck(): Promise<{ status: string; message: string }> {
    return apiClient.get<{ status: string; message: string }>(
      "knowledge/health"
    );
  },
};
