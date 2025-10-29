# User Authentication & Profile Management System - Product Design Document

## Document Information
- **Product**: Roots Revealed - Astrology Synthesis Platform
- **Feature**: User Authentication & Profile Management
- **Author**: Product Management Agent (BMAD)
- **Date**: October 29, 2025
- **Version**: 1.0
- **Status**: Design Phase
- **Issue**: [#5](https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/5)
- **Dependencies**: #1 (Architecture), #2 (Database)

---

## Executive Summary

This document outlines the complete design for the user authentication and profile management system for Roots Revealed. This critical feature enables users to create accounts, securely access the platform, save their birth charts, and maintain personalized astrological data. The system follows modern security best practices while providing a seamless user experience aligned with the BMAD (Behavioral, Modern, Archetypal, and Digital) methodology.

---

## 1. Vision & Goals

### 1.1 Product Vision
Create a secure, intuitive authentication system that allows users to:
- Access personalized astrological insights
- Save and manage multiple birth charts
- Build a library of personal astrological data
- Share charts with trusted individuals
- Experience continuity across devices and sessions

### 1.2 Business Goals
- **User Acquisition**: Enable user onboarding with minimal friction
- **Data Security**: Protect sensitive user information (birth data, personal details)
- **User Retention**: Provide value through saved charts and personalized content
- **Trust Building**: Demonstrate commitment to privacy and security
- **Scalability**: Support growth from hundreds to millions of users

### 1.3 Success Metrics
- Registration conversion rate: >60%
- Login success rate: >95%
- Time to complete registration: <2 minutes
- Password reset completion rate: >80%
- Zero security breaches
- Session retention: >30 days average

---

## 2. BMAD Framework Application

### 2.1 Behavioral
**User Behavior Analysis**:
- Users want quick access without remembering complex credentials
- Users prefer social login options (Google, Facebook)
- Users abandon registration if too many fields are required upfront
- Users expect email verification but often ignore verification emails
- Users forget passwords frequently and need easy reset mechanisms

**Behavioral Design Decisions**:
- Implement progressive disclosure: collect minimal data at registration
- Add social login options to reduce friction
- Send reminder emails for unverified accounts
- Provide instant password reset with magic links
- Auto-save progress during chart creation to prevent data loss

### 2.2 Modern
**Modern Technology Stack**:
- JWT-based stateless authentication
- Bcrypt for password hashing (industry standard)
- PostgreSQL for reliable data persistence
- Express.js middleware architecture
- React Hook Form for client-side validation
- Rate limiting to prevent brute force attacks
- HTTPS/TLS encryption for all data transmission

**Modern UX Patterns**:
- Single Sign-On (SSO) with OAuth 2.0
- Passwordless authentication options (future enhancement)
- Biometric authentication on mobile (future enhancement)
- Two-factor authentication (2FA) for enhanced security
- Responsive design for desktop, tablet, and mobile

### 2.3 Archetypal
**User Archetypes**:

1. **The Seeker** (40% of users)
   - New to astrology, curious about self-discovery
   - Needs: Simple onboarding, educational content, guided experiences
   - Fears: Complexity, judgment, information overload

2. **The Practitioner** (35% of users)
   - Intermediate knowledge, regular chart reader
   - Needs: Efficient workflows, chart library, comparison tools
   - Fears: Data loss, inaccurate calculations, limited features

3. **The Professional** (15% of users)
   - Astrologers, consultants, teachers
   - Needs: Advanced features, client management, export options
   - Fears: Security breaches, lack of professional tools

4. **The Skeptic** (10% of users)
   - Exploring astrology casually, not fully committed
   - Needs: No commitment registration, guest access, clear value
   - Fears: Spam, data misuse, payment requirements

**Archetypal Design Decisions**:
- Offer guest mode for Skeptics (limited chart saves)
- Provide role-based features (basic, premium, professional)
- Create personalized onboarding flows per archetype
- Use astrological metaphors in UX (e.g., "Your Cosmic Portal" for dashboard)

### 2.4 Digital
**Digital-First Approach**:
- Mobile-responsive authentication flows
- Progressive Web App (PWA) capabilities
- Offline mode for viewing saved charts
- Cloud-based data synchronization
- API-first architecture for third-party integrations
- Analytics tracking for user behavior insights
- A/B testing infrastructure for optimization

---

## 3. User Stories & Requirements

### 3.1 Epic: User Registration
**As a new user, I want to create an account so that I can save my birth charts and access personalized astrological insights.**

#### User Stories:

**US-1.1: Email Registration**
- As a user, I want to register with my email and password
- **Acceptance Criteria**:
  - Email validation (format, uniqueness)
  - Password strength requirements (min 8 characters, 1 uppercase, 1 number)
  - Confirmation email sent within 30 seconds
  - User can log in immediately without verification (verification required for premium features)
  - Error handling for duplicate accounts with helpful messaging

**US-1.2: Social Login Registration**
- As a user, I want to register using Google or Facebook
- **Acceptance Criteria**:
  - OAuth 2.0 integration with Google and Facebook
  - One-click registration process
  - Auto-populate profile with social data (name, email, profile picture)
  - Seamless account linking if email already exists
  - Clear privacy policy regarding social data usage

**US-1.3: Email Verification**
- As a registered user, I want to verify my email to unlock all features
- **Acceptance Criteria**:
  - Verification email with unique token (expires in 24 hours)
  - One-click verification link
  - Resend verification option
  - Clear indication of verification status in profile
  - Reminder emails sent at 24h, 72h if unverified

**US-1.4: Profile Setup**
- As a new user, I want to add my birth information during registration
- **Acceptance Criteria**:
  - Optional birth data fields (date, time, location)
  - Timezone auto-detection and manual override
  - Location autocomplete with geocoding
  - Skip option for later completion
  - Progress indicator showing profile completeness

### 3.2 Epic: User Login
**As a returning user, I want to securely access my account so that I can view my saved charts and continue my astrological journey.**

#### User Stories:

**US-2.1: Email/Password Login**
- As a user, I want to log in with my email and password
- **Acceptance Criteria**:
  - Secure password comparison with bcrypt
  - JWT token generated with 24h expiration
  - Refresh token for extended sessions (7 days)
  - "Remember Me" option for 30-day sessions
  - Failed login attempt tracking (max 5 attempts before lockout)
  - Clear error messages without revealing security details

**US-2.2: Social Login**
- As a user, I want to log in using Google or Facebook
- **Acceptance Criteria**:
  - Seamless OAuth redirect flow
  - Auto-login on return visits
  - Session persistence across devices
  - Account linking for users with multiple login methods

**US-2.3: Persistent Sessions**
- As a user, I want to stay logged in across browser sessions
- **Acceptance Criteria**:
  - Secure HTTP-only cookies for refresh tokens
  - Silent token refresh when access token expires
  - Session invalidation on password change
  - Logout from all devices option

### 3.3 Epic: Password Management
**As a user, I want to manage my password securely so that I maintain control over my account.**

#### User Stories:

**US-3.1: Password Reset**
- As a user, I want to reset my password if I forget it
- **Acceptance Criteria**:
  - "Forgot Password" link on login page
  - Email sent with reset token (expires in 1 hour)
  - One-time use reset tokens
  - New password must meet strength requirements
  - Confirmation email sent after successful reset
  - All active sessions invalidated upon reset

**US-3.2: Password Change**
- As a logged-in user, I want to change my password
- **Acceptance Criteria**:
  - Require current password verification
  - New password validation
  - Immediate session refresh with new credentials
  - Notification email sent for security
  - Option to logout all other devices

**US-3.3: Security Notifications**
- As a user, I want to be notified of suspicious account activity
- **Acceptance Criteria**:
  - Email notification for new device logins
  - Notification for password changes
  - Notification for failed login attempts (after 3 attempts)
  - IP address and device information in notifications

### 3.4 Epic: Profile Management
**As a user, I want to manage my profile information so that my charts and interpretations remain accurate and personalized.**

#### User Stories:

**US-4.1: View Profile**
- As a user, I want to view my profile information
- **Acceptance Criteria**:
  - Display all profile fields (name, email, birth data, preferences)
  - Show account status (verified, subscription tier)
  - Display join date and last login
  - Show saved charts count and storage usage

**US-4.2: Edit Profile**
- As a user, I want to update my profile information
- **Acceptance Criteria**:
  - Edit personal information (name, username, bio)
  - Update birth information with validation
  - Change timezone and location preferences
  - Upload profile picture (future enhancement)
  - Real-time validation and error handling
  - Confirmation modal for critical changes

**US-4.3: Privacy Settings**
- As a user, I want to control my privacy settings
- **Acceptance Criteria**:
  - Make profile public/private
  - Control chart visibility (private, friends, public)
  - Manage email notification preferences
  - Control data sharing with third-party integrations
  - Export personal data (GDPR compliance)
  - Delete account with data purge option

**US-4.4: Chart Library Management**
- As a user, I want to manage my saved charts
- **Acceptance Criteria**:
  - View all saved charts in grid/list view
  - Search and filter charts (by name, type, date)
  - Sort charts (by creation date, access date, name)
  - Tag charts for organization
  - Bulk operations (delete, export, share)
  - Chart favorites/pins

### 3.5 Epic: Session Management
**As a user, I want to manage my active sessions for security and convenience.**

#### User Stories:

**US-5.1: View Active Sessions**
- As a user, I want to see all my active sessions
- **Acceptance Criteria**:
  - List all active devices with login times
  - Show device type, browser, IP address, location
  - Indicate current session
  - Show last activity timestamp

**US-5.2: Manage Sessions**
- As a user, I want to control my active sessions
- **Acceptance Criteria**:
  - Logout from specific devices
  - Logout from all other devices
  - Automatic session cleanup after 30 days of inactivity
  - Confirmation modal before ending sessions

### 3.6 Epic: Security Features
**As a user, I want my account to be secure so that my personal astrological data remains private.**

#### User Stories:

**US-6.1: Two-Factor Authentication (Future Enhancement)**
- As a security-conscious user, I want to enable 2FA
- **Acceptance Criteria**:
  - TOTP-based 2FA (Google Authenticator, Authy)
  - Backup codes generation (10 one-time codes)
  - 2FA required for critical operations (password change, data export)
  - Recovery flow for lost 2FA devices

**US-6.2: Login History**
- As a user, I want to view my login history
- **Acceptance Criteria**:
  - Chronological list of login attempts (successful and failed)
  - Device and location information
  - Filter by date range
  - Export login history

---

## 4. Technical Architecture

### 4.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  (React/Next.js - Frontend Authentication Components)       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ HTTPS/TLS
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                      API Gateway Layer                       │
│              (Express.js Middleware)                         │
│  • CORS         • Rate Limiting    • Request Validation      │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                   Authentication Service                     │
│  • JWT Generation/Verification                               │
│  • Password Hashing (Bcrypt)                                 │
│  • Token Refresh Logic                                       │
│  • OAuth Integration (Google, Facebook)                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                     Data Access Layer                        │
│  • User Repository      • Session Repository                 │
│  • Chart Repository     • Audit Log Repository               │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                      PostgreSQL Database                     │
│  • users          • sessions        • charts                 │
│  • audit_logs     • password_resets                          │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Authentication Flow

#### Registration Flow
```
User → Frontend → API (/api/auth/register)
  ↓
Validate Input (express-validator)
  ↓
Check Email Uniqueness (Database Query)
  ↓
Hash Password (bcrypt, 10 rounds)
  ↓
Create User Record (PostgreSQL)
  ↓
Generate JWT Access Token (24h expiry)
  ↓
Generate JWT Refresh Token (7d expiry)
  ↓
Send Verification Email (SendGrid/Nodemailer)
  ↓
Return User Data + Tokens → Frontend
  ↓
Store Tokens (localStorage/sessionStorage/HTTP-only cookie)
  ↓
Redirect to Dashboard
```

#### Login Flow
```
User → Frontend → API (/api/auth/login)
  ↓
Validate Input
  ↓
Find User by Email (Database Query)
  ↓
Compare Password Hash (bcrypt.compare)
  ↓
Check Account Status (active, verified, locked)
  ↓
Log Failed Attempts (if password wrong)
  ↓
Generate JWT Tokens (access + refresh)
  ↓
Create Session Record (PostgreSQL)
  ↓
Update Last Login Timestamp
  ↓
Return Tokens + User Data → Frontend
  ↓
Store Tokens
  ↓
Redirect to Dashboard
```

#### Token Refresh Flow
```
Frontend detects token expiration
  ↓
API Request (/api/auth/refresh) with Refresh Token
  ↓
Verify Refresh Token (jwt.verify)
  ↓
Check Session Validity (not revoked, not expired)
  ↓
Generate New Access Token (24h expiry)
  ↓
Optionally Rotate Refresh Token
  ↓
Return New Tokens → Frontend
  ↓
Update Stored Tokens
  ↓
Retry Original Request with New Access Token
```

#### Password Reset Flow
```
User → Forgot Password Page → API (/api/auth/forgot-password)
  ↓
Validate Email
  ↓
Find User by Email
  ↓
Generate Reset Token (UUID + Timestamp)
  ↓
Store Token in Database (expires in 1 hour)
  ↓
Send Reset Email with Link
  ↓
User Clicks Link → Reset Password Page
  ↓
API (/api/auth/reset-password) with Token + New Password
  ↓
Verify Token (not expired, not used)
  ↓
Validate New Password
  ↓
Hash New Password
  ↓
Update User Password
  ↓
Invalidate All Sessions
  ↓
Mark Token as Used
  ↓
Send Confirmation Email
  ↓
Redirect to Login
```

### 4.3 Security Measures

#### Password Security
- **Hashing Algorithm**: Bcrypt with 10 salt rounds
- **Strength Requirements**:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character (recommended, not required)
- **Password History**: Store last 5 password hashes, prevent reuse
- **Breach Detection**: Check against HaveIBeenPwned API (optional)

#### Token Security
- **Access Token**: JWT with HS256 algorithm, 24h expiry
- **Refresh Token**: JWT with HS256 algorithm, 7d expiry, HTTP-only cookie
- **Token Payload**: Minimal data (user ID, email, role)
- **Token Rotation**: Rotate refresh tokens on each use (optional, enhances security)
- **Token Revocation**: Store revoked tokens in Redis/Database until expiry

#### Session Security
- **Session Storage**: PostgreSQL with indexed queries
- **Session Expiry**: 30 days maximum for inactive sessions
- **Concurrent Sessions**: Allow multiple sessions per user, with management
- **Session Tracking**: IP address, user agent, device fingerprint
- **Suspicious Activity Detection**: Alert on login from new location/device

#### API Security
- **Rate Limiting**:
  - Registration: 3 attempts per IP per hour
  - Login: 5 attempts per IP per 15 minutes
  - Password Reset: 3 requests per email per hour
  - General API: 100 requests per IP per 15 minutes
- **CORS**: Whitelist specific origins (frontend domain)
- **HTTPS Only**: All requests must use TLS 1.2+
- **CSRF Protection**: CSRF tokens for state-changing operations
- **SQL Injection Prevention**: Parameterized queries only
- **XSS Prevention**: Content Security Policy headers

#### Data Protection
- **Encryption at Rest**: PostgreSQL with encryption enabled
- **Encryption in Transit**: TLS 1.2+ for all connections
- **Sensitive Data Masking**: Log sanitization (no passwords, tokens)
- **GDPR Compliance**: Data export, data deletion, consent management
- **Backup & Recovery**: Automated daily backups with encryption

---

## 5. Database Schema

### 5.1 Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    username VARCHAR(80) UNIQUE,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    birth_time TIME,
    birth_latitude DECIMAL(10, 7),
    birth_longitude DECIMAL(10, 7),
    birth_location VARCHAR(255),
    timezone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    preferences JSONB DEFAULT '{}',
    
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_uuid ON users(uuid);
CREATE INDEX idx_users_username ON users(username);
```

### 5.2 Sessions Table
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_jti VARCHAR(36) UNIQUE NOT NULL,
    token_type VARCHAR(20) DEFAULT 'access',
    refresh_token_jti VARCHAR(36),
    expires_at TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    device_info JSONB,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,
    
    CONSTRAINT valid_token_type CHECK (token_type IN ('access', 'refresh'))
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_jti ON sessions(token_jti);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
CREATE INDEX idx_sessions_is_revoked ON sessions(is_revoked);
```

### 5.3 Password Resets Table
```sql
CREATE TABLE password_resets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    reset_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    used_at TIMESTAMP,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_password_resets_token ON password_resets(reset_token);
CREATE INDEX idx_password_resets_user_id ON password_resets(user_id);
CREATE INDEX idx_password_resets_expires_at ON password_resets(expires_at);
```

### 5.4 Audit Logs Table
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    ip_address INET,
    user_agent TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

### 5.5 OAuth Providers Table (Future Enhancement)
```sql
CREATE TABLE oauth_providers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(20) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    profile_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_provider_user UNIQUE (provider, provider_user_id),
    CONSTRAINT valid_provider CHECK (provider IN ('google', 'facebook', 'apple'))
);

CREATE INDEX idx_oauth_providers_user_id ON oauth_providers(user_id);
CREATE INDEX idx_oauth_providers_provider ON oauth_providers(provider);
```

---

## 6. API Endpoints Specification

### 6.1 Authentication Endpoints

#### POST /api/auth/register
**Description**: Register a new user account

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "birthDate": "1990-05-15",
  "birthTime": "14:30:00",
  "birthLocation": "New York, NY, USA",
  "timezone": "America/New_York"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "John Doe",
      "isVerified": false
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 86400
    }
  }
}
```

#### POST /api/auth/login
**Description**: Authenticate user and receive tokens

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "John Doe",
      "isVerified": true,
      "lastLogin": "2025-10-29T14:30:00Z"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 86400
    }
  }
}
```

