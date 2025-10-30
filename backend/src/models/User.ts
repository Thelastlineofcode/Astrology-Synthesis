import { query } from '../db';

export interface User {
  id: number;
  uuid: string;
  email: string;
  password_hash: string;
  name: string;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
  last_login?: Date;
}

export interface UserProfile {
  id: number;
  uuid: string;
  email: string;
  name: string;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
  last_login?: Date;
}

export interface CreateUserData {
  email: string;
  password_hash: string;
  name: string;
}

export interface UpdateUserData {
  name?: string;
  email?: string;
}

/**
 * Create a new user
 */
export const createUser = async (userData: CreateUserData): Promise<User> => {
  const { email, password_hash, name } = userData;
  
  const result = await query(
    `INSERT INTO users (email, password_hash, name) 
     VALUES ($1, $2, $3) 
     RETURNING *`,
    [email, password_hash, name]
  );
  
  return result.rows[0];
};

/**
 * Find user by email
 */
export const findUserByEmail = async (email: string): Promise<User | null> => {
  const result = await query(
    'SELECT * FROM users WHERE email = $1',
    [email]
  );
  
  return result.rows[0] || null;
};

/**
 * Find user by ID
 */
export const findUserById = async (id: number): Promise<User | null> => {
  const result = await query(
    'SELECT * FROM users WHERE id = $1',
    [id]
  );
  
  return result.rows[0] || null;
};

/**
 * Find user by UUID
 */
export const findUserByUuid = async (uuid: string): Promise<User | null> => {
  const result = await query(
    'SELECT * FROM users WHERE uuid = $1',
    [uuid]
  );
  
  return result.rows[0] || null;
};

/**
 * Get user profile (without password hash)
 */
export const getUserProfile = async (id: number): Promise<UserProfile | null> => {
  const result = await query(
    `SELECT id, uuid, email, name, is_active, created_at, updated_at, last_login 
     FROM users 
     WHERE id = $1`,
    [id]
  );
  
  return result.rows[0] || null;
};

/**
 * Update user profile
 */
export const updateUser = async (
  id: number,
  updateData: UpdateUserData
): Promise<UserProfile | null> => {
  const fields: string[] = [];
  const values: unknown[] = [];
  let paramCount = 1;

  if (updateData.name !== undefined) {
    fields.push(`name = $${paramCount}`);
    values.push(updateData.name);
    paramCount++;
  }

  if (updateData.email !== undefined) {
    fields.push(`email = $${paramCount}`);
    values.push(updateData.email);
    paramCount++;
  }

  if (fields.length === 0) {
    return getUserProfile(id);
  }

  fields.push(`updated_at = NOW()`);
  values.push(id);

  const result = await query(
    `UPDATE users 
     SET ${fields.join(', ')} 
     WHERE id = $${paramCount} 
     RETURNING id, uuid, email, name, is_active, created_at, updated_at, last_login`,
    values
  );

  return result.rows[0] || null;
};

/**
 * Update user password
 */
export const updateUserPassword = async (
  id: number,
  newPasswordHash: string
): Promise<boolean> => {
  const result = await query(
    `UPDATE users 
     SET password_hash = $1, updated_at = NOW() 
     WHERE id = $2`,
    [newPasswordHash, id]
  );

  return (result.rowCount ?? 0) > 0;
};

/**
 * Update last login timestamp
 */
export const updateLastLogin = async (id: number): Promise<void> => {
  await query(
    'UPDATE users SET last_login = NOW() WHERE id = $1',
    [id]
  );
};

/**
 * Delete user (soft delete by setting is_active to false)
 */
export const deactivateUser = async (id: number): Promise<boolean> => {
  const result = await query(
    'UPDATE users SET is_active = false, updated_at = NOW() WHERE id = $1',
    [id]
  );

  return (result.rowCount ?? 0) > 0;
};

/**
 * Permanently delete user
 */
export const deleteUser = async (id: number): Promise<boolean> => {
  const result = await query(
    'DELETE FROM users WHERE id = $1',
    [id]
  );

  return (result.rowCount ?? 0) > 0;
};

export default {
  createUser,
  findUserByEmail,
  findUserById,
  findUserByUuid,
  getUserProfile,
  updateUser,
  updateUserPassword,
  updateLastLogin,
  deactivateUser,
  deleteUser,
};
