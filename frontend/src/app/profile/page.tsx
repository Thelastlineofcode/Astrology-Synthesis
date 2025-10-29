"use client";

import React, { useState, useEffect } from 'react';
import Card from '../../components/shared/Card';
import Button from '../../components/shared/Button';
import './profile.css';

interface UserProfile {
  id: string;
  email: string;
  name: string;
  birthDate?: string;
  birthTime?: string;
  birthPlace?: string;
  latitude?: number;
  longitude?: number;
  zodiacSign?: string;
  sunSign?: string;
  moonSign?: string;
  risingSign?: string;
  createdAt: string;
  updatedAt: string;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<Partial<UserProfile>>({});

  // Mock token for demo - in production, this would come from auth context
  const authToken = typeof window !== 'undefined' ? localStorage.getItem('authToken') : null;

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // If no token, show demo data
      if (!authToken) {
        setProfile({
          id: 'demo',
          email: 'demo@example.com',
          name: 'Demo User',
          birthDate: '1990-05-15',
          birthTime: '14:30',
          birthPlace: 'New York, NY',
          latitude: 40.7128,
          longitude: -74.0060,
          zodiacSign: 'Taurus',
          sunSign: 'Taurus',
          moonSign: 'Cancer',
          risingSign: 'Virgo',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        });
        setIsLoading(false);
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/users/profile`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch profile');
      }

      const data = await response.json();
      setProfile(data.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = () => {
    setFormData(profile || {});
    setIsEditing(true);
  };

  const handleCancel = () => {
    setFormData({});
    setIsEditing(false);
    setError(null);
  };

  const handleChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      setError(null);
      
      // Demo mode - just update local state
      if (!authToken) {
        setProfile(prev => prev ? { ...prev, ...formData, updatedAt: new Date().toISOString() } : null);
        setIsEditing(false);
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/users/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const data = await response.json();
      setProfile(data.data);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  if (isLoading) {
    return (
      <div className="profile-page">
        <div className="profile-container">
          <Card className="profile-loading">
            <p>Loading profile...</p>
          </Card>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="profile-page">
        <div className="profile-container">
          <Card className="profile-error">
            <h2>Profile Not Found</h2>
            <p>Please log in to view your profile.</p>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <Card className="profile-card">
          <div className="profile-header">
            <h1>Your Profile</h1>
            {!isEditing && (
              <Button variant="primary" onClick={handleEdit}>
                Edit Profile
              </Button>
            )}
          </div>

          {error && (
            <div className="profile-error-message">
              {error}
            </div>
          )}

          {isEditing ? (
            <div className="profile-form">
              <div className="form-section">
                <h2>Personal Information</h2>
                <div className="form-group">
                  <label htmlFor="name">Name</label>
                  <input
                    id="name"
                    type="text"
                    value={formData.name || ''}
                    onChange={(e) => handleChange('name', e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    id="email"
                    type="email"
                    value={profile.email}
                    disabled
                    className="disabled"
                  />
                  <small>Email cannot be changed</small>
                </div>
              </div>

              <div className="form-section">
                <h2>Birth Information</h2>
                <div className="form-group">
                  <label htmlFor="birthDate">Birth Date</label>
                  <input
                    id="birthDate"
                    type="date"
                    value={formData.birthDate || ''}
                    onChange={(e) => handleChange('birthDate', e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="birthTime">Birth Time</label>
                  <input
                    id="birthTime"
                    type="time"
                    value={formData.birthTime || ''}
                    onChange={(e) => handleChange('birthTime', e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="birthPlace">Birth Place</label>
                  <input
                    id="birthPlace"
                    type="text"
                    value={formData.birthPlace || ''}
                    onChange={(e) => handleChange('birthPlace', e.target.value)}
                    placeholder="City, State/Country"
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="latitude">Latitude</label>
                    <input
                      id="latitude"
                      type="number"
                      step="0.0001"
                      min="-90"
                      max="90"
                      value={formData.latitude || ''}
                      onChange={(e) => handleChange('latitude', parseFloat(e.target.value))}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="longitude">Longitude</label>
                    <input
                      id="longitude"
                      type="number"
                      step="0.0001"
                      min="-180"
                      max="180"
                      value={formData.longitude || ''}
                      onChange={(e) => handleChange('longitude', parseFloat(e.target.value))}
                    />
                  </div>
                </div>
              </div>

              <div className="form-section">
                <h2>Astrological Signs</h2>
                <div className="form-group">
                  <label htmlFor="zodiacSign">Zodiac Sign</label>
                  <input
                    id="zodiacSign"
                    type="text"
                    value={formData.zodiacSign || ''}
                    onChange={(e) => handleChange('zodiacSign', e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="sunSign">Sun Sign</label>
                  <input
                    id="sunSign"
                    type="text"
                    value={formData.sunSign || ''}
                    onChange={(e) => handleChange('sunSign', e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="moonSign">Moon Sign</label>
                  <input
                    id="moonSign"
                    type="text"
                    value={formData.moonSign || ''}
                    onChange={(e) => handleChange('moonSign', e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="risingSign">Rising Sign</label>
                  <input
                    id="risingSign"
                    type="text"
                    value={formData.risingSign || ''}
                    onChange={(e) => handleChange('risingSign', e.target.value)}
                  />
                </div>
              </div>

              <div className="form-actions">
                <Button variant="secondary" onClick={handleCancel}>
                  Cancel
                </Button>
                <Button variant="primary" onClick={handleSave}>
                  Save Changes
                </Button>
              </div>
            </div>
          ) : (
            <div className="profile-view">
              <div className="profile-section">
                <h2>Personal Information</h2>
                <div className="profile-field">
                  <span className="field-label">Name:</span>
                  <span className="field-value">{profile.name}</span>
                </div>
                <div className="profile-field">
                  <span className="field-label">Email:</span>
                  <span className="field-value">{profile.email}</span>
                </div>
              </div>

              <div className="profile-section">
                <h2>Birth Information</h2>
                {profile.birthDate ? (
                  <>
                    <div className="profile-field">
                      <span className="field-label">Birth Date:</span>
                      <span className="field-value">{new Date(profile.birthDate).toLocaleDateString()}</span>
                    </div>
                    <div className="profile-field">
                      <span className="field-label">Birth Time:</span>
                      <span className="field-value">{profile.birthTime || 'Not set'}</span>
                    </div>
                    <div className="profile-field">
                      <span className="field-label">Birth Place:</span>
                      <span className="field-value">{profile.birthPlace || 'Not set'}</span>
                    </div>
                    {profile.latitude && profile.longitude && (
                      <div className="profile-field">
                        <span className="field-label">Coordinates:</span>
                        <span className="field-value">
                          {profile.latitude.toFixed(4)}, {profile.longitude.toFixed(4)}
                        </span>
                      </div>
                    )}
                  </>
                ) : (
                  <p className="field-empty">No birth information provided yet.</p>
                )}
              </div>

              <div className="profile-section profile-zodiac">
                <h2>Your Astrological Profile</h2>
                {profile.zodiacSign || profile.sunSign || profile.moonSign || profile.risingSign ? (
                  <div className="zodiac-grid">
                    {profile.zodiacSign && (
                      <div className="zodiac-item">
                        <span className="zodiac-label">Zodiac Sign</span>
                        <span className="zodiac-value">{profile.zodiacSign}</span>
                      </div>
                    )}
                    {profile.sunSign && (
                      <div className="zodiac-item">
                        <span className="zodiac-label">Sun Sign</span>
                        <span className="zodiac-value">{profile.sunSign}</span>
                      </div>
                    )}
                    {profile.moonSign && (
                      <div className="zodiac-item">
                        <span className="zodiac-label">Moon Sign</span>
                        <span className="zodiac-value">{profile.moonSign}</span>
                      </div>
                    )}
                    {profile.risingSign && (
                      <div className="zodiac-item">
                        <span className="zodiac-label">Rising Sign</span>
                        <span className="zodiac-value">{profile.risingSign}</span>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="field-empty">No astrological information provided yet. Click "Edit Profile" to add your signs.</p>
                )}
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