#### POST /api/auth/refresh
**Description**: Refresh access token using refresh token

**Headers**:
```
Authorization: Bearer <refresh_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 86400
  }
}
```

#### POST /api/auth/logout
**Description**: Invalidate current session

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Logout successful"
}
```

#### POST /api/auth/logout-all
**Description**: Invalidate all user sessions

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "All sessions logged out successfully",
  "data": {
    "sessionsInvalidated": 3
  }
}
```

#### POST /api/auth/forgot-password
**Description**: Request password reset email

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

#### POST /api/auth/reset-password
**Description**: Reset password using reset token

**Request Body**:
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "newPassword": "NewSecurePass123!"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

#### POST /api/auth/verify-email
**Description**: Verify email address using token

**Request Body**:
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

#### POST /api/auth/resend-verification
**Description**: Resend email verification link

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Verification email sent"
}
```

### 6.2 Profile Endpoints

#### GET /api/profile
**Description**: Get current user profile

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "johndoe",
    "firstName": "John",
    "lastName": "Doe",
    "birthDate": "1990-05-15",
    "birthTime": "14:30:00",
    "birthLocation": "New York, NY, USA",
    "birthLatitude": 40.7128,
    "birthLongitude": -74.0060,
    "timezone": "America/New_York",
    "isVerified": true,
    "createdAt": "2025-01-15T10:00:00Z",
    "lastLogin": "2025-10-29T14:30:00Z",
    "preferences": {
      "theme": "dark",
      "defaultChartType": "natal",
      "emailNotifications": true
    },
    "chartCount": 12
  }
}
```

