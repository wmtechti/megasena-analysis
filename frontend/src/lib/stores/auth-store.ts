/**
 * Zustand store for authentication state.
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/types";

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  isAuthenticated: () => boolean;
  isPremium: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,

      setAuth: (user, token) => {
        set({ user, token });
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", token);
        }
      },

      clearAuth: () => {
        set({ user: null, token: null });
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
        }
      },

      isAuthenticated: () => {
        const state = get();
        return state.user !== null && state.token !== null;
      },

      isPremium: () => {
        const state = get();
        return state.user?.has_premium_access || false;
      },
    }),
    {
      name: "auth-storage",
    }
  )
);
