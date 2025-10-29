# Authentication System - User Flows & Diagrams

## Visual Reference for Product Team

This document provides visual representations of the authentication system flows for easy understanding and communication with stakeholders.

---

## 1. High-Level System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Login   │  │ Register │  │  Profile │  │ Settings │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       │ HTTPS/TLS
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                     API LAYER (Express.js)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Auth      │  │   Profile    │  │   Session    │          │
│  │   Routes     │  │   Routes     │  │   Routes     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Middleware Layer                                │   │
│  │  • Authentication  • Rate Limiting  • Validation         │   │
│  │  • CSRF Protection • Error Handling                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    User      │  │   Session    │  │    Email     │          │
│  │  Repository  │  │  Repository  │  │   Service    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   PostgreSQL │  │    Redis     │  │   SendGrid   │          │
│  │   Database   │  │   (Cache)    │  │   (Email)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. User Registration Flow

```
┌─────────────┐
│   START     │
│  New User   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Lands on Homepage       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ Clicks "Sign Up"        │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  REGISTRATION FORM - STEP 1             │
│  ┌───────────────────────────────────┐  │
│  │ Email: ____________________       │  │
│  │ Password: _________________       │  │
│  │ Confirm: __________________       │  │
│  │ [Password Strength: ████░░]       │  │
│  │                                   │  │
│  │ [ Continue ] or [ Google ] [ FB ] │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Validation:                             │
│  • Email format & uniqueness            │
│  • Password strength (8+ chars, 1 upper) │
│  • Passwords match                       │
└──────┬───────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  REGISTRATION FORM - STEP 2 (Optional)  │
│  ┌───────────────────────────────────┐  │
│  │ First Name: _______________       │  │
│  │ Last Name: ________________       │  │
│  │ Birth Date: _______________       │  │
│  │ Birth Time: _______________       │  │
│  │ Location: _________________ 🔍    │  │
│  │ Timezone: [Auto-detected]         │  │
│  │                                   │  │
│  │ [ Skip ] or [ Continue ]          │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  REGISTRATION FORM - STEP 3 (Optional)  │
│  ┌───────────────────────────────────┐  │
│  │ Theme: [ Light ] [ Dark ]         │  │
│  │ Default Chart: [ Natal ▼ ]        │  │
│  │ Email Notifications: [x]          │  │
│  │                                   │  │
│  │ [ Skip ] or [ Create Account ]    │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend Processing:         │
│  1. Hash password (bcrypt)   │
│  2. Create user in DB        │
│  3. Generate JWT tokens      │
│  4. Create session record    │
│  5. Send verification email  │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  SUCCESS SCREEN                         │
│  ┌───────────────────────────────────┐  │
│  │ ✓ Account Created!                │  │
│  │                                   │  │
│  │ Welcome to Roots Revealed!        │  │
│  │                                   │  │
│  │ We've sent a verification email   │  │
│  │ to john@example.com               │  │
│  │                                   │  │
│  │ [ Go to Dashboard ]               │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  DASHBOARD (Logged In)                  │
│  ┌───────────────────────────────────┐  │
│  │ ⚠️ Please verify your email to    │  │
│  │    unlock all features             │  │
│  │    [ Resend Email ]                │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Your Charts (0)                        │
│  Quick Chart Calculator                 │
│  BMAD Analysis                          │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│     END     │
└─────────────┘
```

---

## 3. Login Flow

```
┌─────────────┐
│   START     │
│ User Visits │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Clicks "Log In"         │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  LOGIN FORM                             │
│  ┌───────────────────────────────────┐  │
│  │ Email: ____________________       │  │
│  │ Password: _________________       │  │
│  │ [x] Remember Me                   │  │
│  │                                   │  │
│  │ [ Forgot Password? ]              │  │
│  │                                   │  │
│  │ [ Log In ]                        │  │
│  │                                   │  │
│  │ Or continue with:                 │  │
│  │ [ Google ] [ Facebook ]           │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend Processing:         │
│  1. Find user by email       │
│  2. Verify password (bcrypt) │
│  3. Check account status     │
│  4. Log failed attempts      │
└──────┬───────────────────────┘
       │
       ├────────────────┐
       │                │
    Success          Failure
       │                │
       ▼                ▼
┌──────────────┐  ┌──────────────────┐
│ Generate JWT │  │ Error Handling:  │
│ Create       │  │ • Wrong password │
│ Session      │  │ • Account locked │
│ Update       │  │ • User not found │
│ Last Login   │  └──────────────────┘
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  DASHBOARD                              │
│  ┌───────────────────────────────────┐  │
│  │ Welcome back, John! 👋            │  │
│  │                                   │  │
│  │ Last login: 2 days ago            │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Your Charts (12)                       │
│  Recent: Birth Chart - John Doe         │
│  Quick Actions                          │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│     END     │
└─────────────┘
```

