/**
 * TypeScript definitions for API responses and domain models.
 */

// ========== User Types ==========

export type UserRole = "free" | "individual" | "multi" | "complete" | "admin";

export interface User {
  id: number;
  email: string;
  name: string;
  is_active: boolean;
  role: UserRole;
  created_at: string;
  updated_at: string;
  has_premium_access: boolean;
  can_access_all_lotteries: boolean;
  max_lotteries: number;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserRegister {
  email: string;
  name: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user: User;
}

// ========== Lottery Types ==========

export interface Lottery {
  id: number;
  slug: string;
  name: string;
  total_numbers: number;
  draw_size: number;
  grid_rows: number;
  grid_cols: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Draw {
  id: number;
  lottery_id: number;
  contest_number: number;
  draw_date: string;
  numbers: number[];
  prize_value: number | null;
  winners: number | null;
  created_at: string;
  updated_at: string;
}

export interface DrawFeature {
  id: number;
  draw_id: number;
  // Basic features (15)
  mean_distance: number;
  std_distance: number;
  min_distance: number;
  max_distance: number;
  mean_row: number;
  std_row: number;
  mean_col: number;
  std_col: number;
  spread_row: number;
  spread_col: number;
  count_top_half: number;
  count_bottom_half: number;
  count_left_half: number;
  count_right_half: number;
  count_border: number;
  // Advanced features (12)
  spatial_autocorr: number;
  cluster_coefficient: number;
  mean_nearest_neighbor: number;
  convex_hull_area: number;
  centroid_distance: number;
  quadrant_q1: number;
  quadrant_q2: number;
  quadrant_q3: number;
  quadrant_q4: number;
  entropy_spatial: number;
  dispersion_index: number;
  pattern_regularity: number;
  created_at: string;
  updated_at: string;
}

export interface DrawWithFeatures extends Draw {
  features: DrawFeature | null;
}

export interface NumberFrequency {
  number: number;
  frequency: number;
  percentage: number;
  last_drawn: string | null;
}

export interface DrawStats {
  lottery_slug: string;
  total_draws: number;
  latest_contest: number;
  earliest_date: string;
  latest_date: string;
  total_prize_value: number | null;
}

export interface LotteryAnalysis {
  lottery: Lottery;
  stats: DrawStats;
  most_frequent_numbers: NumberFrequency[];
  least_frequent_numbers: NumberFrequency[];
  avg_features: DrawFeature;
}

// ========== API Response Types ==========

export interface ApiError {
  detail: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// ========== Common Types ==========

export interface HealthCheck {
  status: string;
  environment: string;
  database: string;
}
