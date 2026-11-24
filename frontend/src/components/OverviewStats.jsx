import React from 'react';
import {
  FileCheck2,
  ShieldCheck,
  AlertTriangle,
  ShieldAlert,
  TrendingUp
} from 'lucide-react';

export default function OverviewStats({ history = [] }) {
  const total = history.length;
  const verified = history.filter(
    (h) => (h.risk_level || '').toLowerCase() === 'low'
  ).length;
  const suspicious = history.filter(
    (h) => (h.risk_level || '').toLowerCase() === 'medium'
  ).length;
  const rejected = history.filter(
    (h) => (h.risk_level || '').toLowerCase() === 'high'
  ).length;

  const stats = [
    {
      label: 'Total Scans',
      value: total,
      sub: 'All processed IDs',
      icon: FileCheck2,
      color: '#06B6D4',
      bgGlow: 'bg-[#06B6D4]/10',
      borderGlow: 'border-[#06B6D4]/30',
      textColor: 'text-[#06B6D4]',
    },
    {
      label: 'Verified Documents',
      value: verified,
      sub: 'Passed all checks (Authentic)',
      icon: ShieldCheck,
      color: '#22C55E',
      bgGlow: 'bg-[#22C55E]/10',
      borderGlow: 'border-[#22C55E]/30',
      textColor: 'text-[#22C55E]',
    },
    {
      label: 'Suspicious Documents',
      value: suspicious,
      sub: 'Review required (Quality/Mismatch)',
      icon: AlertTriangle,
      color: '#F59E0B',
      bgGlow: 'bg-[#F59E0B]/10',
      borderGlow: 'border-[#F59E0B]/30',
      textColor: 'text-[#F59E0B]',
    },
    {
      label: 'Rejected Documents',
      value: rejected,
      sub: 'Fraud / Tampering detected',
      icon: ShieldAlert,
      color: '#EF4444',
      bgGlow: 'bg-[#EF4444]/10',
      borderGlow: 'border-[#EF4444]/30',
      textColor: 'text-[#EF4444]',
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6">
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <div
            key={stat.label}
            className="p-4 sm:p-5 rounded-2xl bg-[#151F32] border border-[#23334A] hover:border-[#06B6D4]/40 transition shadow-sm flex flex-col justify-between"
          >
            <div className="flex items-center justify-between gap-2 mb-2">
              <span className="text-xs font-semibold text-[#94A3B8]">{stat.label}</span>
              <div className={`p-2 rounded-xl ${stat.bgGlow} ${stat.textColor}`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>

            <div className="flex items-baseline gap-2">
              <span className={`text-2xl sm:text-3xl font-black ${stat.textColor}`}>
                {stat.value}
              </span>
            </div>

            <p className="text-[11px] text-[#94A3B8] mt-1 truncate">
              {stat.sub}
            </p>
          </div>
        );
      })}
    </div>
  );
}
