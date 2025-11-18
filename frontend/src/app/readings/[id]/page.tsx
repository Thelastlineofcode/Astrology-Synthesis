"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import "./detail.css";

interface ReadingDetail {
  id: string;
  reading_type: string;
  data: {
    card_name?: string;
    card_description?: string;
    card_interpretation?: string;
    element?: string;
    planet?: string;
    advisor_name?: string;
    messages?: Array<{
      role: string;
      content: string;
      timestamp: string;
    }>;
  };
  created_at: string;
}

export default function ReadingDetailPage() {
  const params = useParams();
  const router = useRouter();
  const readingId = params?.id as string;

  const [reading, setReading] = useState<ReadingDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchReadingDetail = async () => {
      try {
        const token = localStorage.getItem("access_token");

        // Demo fallback if no token
        if (
          !token ||
          readingId === "reading-1" ||
          readingId === "reading-2" ||
          readingId === "reading-3"
        ) {
          setReading({
            id: readingId,
            reading_type:
              readingId === "reading-2" ? "consultation" : "fortune",
            data:
              readingId === "reading-2"
                ? {
                    advisor_name: "Papa Legba",
                    messages: [
                      {
                        role: "user",
                        content: "What guidance do you have for me today?",
                        timestamp: new Date(
                          Date.now() - 24 * 60 * 60 * 1000
                        ).toISOString(),
                      },
                      {
                        role: "assistant",
                        content:
                          "Welcome, seeker. The crossroads before you hold many paths. Trust your intuition and the wisdom of your ancestors.",
                        timestamp: new Date(
                          Date.now() - 24 * 60 * 60 * 1000 + 60000
                        ).toISOString(),
                      },
                    ],
                  }
                : {
                    card_name: "The Crossroads",
                    card_description: "A time of important decisions",
                    card_interpretation:
                      "You stand at a significant crossroads in your life. Multiple paths stretch before you, each holding different opportunities and challenges. This is a time to carefully consider your options, trust your inner wisdom, and choose the path that aligns with your true purpose.",
                    element: "Air",
                    planet: "Mercury",
                  },
            created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          });
          setIsLoading(false);
          return;
        }

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/v1/readings/${readingId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (!response.ok) throw new Error("Failed to load reading");
        const data: ReadingDetail = await response.json();
        setReading(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error loading reading");
      } finally {
        setIsLoading(false);
      }
    };

    fetchReadingDetail();
  }, [readingId]);

  if (isLoading) {
    return (
      <div className="reading-detail-container">
        <div className="loading">Loading reading...</div>
      </div>
    );
  }

  if (error || !reading) {
    return (
      <div className="reading-detail-container">
        <div className="error-state">
          <h2>Reading Not Found</h2>
          <p>{error || "This reading could not be loaded."}</p>
          <button onClick={() => router.push("/readings")} className="btn-back">
            Back to History
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="reading-detail-container">
      <button onClick={() => router.back()} className="btn-back-arrow">
        ← Back
      </button>

      <div className="reading-detail-card">
        <div className="reading-header">
          <h1>
            {reading.reading_type === "fortune"
              ? "🃏 Fortune Reading"
              : "🔮 Consultation"}
          </h1>
          <span className="date">
            {new Date(reading.created_at).toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>

        {reading.reading_type === "fortune" ? (
          <div className="fortune-content">
            <div className="card-title">
              <h2>{reading.data.card_name}</h2>
              <p className="card-subtitle">{reading.data.card_description}</p>
            </div>

            {reading.data.card_interpretation && (
              <div className="card-interpretation">
                <h3>Interpretation</h3>
                <p>{reading.data.card_interpretation}</p>
              </div>
            )}

            {(reading.data.element || reading.data.planet) && (
              <div className="card-metadata">
                {reading.data.element && (
                  <div className="metadata-item">
                    <span className="label">Element</span>
                    <span className="value">{reading.data.element}</span>
                  </div>
                )}
                {reading.data.planet && (
                  <div className="metadata-item">
                    <span className="label">Planet</span>
                    <span className="value">{reading.data.planet}</span>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          <div className="consultation-content">
            <div className="advisor-header">
              <h2>Advisor: {reading.data.advisor_name}</h2>
            </div>

            {reading.data.messages && (
              <div className="messages-thread">
                {reading.data.messages.map((msg, idx) => (
                  <div key={idx} className={`message ${msg.role}`}>
                    <p className="message-content">{msg.content}</p>
                    <span className="message-time">
                      {new Date(msg.timestamp).toLocaleTimeString("en-US", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
