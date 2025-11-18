"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Button from "@/components/shared/Button";
import "./dashboard.css";

interface Chart {
  id: string;
  name?: string;
  date: string;
  location?: string;
}

export default function Dashboard() {
  const [recentCharts, setRecentCharts] = useState<Chart[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch recent charts from localStorage
    try {
      const storedCharts = localStorage.getItem("recentCharts");
      const charts = storedCharts ? JSON.parse(storedCharts) : [];
      setRecentCharts(charts.slice(0, 5));
    } catch (error) {
      console.error("Error loading recent charts:", error);
      setRecentCharts([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const quickStats = {
    totalReadings: recentCharts.length,
    thisWeek: recentCharts.filter((c) => {
      const chartDate = new Date(c.date);
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      return chartDate >= weekAgo;
    }).length,
  };

  return (
    <div className="modern-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="dashboard-header__content">
          <h1 className="dashboard-header__title">Dashboard</h1>
          <Link href="/readings/new">
            <Button variant="primary">+ New Reading</Button>
          </Link>
        </div>
      </header>

      {/* Stats Grid */}
      <section className="stats-grid">
        <div className="stat-card">
          <div className="stat-card__value">{quickStats.totalReadings}</div>
          <div className="stat-card__label">Total Readings</div>
        </div>
        <div className="stat-card">
          <div className="stat-card__value">{quickStats.thisWeek}</div>
          <div className="stat-card__label">This Week</div>
        </div>
        <div className="stat-card">
          <div className="stat-card__value">—</div>
          <div className="stat-card__label">Active Clients</div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="quick-actions">
        <h2 className="section-title">Quick Actions</h2>
        <div className="action-grid">
          <Link href="/readings/new" className="action-card">
            <div className="action-card__icon">📊</div>
            <div className="action-card__content">
              <h3 className="action-card__title">New Chart</h3>
              <p className="action-card__description">Calculate natal chart</p>
            </div>
          </Link>

          <Link href="/readings" className="action-card">
            <div className="action-card__icon">📝</div>
            <div className="action-card__content">
              <h3 className="action-card__title">View Readings</h3>
              <p className="action-card__description">Browse past sessions</p>
            </div>
          </Link>

          <Link href="/profile" className="action-card">
            <div className="action-card__icon">⚙️</div>
            <div className="action-card__content">
              <h3 className="action-card__title">Settings</h3>
              <p className="action-card__description">Manage preferences</p>
            </div>
          </Link>
        </div>
      </section>

      {/* Recent Charts */}
      <section className="recent-section">
        <h2 className="section-title">Recent Charts</h2>

        {loading ? (
          <div className="empty-state">
            <p>Loading...</p>
          </div>
        ) : recentCharts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state__icon">📊</div>
            <h3 className="empty-state__title">No charts yet</h3>
            <p className="empty-state__description">
              Create your first chart reading to get started
            </p>
            <Link href="/readings/new">
              <Button variant="primary">Create Chart</Button>
            </Link>
          </div>
        ) : (
          <div className="chart-list">
            {recentCharts.map((chart) => (
              <div key={chart.id} className="chart-item">
                <div className="chart-item__icon">📄</div>
                <div className="chart-item__content">
                  <h3 className="chart-item__title">
                    {chart.name || "Untitled Chart"}
                  </h3>
                  <p className="chart-item__meta">
                    {new Date(chart.date).toLocaleDateString()}
                    {chart.location && ` • ${chart.location}`}
                  </p>
                </div>
                <Link
                  href={`/readings/${chart.id}`}
                  className="chart-item__action"
                >
                  View →
                </Link>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
