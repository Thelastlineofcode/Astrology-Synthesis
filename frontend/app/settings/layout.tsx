import { NavLink } from "@/components/nav-link";

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-6">
      <div className="flex gap-4 text-sm">
        <NavLink href="/settings/notifications">Notifications</NavLink>
      </div>
      {children}
    </div>
  );
}
