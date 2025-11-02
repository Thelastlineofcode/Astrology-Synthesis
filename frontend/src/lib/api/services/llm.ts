/**
 * LLM & Interpretations API Service (Phase 5)
 */

import { apiClient } from "../client";
import type {
  InterpretationRequest,
  InterpretationResponse,
  BudgetResponse,
} from "../types";

export const llmService = {
  /**
   * Generate hybrid interpretation using LLM + Knowledge Base
   */
  async generateInterpretation(
    request: InterpretationRequest
  ): Promise<InterpretationResponse> {
    return apiClient.post<InterpretationResponse>(
      "interpretations/hybrid",
      request,
      { requiresAuth: true }
    );
  },

  /**
   * Get LLM budget status
   */
  async getBudget(): Promise<BudgetResponse> {
    return apiClient.get<BudgetResponse>("budget");
  },

  /**
   * Get LLM statistics
   */
  async getStats(): Promise<{
    hybrid_stats: Record<string, unknown>;
    llm_stats: BudgetResponse["budget"];
    cache_stats: BudgetResponse["cache_stats"];
    vector_stats: Record<string, unknown>;
  }> {
    return apiClient.get("stats");
  },

  /**
   * Health check for LLM service
   */
  async healthCheck(): Promise<{
    status: string;
    llm_service: string;
    vector_store: string;
    cache: string;
  }> {
    return apiClient.get("health");
  },
};
