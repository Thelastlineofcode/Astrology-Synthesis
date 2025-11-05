"use client";
import { usePathname } from "next/navigation";

export function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const pathname = usePathname();
  const active = pathname === href || (href !== "/" && pathname.startsWith(href));
  return (
    <a href={href} className={active ? "active hover:underline" : "hover:underline"}>
      {children}
    </a>
  );
}