#### PUT /api/profile
**Description**: Update user profile

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "username": "johndoe",
  "birthDate": "1990-05-15",
  "birthTime": "14:30:00",
  "birthLocation": "New York, NY, USA",
  "timezone": "America/New_York"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "johndoe",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

#### PUT /api/profile/password
**Description**: Change user password

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "currentPassword": "OldPass123!",
  "newPassword": "NewSecurePass123!",
  "confirmPassword": "NewSecurePass123!"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

#### PUT /api/profile/preferences
**Description**: Update user preferences

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "theme": "dark",
  "defaultChartType": "natal",
  "emailNotifications": true,
  "chartPrivacy": "private"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Preferences updated successfully",
  "data": {
    "theme": "dark",
    "defaultChartType": "natal",
    "emailNotifications": true,
    "chartPrivacy": "private"
  }
}
```

#### DELETE /api/profile
**Description**: Delete user account

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "password": "SecurePass123!",
  "confirmation": "DELETE MY ACCOUNT"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Account deleted successfully"
}
```

### 6.3 Session Endpoints

#### GET /api/sessions
**Description**: Get all active sessions

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "id": "session-123",
        "deviceInfo": "Chrome on Windows 10",
        "ipAddress": "192.168.1.1",
        "location": "New York, USA",
        "isCurrent": true,
        "lastActivity": "2025-10-29T14:30:00Z",
        "createdAt": "2025-10-25T10:00:00Z"
      }
    ]
  }
}
```

#### DELETE /api/sessions/:sessionId
**Description**: Logout specific session

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Session terminated successfully"
}
```

