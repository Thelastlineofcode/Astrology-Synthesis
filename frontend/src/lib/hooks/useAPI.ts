/**
 * Custom React Hooks for API Data Fetching
 */

"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { APIError } from "../api/client";

export interface UseAPIOptions<T = unknown> {
  onSuccess?: (data: T) => void;
  onError?: (error: APIError) => void;
}

export interface UseAPIState<T> {
  data: T | null;
  loading: boolean;
  error: APIError | null;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export interface UseAPIReturn<T, TArgs extends any[]> extends UseAPIState<T> {
  execute: (...args: TArgs) => Promise<T | null>;
  reset: () => void;
}

/**
 * Generic hook for API requests
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function useAPI<T, TArgs extends any[] = []>(
  apiFunction: (...args: TArgs) => Promise<T>,
  options: UseAPIOptions<T> = {}
): UseAPIReturn<T, TArgs> {
  const { onSuccess, onError } = options;
  const isMountedRef = useRef(true);

  const [state, setState] = useState<UseAPIState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(
    async (...args: TArgs): Promise<T | null> => {
      setState((prev) => ({ ...prev, loading: true, error: null }));

      try {
        const result = await apiFunction(...args);
        if (isMountedRef.current) {
          setState({ data: result, loading: false, error: null });
          onSuccess?.(result);
        }
        return result;
      } catch (err) {
        const error =
          err instanceof APIError ? err : new APIError("Unknown error", 0);
        if (isMountedRef.current) {
          setState({ data: null, loading: false, error });
          onError?.(error);
        }
        return null;
      }
    },
    [apiFunction, onSuccess, onError]
  );

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return {
    ...state,
    execute,
    reset,
  };
}

/**
 * Hook with automatic caching
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function useCachedAPI<T, TArgs extends any[] = []>(
  apiFunction: (...args: TArgs) => Promise<T>,
  cacheKey: string,
  options: UseAPIOptions<T> & { cacheDuration?: number } = {}
): UseAPIReturn<T, TArgs> {
  const { cacheDuration = 5 * 60 * 1000, ...apiOptions } = options; // 5 minutes default

  const getCachedData = useCallback((): T | null => {
    if (typeof window === "undefined") return null;

    try {
      const cached = sessionStorage.getItem(cacheKey);
      if (!cached) return null;

      const { data, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp > cacheDuration) {
        sessionStorage.removeItem(cacheKey);
        return null;
      }

      return data;
    } catch {
      return null;
    }
  }, [cacheKey, cacheDuration]);

  const setCachedData = useCallback(
    (data: T) => {
      if (typeof window === "undefined") return;

      try {
        sessionStorage.setItem(
          cacheKey,
          JSON.stringify({ data, timestamp: Date.now() })
        );
      } catch {
        // Ignore storage errors
      }
    },
    [cacheKey]
  );

  const {
    execute: originalExecute,
    reset,
    ...rest
  } = useAPI<T, TArgs>(apiFunction, {
    ...apiOptions,
    onSuccess: (data) => {
      setCachedData(data);
      apiOptions.onSuccess?.(data);
    },
  });

  const [state, setState] = useState<UseAPIState<T>>(rest);

  useEffect(() => {
    const cached = getCachedData();
    if (cached && rest.data === null) {
      setState((prev) => ({ ...prev, data: cached }));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    ...state,
    execute: originalExecute,
    reset: () => {
      if (typeof window !== "undefined") {
        sessionStorage.removeItem(cacheKey);
      }
      reset();
    },
  };
}

/**
 * Hook for paginated data
 */
export interface UsePaginatedAPIReturn<T> extends UseAPIState<T[]> {
  page: number;
  hasMore: boolean;
  loadMore: () => Promise<void>;
  reset: () => void;
}

export function usePaginatedAPI<T>(
  apiFunction: (
    page: number,
    limit: number
  ) => Promise<{ items: T[]; hasMore: boolean }>,
  limit: number = 20
): UsePaginatedAPIReturn<T> {
  const [state, setState] = useState<{
    data: T[];
    loading: boolean;
    error: APIError | null;
    page: number;
    hasMore: boolean;
  }>({
    data: [],
    loading: false,
    error: null,
    page: 1,
    hasMore: true,
  });

  const loadMore = useCallback(async () => {
    if (state.loading || !state.hasMore) return;

    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const result = await apiFunction(state.page, limit);
      setState((prev) => ({
        ...prev,
        data: [...prev.data, ...result.items],
        page: prev.page + 1,
        hasMore: result.hasMore,
        loading: false,
      }));
    } catch (err) {
      const error =
        err instanceof APIError ? err : new APIError("Unknown error", 0);
      setState((prev) => ({ ...prev, loading: false, error }));
    }
  }, [apiFunction, state.page, state.loading, state.hasMore, limit]);

  const reset = useCallback(() => {
    setState({
      data: [],
      loading: false,
      error: null,
      page: 1,
      hasMore: true,
    });
  }, []);

  useEffect(() => {
    // Initial load
    void loadMore();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    data: state.data,
    loading: state.loading,
    error: state.error,
    page: state.page,
    hasMore: state.hasMore,
    loadMore,
    reset,
  };
}
