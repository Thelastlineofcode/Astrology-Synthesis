import { query } from '../db';

export interface Chart {
  id: number;
  uuid: string;
  user_id: number;
  name: string;
  birth_date: Date;
  birth_time: string;
  latitude: number;
  longitude: number;
  birth_location?: string;
  timezone?: string;
  chart_data?: Record<string, unknown>;
  created_at: Date;
  updated_at: Date;
}

export interface CreateChartData {
  user_id: number;
  name: string;
  birth_date: Date;
  birth_time: string;
  latitude: number;
  longitude: number;
  birth_location?: string;
  timezone?: string;
  chart_data?: Record<string, unknown>;
}

export interface UpdateChartData {
  name?: string;
  birth_location?: string;
  timezone?: string;
  chart_data?: Record<string, unknown>;
}

/**
 * Create a new chart
 */
export const createChart = async (chartData: CreateChartData): Promise<Chart> => {
  const {
    user_id,
    name,
    birth_date,
    birth_time,
    latitude,
    longitude,
    birth_location,
    timezone,
    chart_data,
  } = chartData;

  const result = await query(
    `INSERT INTO charts (
      user_id, name, birth_date, birth_time, latitude, longitude, 
      birth_location, timezone, chart_data
    ) 
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) 
    RETURNING *`,
    [
      user_id,
      name,
      birth_date,
      birth_time,
      latitude,
      longitude,
      birth_location,
      timezone,
      chart_data ? JSON.stringify(chart_data) : null,
    ]
  );

  return result.rows[0];
};

/**
 * Find all charts for a user
 */
export const findChartsByUserId = async (userId: number): Promise<Chart[]> => {
  const result = await query(
    'SELECT * FROM charts WHERE user_id = $1 ORDER BY created_at DESC',
    [userId]
  );

  return result.rows;
};

/**
 * Find chart by ID
 */
export const findChartById = async (
  id: number,
  userId: number
): Promise<Chart | null> => {
  const result = await query(
    'SELECT * FROM charts WHERE id = $1 AND user_id = $2',
    [id, userId]
  );

  return result.rows[0] || null;
};

/**
 * Find chart by UUID
 */
export const findChartByUuid = async (
  uuid: string,
  userId: number
): Promise<Chart | null> => {
  const result = await query(
    'SELECT * FROM charts WHERE uuid = $1 AND user_id = $2',
    [uuid, userId]
  );

  return result.rows[0] || null;
};

/**
 * Update chart
 */
export const updateChart = async (
  id: number,
  userId: number,
  updateData: UpdateChartData
): Promise<Chart | null> => {
  const fields: string[] = [];
  const values: unknown[] = [];
  let paramCount = 1;

  if (updateData.name !== undefined) {
    fields.push(`name = $${paramCount}`);
    values.push(updateData.name);
    paramCount++;
  }

  if (updateData.birth_location !== undefined) {
    fields.push(`birth_location = $${paramCount}`);
    values.push(updateData.birth_location);
    paramCount++;
  }

  if (updateData.timezone !== undefined) {
    fields.push(`timezone = $${paramCount}`);
    values.push(updateData.timezone);
    paramCount++;
  }

  if (updateData.chart_data !== undefined) {
    fields.push(`chart_data = $${paramCount}`);
    values.push(JSON.stringify(updateData.chart_data));
    paramCount++;
  }

  if (fields.length === 0) {
    return findChartById(id, userId);
  }

  fields.push(`updated_at = NOW()`);
  values.push(id);
  values.push(userId);

  const result = await query(
    `UPDATE charts 
     SET ${fields.join(', ')} 
     WHERE id = $${paramCount} AND user_id = $${paramCount + 1}
     RETURNING *`,
    values
  );

  return result.rows[0] || null;
};

/**
 * Delete chart
 */
export const deleteChart = async (
  id: number,
  userId: number
): Promise<boolean> => {
  const result = await query(
    'DELETE FROM charts WHERE id = $1 AND user_id = $2',
    [id, userId]
  );

  return (result.rowCount ?? 0) > 0;
};

/**
 * Get chart count for user
 */
export const getChartCount = async (userId: number): Promise<number> => {
  const result = await query(
    'SELECT COUNT(*) as count FROM charts WHERE user_id = $1',
    [userId]
  );

  return parseInt(result.rows[0].count);
};

export default {
  createChart,
  findChartsByUserId,
  findChartById,
  findChartByUuid,
  updateChart,
  deleteChart,
  getChartCount,
};