---

## 7. Frontend Components

### 7.1 Component Structure

```
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   ├── ForgotPasswordForm.tsx
│   │   ├── ResetPasswordForm.tsx
│   │   ├── EmailVerification.tsx
│   │   ├── SocialLoginButtons.tsx
│   │   └── ProtectedRoute.tsx
│   ├── profile/
│   │   ├── ProfileView.tsx
│   │   ├── ProfileEditForm.tsx
│   │   ├── PasswordChangeForm.tsx
│   │   ├── PreferencesForm.tsx
│   │   ├── SessionManager.tsx
│   │   └── AccountDeletion.tsx
│   └── common/
│       ├── Input.tsx
│       ├── Button.tsx
│       ├── FormError.tsx
│       └── LoadingSpinner.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useProfile.ts
│   └── useSession.ts
├── contexts/
│   └── AuthContext.tsx
├── services/
│   ├── authService.ts
│   ├── profileService.ts
│   └── sessionService.ts
├── utils/
│   ├── validators.ts
│   ├── tokenManager.ts
│   └── apiClient.ts
└── pages/
    ├── login.tsx
    ├── register.tsx
    ├── forgot-password.tsx
    ├── reset-password.tsx
    ├── verify-email.tsx
    └── profile.tsx
```

### 7.2 Key Component Specifications

