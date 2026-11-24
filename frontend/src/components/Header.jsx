import React from 'react';
import { ShieldCheck, History, BookOpen, ExternalLink } from 'lucide-react';

export default function Header({ onOpenHistory }) {
  return (
    <header className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 mb-6 border-b border-slate-200 gap-4">
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-500 rounded-2xl flex items-center justify-center text-white shadow-md shadow-blue-500/25">
          <ShieldCheck className="w-7 h-7" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-black tracking-tight text-slate-900">
              AI Fake Identity & Document Screening System
            </h1>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 font-medium">
            Automated Forensic, Tampering & Mathematical Checksum Verification
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 self-start sm:self-auto">
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-full text-[11px] font-bold">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Forensic Core: Active
        </div>

        <a
          href="/docs"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-bold text-slate-600 hover:text-blue-600 bg-white border border-slate-200 hover:border-blue-400 rounded-xl shadow-sm transition"
          title="Open OpenAPI / Swagger Documentation"
        >
          <BookOpen className="w-3.5 h-3.5 text-slate-500" />
          API Docs
        </a>

        <button
          onClick={onOpenHistory}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs sm:text-sm font-bold text-slate-700 hover:text-blue-600 bg-white border border-slate-200 hover:border-blue-400 rounded-xl shadow-sm transition"
        >
          <History className="w-4 h-4 text-slate-500" />
          History
        </button>
      </div>
    </header>
  );
}
