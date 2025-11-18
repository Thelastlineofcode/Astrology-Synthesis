"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import ChartCanvas from "@/components/chart/ChartCanvas";
import { mockChartData } from "@/components/chart/mockChartData";
import authService from "@/services/auth";
import chartService from "@/services/chart";
import predictionService, { PredictionResponse } from "@/services/prediction";

interface BirthData {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
  location_name: string;
}

interface Prediction {
  id: string;
  type: "transit" | "dasha" | "progression" | "aspect" | "custom";
  title: string;
  description: string;
  timestamp: string;
  verified?: boolean;
  accuracy?: number;
  notes?: string;
}

export default function NewChartReadingPage() {
  const router = useRouter();
  const [chartData, setChartData] = useState(mockChartData);
  const [showForm, setShowForm] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Prediction state
  const [predictionData, setPredictionData] =
    useState<PredictionResponse | null>(null);
  const [isGeneratingPrediction, setIsGeneratingPrediction] = useState(false);
  const [predictionQuery] = useState(
    "Generate a comprehensive reading covering career, relationships, health, and finances for the next 90 days."
  );

  // Client notes and predictions
  const [clientNotes, setClientNotes] = useState("");
  const [methodNotes, setMethodNotes] = useState("");
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [newPrediction, setNewPrediction] = useState({
    type: "custom",
    title: "",
    description: "",
  });

  // Form state
  const [birthData, setBirthData] = useState<BirthData>({
    date: "1984-12-19",
    time: "12:00",
    latitude: 29.9844,
    longitude: -90.1547,
    timezone: "America/Chicago",
    location_name: "Metairie, LA",
  });

  // Check authentication on mount
  useEffect(() => {
    const authenticated = authService.isAuthenticated();

    if (!authenticated) {
      router.push("/auth/login");
    }
  }, [router]);

  // Transform backend chart data to frontend format
  const transformChartData = (backendData: Record<string, unknown>) => {
    console.log("Transforming backend data:", backendData);

    // Convert planet_positions array to planets object
    const planets: Record<string, unknown> = {};
    if (
      backendData.planet_positions &&
      Array.isArray(backendData.planet_positions)
    ) {
      (backendData.planet_positions as Array<Record<string, unknown>>).forEach(
        (p: Record<string, unknown>) => {
          planets[p.planet as string] = {
            longitude: p.longitude,
            sign: p.zodiac_sign,
            degree: p.degree,
            house: p.house,
            retrograde: p.retrograde,
            nakshatra: p.nakshatra,
            pada: p.pada,
          };
        }
      );
      console.log("Transformed planets:", planets);
    } else {
      console.error("No planet_positions in backend data!");
    }

    // Convert house_cusps array to houses object
    const houses: Record<string, unknown> = {};
    if (backendData.house_cusps && Array.isArray(backendData.house_cusps)) {
      (backendData.house_cusps as Array<Record<string, unknown>>).forEach(
        (h: Record<string, unknown>) => {
          houses[`house_${h.house}`] = {
            longitude: h.longitude || h.cusp,
            sign: h.zodiac_sign,
            degree: h.degree,
          };
        }
      );
      console.log("Transformed houses:", houses);
    } else {
      console.error("No house_cusps in backend data!");
    }

    const result = {
      planets,
      houses,
      aspects: backendData.aspects || [],
    };

    console.log("Final transformed data:", result);
    return result;
  };

  const handleGenerateChart = async () => {
    setIsGenerating(true);
    setError(null);
    setPredictionData(null);

    try {
      if (!authService.isAuthenticated()) {
        setError("Please log in to generate charts");
        router.push("/auth/login");
        return;
      }

      console.log("🔮 Generating chart with data:", birthData);

      // Step 1: Generate Chart
      const chartResponse = await chartService.generateChart({
        birth_date: birthData.date,
        birth_time: `${birthData.time}:00`,
        birth_location: birthData.location_name,
        latitude: birthData.latitude,
        longitude: birthData.longitude,
        timezone: birthData.timezone,
      });

      console.log("✅ Chart API response:", chartResponse);

      // Check if chart_data exists and has the expected structure
      if (!chartResponse.chart_data) {
        throw new Error("No chart data received from server");
      }

      if (
        !chartResponse.chart_data.planet_positions ||
        !chartResponse.chart_data.house_cusps
      ) {
        console.error(
          "Invalid chart data structure:",
          chartResponse.chart_data
        );
        throw new Error("Invalid chart data structure received from server");
      }

      // Transform and update chart with real data from API
      const transformedData = transformChartData(chartResponse.chart_data);
      setChartData(transformedData as typeof mockChartData);
      console.log("✅ Chart data transformed and set!");

      // Step 2: Generate Predictions (the main function!)
      console.log("🔮 Generating predictions...");
      setIsGeneratingPrediction(true);

      try {
        const predictionResponse = await predictionService.generatePrediction({
          birth_data: {
            date: birthData.date,
            time: `${birthData.time}:00`,
            location_name: birthData.location_name,
            latitude: birthData.latitude,
            longitude: birthData.longitude,
            timezone: birthData.timezone,
          },
          query: predictionQuery,
          prediction_window_days: 90,
        });

        console.log("✅ Prediction API response:", predictionResponse);
        setPredictionData(predictionResponse);
        console.log(
          `✨ Generated ${predictionResponse.events.length} predictions with ${(predictionResponse.confidence_score * 100).toFixed(1)}% confidence`
        );
      } catch (predError) {
        console.error("⚠️ Prediction generation failed:", predError);
        // Don't fail the whole operation if predictions fail
        setError("Chart generated but predictions failed. Please try again.");
      } finally {
        setIsGeneratingPrediction(false);
      }
    } catch (err) {
      const errorMsg =
        err instanceof Error ? err.message : "Failed to generate chart";
      setError(errorMsg);
      console.error("❌ Chart generation error:", err);

      // If auth error, redirect to login
      if (errorMsg.includes("expired") || errorMsg.includes("authenticated")) {
        setTimeout(() => router.push("/auth/login"), 2000);
      }
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div
      style={{
        padding: "2rem",
        maxWidth: "1400px",
        margin: "0 auto",
        minHeight: "100vh",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "2rem",
        }}
      >
        <h1
          style={{
            fontSize: "2rem",
            fontWeight: "bold",
            color: "var(--accent-golden)",
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
          }}
        >
          Chart Reading Tool
        </h1>
        <button
          onClick={() => setShowForm(!showForm)}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "var(--accent-purple)",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "0.875rem",
          }}
        >
          {showForm ? "Hide Form" : "Show Form"}
        </button>
      </div>

      {showForm && (
        <div
          style={{
            marginBottom: "2rem",
            padding: "2rem",
            backgroundColor: "var(--bg-card-surface)",
            borderRadius: "12px",
            boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
          }}
        >
          <h2
            style={{
              fontSize: "1.5rem",
              fontWeight: "600",
              marginBottom: "1.5rem",
              color: "var(--accent-golden)",
            }}
          >
            Enter Client Birth Data
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {/* Name/Location */}
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "0.5rem",
                  color: "var(--text-primary)",
                  fontWeight: "500",
                }}
              >
                Location Name
              </label>
              <input
                type="text"
                value={birthData.location_name}
                onChange={(e) =>
                  setBirthData({ ...birthData, location_name: e.target.value })
                }
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  backgroundColor: "var(--bg-input)",
                  border: "1px solid var(--accent-purple)",
                  borderRadius: "8px",
                  color: "var(--text-primary)",
                  fontSize: "1rem",
                }}
                placeholder="e.g., Metairie, LA"
              />
            </div>

            {/* Birth Date */}
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "0.5rem",
                  color: "var(--text-primary)",
                  fontWeight: "500",
                }}
              >
                Birth Date
              </label>
              <input
                type="date"
                value={birthData.date}
                onChange={(e) =>
                  setBirthData({ ...birthData, date: e.target.value })
                }
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  backgroundColor: "var(--bg-input)",
                  border: "1px solid var(--accent-purple)",
                  borderRadius: "8px",
                  color: "var(--text-primary)",
                  fontSize: "1rem",
                }}
              />
            </div>

            {/* Birth Time */}
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "0.5rem",
                  color: "var(--text-primary)",
                  fontWeight: "500",
                }}
              >
                Birth Time
              </label>
              <input
                type="time"
                value={birthData.time}
                onChange={(e) =>
                  setBirthData({ ...birthData, time: e.target.value })
                }
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  backgroundColor: "var(--bg-input)",
                  border: "1px solid var(--accent-purple)",
                  borderRadius: "8px",
                  color: "var(--text-primary)",
                  fontSize: "1rem",
                }}
              />
            </div>

            {/* Latitude */}
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "0.5rem",
                  color: "var(--text-primary)",
                  fontWeight: "500",
                }}
              >
                Latitude
              </label>
              <input
                type="number"
                step="0.0001"
                value={birthData.latitude}
                onChange={(e) =>
                  setBirthData({
                    ...birthData,
                    latitude: parseFloat(e.target.value),
                  })
                }
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  backgroundColor: "var(--bg-input)",
                  border: "1px solid var(--accent-purple)",
                  borderRadius: "8px",
                  color: "var(--text-primary)",
                  fontSize: "1rem",
                }}
              />
            </div>

            {/* Longitude */}
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "0.5rem",
                  color: "var(--text-primary)",
                  fontWeight: "500",
                }}
              >
                Longitude
              </label>
              <input
                type="number"
                step="0.0001"
                value={birthData.longitude}
                onChange={(e) =>
                  setBirthData({
                    ...birthData,
                    longitude: parseFloat(e.target.value),
                  })
                }
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  backgroundColor: "var(--bg-input)",
                  border: "1px solid var(--accent-purple)",
                  borderRadius: "8px",
                  color: "var(--text-primary)",
                  fontSize: "1rem",
                }}
              />
            </div>

            {/* Timezone */}
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "0.5rem",
                  color: "var(--text-primary)",
                  fontWeight: "500",
                }}
              >
                Timezone
              </label>
              <select
                value={birthData.timezone}
                onChange={(e) =>
                  setBirthData({ ...birthData, timezone: e.target.value })
                }
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  backgroundColor: "var(--bg-input)",
                  border: "1px solid var(--accent-purple)",
                  borderRadius: "8px",
                  color: "var(--text-primary)",
                  fontSize: "1rem",
                }}
              >
                <option value="America/New_York">Eastern (ET)</option>
                <option value="America/Chicago">Central (CT)</option>
                <option value="America/Denver">Mountain (MT)</option>
                <option value="America/Los_Angeles">Pacific (PT)</option>
                <option value="America/Phoenix">Arizona</option>
                <option value="America/Anchorage">Alaska</option>
                <option value="Pacific/Honolulu">Hawaii</option>
              </select>
            </div>
          </div>

          {error && (
            <div
              style={{
                marginTop: "1rem",
                padding: "1rem",
                backgroundColor: "rgba(232, 111, 77, 0.1)",
                border: "1px solid var(--accent-orange)",
                borderRadius: "8px",
                color: "var(--accent-orange)",
              }}
            >
              {error}
            </div>
          )}

          <button
            onClick={handleGenerateChart}
            disabled={isGenerating}
            style={{
              marginTop: "1.5rem",
              padding: "1rem 2rem",
              backgroundColor: isGenerating ? "#666" : "var(--accent-golden)",
              color: "var(--bg-cosmic-dark)",
              border: "none",
              borderRadius: "8px",
              cursor: isGenerating ? "not-allowed" : "pointer",
              fontSize: "1.125rem",
              fontWeight: "600",
              width: "100%",
              transition: "all 0.2s",
            }}
          >
            {isGenerating
              ? "🔮 Generating Chart & Predictions..."
              : "✨ Generate Chart & Reading"}
          </button>

          <div
            style={{
              marginTop: "1rem",
              padding: "1rem",
              backgroundColor: "rgba(139, 111, 168, 0.1)",
              borderRadius: "8px",
            }}
          >
            <p
              style={{
                color: "var(--text-secondary)",
                fontSize: "0.875rem",
                margin: 0,
              }}
            >
              <strong>Note:</strong> Currently using sample data. To connect to
              backend:
              <br />• Backend is running on <code>http://localhost:8001</code>
              <br />• Add authentication (register/login at{" "}
              <code>/api/v1/auth/register</code>)
              <br />• Uncomment API call in the code (see console)
            </p>
          </div>
        </div>
      )}

      <div
        style={{
          padding: "1rem",
          backgroundColor: "var(--bg-card-surface)",
          borderRadius: "8px",
          marginBottom: "1rem",
        }}
      >
        <h3 style={{ color: "var(--accent-golden)", marginBottom: "0.5rem" }}>
          Current Chart: {birthData.location_name}
        </h3>
        <p
          style={{
            color: "var(--text-secondary)",
            fontSize: "0.875rem",
            margin: 0,
          }}
        >
          {birthData.date} at {birthData.time} • {birthData.latitude.toFixed(4)}
          °N, {birthData.longitude.toFixed(4)}°W
        </p>
      </div>

      <ChartCanvas chartData={chartData} />

      {/* AI-Generated Predictions Section */}
      {predictionData && (
        <div
          style={{
            marginTop: "2rem",
            padding: "2rem",
            backgroundColor: "var(--bg-card-surface)",
            borderRadius: "12px",
            border: "3px solid var(--accent-golden)",
            boxShadow: "0 4px 20px rgba(218, 165, 32, 0.2)",
          }}
        >
          <div style={{ marginBottom: "1.5rem" }}>
            <h2
              style={{
                fontSize: "1.75rem",
                fontWeight: "bold",
                color: "var(--accent-golden)",
                marginBottom: "0.5rem",
                display: "flex",
                alignItems: "center",
                gap: "0.75rem",
              }}
            >
              ✨ Syncretic Astrological Reading
            </h2>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem" }}>
              Based on KP Astrology, Vimshottari Dasha & Transit Analysis
            </p>
          </div>

          {/* Confidence Score */}
          <div
            style={{
              display: "flex",
              gap: "2rem",
              marginBottom: "2rem",
              padding: "1rem",
              backgroundColor: "rgba(139, 92, 246, 0.1)",
              borderRadius: "8px",
              flexWrap: "wrap",
            }}
          >
            <div>
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--text-secondary)",
                  marginBottom: "0.25rem",
                }}
              >
                Overall Confidence
              </div>
              <div
                style={{
                  fontSize: "1.5rem",
                  fontWeight: "bold",
                  color: "var(--accent-golden)",
                }}
              >
                {(predictionData.confidence_score * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--text-secondary)",
                  marginBottom: "0.25rem",
                }}
              >
                KP Contribution
              </div>
              <div
                style={{
                  fontSize: "1.25rem",
                  fontWeight: "600",
                  color: "var(--accent-purple)",
                }}
              >
                {(predictionData.kp_contribution * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--text-secondary)",
                  marginBottom: "0.25rem",
                }}
              >
                Dasha Contribution
              </div>
              <div
                style={{
                  fontSize: "1.25rem",
                  fontWeight: "600",
                  color: "var(--accent-purple)",
                }}
              >
                {(predictionData.dasha_contribution * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--text-secondary)",
                  marginBottom: "0.25rem",
                }}
              >
                Transit Contribution
              </div>
              <div
                style={{
                  fontSize: "1.25rem",
                  fontWeight: "600",
                  color: "var(--accent-purple)",
                }}
              >
                {(predictionData.transit_contribution * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--text-secondary)",
                  marginBottom: "0.25rem",
                }}
              >
                Events Identified
              </div>
              <div
                style={{
                  fontSize: "1.25rem",
                  fontWeight: "600",
                  color: "var(--text-primary)",
                }}
              >
                {predictionData.events.length}
              </div>
            </div>
          </div>

          {/* Prediction Events */}
          <div>
            <h3
              style={{
                fontSize: "1.25rem",
                fontWeight: "600",
                color: "var(--text-primary)",
                marginBottom: "1rem",
              }}
            >
              Predicted Events (Next 90 Days)
            </h3>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
            >
              {predictionData.events.map((event, index) => (
                <div
                  key={index}
                  style={{
                    padding: "1.25rem",
                    backgroundColor: "var(--bg-input)",
                    borderRadius: "8px",
                    border: `2px solid ${
                      event.strength_score > 0.7
                        ? "var(--accent-golden)"
                        : event.strength_score > 0.4
                          ? "var(--accent-purple)"
                          : "var(--accent-blue)"
                    }`,
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "start",
                      marginBottom: "0.75rem",
                      flexWrap: "wrap",
                      gap: "0.5rem",
                    }}
                  >
                    <div>
                      <div
                        style={{
                          fontSize: "1.1rem",
                          fontWeight: "600",
                          color: "var(--text-primary)",
                          marginBottom: "0.25rem",
                        }}
                      >
                        {event.event_type.replace(/_/g, " ").toUpperCase()}
                      </div>
                      <div
                        style={{
                          fontSize: "0.875rem",
                          color: "var(--text-secondary)",
                        }}
                      >
                        {new Date(event.event_date).toLocaleDateString(
                          "en-US",
                          {
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          }
                        )}
                      </div>
                    </div>
                    <div
                      style={{
                        padding: "0.25rem 0.75rem",
                        backgroundColor:
                          event.strength_score > 0.7
                            ? "rgba(218, 165, 32, 0.2)"
                            : event.strength_score > 0.4
                              ? "rgba(139, 92, 246, 0.2)"
                              : "rgba(59, 130, 246, 0.2)",
                        borderRadius: "12px",
                        fontSize: "0.875rem",
                        fontWeight: "600",
                        color:
                          event.strength_score > 0.7
                            ? "var(--accent-golden)"
                            : event.strength_score > 0.4
                              ? "var(--accent-purple)"
                              : "var(--accent-blue)",
                      }}
                    >
                      {(event.strength_score * 100).toFixed(0)}% Strength
                    </div>
                  </div>

                  {event.influence_area && (
                    <div
                      style={{
                        fontSize: "0.875rem",
                        color: "var(--accent-purple)",
                        marginBottom: "0.5rem",
                        fontWeight: "500",
                      }}
                    >
                      📍 {event.influence_area}
                    </div>
                  )}

                  {(event.primary_planet || event.secondary_planet) && (
                    <div
                      style={{
                        fontSize: "0.875rem",
                        color: "var(--text-secondary)",
                        marginBottom: "0.75rem",
                      }}
                    >
                      🪐 Planets:{" "}
                      {[event.primary_planet, event.secondary_planet]
                        .filter(Boolean)
                        .join(" • ")}
                    </div>
                  )}

                  <p
                    style={{
                      color: "var(--text-primary)",
                      lineHeight: "1.6",
                      marginBottom: "0.75rem",
                    }}
                  >
                    {event.description}
                  </p>

                  {event.recommendation && (
                    <div
                      style={{
                        marginTop: "0.75rem",
                        padding: "0.75rem",
                        backgroundColor: "rgba(34, 197, 94, 0.1)",
                        borderRadius: "6px",
                        borderLeft: "3px solid rgba(34, 197, 94, 0.5)",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "0.875rem",
                          fontWeight: "600",
                          color: "rgba(34, 197, 94, 1)",
                          marginBottom: "0.25rem",
                        }}
                      >
                        💡 Recommendation
                      </div>
                      <div
                        style={{
                          fontSize: "0.875rem",
                          color: "var(--text-primary)",
                        }}
                      >
                        {event.recommendation}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Query Info */}
          <div
            style={{
              marginTop: "2rem",
              padding: "1rem",
              backgroundColor: "rgba(139, 92, 246, 0.05)",
              borderRadius: "8px",
              fontSize: "0.875rem",
              color: "var(--text-secondary)",
            }}
          >
            <div style={{ marginBottom: "0.5rem" }}>
              <strong>Query:</strong> {predictionData.query}
            </div>
            <div>
              <strong>Prediction Window:</strong>{" "}
              {new Date(
                predictionData.prediction_window_start
              ).toLocaleDateString()}{" "}
              -{" "}
              {new Date(
                predictionData.prediction_window_end
              ).toLocaleDateString()}
            </div>
            <div style={{ marginTop: "0.5rem", fontSize: "0.75rem" }}>
              Calculated in {predictionData.calculation_time_ms.toFixed(2)}ms •
              Model v{predictionData.model_version}
            </div>
          </div>
        </div>
      )}

      {/* Loading State for Predictions */}
      {isGeneratingPrediction && (
        <div
          style={{
            marginTop: "2rem",
            padding: "2rem",
            backgroundColor: "var(--bg-card-surface)",
            borderRadius: "12px",
            border: "2px solid var(--accent-purple)",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>🔮</div>
          <div
            style={{
              fontSize: "1.25rem",
              fontWeight: "600",
              color: "var(--accent-golden)",
            }}
          >
            Generating Syncretic Predictions...
          </div>
          <div
            style={{
              fontSize: "0.95rem",
              color: "var(--text-secondary)",
              marginTop: "0.5rem",
            }}
          >
            Analyzing KP Astrology, Dasha periods, and transits...
          </div>
        </div>
      )}

      {/* Predictions & Method Tracking Section */}
      <div
        style={{
          marginTop: "2rem",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
          gap: "1.5rem",
        }}
      >
        {/* Predictions Panel */}
        <div
          style={{
            padding: "1.5rem",
            backgroundColor: "var(--bg-card-surface)",
            borderRadius: "12px",
            border: "2px solid var(--accent-purple)",
          }}
        >
          <h3
            style={{
              fontSize: "1.25rem",
              fontWeight: "600",
              marginBottom: "1rem",
              color: "var(--accent-golden)",
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
            }}
          >
            🔮 Predictions & Forecasts
          </h3>

          {/* Add New Prediction */}
          <div style={{ marginBottom: "1.5rem" }}>
            <select
              value={newPrediction.type}
              onChange={(e) =>
                setNewPrediction({
                  ...newPrediction,
                  type: e.target.value as Prediction["type"],
                })
              }
              style={{
                width: "100%",
                padding: "0.75rem",
                marginBottom: "0.75rem",
                backgroundColor: "var(--bg-input)",
                border: "1px solid var(--accent-purple)",
                borderRadius: "8px",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
              }}
            >
              <option value="transit">Transit</option>
              <option value="dasha">Dasha Period</option>
              <option value="progression">Progression</option>
              <option value="aspect">Aspect</option>
              <option value="custom">Custom Method</option>
            </select>

            <input
              type="text"
              placeholder="Prediction title..."
              value={newPrediction.title}
              onChange={(e) =>
                setNewPrediction({ ...newPrediction, title: e.target.value })
              }
              style={{
                width: "100%",
                padding: "0.75rem",
                marginBottom: "0.75rem",
                backgroundColor: "var(--bg-input)",
                border: "1px solid var(--accent-purple)",
                borderRadius: "8px",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
              }}
            />

            <textarea
              placeholder="Prediction details and reasoning..."
              value={newPrediction.description}
              onChange={(e) =>
                setNewPrediction({
                  ...newPrediction,
                  description: e.target.value,
                })
              }
              style={{
                width: "100%",
                padding: "0.75rem",
                marginBottom: "0.75rem",
                backgroundColor: "var(--bg-input)",
                border: "1px solid var(--accent-purple)",
                borderRadius: "8px",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
                minHeight: "80px",
                fontFamily: "inherit",
                resize: "vertical",
              }}
            />

            <button
              onClick={() => {
                if (newPrediction.title && newPrediction.description) {
                  setPredictions([
                    ...predictions,
                    {
                      id: Date.now().toString(),
                      type: newPrediction.type as Prediction["type"],
                      title: newPrediction.title,
                      description: newPrediction.description,
                      timestamp: new Date().toISOString(),
                    },
                  ]);
                  setNewPrediction({
                    type: "custom",
                    title: "",
                    description: "",
                  });
                }
              }}
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "var(--accent-golden)",
                color: "var(--bg-cosmic-dark)",
                border: "none",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "0.875rem",
                fontWeight: "600",
              }}
            >
              + Add Prediction
            </button>
          </div>

          {/* Predictions List */}
          <div style={{ maxHeight: "400px", overflowY: "auto" }}>
            {predictions.length === 0 ? (
              <p
                style={{
                  color: "var(--text-secondary)",
                  fontSize: "0.875rem",
                  textAlign: "center",
                  padding: "2rem",
                }}
              >
                No predictions yet. Add your first prediction above.
              </p>
            ) : (
              predictions.map((pred) => (
                <div
                  key={pred.id}
                  style={{
                    padding: "1rem",
                    marginBottom: "0.75rem",
                    backgroundColor: "var(--bg-input)",
                    borderRadius: "8px",
                    borderLeft: `4px solid ${
                      pred.type === "transit"
                        ? "#5FA9B8"
                        : pred.type === "dasha"
                          ? "#E8B598"
                          : pred.type === "progression"
                            ? "#8B6FA8"
                            : pred.type === "aspect"
                              ? "#E86F4D"
                              : "#666"
                    }`,
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      marginBottom: "0.5rem",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "0.75rem",
                        padding: "0.25rem 0.5rem",
                        backgroundColor: "var(--bg-cosmic-dark)",
                        borderRadius: "4px",
                        color: "var(--accent-golden)",
                      }}
                    >
                      {pred.type.toUpperCase()}
                    </span>
                    <span
                      style={{
                        fontSize: "0.75rem",
                        color: "var(--text-secondary)",
                      }}
                    >
                      {new Date(pred.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                  <h4
                    style={{
                      fontSize: "0.95rem",
                      fontWeight: "600",
                      color: "var(--text-primary)",
                      marginBottom: "0.5rem",
                    }}
                  >
                    {pred.title}
                  </h4>
                  <p
                    style={{
                      fontSize: "0.875rem",
                      color: "var(--text-secondary)",
                      lineHeight: "1.5",
                    }}
                  >
                    {pred.description}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Client & Method Notes Panel */}
        <div
          style={{
            padding: "1.5rem",
            backgroundColor: "var(--bg-card-surface)",
            borderRadius: "12px",
            border: "2px solid var(--accent-cyan)",
          }}
        >
          <h3
            style={{
              fontSize: "1.25rem",
              fontWeight: "600",
              marginBottom: "1rem",
              color: "var(--accent-golden)",
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
            }}
          >
            📝 Session Notes
          </h3>

          {/* Client Notes */}
          <div style={{ marginBottom: "1.5rem" }}>
            <label
              style={{
                display: "block",
                marginBottom: "0.5rem",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
                fontWeight: "600",
              }}
            >
              Client Notes & Observations
            </label>
            <textarea
              value={clientNotes}
              onChange={(e) => setClientNotes(e.target.value)}
              placeholder="Current life situation, questions asked, intuitive observations..."
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "var(--bg-input)",
                border: "1px solid var(--accent-cyan)",
                borderRadius: "8px",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
                minHeight: "150px",
                fontFamily: "inherit",
                resize: "vertical",
              }}
            />
          </div>

          {/* Method Notes */}
          <div>
            <label
              style={{
                display: "block",
                marginBottom: "0.5rem",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
                fontWeight: "600",
              }}
            >
              Method Development & Insights
            </label>
            <textarea
              value={methodNotes}
              onChange={(e) => setMethodNotes(e.target.value)}
              placeholder="New techniques discovered, accuracy observations, areas for improvement..."
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "var(--bg-input)",
                border: "1px solid var(--accent-cyan)",
                borderRadius: "8px",
                color: "var(--text-primary)",
                fontSize: "0.875rem",
                minHeight: "150px",
                fontFamily: "inherit",
                resize: "vertical",
              }}
            />
          </div>

          {/* Save Button */}
          <button
            onClick={() => {
              const sessionData = {
                birthData,
                clientNotes,
                methodNotes,
                predictions,
                timestamp: new Date().toISOString(),
              };
              console.log("Session saved:", sessionData);
              localStorage.setItem(
                `session_${Date.now()}`,
                JSON.stringify(sessionData)
              );
              alert("Session notes saved locally!");
            }}
            style={{
              width: "100%",
              marginTop: "1rem",
              padding: "0.75rem",
              backgroundColor: "var(--accent-cyan)",
              color: "var(--bg-cosmic-dark)",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "0.875rem",
              fontWeight: "600",
            }}
          >
            💾 Save Session Notes
          </button>
        </div>
      </div>
    </div>
  );
}
