"use client";

import React, { useState, useEffect } from "react";
import "./profile.css";

interface UserProfile {
  id: string;
  username: string;
  email: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  timezone: string;
  created_at: string;
}

interface ProfileFormProps {
  profile: UserProfile;
  onSave: (data: Partial<UserProfile>) => void;
  onCancel: () => void;
}

function ProfileForm({ profile, onSave, onCancel }: ProfileFormProps) {
  const [formData, setFormData] = useState<Partial<UserProfile>>(profile);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (field: keyof UserProfile, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className="profile-form">
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <input
          id="username"
          type="text"
          value={formData.username || ""}
          onChange={(e) => handleChange("username", e.target.value)}
          className="form-input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={formData.email || ""}
          onChange={(e) => handleChange("email", e.target.value)}
          className="form-input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="birth_date">Birth Date</label>
        <input
          id="birth_date"
          type="date"
          value={formData.birth_date || ""}
          onChange={(e) => handleChange("birth_date", e.target.value)}
          className="form-input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="birth_time">Birth Time</label>
        <input
          id="birth_time"
          type="time"
          value={formData.birth_time || ""}
          onChange={(e) => handleChange("birth_time", e.target.value)}
          className="form-input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="birth_location">Birth Location</label>
        <input
          id="birth_location"
          type="text"
          value={formData.birth_location || ""}
          onChange={(e) => handleChange("birth_location", e.target.value)}
          placeholder="City, State/Country"
          className="form-input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="timezone">Timezone</label>
        <input
          id="timezone"
          type="text"
          value={formData.timezone || ""}
          onChange={(e) => handleChange("timezone", e.target.value)}
          placeholder="e.g., America/New_York"
          className="form-input"
        />
      </div>

      <div className="form-actions">
        <button type="button" onClick={onCancel} className="btn-secondary">
          Cancel
        </button>
        <button type="submit" className="btn-primary">
          Save Changes
        </button>
      </div>
    </form>
  );
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem("access_token");

      // Demo fallback if no token
      if (!token) {
        setProfile({
          id: "demo-123",
          username: "demo_user",
          email: "demo@mularoot.com",
          birth_date: "1990-05-15",
          birth_time: "14:30",
          birth_location: "New York, NY, USA",
          timezone: "America/New_York",
          created_at: new Date().toISOString(),
        });
        setIsLoading(false);
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/v1/user/profile`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!response.ok) throw new Error("Failed to load profile");
      const data = await response.json();
      setProfile(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error loading profile");
      // Fallback to demo data on error
      setProfile({
        id: "demo-123",
        username: "demo_user",
        email: "demo@mularoot.com",
        birth_date: "1990-05-15",
        birth_time: "14:30",
        birth_location: "New York, NY, USA",
        timezone: "America/New_York",
        created_at: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async (updatedData: Partial<UserProfile>) => {
    try {
      const token = localStorage.getItem("access_token");

      // Demo mode - just update local state
      if (!token) {
        setProfile((prev) => (prev ? { ...prev, ...updatedData } : null));
        setIsEditing(false);
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/v1/user/profile`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(updatedData),
        }
      );

      if (!response.ok) throw new Error("Failed to update profile");
      const data = await response.json();
      setProfile(data);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error saving profile");
    }
  };

  if (isLoading) {
    return (
      <div className="profile-container">
        <div className="loading">Loading profile...</div>
      </div>
    );
  }

  if (error && !profile) {
    return (
      <div className="profile-container">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>Your Profile</h1>
        {!isEditing && (
          <button onClick={() => setIsEditing(true)} className="btn-edit">
            Edit Profile
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      {profile && (
        <div className="profile-card">
          {isEditing ? (
            <ProfileForm
              profile={profile}
              onSave={handleSave}
              onCancel={() => setIsEditing(false)}
            />
          ) : (
            <div className="profile-view">
              <div className="field-group">
                <label>Username</label>
                <p>{profile.username}</p>
              </div>

              <div className="field-group">
                <label>Email</label>
                <p>{profile.email}</p>
              </div>

              <div className="field-group">
                <label>Birth Date</label>
                <p>{new Date(profile.birth_date).toLocaleDateString()}</p>
              </div>

              <div className="field-group">
                <label>Birth Time</label>
                <p>{profile.birth_time}</p>
              </div>

              <div className="field-group">
                <label>Birth Location</label>
                <p>{profile.birth_location}</p>
              </div>

              <div className="field-group">
                <label>Timezone</label>
                <p>{profile.timezone}</p>
              </div>

              <div className="field-group">
                <label>Member Since</label>
                <p>{new Date(profile.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
