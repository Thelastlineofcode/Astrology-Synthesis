"use client";

import Link from "next/link";
import Image from "next/image";
import Button from "@/components/shared/Button";
import Card from "@/components/shared/Card";
import "./landing.css";

export default function Home() {
  return (
    <div className="landing">
      <header className="landing__header">
        <div className="landing__header-content">
          <Image
            src="/images/logo/Icon_logo.png"
            alt="Mula: The Root"
            width={60}
            height={60}
            className="landing__logo"
          />
          <h1>Mula: The Root</h1>
        </div>
        <p className="landing__subtitle">
          Discover the roots of your astrological birth chart
        </p>
      </header>

      <main className="landing__main">
        <div className="landing__grid">
          <Card className="landing__card landing__card--primary">
            <h2>✨ Generate Your Chart</h2>
            <p>
              Create your natal chart instantly. Enter your birth details and
              unlock cosmic insights about your personality and life path.
            </p>
            <Link href="/chart-demo">
              <Button variant="primary" size="large">
                Calculate Chart
              </Button>
            </Link>
          </Card>

          <Card className="landing__card landing__card--secondary">
            <h2>🌙 Planetary Positions</h2>
            <div className="landing__planets">
              {["Sun", "Moon", "Venus", "Neptune", "Uranus"].map((planet) => (
                <div key={planet} className="landing__planet">
                  <Image
                    src={`/images/planets/${planet === "Moon" ? "MooN" : planet}_render.png`}
                    alt={planet}
                    width={50}
                    height={50}
                  />
                </div>
              ))}
            </div>
            <p className="landing__note">View planetary aspects and transits</p>
          </Card>

          <Card className="landing__card landing__card--tertiary">
            <h2>📊 Your Dashboard</h2>
            <p>
              Access your saved charts, birth data profiles, and personalized
              astrological insights all in one place.
            </p>
            <Link href="/dashboard">
              <Button variant="secondary" size="large">
                View Dashboard
              </Button>
            </Link>
          </Card>

          <Card className="landing__card landing__card--features">
            <h2>🔮 Cosmic Features</h2>
            <ul className="landing__features">
              <li>☉ Natal Chart Calculation</li>
              <li>☽ House Positions</li>
              <li>⚹ Planetary Aspects</li>
              <li>✧ Transits & Progressions</li>
              <li>�� Symbolon Cards</li>
            </ul>
          </Card>
        </div>

        <Card className="landing__cta">
          <h2>Begin Your Cosmic Journey</h2>
          <p>
            Unlock the ancient wisdom of astrology with precision calculations
            and beautiful visualizations
          </p>
          <Link href="/chart-demo">
            <Button variant="primary" size="large">
              Calculate Your Chart Now
            </Button>
          </Link>
        </Card>
      </main>
    </div>
  );
}
