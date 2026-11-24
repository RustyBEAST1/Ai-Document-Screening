import React from 'react';
import {
  ShieldCheck,
  LayoutDashboard,
  ScanLine,
  History,
  FileText,
  Settings,
  Cpu,
  X
} from 'lucide-react';

export default function Sidebar({
  activeNav,
  setActiveNav,
  isMobileOpen,
  setIsMobileOpen,
  totalScans = 0
}) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'scanner', label: 'Document Scanner', icon: ScanLine },
    { id: 'history', label: 'Verification History', icon: History, count: totalScans },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobileOpen && (
        <div
          onClick={() => setIsMobileOpen(false)}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-[#151F32] border-r border-[#23334A] flex flex-col justify-between transition-transform duration-200 lg:translate-x-0 ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Logo & Title */}
        <div>
          <div className="h-16 px-6 flex items-center justify-between border-b border-[#23334A]">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#06B6D4] to-[#0891B2] flex items-center justify-center text-[#0B1120] font-black shadow-lg shadow-cyan-500/20">
                <ShieldCheck className="w-6 h-6 stroke-[2.5]" />
              </div>
              <div>
                <h1 className="text-base font-black tracking-tight text-[#E5EDF7]">
                  AEGIS <span className="text-[#06B6D4]">AI</span>
                </h1>
                <p className="text-[11px] font-semibold text-[#94A3B8] tracking-wider uppercase">
                  Identity Screener
                </p>
              </div>
            </div>

            {/* Close button for mobile */}
            <button
              onClick={() => setIsMobileOpen(false)}
              className="p-1 text-[#94A3B8] hover:text-[#E5EDF7] rounded-lg lg:hidden"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1.5">
            <div className="px-3 py-2 text-[10px] font-extrabold uppercase tracking-wider text-[#94A3B8]/70">
              Navigation
            </div>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeNav === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveNav(item.id);
                    setIsMobileOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                    isActive
                      ? 'bg-[#06B6D4]/15 text-[#06B6D4] border border-[#06B6D4]/30 shadow-sm'
                      : 'text-[#94A3B8] hover:bg-[#1E2D44] hover:text-[#E5EDF7]'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-[#06B6D4]' : 'text-[#94A3B8]'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.count !== undefined && item.count > 0 && (
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                      isActive ? 'bg-[#06B6D4]/25 text-[#06B6D4]' : 'bg-[#23334A] text-[#94A3B8]'
                    }`}>
                      {item.count}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Engine Status Bottom Panel */}
        <div className="p-4 m-4 rounded-xl bg-[#0B1120] border border-[#23334A]">
          <div className="flex items-center gap-2 mb-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#22C55E] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#22C55E]"></span>
            </span>
            <span className="text-xs font-bold text-[#E5EDF7]">AI Engine: Online</span>
          </div>
          <p className="text-[11px] text-[#94A3B8] leading-tight">
            Verhoeff checksum, ELA tampering & OCR model running.
          </p>
          <div className="mt-2 pt-2 border-t border-[#23334A]/80 flex items-center justify-between text-[10px] text-[#94A3B8]">
            <span>Security Core v2.4</span>
            <span className="text-[#06B6D4] font-semibold">Active</span>
          </div>
        </div>
      </aside>
    </>
  );
}
