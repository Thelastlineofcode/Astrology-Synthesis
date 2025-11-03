"use client";

import React, { useState } from "react";
import ChartCanvas from "@/components/chart/ChartCanvas";
import { mockChartData } from "@/components/chart/mockChartData";

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
  const [chartData] = useState(mockChartData);
  const [showForm, setShowForm] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  const handleGenerateChart = async () => {
    setLoading(true);
    setError(null);

    try {
      // Note: This requires authentication. For now, using mock data
      // When you add auth, uncomment this:
      /*
      const response = await fetch('http://localhost:8001/api/v1/chart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${yourAuthToken}`
        },
        body: JSON.stringify({
          birth_data: {
            ...birthData,
            time: birthData.time + ':00' // Add seconds
          }
        })
      });
      
      if (!response.ok) throw new Error('Chart generation failed');
      const data = await response.json();
      setChartData(data.chart_data);
      */

      // For now, using mock data with the entered birth info
      console.log("Would generate chart for:", birthData);
      alert(
        `Chart calculation ready!\n\nTo connect to backend:\n1. Implement authentication\n2. Uncomment API call in code\n3. Backend is running on port 8001`
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate chart");
    } finally {
      setLoading(false);
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
            disabled={loading}
            style={{
              marginTop: "1.5rem",
              padding: "1rem 2rem",
              backgroundColor: loading ? "#666" : "var(--accent-golden)",
              color: "var(--bg-cosmic-dark)",
              border: "none",
              borderRadius: "8px",
              cursor: loading ? "not-allowed" : "pointer",
              fontSize: "1.125rem",
              fontWeight: "600",
              width: "100%",
              transition: "all 0.2s",
            }}
          >
            {loading ? "Calculating..." : "✨ Generate Birth Chart"}
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
