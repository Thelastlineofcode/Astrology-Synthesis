"use client";

import Link from "next/link";
import Image from "next/image";
import Button from "@/components/shared/Button";
import "./landing.css";

export default function Home() {
  return (
    <div className="modern-landing">
      {/* Header/Logo */}
      <header className="landing-header">
        <div className="landing-header__container">
          <Link href="/" className="landing-header__logo">
            <Image
              src="/images/logo/Icon_logo.png"
              alt="Mula"
              width={40}
              height={40}
              priority
            />
            <span className="landing-header__title">Mula</span>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero__content">
          <div className="hero__badge">Professional Astrology Tool</div>
          <h1 className="hero__title">
            Chart Reading
            <span className="hero__title-accent">Simplified</span>
          </h1>
          <p className="hero__description">
            A modern companion app for professional astrologers. Calculate
            accurate natal charts and track client insights.
          </p>
          <div className="hero__actions">
            <Link href="/readings/new">
              <Button variant="primary" size="large">
                New Chart Reading
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="secondary" size="large">
                View Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="features">
        <div className="feature-card">
          <div className="feature-card__icon">📊</div>
          <h3 className="feature-card__title">Precise Calculations</h3>
          <p className="feature-card__description">
            Swiss Ephemeris powered chart calculations with house systems and
            aspects
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-card__icon">📝</div>
          <h3 className="feature-card__title">Client Notes</h3>
          <p className="feature-card__description">
            Track predictions, observations, and method development for each
            reading
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-card__icon">🎯</div>
          <h3 className="feature-card__title">Prediction Tracking</h3>
          <p className="feature-card__description">
            Log transits, dashas, progressions with timestamps for accuracy
            verification
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-card__icon">💾</div>
          <h3 className="feature-card__title">Session Management</h3>
          <p className="feature-card__description">
            Save and retrieve client sessions with all notes and chart data
          </p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="cta__content">
          <h2 className="cta__title">Ready to work?</h2>
          <p className="cta__description">
            Generate your first chart reading and start tracking insights
          </p>
          <Link href="/readings/new">
            <Button variant="primary" size="large">
              Get Started
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