#### LoginForm.tsx
**Purpose**: User login interface

**Features**:
- Email and password inputs with validation
- "Remember Me" checkbox
- "Forgot Password" link
- Social login buttons
- Error message display
- Loading state during authentication
- Redirect to dashboard on success

**Validation**:
- Email format validation
- Required field validation
- Real-time error display

#### RegisterForm.tsx
**Purpose**: New user registration

**Features**:
- Multi-step form (basic info → birth data → preferences)
- Progress indicator
- Email, password, name inputs
- Optional birth information
- Password strength indicator
- Terms of service checkbox
- Social registration options
- Success message with verification reminder

**Validation**:
- Email uniqueness check (debounced)
- Password strength requirements
- Matching password confirmation
- Terms acceptance requirement

#### ProfileEditForm.tsx
**Purpose**: Edit user profile information

**Features**:
- All editable profile fields
- Birth location autocomplete
- Timezone selector
- Real-time validation
- Unsaved changes warning
- Success/error notifications

---

## 8. User Experience Flows

### 8.1 New User Registration Flow

**Scenario**: First-time visitor wants to create an account

1. User lands on homepage
2. Clicks "Sign Up" button
3. **Registration Page**:
   - Step 1: Email & Password
     - Enters email
     - Creates password (strength indicator shown)
     - Confirms password
     - Clicks "Continue"
   - Step 2: Personal Information (Optional)
     - Enters first and last name
     - Adds birth date, time, location (autocomplete)
     - Selects timezone (auto-detected)
     - Option to skip
   - Step 3: Preferences (Optional)
     - Chooses theme (light/dark)
     - Selects default chart type
     - Email notification preferences
     - Option to skip
