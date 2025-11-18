/**
 * Authentication Service
 * Handles user registration, login, token management, and session persistence
 */

interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface User {
  user_id: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthResponse {
  user: User;
  tokens: AuthTokens;
}

class AuthService {
  private readonly API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

  /**
   * Register a new user account
   */
  async register(
    email: string,
    password: string,
    firstName: string,
    lastName: string
  ): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.API_URL}/api/v1/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          first_name: firstName,
          last_name: lastName,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Registration failed");
      }

      const data = await response.json();

      // Store tokens in localStorage
      this.storeTokens(data.access_token, data.refresh_token);
      this.storeUser({
        user_id: data.user_id,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      });

      return {
        user: {
          user_id: data.user_id,
          email: data.email,
          first_name: data.first_name,
          last_name: data.last_name,
        },
        tokens: {
          access_token: data.access_token,
          refresh_token: data.refresh_token,
          token_type: data.token_type,
        },
      };
    } catch (error) {
      console.error("Registration error:", error);
      throw error;
    }
  }

  /**
   * Login with email and password
   */
  async login(email: string, password: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.API_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }

      const data = await response.json();

      // Store tokens
      this.storeTokens(data.access_token, data.refresh_token);
      this.storeUser({
        user_id: data.user_id,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      });

      return {
        user: {
          user_id: data.user_id,
          email: data.email,
          first_name: data.first_name,
          last_name: data.last_name,
        },
        tokens: {
          access_token: data.access_token,
          refresh_token: data.refresh_token,
          token_type: data.token_type,
        },
      };
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  }

  /**
   * Get stored access token
   */
  getAccessToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  }

  /**
   * Get current authenticated user
   */
  getCurrentUser(): User | null {
    if (typeof window === "undefined") return null;
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  /**
   * Logout and clear session
   */
  logout(): void {
    if (typeof window === "undefined") return;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  }

  /**
   * Store tokens in localStorage
   */
  private storeTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === "undefined") return;
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
  }

  /**
   * Store user data in localStorage
   */
  private storeUser(user: User): void {
    if (typeof window === "undefined") return;
    localStorage.setItem("user", JSON.stringify(user));
  }
}

const authService = new AuthService();
export default authService;
