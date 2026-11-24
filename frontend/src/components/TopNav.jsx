import React from 'react';
import {
  Menu,
  Search,
  Bell,
  User,
  Shield,
  Activity,
  CheckCircle2
} from 'lucide-react';

export default function TopNav({
  onToggleSidebar,
  searchQuery,
  setSearchQuery,
  activeNav
}) {
  const titles = {
    dashboard: 'Security Screening Dashboard',
    scanner: 'Document Upload & AI Analysis',
    history: 'Verification Audit Logs',
    reports: 'Compliance & Audit Reports',
    settings: 'System Configuration',
  };

  return (
    <header className="h-16 bg-[#151F32] border-b border-[#23334A] px-4 sm:px-6 flex items-center justify-between gap-4 sticky top-0 z-30">
      
      {/* Left: Mobile Toggle & Page Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg text-[#94A3B8] hover:text-[#E5EDF7] hover:bg-[#1E2D44] lg:hidden"
          title="Toggle Navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:block">
          <h2 className="text-sm sm:text-base font-bold text-[#E5EDF7]">
            {titles[activeNav] || 'Security Dashboard'}
          </h2>
          <p className="text-[11px] text-[#94A3B8] hidden md:block">
            Indian ID Fraud Detection • Verhoeff, ELA & Quality
          </p>
        </div>
      </div>

      {/* Center: Search input */}
      <div className="flex-1 max-w-md mx-2">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search scan ID, holder name, or document number..."
            className="w-full pl-9 pr-4 py-1.5 bg-[#0B1120] border border-[#23334A] rounded-xl text-xs sm:text-sm text-[#E5EDF7] placeholder-[#94A3B8]/60 focus:outline-none focus:border-[#06B6D4] focus:ring-1 focus:ring-[#06B6D4] transition"
          />
        </div>
      </div>

      {/* Right: Status, Alerts, Profile */}
      <div className="flex items-center gap-2 sm:gap-3">
        
        {/* Live System Badge */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1 bg-[#0B1120] border border-[#23334A] rounded-full text-xs font-semibold text-[#94A3B8]">
          <span className="w-2 h-2 rounded-full bg-[#22C55E]"></span>
          <span className="text-[#E5EDF7]">Online</span>
        </div>

        {/* Notifications */}
        <button
          className="relative p-2 text-[#94A3B8] hover:text-[#E5EDF7] hover:bg-[#1E2D44] rounded-xl transition"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-[#06B6D4] rounded-full"></span>
        </button>

        {/* Profile Badge */}
        <div className="flex items-center gap-2 pl-2 border-l border-[#23334A]">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#1E2D44] to-[#23334A] border border-[#23334A] flex items-center justify-center text-[#06B6D4] font-bold text-xs">
            SA
          </div>
          <div className="hidden xl:block text-left">
            <p className="text-xs font-bold text-[#E5EDF7] leading-none">Security Officer</p>
            <p className="text-[10px] text-[#94A3B8] leading-tight">Station #01</p>
          </div>
        </div>

      </div>
    </header>
  );
}
