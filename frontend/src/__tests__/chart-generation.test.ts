/**
 * Frontend Chart Generation Test Suite
 * Tests chart service, data transformation, and UI integration
 */

import { describe, it, expect, beforeEach, vi } from "vitest";
import chartService from "@/services/chart";
import authService from "@/services/auth";

// Mock fetch globally
global.fetch = vi.fn();

describe("Chart Service Tests", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock auth service to return a token
    vi.spyOn(authService, "getAccessToken").mockReturnValue("mock-token-123");
  });

  describe("Chart Generation API Calls", () => {
    it("should send correct payload format to backend", async () => {
      const mockResponse = {
        chart_id: "test-chart-id",
        user_id: "test-user-id",
        chart_data: {
          planet_positions: [],
          house_cusps: [],
          aspects: [],
        },
        created_at: new Date().toISOString(),
        birth_location: "Test Location",
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const birthData = {
        birth_date: "1984-12-19",
        birth_time: "12:00:00",
        birth_location: "Metairie, LA",
        latitude: 29.9844,
        longitude: -90.1547,
        timezone: "America/Chicago",
      };

      await chartService.generateChart(birthData);

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/api/v1/chart"),
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
            Authorization: "Bearer mock-token-123",
          }),
          body: expect.stringContaining('"date":"1984-12-19"'),
        })
      );
    });

    it("should transform birth_date to date field", async () => {
      const mockResponse = {
        chart_id: "test",
        chart_data: { planet_positions: [], house_cusps: [], aspects: [] },
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const birthData = {
        birth_date: "1955-02-24",
        birth_time: "19:15:00",
        birth_location: "San Francisco, CA",
        latitude: 37.7749,
        longitude: -122.4194,
        timezone: "America/Los_Angeles",
      };

      await chartService.generateChart(birthData);

      const callBody = JSON.parse((global.fetch as any).mock.calls[0][1].body);
      expect(callBody.birth_data.date).toBe("1955-02-24");
      expect(callBody.birth_data.time).toBe("19:15:00");
      expect(callBody.birth_data.location_name).toBe("San Francisco, CA");
    });

    it("should handle authentication errors", async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: "Unauthorized" }),
      });

      vi.spyOn(authService, "logout");

      await expect(
        chartService.generateChart({
          birth_date: "2000-01-01",
          birth_time: "12:00:00",
          birth_location: "Test",
          latitude: 0,
          longitude: 0,
          timezone: "UTC",
        })
      ).rejects.toThrow();

      expect(authService.logout).toHaveBeenCalled();
    });

    it("should handle network errors gracefully", async () => {
      (global.fetch as any).mockRejectedValueOnce(new Error("Network error"));

      await expect(
        chartService.generateChart({
          birth_date: "2000-01-01",
          birth_time: "12:00:00",
          birth_location: "Test",
          latitude: 0,
          longitude: 0,
          timezone: "UTC",
        })
      ).rejects.toThrow();
    });
  });

  describe("Chart Data Retrieval", () => {
    it("should fetch existing chart by ID", async () => {
      const mockChart = {
        chart_id: "existing-chart-123",
        chart_data: {
          planet_positions: [
            {
              planet: "Sun",
              longitude: 267.5,
              zodiac_sign: "Sagittarius",
              house: 10,
              retrograde: false,
            },
          ],
          house_cusps: [],
          aspects: [],
        },
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockChart,
      });

      const result = await chartService.getChart("existing-chart-123");

      expect(result).toEqual(mockChart);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/api/v1/chart/existing-chart-123"),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: "Bearer mock-token-123",
          }),
        })
      );
    });
  });
});

describe("Data Transformation Tests", () => {
  const transformChartData = (backendData: Record<string, any>) => {
    const planets: Record<string, any> = {};
    if (backendData.planet_positions) {
      backendData.planet_positions.forEach((p: any) => {
        planets[p.planet] = {
          longitude: p.longitude,
          sign: p.zodiac_sign,
          degree: p.degree,
          house: p.house,
          retrograde: p.retrograde,
        };
      });
    }

    const houses: Record<string, any> = {};
    if (backendData.house_cusps) {
      backendData.house_cusps.forEach((h: any) => {
        houses[`house_${h.house}`] = {
          longitude: h.longitude || h.cusp,
          sign: h.zodiac_sign,
          degree: h.degree,
        };
      });
    }

    return {
      planets,
      houses,
      aspects: backendData.aspects || [],
    };
  };

  it("should transform backend planet array to frontend object", () => {
    const backendData = {
      planet_positions: [
        {
          planet: "Sun",
          longitude: 267.5,
          zodiac_sign: "Sagittarius",
          degree: 27.5,
          house: 10,
          retrograde: false,
          nakshatra: "Mula",
          pada: 2,
        },
        {
          planet: "Moon",
          longitude: 215.3,
          zodiac_sign: "Scorpio",
          degree: 5.3,
          house: 8,
          retrograde: false,
          nakshatra: "Vishakha",
          pada: 4,
        },
      ],
      house_cusps: [],
      aspects: [],
    };

    const transformed = transformChartData(backendData);

    expect(transformed.planets).toHaveProperty("Sun");
    expect(transformed.planets).toHaveProperty("Moon");
    expect(transformed.planets.Sun.longitude).toBe(267.5);
    expect(transformed.planets.Sun.sign).toBe("Sagittarius");
    expect(transformed.planets.Moon.retrograde).toBe(false);
  });

  it("should transform backend house array to frontend object", () => {
    const backendData = {
      planet_positions: [],
      house_cusps: [
        {
          house: 1,
          degree: 315.5,
          zodiac_sign: "Pisces",
          longitude: 315.5,
          minutes: 30,
          seconds: 15,
        },
        {
          house: 2,
          degree: 345.2,
          zodiac_sign: "Aries",
          longitude: 345.2,
          minutes: 12,
          seconds: 30,
        },
      ],
      aspects: [],
    };

    const transformed = transformChartData(backendData);

    expect(transformed.houses).toHaveProperty("house_1");
    expect(transformed.houses).toHaveProperty("house_2");
    expect(transformed.houses.house_1.longitude).toBe(315.5);
    expect(transformed.houses.house_1.sign).toBe("Pisces");
    expect(transformed.houses.house_2.degree).toBe(345.2);
  });

  it("should handle missing planet_positions gracefully", () => {
    const backendData = {
      house_cusps: [],
      aspects: [],
    };

    const transformed = transformChartData(backendData);

    expect(transformed.planets).toEqual({});
    expect(transformed.houses).toEqual({});
    expect(transformed.aspects).toEqual([]);
  });

  it("should preserve aspects array", () => {
    const backendData = {
      planet_positions: [],
      house_cusps: [],
      aspects: [
        {
          planet1: "Sun",
          planet2: "Moon",
          aspect: "trine",
          angle: 120,
          orb: 2.5,
        },
      ],
    };

    const transformed = transformChartData(backendData);

    expect(transformed.aspects).toHaveLength(1);
    expect(transformed.aspects[0].planet1).toBe("Sun");
    expect(transformed.aspects[0].aspect).toBe("trine");
  });
});

