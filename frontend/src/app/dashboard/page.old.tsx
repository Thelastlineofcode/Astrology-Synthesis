"use client";

import React, { useState, useEffect } from "react";
import QuickChartCard from "@/components/dashboard/QuickChartCard";
import RecentChartsCard from "@/components/dashboard/RecentChartsCard";
import "./dashboard.css";

interface Chart {
  id: string;
  name?: string;
  date: string;
}

export default function Dashboard() {
  const [recentCharts, setRecentCharts] = useState<Chart[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch recent charts from localStorage
    try {
      const storedCharts = localStorage.getItem("recentCharts");
      const charts = storedCharts ? JSON.parse(storedCharts) : [];
      setRecentCharts(charts.slice(0, 3));
    } catch (error) {
      console.error("Error loading recent charts:", error);
      setRecentCharts([]);
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <h1>Your Astrology Dashboard</h1>
        <p className="dashboard__subtitle">
          Welcome back. Ready to explore the cosmos?
        </p>
      </header>

      <div className="dashboard__grid">
        <QuickChartCard />

        <RecentChartsCard charts={recentCharts} loading={loading} />
      </div>
    </div>
  );
}
