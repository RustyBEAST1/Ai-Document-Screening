import React, { useEffect, useState } from 'react';
import { X, Clock, Trash2, ExternalLink, Filter } from 'lucide-react';

export default function HistoryModal({ isOpen, onClose, onSelectScreening }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterRisk, setFilterRisk] = useState("all");

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/history?limit=50');
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteItem = async (e, id) => {
    e.stopPropagation();
    if (!window.confirm("Permanently delete this screening record and document from server?")) return;
    try {
      const res = await fetch(`/api/screening/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setHistory(history.filter(h => h.id !== id));
      }
    } catch (err) {
      alert("Failed to delete record: " + err.message);
    }
  };

  if (!isOpen) return null;

  const filteredHistory = history.filter(item => {
    if (filterRisk === "all") return true;
    return (item.risk_level || "").toLowerCase() === filterRisk;
  });

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden border border-slate-200">
        
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-bold text-slate-900">Screening Audit History</h3>
            <span className="text-xs bg-slate-100 text-slate-600 font-bold px-2 py-0.5 rounded-full">
              {history.length} Records
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Filter Pills */}
        <div className="px-6 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center gap-2 overflow-x-auto text-xs font-bold">
          <span className="text-slate-400 flex items-center gap-1"><Filter className="w-3 h-3" /> Filter:</span>
          {["all", "high", "medium", "low"].map(risk => (
            <button
              key={risk}
              type="button"
              onClick={() => setFilterRisk(risk)}
              className={`px-3 py-1 rounded-full uppercase transition ${
                filterRisk === risk
                  ? "bg-blue-600 text-white shadow-sm"
                  : "bg-white text-slate-600 border border-slate-200 hover:border-blue-400"
              }`}
            >
              {risk}
            </button>
          ))}
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-2.5 flex-1">
          {loading ? (
            <p className="text-center text-sm text-slate-400 py-12">Loading screening records...</p>
          ) : filteredHistory.length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <Clock className="w-10 h-10 mx-auto mb-2 opacity-40" />
              <p className="font-semibold text-sm">No screening records found.</p>
              <p className="text-xs text-slate-400 mt-1">Screen a document or test sample to record an audit.</p>
            </div>
          ) : (
            filteredHistory.map((item) => {
              const risk = (item.risk_level || 'low').toLowerCase();
              const badgeClass = {
                low: 'bg-emerald-100 text-emerald-800 border-emerald-300',
                medium: 'bg-amber-100 text-amber-800 border-amber-300',
                high: 'bg-red-100 text-red-800 border-red-300'
              }[risk] || 'bg-slate-100 text-slate-800 border-slate-300';

              return (
                <div
                  key={item.id}
                  onClick={() => onSelectScreening(item.id)}
                  className="p-3.5 border border-slate-200 hover:border-blue-400 hover:bg-slate-50/70 rounded-xl flex items-center justify-between cursor-pointer transition gap-3 shadow-xs"
                >
                  <div className="overflow-hidden">
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-slate-900">{item.document_type}</h4>
                      <span className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${badgeClass}`}>
                        {item.risk_level.toUpperCase()} ({item.risk_score}/100)
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5 truncate">
                      {new Date(item.created_at).toLocaleString()} • {item.filename}
                    </p>
                  </div>
                  
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      type="button"
                      onClick={(e) => handleDeleteItem(e, item.id)}
                      className="p-1.5 text-slate-400 hover:text-red-500 rounded-lg hover:bg-red-50 transition"
                      title="Permanently delete record"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <span className="text-xs font-bold text-blue-600 hover:underline">
                      View Report &rarr;
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

      </div>
    </div>
  );
}
