"use client";
import { useEffect } from "react";

export function useRequireAuth() {
  useEffect(() => {
    if (typeof window === "undefined") return;
    const token = localStorage.getItem("mula_token");
    if (!token) window.location.href = "/auth/login";
  }, []);
}
