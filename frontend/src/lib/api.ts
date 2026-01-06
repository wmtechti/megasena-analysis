/**
 * API service functions for all endpoints.
 */

import { apiClient } from "./api-client";
import type {
  User,
  UserLogin,
  UserRegister,
  AuthToken,
  Lottery,
  Draw,
  DrawWithFeatures,
  LotteryAnalysis,
  NumberFrequency,
  DrawStats,
  HealthCheck,
} from "@/types";

// ========== Health ==========

export const healthApi = {
  check: async (): Promise<HealthCheck> => {
    const response = await apiClient.get<HealthCheck>("/health");
    return response.data;
  },
};

// ========== Auth ==========

export const authApi = {
  register: async (data: UserRegister): Promise<AuthToken> => {
    const response = await apiClient.post<AuthToken>("/api/v1/auth/register", data);
    return response.data;
  },

  login: async (data: UserLogin): Promise<AuthToken> => {
    const response = await apiClient.post<AuthToken>("/api/v1/auth/login", data);
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>("/api/v1/auth/me");
    return response.data;
  },

  refresh: async (): Promise<AuthToken> => {
    const response = await apiClient.post<AuthToken>("/api/v1/auth/refresh");
    return response.data;
  },
};

// ========== Lotteries ==========

export const lotteriesApi = {
  list: async (): Promise<Lottery[]> => {
    const response = await apiClient.get<Lottery[]>("/api/v1/lotteries");
    return response.data;
  },

  get: async (slug: string): Promise<Lottery> => {
    const response = await apiClient.get<Lottery>(`/api/v1/lotteries/${slug}`);
    return response.data;
  },

  getDraws: async (
    slug: string,
    page: number = 1,
    size: number = 50
  ): Promise<Draw[]> => {
    const response = await apiClient.get<Draw[]>(`/api/v1/lotteries/${slug}/draws`, {
      params: { page, size },
    });
    return response.data;
  },

  getDraw: async (slug: string, contest: number): Promise<DrawWithFeatures> => {
    const response = await apiClient.get<DrawWithFeatures>(
      `/api/v1/lotteries/${slug}/draws/${contest}`
    );
    return response.data;
  },

  getStats: async (slug: string): Promise<DrawStats> => {
    const response = await apiClient.get<DrawStats>(`/api/v1/lotteries/${slug}/stats`);
    return response.data;
  },

  getFrequency: async (slug: string): Promise<NumberFrequency[]> => {
    const response = await apiClient.get<NumberFrequency[]>(
      `/api/v1/lotteries/${slug}/frequency`
    );
    return response.data;
  },

  getAnalysis: async (slug: string): Promise<LotteryAnalysis> => {
    const response = await apiClient.get<LotteryAnalysis>(
      `/api/v1/lotteries/${slug}/analysis`
    );
    return response.data;
  },
};