4. Clicks "Create Account"
5. Account created, receives verification email
6. Automatically logged in and redirected to dashboard
7. Banner prompts email verification

**Alternative**: Social Registration
1. User clicks "Continue with Google"
2. OAuth popup opens
3. User authenticates with Google
4. Redirected back with pre-filled profile
5. Confirms/edits information
6. Account created (pre-verified)
7. Redirected to dashboard

### 8.2 Returning User Login Flow

**Scenario**: Existing user wants to access their account

1. User lands on homepage
2. Clicks "Log In" button
3. **Login Page**:
   - Enters email
   - Enters password
   - Optionally checks "Remember Me"
   - Clicks "Log In"
4. Authentication successful
5. Redirected to dashboard with saved charts
6. Welcome notification: "Welcome back, John!"

**Alternative**: Social Login
1. User clicks "Continue with Google"
2. OAuth popup (auto-closes if already authenticated)
3. Logged in immediately
4. Redirected to dashboard

### 8.3 Password Reset Flow

**Scenario**: User forgot their password

1. User on login page
2. Clicks "Forgot Password?"
3. **Forgot Password Page**:
   - Enters email
   - Clicks "Send Reset Link"
4. Confirmation: "Check your email"
5. Receives password reset email
6. Clicks reset link in email
7. **Reset Password Page**:
   - Enters new password (strength indicator)
   - Confirms new password
   - Clicks "Reset Password"
8. Success message
9. All sessions invalidated
10. Redirected to login page
11. Logs in with new password

### 8.4 Profile Update Flow

**Scenario**: User wants to update birth information

1. User logged in on dashboard
2. Clicks profile icon → "Profile Settings"
3. **Profile Page**:
   - Views current profile information
   - Clicks "Edit Profile"
4. **Edit Mode**:
   - Updates birth time
   - Changes timezone
   - Clicks "Save Changes"
5. Confirmation modal: "This will affect your saved charts"
6. Confirms changes
7. Profile updated
8. Success notification
9. Option to recalculate affected charts

---

## 9. Security & Privacy

### 9.1 Data Protection
- **Password Hashing**: Bcrypt with 10 rounds (adjustable)
- **Encrypted Storage**: PostgreSQL encryption at rest
- **Secure Transmission**: TLS 1.2+ for all API calls
- **Token Security**: HTTP-only cookies for refresh tokens
- **Session Management**: Automatic cleanup of expired sessions

### 9.2 Privacy Compliance
- **GDPR**: Right to access, right to be forgotten, data portability
- **CCPA**: California Consumer Privacy Act compliance
- **Data Minimization**: Collect only necessary information
- **Consent Management**: Clear opt-in for data processing
- **Transparent Privacy Policy**: Detailed, easy-to-understand

### 9.3 Audit & Monitoring
- **Login Attempts**: Track all login attempts (success/failure)
- **Password Changes**: Log all password-related actions
- **Data Access**: Track profile views and edits
- **Session Activity**: Monitor active sessions
- **Security Alerts**: Email notifications for suspicious activity

---

## 10. Testing Strategy

### 10.1 Unit Tests
- Password hashing and comparison
- JWT token generation and verification
- Input validation functions
- Database query functions
- Email service functions

### 10.2 Integration Tests
- Registration flow end-to-end
- Login flow end-to-end
- Password reset flow end-to-end
- Profile update flow end-to-end
- Session management operations
- Token refresh mechanism

### 10.3 Security Tests
- SQL injection prevention
- XSS attack prevention
- CSRF protection validation
- Rate limiting effectiveness
- Brute force attack resistance
- Session hijacking prevention

### 10.4 Performance Tests
- Concurrent login load testing (1000 users)
- Database query optimization
- Token generation performance
- API response times (<200ms average)

### 10.5 User Acceptance Tests
- Registration usability
- Login ease of use
- Password reset clarity
- Profile editing intuitiveness
- Error message helpfulness

---

## 11. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
**Estimated Effort**: 8 story points

- [ ] Set up PostgreSQL database with schema
- [ ] Implement user model and repository
- [ ] Create password hashing utilities
- [ ] Set up JWT token generation
- [ ] Implement basic registration endpoint
- [ ] Implement basic login endpoint
- [ ] Create authentication middleware
- [ ] Write unit tests for core functions

**Deliverables**:
- Database tables created
- Basic auth API functional
- Unit tests passing

### Phase 2: Core Features (Week 3-4)
**Estimated Effort**: 13 story points

- [ ] Implement email verification system
- [ ] Create password reset functionality
- [ ] Add refresh token mechanism
- [ ] Implement session management
- [ ] Create logout and logout-all endpoints
- [ ] Add rate limiting middleware
- [ ] Implement CSRF protection
- [ ] Write integration tests
- [ ] Create API documentation

