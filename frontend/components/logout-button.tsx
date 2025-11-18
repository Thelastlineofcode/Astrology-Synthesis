"use client";

export function LogoutButton() {
  return (
    <button
      onClick={() => {
        localStorage.removeItem("mula_token");
        window.location.href = "/";
      }}
      className="px-3 py-1.5 rounded border border-white/20 text-sm hover:bg-white hover:text-black transition"
    >
      Logout
    </button>
  );
}