describe("Famous People Chart Validation", () => {
  beforeEach(() => {
    vi.spyOn(authService, "getAccessToken").mockReturnValue("mock-token");
  });

  const famousCharts = [
    {
      name: "Steve Jobs",
      data: {
        birth_date: "1955-02-24",
        birth_time: "19:15:00",
        birth_location: "San Francisco, CA",
        latitude: 37.7749,
        longitude: -122.4194,
        timezone: "America/Los_Angeles",
      },
      expectedSunSign: "Pisces",
    },
    {
      name: "Princess Diana",
      data: {
        birth_date: "1961-07-01",
        birth_time: "19:45:00",
        birth_location: "Sandringham, England",
        latitude: 52.8303,
        longitude: 0.5115,
        timezone: "Europe/London",
      },
      expectedSunSign: "Cancer",
    },
    {
      name: "Albert Einstein",
      data: {
        birth_date: "1879-03-14",
        birth_time: "11:30:00",
        birth_location: "Ulm, Germany",
        latitude: 48.4011,
        longitude: 9.9876,
        timezone: "Europe/Berlin",
      },
      expectedSunSign: "Pisces",
    },
  ];

  famousCharts.forEach(({ name, data, expectedSunSign }) => {
    it(`should correctly format ${name}'s birth data`, async () => {
      const mockResponse = {
        chart_id: "test-id",
        chart_data: {
          planet_positions: [
            {
              planet: "Sun",
              zodiac_sign: expectedSunSign,
              longitude: 267.5,
              house: 10,
              retrograde: false,
            },
          ],
          house_cusps: [],
          aspects: [],
        },
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      await chartService.generateChart(data);

      const callBody = JSON.parse((global.fetch as any).mock.calls[0][1].body);
      expect(callBody.birth_data.date).toBe(data.birth_date);
      expect(callBody.birth_data.time).toBe(data.birth_time);
      expect(callBody.birth_data.latitude).toBe(data.latitude);
      expect(callBody.birth_data.longitude).toBe(data.longitude);
    });
  });
});

describe("Integration Tests", () => {
  it("should handle complete chart generation flow", async () => {
    vi.spyOn(authService, "getAccessToken").mockReturnValue("valid-token");

    const mockBackendResponse = {
      chart_id: "chart-123",
      user_id: "user-456",
      chart_data: {
        planet_positions: [
          {
            planet: "Sun",
            longitude: 267.5,
            zodiac_sign: "Sagittarius",
            degree: 27.5,
            minutes: 30,
            seconds: 15,
            house: 10,
            retrograde: false,
            nakshatra: "Mula",
            pada: 2,
          },
        ],
        house_cusps: [
          {
            house: 1,
            degree: 315.5,
            minutes: 30,
            seconds: 0,
            zodiac_sign: "Pisces",
            longitude: 315.5,
          },
        ],
        aspects: [
          {
            planet1: "Sun",
            planet2: "Moon",
            aspect: "trine",
            angle: 120,
            orb: 2.3,
          },
        ],
      },
      created_at: new Date().toISOString(),
    };

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockBackendResponse,
    });

    const birthData = {
      birth_date: "1984-12-19",
      birth_time: "12:00:00",
      birth_location: "Metairie, LA",
      latitude: 29.9844,
      longitude: -90.1547,
      timezone: "America/Chicago",
    };

    const result = await chartService.generateChart(birthData);

    expect(result).toHaveProperty("chart_id");
    expect(result).toHaveProperty("chart_data");
    expect(result.chart_data).toHaveProperty("planet_positions");
    expect(result.chart_data).toHaveProperty("house_cusps");
    expect(result.chart_data).toHaveProperty("aspects");
  });
});