**Deliverables**:
- Full authentication flow working
- Email system operational
- Security measures in place

### Phase 3: Profile Management (Week 5-6)
**Estimated Effort**: 8 story points

- [ ] Create profile view endpoint
- [ ] Implement profile update endpoint
- [ ] Add password change endpoint
- [ ] Create preferences management
- [ ] Implement account deletion
- [ ] Add session viewer endpoint
- [ ] Write profile tests
- [ ] Update API documentation

**Deliverables**:
- Profile management functional
- User preferences working
- Session management complete

### Phase 4: Frontend Components (Week 7-9)
**Estimated Effort**: 13 story points

- [ ] Create login form component
- [ ] Create registration form component
- [ ] Implement forgot password form
- [ ] Create reset password form
- [ ] Build email verification page
- [ ] Create profile view component
- [ ] Implement profile edit form
- [ ] Build password change form
- [ ] Create preferences form
- [ ] Implement session manager
- [ ] Add protected route wrapper
- [ ] Write component tests
- [ ] Ensure responsive design

**Deliverables**:
- All frontend components built
- Forms fully functional
- Mobile-responsive design

### Phase 5: OAuth & Advanced Features (Week 10-12)
**Estimated Effort**: 13 story points

- [ ] Integrate Google OAuth
- [ ] Integrate Facebook OAuth
- [ ] Implement account linking
- [ ] Add two-factor authentication (2FA)
- [ ] Create login history view
- [ ] Implement audit logging
- [ ] Add security notifications
- [ ] Create admin user management (future)
- [ ] Write OAuth tests
- [ ] Update documentation

**Deliverables**:
- Social login functional
- 2FA working
- Enhanced security features

### Phase 6: Polish & Launch (Week 13-14)
**Estimated Effort**: 8 story points

- [ ] Comprehensive testing (all flows)
- [ ] Security audit
- [ ] Performance optimization
- [ ] Error handling refinement
- [ ] UI/UX polish
- [ ] Analytics integration
- [ ] Documentation finalization
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] Launch announcement

**Deliverables**:
- Production-ready system
- Full documentation
- Monitoring in place
- Public launch

**Total Estimated Effort**: 63 story points (~14 weeks)

---

## 12. Success Criteria

### 12.1 Functional Requirements
✅ All user stories implemented and tested
✅ All API endpoints functional
✅ All frontend components operational
✅ Email system working reliably
✅ Social login operational (Google, Facebook)

### 12.2 Non-Functional Requirements
✅ 99.9% uptime SLA
✅ API response time <200ms (95th percentile)
✅ Mobile-responsive design (all breakpoints)
✅ Accessibility WCAG 2.1 AA compliant
✅ Browser compatibility (Chrome, Firefox, Safari, Edge)

### 12.3 Security Requirements
✅ Zero security vulnerabilities (OWASP Top 10)
✅ Penetration testing passed
✅ GDPR/CCPA compliant
✅ Encrypted data at rest and in transit
✅ Rate limiting effective against attacks

### 12.4 User Metrics
✅ Registration conversion >60%
✅ Login success rate >95%
✅ Time to register <2 minutes
✅ Password reset completion >80%
✅ User satisfaction score >4.5/5

---

## 13. Risk Management

### 13.1 Technical Risks

**Risk**: Database performance degradation with scale
- **Likelihood**: Medium
- **Impact**: High
- **Mitigation**: Database indexing, query optimization, caching layer (Redis)

**Risk**: JWT token security vulnerabilities
- **Likelihood**: Low
- **Impact**: Critical
- **Mitigation**: Token rotation, short expiry times, secure storage, regular security audits

**Risk**: Email delivery failures
- **Likelihood**: Medium
- **Impact**: Medium
- **Mitigation**: Multiple email providers (failover), retry logic, email queue system

### 13.2 User Experience Risks

**Risk**: Low email verification completion rate
- **Likelihood**: High
- **Impact**: Medium
- **Mitigation**: Allow basic features without verification, reminder emails, incentives

**Risk**: Password reset abuse
- **Likelihood**: Medium
- **Impact**: Medium
- **Mitigation**: Rate limiting, CAPTCHA, security questions (future)

**Risk**: Complex registration deterring users
- **Likelihood**: Medium
- **Impact**: High
- **Mitigation**: Progressive disclosure, optional fields, social login, guest mode

### 13.3 Security Risks

**Risk**: Brute force password attacks
- **Likelihood**: High
- **Impact**: High
- **Mitigation**: Rate limiting, account lockout, CAPTCHA, IP blocking

**Risk**: Session hijacking
- **Likelihood**: Low
- **Impact**: Critical
- **Mitigation**: HTTPS only, HTTP-only cookies, device fingerprinting, suspicious activity detection

**Risk**: Data breach
- **Likelihood**: Low
- **Impact**: Critical
- **Mitigation**: Encryption, access controls, regular security audits, penetration testing

