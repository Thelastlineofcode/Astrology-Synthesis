/**
 * API Services Index
 * Central export point for all API services
 */

export { apiClient, APIError } from "./client";
export type { APIResponse } from "./client";

import { authService } from "./services/auth";
import { chartsService } from "./services/charts";
import { predictionsService } from "./services/predictions";
import { transitsService } from "./services/transits";
import { knowledgeService } from "./services/knowledge";
import { llmService } from "./services/llm";
import { healthService } from "./services/health";

export {
  authService,
  chartsService,
  predictionsService,
  transitsService,
  knowledgeService,
  llmService,
  healthService,
};

export * from "./types";

// Convenience object for all services
export const api = {
  auth: authService,
  charts: chartsService,
  predictions: predictionsService,
  transits: transitsService,
  knowledge: knowledgeService,
  llm: llmService,
  health: healthService,
} as const;
