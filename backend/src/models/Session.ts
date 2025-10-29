import { query } from '../db';

export interface Session {
  id: number;
  user_id: number;
  token_jti: string;
  token_type: string;
  expires_at: Date;
  ip_address?: string;
  user_agent?: string;
  is_revoked: boolean;
  created_at: Date;
  revoked_at?: Date;
}

export interface CreateSessionData {
  user_id: number;
  token_jti: string;
  token_type: string;
  expires_at: Date;
  ip_address?: string;
  user_agent?: string;
}

/**
 * Create a new session
 */
export const createSession = async (
  sessionData: CreateSessionData
): Promise<Session> => {
  const {
    user_id,
    token_jti,
    token_type,
    expires_at,
    ip_address,
    user_agent,
  } = sessionData;

  const result = await query(
    `INSERT INTO sessions (
      user_id, token_jti, token_type, expires_at, ip_address, user_agent
    ) 
    VALUES ($1, $2, $3, $4, $5, $6) 
    RETURNING *`,
    [user_id, token_jti, token_type, expires_at, ip_address, user_agent]
  );

  return result.rows[0];
};

/**
 * Find session by JTI
 */
export const findSessionByJti = async (
  jti: string
): Promise<Session | null> => {
  const result = await query(
    'SELECT * FROM sessions WHERE token_jti = $1',
    [jti]
  );

  return result.rows[0] || null;
};

/**
 * Find all sessions for a user
 */
export const findSessionsByUserId = async (userId: number): Promise<Session[]> => {
  const result = await query(
    `SELECT * FROM sessions 
     WHERE user_id = $1 AND is_revoked = false 
     ORDER BY created_at DESC`,
    [userId]
  );

  return result.rows;
};

/**
 * Revoke a session
 */
export const revokeSession = async (jti: string): Promise<boolean> => {
  const result = await query(
    `UPDATE sessions 
     SET is_revoked = true, revoked_at = NOW() 
     WHERE token_jti = $1`,
    [jti]
  );

  return (result.rowCount ?? 0) > 0;
};

/**
 * Revoke all sessions for a user
 */
export const revokeAllUserSessions = async (userId: number): Promise<number> => {
  const result = await query(
    `UPDATE sessions 
     SET is_revoked = true, revoked_at = NOW() 
     WHERE user_id = $1 AND is_revoked = false`,
    [userId]
  );

  return result.rowCount ?? 0;
};

/**
 * Check if session is valid
 */
export const isSessionValid = async (jti: string): Promise<boolean> => {
  const result = await query(
    `SELECT * FROM sessions 
     WHERE token_jti = $1 
     AND is_revoked = false 
     AND expires_at > NOW()`,
    [jti]
  );

  return result.rows.length > 0;
};

/**
 * Clean up expired sessions
 */
export const cleanupExpiredSessions = async (): Promise<number> => {
  const result = await query(
    'DELETE FROM sessions WHERE expires_at < NOW()'
  );

  return result.rowCount ?? 0;
};

/**
 * Clean up old revoked sessions
 */
export const cleanupRevokedSessions = async (
  daysOld: number = 30
): Promise<number> => {
  const result = await query(
    `DELETE FROM sessions 
     WHERE is_revoked = true 
     AND revoked_at < NOW() - INTERVAL '${daysOld} days'`
  );

  return result.rowCount ?? 0;
};

export default {
  createSession,
  findSessionByJti,
  findSessionsByUserId,
  revokeSession,
  revokeAllUserSessions,
  isSessionValid,
  cleanupExpiredSessions,
  cleanupRevokedSessions,
};
