"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import "./readings.css";

interface Reading {
  id: string;
  reading_type: string;
  data: {
    card_name?: string;
    card_description?: string;
    advisor_name?: string;
    message_count?: number;
  };
  created_at: string;
}

interface ReadingsResponse {
  readings: Reading[];
  total: number;
  page: number;
  total_pages: number;
}

export default function ReadingsPage() {
  const [readings, setReadings] = useState<Reading[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 20;

  useEffect(() => {
    const fetchReadings = async () => {
      try {
        const token = localStorage.getItem("access_token");

        // Demo fallback if no token
        if (!token) {
          setReadings([
            {
              id: "reading-1",
              reading_type: "fortune",
              data: {
                card_name: "The Crossroads",
                card_description: "A time of important decisions",
              },
              created_at: new Date(
                Date.now() - 2 * 60 * 60 * 1000
              ).toISOString(), // 2 hours ago
            },
            {
              id: "reading-2",
              reading_type: "consultation",
              data: {
                advisor_name: "Papa Legba",
                message_count: 5,
              },
              created_at: new Date(
                Date.now() - 24 * 60 * 60 * 1000
              ).toISOString(), // 1 day ago
            },
            {
              id: "reading-3",
              reading_type: "fortune",
              data: {
                card_name: "The Mountain",
                card_description: "Strength and perseverance",
              },
              created_at: new Date(
                Date.now() - 3 * 24 * 60 * 60 * 1000
              ).toISOString(), // 3 days ago
            },
          ]);
          setTotalPages(1);
          setIsLoading(false);
          return;
        }

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/v1/readings?page=${page}&limit=${itemsPerPage}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (!response.ok) throw new Error("Failed to load readings");
        const data: ReadingsResponse = await response.json();
        setReadings(data.readings);
        setTotalPages(data.total_pages || 1);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error loading readings");
        // Fallback to demo data on error
        setReadings([
          {
            id: "reading-1",
            reading_type: "fortune",
            data: {
              card_name: "The Crossroads",
              card_description: "A time of important decisions",
            },
            created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          },
        ]);
        setTotalPages(1);
      } finally {
        setIsLoading(false);
      }
    };

    fetchReadings();
  }, [page, itemsPerPage]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  if (isLoading) {
    return (
      <div className="readings-container">
        <div className="loading">Loading readings...</div>
      </div>
    );
  }

  return (
    <div className="readings-container">
      <div className="readings-header">
        <h1>Reading History</h1>
      </div>

      {error && <div className="error-message">{error}</div>}

      {readings.length === 0 ? (
        <div className="empty-state">
          <p>No readings yet.</p>
          <Link href="/fortune" className="btn-primary">
            Get a Fortune Reading
          </Link>
        </div>
      ) : (
        <>
          <div className="readings-list">
            {readings.map((reading) => (
              <Link
                key={reading.id}
                href={`/readings/${reading.id}`}
                className="reading-card"
              >
                <div className="card-header">
                  <h3>
                    {reading.reading_type === "fortune"
                      ? "🃏 Fortune Card"
                      : "🔮 Consultation"}
                  </h3>
                  <span className="date">{formatDate(reading.created_at)}</span>
                </div>
                <div className="card-preview">
                  {reading.reading_type === "fortune" ? (
                    <>
                      <p className="card-name">{reading.data?.card_name}</p>
                      <p className="card-desc">
                        {reading.data?.card_description}
                      </p>
                    </>
                  ) : (
                    <>
                      <p className="advisor-name">
                        Advisor: {reading.data?.advisor_name}
                      </p>
                      <p className="message-count">
                        {reading.data?.message_count} messages
                      </p>
                    </>
                  )}
                </div>
              </Link>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button
                disabled={page === 1}
                onClick={() => setPage(page - 1)}
                className="btn-pagination"
              >
                ← Previous
              </button>
              <span className="page-info">
                Page {page} of {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
                className="btn-pagination"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
