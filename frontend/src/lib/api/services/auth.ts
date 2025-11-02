/**
 * Authentication API Service
 */

import { apiClient } from "../client";
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
} from "../types";

export const authService = {
  /**
   * Login user
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>(
      "auth/login",
      credentials
    );

    // Store token in localStorage
    if (typeof window !== "undefined" && response.access_token) {
      localStorage.setItem("auth_token", response.access_token);
      localStorage.setItem("refresh_token", response.refresh_token);
      apiClient.setAuthToken(response.access_token);
    }

    return response;
  },

  /**
   * Register new user
   */
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>(
      "auth/register",
      userData
    );

    // Store token in localStorage
    if (typeof window !== "undefined" && response.access_token) {
      localStorage.setItem("auth_token", response.access_token);
      localStorage.setItem("refresh_token", response.refresh_token);
      apiClient.setAuthToken(response.access_token);
    }

    return response;
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post("auth/logout", {}, { requiresAuth: true });
    } finally {
      // Clear tokens even if API call fails
      if (typeof window !== "undefined") {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("refresh_token");
        apiClient.setAuthToken(null);
      }
    }
  },

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>("auth/me", { requiresAuth: true });
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<AuthResponse> {
    const refreshToken =
      typeof window !== "undefined"
        ? localStorage.getItem("refresh_token")
        : null;

    if (!refreshToken) {
      throw new Error("No refresh token available");
    }

    const response = await apiClient.post<AuthResponse>("auth/refresh", {
      refresh_token: refreshToken,
    });

    // Update stored token
    if (typeof window !== "undefined" && response.access_token) {
      localStorage.setItem("auth_token", response.access_token);
      apiClient.setAuthToken(response.access_token);
    }

    return response;
  },

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<{ message: string }> {
    return apiClient.post("auth/password-reset/request", { email });
  },

  /**
   * Reset password with token
   */
  async resetPassword(
    token: string,
    newPassword: string
  ): Promise<{ message: string }> {
    return apiClient.post("auth/password-reset/confirm", {
      token,
      new_password: newPassword,
    });
  },

  /**
   * Change password
   */
  async changePassword(
    currentPassword: string,
    newPassword: string
  ): Promise<{ message: string }> {
    return apiClient.post(
      "auth/change-password",
      {
        current_password: currentPassword,
        new_password: newPassword,
      },
      { requiresAuth: true }
    );
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    if (typeof window === "undefined") return false;
    return !!localStorage.getItem("auth_token");
  },
};