---

## 4. Password Reset Flow

```
┌─────────────┐
│   START     │
│ User Forgot │
│  Password   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Clicks "Forgot          │
│  Password?" link        │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  FORGOT PASSWORD FORM                   │
│  ┌───────────────────────────────────┐  │
│  │ Enter your email address:         │  │
│  │ Email: ____________________       │  │
│  │                                   │  │
│  │ [ Send Reset Link ]               │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend Processing:         │
│  1. Validate email           │
│  2. Generate reset token     │
│  3. Store token in DB        │
│  4. Send reset email         │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  CONFIRMATION SCREEN                    │
│  ┌───────────────────────────────────┐  │
│  │ ✓ Check Your Email                │  │
│  │                                   │  │
│  │ We've sent a password reset link  │  │
│  │ to john@example.com               │  │
│  │                                   │  │
│  │ Didn't receive it?                │  │
│  │ [ Resend Email ]                  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────┐
│ User checks email       │
│ Clicks reset link       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  RESET PASSWORD FORM                    │
│  ┌───────────────────────────────────┐  │
│  │ New Password: _____________       │  │
│  │ [Password Strength: ████░░]       │  │
│  │                                   │  │
│  │ Confirm Password: __________      │  │
│  │                                   │  │
│  │ [ Reset Password ]                │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend Processing:         │
│  1. Verify reset token       │
│  2. Check token expiry       │
│  3. Hash new password        │
│  4. Update user password     │
│  5. Invalidate all sessions  │
│  6. Mark token as used       │
│  7. Send confirmation email  │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  SUCCESS SCREEN                         │
│  ┌───────────────────────────────────┐  │
│  │ ✓ Password Reset Successful       │  │
│  │                                   │  │
│  │ Your password has been changed.   │  │
│  │                                   │  │
│  │ [ Log In with New Password ]      │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────┐
│     END     │
└─────────────┘
```

---

## 5. Profile Management Flow

```
┌─────────────┐
│   START     │
│ Logged In   │
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Clicks Profile Icon     │
│ Selects "Profile"       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  PROFILE VIEW (Read-Only)               │
│  ┌───────────────────────────────────┐  │
│  │ Profile Picture          [Edit]   │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │  │
│  │                                   │  │
│  │ Personal Information              │  │
│  │ Name: John Doe                    │  │
│  │ Email: john@example.com ✓         │  │
│  │ Username: johndoe                 │  │
│  │                                   │  │
│  │ Birth Information                 │  │
│  │ Date: May 15, 1990                │  │
│  │ Time: 2:30 PM                     │  │
│  │ Location: New York, NY            │  │
│  │ Timezone: America/New_York        │  │
│  │                                   │  │
│  │ Account Info                      │  │
│  │ Member since: Jan 15, 2025        │  │
│  │ Charts created: 12                │  │
│  │                                   │  │
│  │ [ Edit Profile ] [ Change Pass ]  │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       │ Clicks "Edit Profile"
       ▼
┌─────────────────────────────────────────┐
│  PROFILE EDIT FORM                      │
│  ┌───────────────────────────────────┐  │
│  │ First Name: [John______]          │  │
│  │ Last Name: [Doe_______]           │  │
│  │ Username: [johndoe___]            │  │
│  │                                   │  │
│  │ Birth Date: [05/15/1990]          │  │
│  │ Birth Time: [14:30____]           │  │
│  │ Location: [New York, NY_] 🔍      │  │
│  │ Timezone: [America/New_York ▼]    │  │
│  │                                   │  │
│  │ ⚠️ Changes to birth data will     │  │
│  │    affect your saved charts       │  │
│  │                                   │  │
│  │ [ Cancel ] [ Save Changes ]       │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Unsaved Changes Warning     │
│  ┌────────────────────────┐  │
│  │ You have unsaved       │  │
│  │ changes. Continue?     │  │
│  │                        │  │
│  │ [ No ] [ Yes, Save ]   │  │
│  └────────────────────────┘  │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend Processing:         │
│  1. Validate inputs          │
│  2. Update user record       │
│  3. Log change in audit      │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  SUCCESS NOTIFICATION                   │
│  ┌───────────────────────────────────┐  │
│  │ ✓ Profile updated successfully!   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Back to Profile View                   │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│     END     │
└─────────────┘
```

