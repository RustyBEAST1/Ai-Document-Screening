import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import OverviewStats from './components/OverviewStats';
import UploadScreen from './components/UploadScreen';
import ResultScreen from './components/ResultScreen';
import RecentActivityTable from './components/RecentActivityTable';
import DisclaimerBanner from './components/DisclaimerBanner';
import {
  ShieldCheck,
  Cpu,
  Layers,
  FileCheck2,
  Printer,
  Sliders,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';

export default function App() {
  const [activeNav, setActiveNav] = useState('dashboard'); // 'dashboard' | 'scanner' | 'history' | 'reports' | 'settings'
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const [screen, setScreen] = useState('upload'); // 'upload' | 'scanning' | 'result'
  const [screeningResult, setScreeningResult] = useState(null);
  const [scannerStatus, setScannerStatus] = useState("Analyzing Document...");

  // History state
  const [history, setHistory] = useState([]);
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);

  // Fetch audit history on mount
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setIsHistoryLoading(true);
    try {
      const res = await fetch('/api/history?limit=50');
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (err) {
      console.error("Failed to load history:", err);
    } finally {
      setIsHistoryLoading(false);
    }
  };

  // Handler for custom uploaded document
  const handleStartScreening = async (formDataPayload) => {
    setScreen('scanning');
    setScannerStatus("Running AI tamper detection & checksum validation...");

    try {
      const fd = new FormData();
      fd.append("file", formDataPayload.file);
      fd.append("document_type", formDataPayload.documentType);
      if (formDataPayload.name) fd.append("user_name", formDataPayload.name);
      if (formDataPayload.dob) fd.append("user_dob", formDataPayload.dob);
      if (formDataPayload.docNumber) fd.append("user_number", formDataPayload.docNumber);

      const res = await fetch('/api/screen', {
        method: 'POST',
        body: fd
      });

      if (!res.ok) {
        let errText = "Screening failed";
        try {
          const errData = await res.json();
          errText = errData.detail || errText;
        } catch (_) {
          errText = `Server connection failed (HTTP ${res.status}). Ensure backend is active on port 8000.`;
        }
        throw new Error(errText);
      }

      const data = await res.json();
      setScreeningResult(data);
      setScreen('result');
      fetchHistory(); // Refresh history table below
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      alert("Error: " + err.message);
      setScreen('upload');
    }
  };

  // Handler for 1-click sample document testing
  const handleSelectSample = async (sampleId, docType, crossCheck = {}) => {
    setScreen('scanning');
    setScannerStatus("Analyzing sample document...");

    try {
      const params = new URLSearchParams();
      if (crossCheck.name) params.append("user_name", crossCheck.name);
      if (crossCheck.dob) params.append("user_dob", crossCheck.dob);
      if (crossCheck.docNumber) params.append("user_number", crossCheck.docNumber);
      const q = params.toString() ? `?${params.toString()}` : "";

      const res = await fetch(`/api/screen-sample/${sampleId}${q}`, {
        method: 'POST'
      });

      if (!res.ok) {
        let errText = "Sample verification failed";
        try {
          const errData = await res.json();
          errText = errData.detail || errText;
        } catch (_) {
          errText = `Server connection failed (HTTP ${res.status}). Ensure backend is active on port 8000.`;
        }
        throw new Error(errText);
      }

      const data = await res.json();
      setScreeningResult(data);
      setScreen('result');
      fetchHistory(); // Refresh history table below
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      alert("Error: " + err.message);
      setScreen('upload');
    }
  };

  // Handler for deleting current document
  const handleDeleteCurrentDocument = async () => {
    if (!screeningResult || !screeningResult.id) return;
    const confirmDelete = window.confirm(
      "Permanently delete this document scan and its forensic report from server storage?"
    );
    if (!confirmDelete) return;

    try {
      await fetch(`/api/screening/${screeningResult.id}`, { method: 'DELETE' });
      setScreeningResult(null);
      setScreen('upload');
      fetchHistory();
    } catch (err) {
      alert("Failed to delete record: " + err.message);
    }
  };

  // Handler for selecting an item from the history table below
  const handleSelectHistoryItem = async (screeningId) => {
    try {
      const res = await fetch(`/api/screening/${screeningId}`);
      if (res.ok) {
        const data = await res.json();
        setScreeningResult(data);
        setScreen('result');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } catch (e) {
      alert("Failed to load historical record: " + e.message);
    }
  };

  // Handler for deleting an item from the history table
  const handleDeleteHistoryItem = async (screeningId) => {
    if (!window.confirm("Delete this screening record?")) return;
    try {
      const res = await fetch(`/api/screening/${screeningId}`, { method: 'DELETE' });
      if (res.ok) {
        setHistory(prev => prev.filter(item => item.id !== screeningId));
        if (screeningResult && screeningResult.id === screeningId) {
          setScreeningResult(null);
          setScreen('upload');
        }
      }
    } catch (err) {
      alert("Failed to delete: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1120] text-[#E5EDF7] flex">

      {/* Left Sidebar */}
      <Sidebar
        activeNav={activeNav}
        setActiveNav={setActiveNav}
        isMobileOpen={isMobileSidebarOpen}
        setIsMobileOpen={setIsMobileSidebarOpen}
        totalScans={history.length}
      />

      {/* Main Content Area (Offset for lg:w-64 sidebar) */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64">

        {/* Top Navigation */}
        <TopNav
          onToggleSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          activeNav={activeNav}
        />

        {/* Page Container */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">

          {/* Overview Stat Cards (Always visible on dashboard/scanner/history) */}
          <OverviewStats history={history} />

          {/* VIEW: Dashboard & Document Scanner */}
          {(activeNav === 'dashboard' || activeNav === 'scanner') && (
            <div className="space-y-8">
              
              {/* Screening Upload / Scanning / Result Area */}
              {screen === 'upload' && (
                <UploadScreen
                  onStartScreening={handleStartScreening}
                  onSelectSample={handleSelectSample}
                />
              )}

              {screen === 'scanning' && (
                <div className="text-center py-20 px-4 bg-[#151F32] border border-[#23334A] rounded-2xl shadow-xl">
                  <div className="relative w-28 h-36 mx-auto mb-6 border-2 border-[#23334A] rounded-xl overflow-hidden bg-[#0B1120] flex flex-col justify-between p-3">
                    <div className="h-2 bg-[#1E2D44] rounded"></div>
                    <div className="w-10 h-10 bg-[#1E2D44] rounded-full mx-auto"></div>
                    <div className="h-2 bg-[#1E2D44] rounded"></div>
                    <div className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-[#06B6D4] to-transparent shadow-[0_0_10px_#06B6D4] animate-bounce"></div>
                  </div>
                  <h3 className="text-lg sm:text-xl font-bold text-[#E5EDF7] mb-1">
                    {scannerStatus}
                  </h3>
                  <p className="text-xs text-[#94A3B8]">
                    Testing image tampering (ELA), OCR extraction, and official format checksums...
                  </p>
                </div>
              )}

              {screen === 'result' && screeningResult && (
                <ResultScreen
                  result={screeningResult}
                  onScreenAnother={() => {
                    setScreeningResult(null);
                    setScreen('upload');
                  }}
                  onDeleteDocument={handleDeleteCurrentDocument}
                />
              )}

              {/* HISTORY TABLE PLACED BELOW */}
              <RecentActivityTable
                history={history}
                loading={isHistoryLoading}
                onRefresh={fetchHistory}
                onSelectScreening={handleSelectHistoryItem}
                onDeleteItem={handleDeleteHistoryItem}
                searchQuery={searchQuery}
              />
            </div>
          )}

          {/* VIEW: History Dedicated View */}
          {activeNav === 'history' && (
            <RecentActivityTable
              history={history}
              loading={isHistoryLoading}
              onRefresh={fetchHistory}
              onSelectScreening={handleSelectHistoryItem}
              onDeleteItem={handleDeleteHistoryItem}
              searchQuery={searchQuery}
            />
          )}

          {/* VIEW: Reports */}
          {activeNav === 'reports' && (
            <div className="bg-[#151F32] border border-[#23334A] rounded-2xl p-6 sm:p-8 space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-[#23334A]">
                <div>
                  <h3 className="text-lg font-bold text-[#E5EDF7]">Screening Audit & Compliance Reports</h3>
                  <p className="text-xs text-[#94A3B8]">Generate printable audit logs for verification records</p>
                </div>
                <button
                  type="button"
                  onClick={() => window.print()}
                  className="px-4 py-2 bg-[#06B6D4] text-[#0B1120] font-black rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/20"
                >
                  <Printer className="w-4 h-4 stroke-[2.5]" />
                  Print All Reports
                </button>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl">
                  <p className="text-xs text-[#94A3B8]">Total Processed</p>
                  <p className="text-2xl font-black text-[#06B6D4] mt-1">{history.length}</p>
                </div>
                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl">
                  <p className="text-xs text-[#94A3B8]">Authentic Documents</p>
                  <p className="text-2xl font-black text-[#22C55E] mt-1">
                    {history.filter(h => (h.risk_level || '').toLowerCase() === 'low').length}
                  </p>
                </div>
                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl">
                  <p className="text-xs text-[#94A3B8]">Flagged / Fraudulent</p>
                  <p className="text-2xl font-black text-[#EF4444] mt-1">
                    {history.filter(h => (h.risk_level || '').toLowerCase() === 'high').length}
                  </p>
                </div>
              </div>

              <p className="text-xs text-[#94A3B8]">
                All screenings are logged with unique UUIDs, timestamp records, and tamper heatmaps for verification auditing.
              </p>
            </div>
          )}

          {/* VIEW: Settings */}
          {activeNav === 'settings' && (
            <div className="bg-[#151F32] border border-[#23334A] rounded-2xl p-6 sm:p-8 space-y-6">
              <div className="pb-4 border-b border-[#23334A]">
                <h3 className="text-lg font-bold text-[#E5EDF7]">Verification Engine Settings</h3>
                <p className="text-xs text-[#94A3B8]">Current configuration of forensic and checksum modules</p>
              </div>

              <div className="space-y-3">
                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl flex items-center justify-between">
                  <div>
                    <p className="text-sm font-bold text-[#E5EDF7]">Verhoeff Dihedral D5 Algorithm</p>
                    <p className="text-xs text-[#94A3B8]">Validates 12-digit UIDAI Aadhaar checksum sequences</p>
                  </div>
                  <span className="text-xs font-bold text-[#22C55E] bg-[#22C55E]/10 border border-[#22C55E]/30 px-3 py-1 rounded-full">
                    Active
                  </span>
                </div>

                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl flex items-center justify-between">
                  <div>
                    <p className="text-sm font-bold text-[#E5EDF7]">Error Level Analysis (ELA)</p>
                    <p className="text-xs text-[#94A3B8]">Detects digital splice artifacts at 95% JPEG re-save delta</p>
                  </div>
                  <span className="text-xs font-bold text-[#22C55E] bg-[#22C55E]/10 border border-[#22C55E]/30 px-3 py-1 rounded-full">
                    Active
                  </span>
                </div>

                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl flex items-center justify-between">
                  <div>
                    <p className="text-sm font-bold text-[#E5EDF7]">ICAO Doc 9303 Passport MRZ Validator</p>
                    <p className="text-xs text-[#94A3B8]">Calculates 7-3-1 weighted modulus 10 passport checksum</p>
                  </div>
                  <span className="text-xs font-bold text-[#22C55E] bg-[#22C55E]/10 border border-[#22C55E]/30 px-3 py-1 rounded-full">
                    Active
                  </span>
                </div>

                <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-xl flex items-center justify-between">
                  <div>
                    <p className="text-sm font-bold text-[#E5EDF7]">Laplacian Variance Blur & Glare Detector</p>
                    <p className="text-xs text-[#94A3B8]">Threshold score 100 for camera motion blur and flash reflection</p>
                  </div>
                  <span className="text-xs font-bold text-[#22C55E] bg-[#22C55E]/10 border border-[#22C55E]/30 px-3 py-1 rounded-full">
                    Active
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Verification Disclaimer */}
          <DisclaimerBanner />

        </main>
      </div>

    </div>
  );
}
