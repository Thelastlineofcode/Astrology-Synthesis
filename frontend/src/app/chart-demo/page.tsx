"use client";

import React, { useState } from "react";
import ChartCanvas from "@/components/chart/ChartCanvas";
import { mockChartData } from "@/components/chart/mockChartData";
import { api } from "@/lib/api";
import Button from "@/components/shared/Button";

export default function ChartDemoPage() {
  const [chartData, setChartData] = useState(mockChartData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    date: "1984-12-19",
    time: "12:00",
    latitude: "29.9844",
    longitude: "-90.1547",
    locationName: "Metairie, LA",
    timezone: "America/Chicago",
  });

  const handleCalculate = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.charts.calculate({
        date: formData.date,
        time: formData.time + ":00",
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        timezone: formData.timezone,
        location_name: formData.locationName,
      });

      if (response.chart_data) {
        setChartData(response.chart_data);
      }
    } catch (err: any) {
      setError(err.message || "Failed to calculate chart");
      console.error("Chart calculation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: "2rem",
        maxWidth: "1200px",
        margin: "0 auto",
        minHeight: "100vh",
      }}
    >
      <h1
        style={{
          fontSize: "2rem",
          fontWeight: "bold",
          marginBottom: "1rem",
          color: "var(--text-primary)",
        }}
      >
        Interactive Natal Chart Calculator
      </h1>

      <p
        style={{
          marginBottom: "2rem",
          color: "var(--text-secondary)",
          lineHeight: "1.6",
        }}
      >
        This is a demonstration of the interactive natal chart canvas. Try
        zooming in and out, toggling aspects, and hovering over planets to see
        their details.
      </p>

      <div style={{ marginBottom: "2rem" }}>
        <h2
          style={{
            fontSize: "1.25rem",
            fontWeight: "600",
            marginBottom: "0.5rem",
            color: "var(--text-primary)",
          }}
        >
          Sample Chart Data
        </h2>
        <p style={{ color: "var(--text-secondary)" }}>
          Birth: December 19, 1984, Metairie, LA
        </p>
      </div>

      <ChartCanvas chartData={mockChartData} />

      <div
        style={{
          marginTop: "3rem",
          padding: "1.5rem",
          backgroundColor: "var(--bg-secondary)",
          borderRadius: "8px",
        }}
      >
        <h3
          style={{
            fontSize: "1.125rem",
            fontWeight: "600",
            marginBottom: "1rem",
            color: "var(--text-primary)",
          }}
        >
          Features
        </h3>
        <ul
          style={{
            listStyleType: "disc",
            paddingLeft: "1.5rem",
            color: "var(--text-primary)",
            lineHeight: "1.8",
          }}
        >
          <li>Interactive SVG chart with zoom controls</li>
          <li>12 houses with division lines</li>
          <li>Planet glyphs with accurate positioning</li>
          <li>Zodiac signs around perimeter</li>
          <li>Toggleable aspect lines between planets</li>
          <li>Hover tooltips showing planet details</li>
          <li>Keyboard accessible (Tab to planets, Enter to show tooltip)</li>
          <li>Responsive design for mobile, tablet, and desktop</li>
        </ul>
      </div>
    </div>
  );
}
