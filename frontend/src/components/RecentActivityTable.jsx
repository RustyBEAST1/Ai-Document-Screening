import React, { useState } from 'react';
import {
  History,
  ShieldCheck,
  AlertTriangle,
  AlertCircle,
  Eye,
  Trash2,
  Filter,
  RefreshCw,
  Search,
  FileText
} from 'lucide-react';

export default function RecentActivityTable({
  history = [],
  loading = false,
  onRefresh,
  onSelectScreening,
  onDeleteItem,
  searchQuery = ''
}) {
  const [filterRisk, setFilterRisk] = useState('all');

  const statusBadge = {
    low: {
      badge: 'bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30',
      text: 'Authentic',
      icon: ShieldCheck
    },
    medium: {
      badge: 'bg-[#F59E0B]/15 text-[#F59E0B] border-[#F59E0B]/30',
      text: 'Suspicious',
      icon: AlertCircle
    },
    high: {
      badge: 'bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30',
      text: 'Fraudulent',
      icon: AlertTriangle
    }
  };

  // Filter history
  const filtered = history.filter((item) => {
    const risk = (item.risk_level || '').toLowerCase();
    if (filterRisk !== 'all' && risk !== filterRisk) return false;

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchDoc = (item.document_type || '').toLowerCase().includes(q);
      const matchFile = (item.filename || '').toLowerCase().includes(q);
      const matchId = (item.id || '').toLowerCase().includes(q);
      const matchName = (item.extracted_name || '').toLowerCase().includes(q);
      if (!matchDoc && !matchFile && !matchId && !matchName) return false;
    }
    return true;
  });

  return (
    <div id="recent-history" className="bg-[#151F32] border border-[#23334A] rounded-2xl p-5 sm:p-7 shadow-xl mt-8">
      
      {/* Table Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-[#23334A]">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-[#06B6D4]/15 border border-[#06B6D4]/30 flex items-center justify-center text-[#06B6D4]">
              <History className="w-4 h-4" />
            </div>
            <h3 className="text-base sm:text-lg font-bold text-[#E5EDF7]">
              Recent Verification History
            </h3>
            <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-[#0B1120] border border-[#23334A] text-[#94A3B8]">
              {history.length} Records
            </span>
          </div>
          <p className="text-xs text-[#94A3B8] mt-1">
            Audit logs of all screened identity documents and forensic scores
          </p>
        </div>

        {/* Filter Pills & Refresh */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1 bg-[#0B1120] p-1 rounded-xl border border-[#23334A] text-xs font-bold">
            {[
              { id: 'all', label: 'All' },
              { id: 'low', label: 'Authentic' },
              { id: 'medium', label: 'Suspicious' },
              { id: 'high', label: 'Fraudulent' },
            ].map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setFilterRisk(tab.id)}
                className={`px-3 py-1 rounded-lg transition ${
                  filterRisk === tab.id
                    ? 'bg-[#06B6D4] text-[#0B1120] font-black'
                    : 'text-[#94A3B8] hover:text-[#E5EDF7]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <button
            type="button"
            onClick={onRefresh}
            className="p-2 bg-[#0B1120] border border-[#23334A] text-[#94A3B8] hover:text-[#06B6D4] hover:border-[#06B6D4] rounded-xl transition"
            title="Refresh history"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-[#06B6D4]' : ''}`} />
          </button>
        </div>
      </div>

      {/* Table Content */}
      <div className="overflow-x-auto mt-4">
        {loading && history.length === 0 ? (
          <div className="text-center py-12 text-[#94A3B8] text-sm">
            <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-[#06B6D4]" />
            Loading verification history...
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12 text-[#94A3B8]">
            <FileText className="w-10 h-10 mx-auto mb-2 text-[#23334A]" />
            <p className="text-sm font-semibold text-[#E5EDF7]">No verification records found</p>
            <p className="text-xs text-[#94A3B8] mt-1">
              Upload an ID or click a Quick Test Case above to run your first screening.
            </p>
          </div>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-[#23334A] text-[#94A3B8] uppercase text-[10px] tracking-wider font-extrabold">
                <th className="py-3 px-3">Document Type</th>
                <th className="py-3 px-3">Scan / File Name</th>
                <th className="py-3 px-3">Verification Status</th>
                <th className="py-3 px-3 text-center">Risk Score</th>
                <th className="py-3 px-3">Tamper Check</th>
                <th className="py-3 px-3">Date & Time</th>
                <th className="py-3 px-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#23334A]/60">
              {filtered.map((item) => {
                const risk = (item.risk_level || 'low').toLowerCase();
                const badge = statusBadge[risk] || statusBadge.low;
                const StatusIcon = badge.icon;
                const dateStr = item.timestamp
                  ? new Date(item.timestamp).toLocaleString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })
                  : 'Recent';

                return (
                  <tr
                    key={item.id}
                    onClick={() => onSelectScreening(item.id)}
                    className="hover:bg-[#0B1120]/60 transition cursor-pointer group"
                  >
                    {/* Document Type */}
                    <td className="py-3.5 px-3">
                      <div className="font-bold text-[#E5EDF7] group-hover:text-[#06B6D4] transition flex items-center gap-2">
                        <span>{item.document_type || 'Unknown ID'}</span>
                      </div>
                      <span className="text-[10px] text-[#94A3B8] font-mono">
                        #{item.id?.slice(0, 8)}
                      </span>
                    </td>

                    {/* File / Holder Name */}
                    <td className="py-3.5 px-3 max-w-[180px] truncate text-[#94A3B8]">
                      {item.extracted_name ? (
                        <div>
                          <p className="font-semibold text-[#E5EDF7] truncate">{item.extracted_name}</p>
                          <p className="text-[10px] text-[#94A3B8] truncate">{item.filename}</p>
                        </div>
                      ) : (
                        <span className="truncate">{item.filename || 'Camera Scan'}</span>
                      )}
                    </td>

                    {/* Status Badge */}
                    <td className="py-3.5 px-3">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold border ${badge.badge}`}>
                        <StatusIcon className="w-3 h-3" />
                        {badge.text}
                      </span>
                    </td>

                    {/* Risk Score */}
                    <td className="py-3.5 px-3 text-center">
                      <span className="font-black text-sm text-[#E5EDF7]">
                        {item.risk_score !== undefined ? `${item.risk_score}/100` : '-'}
                      </span>
                    </td>

                    {/* Tamper Result */}
                    <td className="py-3.5 px-3">
                      {item.tampering_detected ? (
                        <span className="text-[#EF4444] font-semibold text-[11px]">
                          Tampered
                        </span>
                      ) : (
                        <span className="text-[#22C55E] font-semibold text-[11px]">
                          Passed (No Splice)
                        </span>
                      )}
                    </td>

                    {/* Timestamp */}
                    <td className="py-3.5 px-3 text-[#94A3B8] whitespace-nowrap">
                      {dateStr}
                    </td>

                    {/* Actions */}
                    <td className="py-3.5 px-3 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectScreening(item.id);
                          }}
                          className="p-1.5 rounded-lg bg-[#0B1120] border border-[#23334A] text-[#06B6D4] hover:bg-[#06B6D4] hover:text-[#0B1120] transition"
                          title="View analysis report"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            onDeleteItem(item.id);
                          }}
                          className="p-1.5 rounded-lg bg-[#0B1120] border border-[#23334A] text-[#EF4444] hover:bg-[#EF4444] hover:text-white transition"
                          title="Delete record"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

    </div>
  );
}
