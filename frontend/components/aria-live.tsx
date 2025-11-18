"use client";
import { useEffect, useState } from "react";

export function AriaLive({ message }: { message: string }) {
  const [msg, setMsg] = useState("");
  useEffect(() => {
    setMsg(message);
  }, [message]);
  return (
    <div aria-live="polite" aria-atomic="true" className="sr-only">
      {msg}
    </div>
  );
}