---

## 6. Session Management Flow

```
┌─────────────┐
│   START     │
│ Logged In   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Profile → Sessions      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  ACTIVE SESSIONS                        │
│  ┌───────────────────────────────────┐  │
│  │ Your Active Sessions              │  │
│  │                                   │  │
│  │ ┌─────────────────────────────┐   │  │
│  │ │ 🖥️ Chrome on Windows 10      │   │  │
│  │ │ Current Session              │   │  │
│  │ │ New York, USA                │   │  │
│  │ │ Last active: Just now        │   │  │
│  │ └─────────────────────────────┘   │  │
│  │                                   │  │
│  │ ┌─────────────────────────────┐   │  │
│  │ │ 📱 Safari on iPhone          │   │  │
│  │ │ Boston, USA                  │   │  │
│  │ │ Last active: 2 hours ago     │   │  │
│  │ │ [ End Session ]              │   │  │
│  │ └─────────────────────────────┘   │  │
│  │                                   │  │
│  │ ┌─────────────────────────────┐   │  │
│  │ │ 💻 Firefox on MacOS          │   │  │
│  │ │ San Francisco, USA           │   │  │
│  │ │ Last active: 1 day ago       │   │  │
│  │ │ [ End Session ]              │   │  │
│  │ └─────────────────────────────┘   │  │
│  │                                   │  │
│  │ [ Logout All Other Devices ]      │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       │ Clicks "End Session"
       ▼
┌──────────────────────────────┐
│  Confirmation Dialog         │
│  ┌────────────────────────┐  │
│  │ End this session?      │  │
│  │                        │  │
│  │ Firefox on MacOS       │  │
│  │                        │  │
│  │ [ Cancel ] [ End ]     │  │
│  └────────────────────────┘  │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend Processing:         │
│  1. Revoke session           │
│  2. Update database          │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  UPDATED SESSIONS LIST                  │
│  ┌───────────────────────────────────┐  │
│  │ ✓ Session ended                   │  │
│  │                                   │  │
│  │ (Firefox session removed)         │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│     END     │
└─────────────┘
```

---

## 7. Token Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    Token Lifecycle                          │
└─────────────────────────────────────────────────────────────┘

Login/Register
     │
     ▼
┌─────────────────────┐
│ Generate Tokens:    │
│ • Access Token      │ ───────────► Expires in 24h
│   (24h expiry)      │
│                     │
│ • Refresh Token     │ ───────────► Expires in 7d
│   (7d expiry)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Store in Client:    │
│ • localStorage      │
│ • sessionStorage    │
│ • HTTP-only cookie  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Use Access Token    │
│ for API Requests    │
└──────────┬──────────┘
           │
           ▼
      ┌────────┐
      │ Token  │
      │ Valid? │
      └───┬────┘
          │
    ┌─────┴─────┐
    │           │
   Yes          No
    │           │
    ▼           ▼
┌────────┐  ┌─────────────────┐
│ Allow  │  │ Return 401      │
│ Access │  │ Unauthorized    │
└────────┘  └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Frontend:       │
            │ Attempt Token   │
            │ Refresh         │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Send Refresh    │
            │ Token to API    │
            └────────┬────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Verify Refresh   │
            │ Token Valid?     │
            └────┬─────────────┘
                 │
           ┌─────┴─────┐
           │           │
          Yes          No
           │           │
           ▼           ▼
┌──────────────────┐  ┌────────────────┐
│ Generate New     │  │ Redirect to    │
│ Access Token     │  │ Login Page     │
└────────┬─────────┘  └────────────────┘
         │
         ▼