---

## 14. Monitoring & Analytics

### 14.1 Key Metrics to Track

**Authentication Metrics**:
- Registration attempts vs. completions
- Login success rate
- Failed login attempts by reason
- Social login vs. email login ratio
- Password reset requests and completions
- Email verification rate

**User Engagement**:
- Daily/Weekly/Monthly Active Users (DAU/WAU/MAU)
- Average session duration
- Charts created per user
- Feature adoption rates
- Return user rate

**Performance Metrics**:
- API response times (p50, p95, p99)
- Database query performance
- Email delivery success rate
- Error rates by endpoint
- Uptime percentage

**Security Metrics**:
- Failed login attempts per user/IP
- Account lockouts
- Suspicious activity detections
- Token refresh frequency
- Session durations

### 14.2 Alerting Thresholds

**Critical Alerts** (immediate action required):
- API downtime >1 minute
- Login success rate <80%
- Error rate >5%
- Failed login attempts >100 per IP per hour
- Database connection failures

**Warning Alerts** (monitor closely):
- API response time >500ms
- Email delivery rate <90%
- Registration conversion <50%
- Password reset completion <70%

---

## 15. Future Enhancements

### 15.1 Short-Term (3-6 months)
- [ ] Passwordless authentication (magic links)
- [ ] Apple Sign-In integration
- [ ] Enhanced 2FA with SMS option
- [ ] Biometric authentication (mobile)
- [ ] Profile pictures and avatars
- [ ] Account recovery questions
- [ ] Remember trusted devices

### 15.2 Long-Term (6-12 months)
- [ ] Enterprise SSO (SAML, LDAP)
- [ ] Multi-account support
- [ ] Account delegation (consultants managing client accounts)
- [ ] Advanced audit logging dashboard
- [ ] Compliance certifications (SOC 2, ISO 27001)
- [ ] API key management for developers
- [ ] Webhook notifications for account events
- [ ] Account sharing and permissions

---

## 16. Appendices

### Appendix A: Password Strength Requirements
```
Minimum Requirements:
- Length: 8 characters
- Uppercase: 1 letter (A-Z)
- Lowercase: 1 letter (a-z)
- Number: 1 digit (0-9)
- Special Character: Optional but recommended

Strength Levels:
- Weak: Meets minimum requirements
- Medium: 10+ characters with 3 character types
- Strong: 12+ characters with 4 character types
- Very Strong: 15+ characters with all types + no dictionary words
```

### Appendix B: JWT Token Structure
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "user",
    "iat": 1698600000,
    "exp": 1698686400,
    "jti": "token-unique-id-123"
  }
}
```

### Appendix C: Email Templates

**Welcome Email**:
- Subject: "Welcome to Roots Revealed! ✨"
- Content: Introduction, verification link, getting started guide

**Email Verification**:
- Subject: "Verify Your Email Address"
- Content: Verification link (24h expiry), benefits of verification

**Password Reset**:
- Subject: "Reset Your Password"
- Content: Reset link (1h expiry), security reminder, support link

**Password Changed**:
- Subject: "Your Password Has Been Changed"
- Content: Confirmation, revert instructions, security tips

**New Device Login**:
- Subject: "New Login Detected"
- Content: Device info, location, "Was this you?" button

### Appendix D: Error Codes

| Code | Message | Description |
|------|---------|-------------|
| AUTH_001 | Invalid credentials | Email/password combination incorrect |
| AUTH_002 | Account locked | Too many failed login attempts |
| AUTH_003 | Email not verified | Action requires verified email |
| AUTH_004 | Token expired | JWT token has expired |
| AUTH_005 | Invalid token | JWT token is malformed or tampered |
| AUTH_006 | User already exists | Email already registered |
| AUTH_007 | Weak password | Password doesn't meet requirements |
| AUTH_008 | Reset token invalid | Password reset token is invalid/expired |
| AUTH_009 | Session not found | Session has been invalidated |
| AUTH_010 | Rate limit exceeded | Too many requests |

---

## 17. Conclusion

This authentication and profile management system provides a comprehensive, secure, and user-friendly foundation for the Roots Revealed platform. By following the BMAD methodology, we ensure that the system addresses both user needs and business goals while maintaining modern technical standards.

The phased implementation approach allows for iterative development, testing, and refinement. The system is designed to scale from initial launch to supporting millions of users while maintaining security, performance, and user satisfaction.

**Next Steps**:
1. ✅ Review and approve this design document
2. Begin Phase 1 implementation (Database & Core Auth)
3. Set up development environment
4. Create GitHub project board with all tasks
5. Schedule weekly sprint planning and retrospectives

---

**Document Status**: ✅ Ready for Review  
**Next Review Date**: Before Phase 1 Implementation  
**Approvers**: Product Owner, Tech Lead, Security Lead

---

*This document is a living document and will be updated as requirements evolve and implementation progresses.*
