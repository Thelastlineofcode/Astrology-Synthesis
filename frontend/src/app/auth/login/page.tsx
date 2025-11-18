"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import authService from "@/services/auth";
import "./login.css";

export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    firstName: "",
    lastName: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (isLogin) {
        // Login
        const response = await authService.login(
          formData.email,
          formData.password
        );
        setSuccess(`Welcome back, ${response.user.first_name}!`);

        // Redirect to readings page
        setTimeout(() => {
          router.push("/readings/new");
        }, 1500);
      } else {
        // Register
        const response = await authService.register(
          formData.email,
          formData.password,
          formData.firstName,
          formData.lastName
        );
        setSuccess(`Account created! Welcome, ${response.user.first_name}!`);

        // Redirect to readings page
        setTimeout(() => {
          router.push("/readings/new");
        }, 1500);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title">Mula</h1>
          <p className="auth-subtitle">
            {isLogin ? "Access your readings" : "Create your account"}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="form-error">{error}</div>}
          {success && <div className="form-success">{success}</div>}

          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              required
              className="form-input"
            />
          </div>

          {!isLogin && (
            <>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="firstName" className="form-label">
                    First Name
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleChange}
                    placeholder="John"
                    required={!isLogin}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="lastName" className="form-label">
                    Last Name
                  </label>
                  <input
                    type="text"
                    id="lastName"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleChange}
                    placeholder="Doe"
                    required={!isLogin}
                    className="form-input"
                  />
                </div>
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Min. 8 characters"
              required
              className="form-input"
            />
            {!isLogin && (
              <p className="form-help">
                Password must be at least 8 characters with uppercase and number
              </p>
            )}
          </div>

          <button type="submit" disabled={loading} className="form-button">
            {loading ? "Processing..." : isLogin ? "Sign In" : "Create Account"}
          </button>
        </form>

        <div className="auth-footer">
          <p className="auth-toggle">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError("");
                setSuccess("");
              }}
              className="auth-toggle-button"
            >
              {isLogin ? "Sign Up" : "Sign In"}
            </button>
          </p>
        </div>

        <div className="auth-demo">
          <p className="auth-demo-title">Demo Account:</p>
          <code className="auth-demo-code">laplace@mula.app</code>
          <code className="auth-demo-code">Mula2025!Astrology</code>
        </div>
      </div>
    </div>
  );
}