┌──────────────────┐
│ Retry Original   │
│ Request          │
└──────────────────┘
```

---

## 8. Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Architecture                    │
└─────────────────────────────────────────────────────────────┘

Layer 1: Network Security
  │
  ├── HTTPS/TLS 1.2+ Encryption
  ├── Firewall Rules
  └── DDoS Protection

Layer 2: API Gateway Security
  │
  ├── CORS Configuration
  ├── Rate Limiting (100 req/15min)
  ├── Request Size Limits
  └── IP Whitelisting/Blacklisting

Layer 3: Authentication
  │
  ├── JWT Token Verification
  ├── Session Validation
  ├── Multi-Factor Authentication (future)
  └── OAuth 2.0 (Google, Facebook)

Layer 4: Authorization
  │
  ├── Role-Based Access Control
  ├── Resource Ownership Checks
  └── Permission Validation

Layer 5: Input Validation
  │
  ├── Express-validator
  ├── SQL Injection Prevention
  ├── XSS Prevention
  └── CSRF Protection

Layer 6: Data Security
  │
  ├── Password Hashing (Bcrypt)
  ├── Database Encryption
  ├── Sensitive Data Masking
  └── Secure Token Storage

Layer 7: Monitoring & Audit
  │
  ├── Failed Login Tracking
  ├── Suspicious Activity Detection
  ├── Audit Logging
  └── Security Alerts
```

---

## 9. Error Handling Flow

```
┌─────────────────────┐
│  API Request        │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  Validation  │
    │  Layer       │
    └──────┬───────┘
           │
     ┌─────┴─────┐
     │           │
   Valid      Invalid
     │           │
     ▼           ▼
┌─────────┐  ┌────────────────────────┐
│ Process │  │ Return 400 Bad Request │
│ Request │  │ {                      │
└─────────┘  │   "success": false,    │
             │   "errors": [...]      │
             │ }                      │
             └────────────────────────┘

     │
     ▼
┌─────────────────┐
│ Business Logic  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
 Success   Error
    │         │
    ▼         ▼
┌─────┐  ┌────────────────────────┐
│ 200 │  │ Return Error Response  │
│ OK  │  │ • 401 Unauthorized     │
└─────┘  │ • 403 Forbidden        │
         │ • 404 Not Found        │
         │ • 500 Server Error     │
         └────────────────────────┘

Frontend Error Handling:
  │
  ├── Display user-friendly message
  ├── Log error to monitoring service
  ├── Offer retry option
  └── Redirect if authentication failed
```

---

## 10. Quick Reference - HTTP Status Codes

| Code | Status | Usage |
|------|--------|-------|
| 200 | OK | Successful request |
| 201 | Created | User registered, resource created |
| 400 | Bad Request | Validation failed, malformed request |
| 401 | Unauthorized | Missing/invalid token, login required |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate email, resource conflict |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unhandled server error |
| 503 | Service Unavailable | Maintenance mode, service down |

---

## 11. API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {
    // Response payload
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Operation failed",
  "error": {
    "code": "AUTH_001",
    "message": "Invalid credentials",
    "details": [
      {
        "field": "password",
        "message": "Password is incorrect"
      }
    ]
  }
}
```

---

## 12. Development Timeline

```
Phase 1: Foundation (Weeks 1-2)
├── Database setup
├── Core authentication
└── Basic tests
    │
    ▼
Phase 2: Core Features (Weeks 3-4)
├── Email verification
├── Password reset
├── Session management
└── Security measures
    │
    ▼
Phase 3: Profile Management (Weeks 5-6)
├── Profile CRUD
├── Preferences
└── Account deletion
    │
    ▼
Phase 4: Frontend (Weeks 7-9)
├── All UI components
├── Forms & validation
└── Responsive design
    │
    ▼
Phase 5: OAuth & Advanced (Weeks 10-12)
├── Social login
├── 2FA
└── Enhanced security
    │
    ▼
Phase 6: Polish & Launch (Weeks 13-14)
├── Testing
├── Security audit
├── Performance optimization
└── Production deployment
    │
    ▼
🎉 LAUNCH 🎉
```

---

*This visual guide complements the detailed product design and implementation guides.*

**Last Updated**: October 29, 2025
