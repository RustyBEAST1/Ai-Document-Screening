import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  AlertCircle,
  Eye,
  EyeOff,
  RotateCcw,
  Trash2,
  FileCheck,
  Layers,
  Printer,
  ShieldAlert,
  ShieldCheck,
  Search,
  Sparkles,
  RotateCw
} from 'lucide-react';

export default function ResultScreen({ result, onScreenAnother, onDeleteDocument }) {
  const [isMasked, setIsMasked] = useState(true);
  const [viewMode, setViewMode] = useState('side-by-side'); // 'side-by-side' | 'original' | 'ela'
  const [rotation, setRotation] = useState(0);

  const risk = (result.risk_level || 'low').toLowerCase();
  const score = result.risk_score || 0;

  // Status-specific themes
  const statusTheme = {
    low: {
      bg: 'bg-[#22C55E]/10 border-[#22C55E]/30 text-[#22C55E]',
      badge: 'bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30',
      gauge: '#22C55E',
      statusText: 'Authentic / Low Risk',
      icon: <CheckCircle2 className="w-8 h-8 text-[#22C55E] flex-shrink-0" />
    },
    medium: {
      bg: 'bg-[#F59E0B]/10 border-[#F59E0B]/30 text-[#F59E0B]',
      badge: 'bg-[#F59E0B]/15 text-[#F59E0B] border-[#F59E0B]/30',
      gauge: '#F59E0B',
      statusText: 'Suspicious / Manual Review',
      icon: <AlertCircle className="w-8 h-8 text-[#F59E0B] flex-shrink-0" />
    },
    high: {
      bg: 'bg-[#EF4444]/10 border-[#EF4444]/30 text-[#EF4444]',
      badge: 'bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30',
      gauge: '#EF4444',
      statusText: 'Potentially Fraudulent / High Risk',
      icon: <AlertTriangle className="w-8 h-8 text-[#EF4444] flex-shrink-0" />
    }
  }[risk] || {
    bg: 'bg-[#06B6D4]/10 border-[#06B6D4]/30 text-[#06B6D4]',
    badge: 'bg-[#06B6D4]/15 text-[#06B6D4] border-[#06B6D4]/30',
    gauge: '#06B6D4',
    statusText: 'Analysis Complete',
    icon: <ShieldCheck className="w-8 h-8 text-[#06B6D4] flex-shrink-0" />
  };

  const circumference = 251.2;
  const strokeOffset = circumference - (score / 100) * circumference;

  const details = result.extracted_details || {};
  const crossChecks = result.cross_checks || {};
  const issues = result.issues || [];

  // Filter issues by category
  const tamperIssues = issues.filter(i => i.category === 'Forensics' || i.category === 'Integrity');
  const isTampered = tamperIssues.length > 0;

  const formatIssues = issues.filter(i => i.category === 'Format');
  const isFormatValid = details.format_valid !== false && formatIssues.length === 0;

  const qualityIssues = issues.filter(i => i.category === 'Quality');
  const hasQualityDefects = qualityIssues.length > 0;

  const faceIssues = issues.filter(i =>
    (i.title && i.title.toLowerCase().includes('face')) ||
    (i.description && i.description.toLowerCase().includes('face'))
  );
  const faceOk = faceIssues.length === 0;

  const originalImg = result.preview_url || result.original_image_url;
  const elaImg = result.ela_url || result.ela_image_url;

  const maskedNumber = details.document_number_masked || '•••• •••• ••••';
  const rawNumber = details.full_number || details.document_number || 'Detected in scan';

  const handlePrint = () => {
    window.print();
  };

  const handleRotate = () => {
    setRotation((prev) => (prev + 90) % 360);
  };

  return (
    <div className="space-y-6">

      {/* Top Overall Status Card */}
      <div className={`p-5 sm:p-7 rounded-2xl border ${statusTheme.bg} bg-[#151F32] shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6`}>
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-2xl bg-[#0B1120] border border-[#23334A]">
            {statusTheme.icon}
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[10px] uppercase font-bold tracking-wider text-[#94A3B8]">
                Screening Verdict
              </span>
              <span className={`text-[10px] font-black px-2.5 py-0.5 rounded-full border ${statusTheme.badge}`}>
                {statusTheme.statusText}
              </span>
            </div>

            <h2 className="text-xl sm:text-2xl font-black tracking-tight text-[#E5EDF7]">
              {result.risk_level} Risk • Score {score}/100
            </h2>

            <p className="text-xs sm:text-sm font-medium text-[#E5EDF7]/90 mt-1.5 max-w-xl leading-relaxed">
              {result.short_message}
            </p>

            <div className="flex flex-wrap items-center gap-2 mt-3 text-[11px] font-semibold text-[#94A3B8]">
              <span className="bg-[#0B1120] px-2.5 py-0.5 rounded-lg border border-[#23334A] text-[#E5EDF7]">
                Document: {result.document_type}
              </span>
              <span>•</span>
              <span className="bg-[#0B1120] px-2.5 py-0.5 rounded-lg border border-[#23334A] text-[#E5EDF7]">
                Confidence: {result.confidence}%
              </span>
              <span>•</span>
              <span className="bg-[#0B1120] px-2.5 py-0.5 rounded-lg border border-[#23334A] text-[#06B6D4]">
                ID: #{result.id?.slice(0, 8)}
              </span>
            </div>
          </div>
        </div>

        {/* Circular Risk Gauge */}
        <div className="relative w-24 h-24 flex-shrink-0 mx-auto sm:mx-0">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="40"
              className="stroke-[#23334A] fill-none"
              strokeWidth="8"
            />
            <circle
              cx="50"
              cy="50"
              r="40"
              fill="none"
              strokeWidth="8"
              strokeLinecap="round"
              stroke={statusTheme.gauge}
              strokeDasharray={circumference}
              strokeDashoffset={strokeOffset}
              style={{ transition: 'stroke-dashoffset 1s ease-out' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-xl font-black text-[#E5EDF7]">{score}</span>
            <span className="text-[9px] font-bold text-[#94A3B8] uppercase">Risk</span>
          </div>
        </div>
      </div>

      {/* Main Dual-Column Panel: Document Preview & AI Checks */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Left Column (6 cols): Document View & ELA Tamper Analysis */}
        <div className="lg:col-span-6 bg-[#151F32] border border-[#23334A] rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[#23334A]">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#06B6D4]" />
              <h3 className="text-xs sm:text-sm font-bold text-[#E5EDF7]">
                Document Inspection & ELA Heatmap
              </h3>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center gap-1 bg-[#0B1120] p-1 rounded-xl border border-[#23334A] text-[11px] font-bold">
              <button
                type="button"
                onClick={() => setViewMode('side-by-side')}
                className={`px-2.5 py-1 rounded-lg transition ${
                  viewMode === 'side-by-side'
                    ? 'bg-[#06B6D4] text-[#0B1120] font-black'
                    : 'text-[#94A3B8] hover:text-[#E5EDF7]'
                }`}
              >
                Split View
              </button>
              <button
                type="button"
                onClick={() => setViewMode('original')}
                className={`px-2.5 py-1 rounded-lg transition ${
                  viewMode === 'original'
                    ? 'bg-[#06B6D4] text-[#0B1120] font-black'
                    : 'text-[#94A3B8] hover:text-[#E5EDF7]'
                }`}
              >
                Original
              </button>
              <button
                type="button"
                onClick={() => setViewMode('ela')}
                className={`px-2.5 py-1 rounded-lg transition ${
                  viewMode === 'ela'
                    ? 'bg-[#06B6D4] text-[#0B1120] font-black'
                    : 'text-[#94A3B8] hover:text-[#E5EDF7]'
                }`}
              >
                Tamper Heatmap
              </button>
            </div>
          </div>

          {/* Controls Bar: Rotate & Privacy Mask */}
          <div className="flex items-center justify-between text-xs">
            <button
              type="button"
              onClick={handleRotate}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0B1120] border border-[#23334A] text-[#94A3B8] hover:text-[#E5EDF7] hover:border-[#06B6D4] transition"
            >
              <RotateCw className="w-3.5 h-3.5 text-[#06B6D4]" />
              Rotate 90°
            </button>

            <button
              type="button"
              onClick={() => setIsMasked(!isMasked)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0B1120] border border-[#23334A] text-[#94A3B8] hover:text-[#E5EDF7] hover:border-[#06B6D4] transition"
            >
              {isMasked ? (
                <>
                  <Eye className="w-3.5 h-3.5 text-[#06B6D4]" />
                  <span>Show ID Digits</span>
                </>
              ) : (
                <>
                  <EyeOff className="w-3.5 h-3.5 text-[#F59E0B]" />
                  <span>Mask ID Digits</span>
                </>
              )}
            </button>
          </div>

          {/* Visual Images Display */}
          <div className="space-y-3">
            {viewMode === 'side-by-side' ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="bg-[#0B1120] border border-[#23334A] rounded-xl p-2">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-[#94A3B8] mb-1.5 text-center">
                    Original ID Scan
                  </p>
                  <div className="h-48 sm:h-56 flex items-center justify-center overflow-hidden rounded-lg bg-black">
                    {originalImg ? (
                      <img
                        src={originalImg}
                        alt="Original"
                        style={{ transform: `rotate(${rotation}deg)` }}
                        className="max-h-full max-w-full object-contain transition-transform duration-200"
                      />
                    ) : (
                      <div className="text-center text-[#94A3B8] text-xs">No scan image available</div>
                    )}
                  </div>
                </div>

                <div className="bg-[#0B1120] border border-[#23334A] rounded-xl p-2">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-[#94A3B8] mb-1.5 text-center">
                    Tamper Heatmap (ELA)
                  </p>
                  <div className="h-48 sm:h-56 flex items-center justify-center overflow-hidden rounded-lg bg-black">
                    {elaImg ? (
                      <img
                        src={elaImg}
                        alt="Tamper Heatmap"
                        style={{ transform: `rotate(${rotation}deg)` }}
                        className="max-h-full max-w-full object-contain transition-transform duration-200"
                      />
                    ) : (
                      <div className="text-center text-[#94A3B8] text-xs">Tamper heatmap not generated</div>
                    )}
                  </div>
                </div>
              </div>
            ) : viewMode === 'original' ? (
              <div className="bg-[#0B1120] border border-[#23334A] rounded-xl p-3">
                <p className="text-xs font-bold text-[#94A3B8] mb-2">Original Document Scan</p>
                <div className="h-72 flex items-center justify-center overflow-hidden rounded-lg bg-black">
                  {originalImg ? (
                    <img
                      src={originalImg}
                      alt="Original"
                      style={{ transform: `rotate(${rotation}deg)` }}
                      className="max-h-full max-w-full object-contain transition-transform duration-200"
                    />
                  ) : (
                    <div className="text-center text-[#94A3B8] text-xs">No scan image available</div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-[#0B1120] border border-[#23334A] rounded-xl p-3">
                <p className="text-xs font-bold text-[#94A3B8] mb-2">
                  Tamper Heatmap (Bright glows indicate digital editing)
                </p>
                <div className="h-72 flex items-center justify-center overflow-hidden rounded-lg bg-black">
                  {elaImg ? (
                    <img
                      src={elaImg}
                      alt="Tamper Heatmap"
                      style={{ transform: `rotate(${rotation}deg)` }}
                      className="max-h-full max-w-full object-contain transition-transform duration-200"
                    />
                  ) : (
                    <div className="text-center text-[#94A3B8] text-xs">Tamper heatmap not generated</div>
                  )}
                </div>
              </div>
            )}
          </div>

          <p className="text-[11px] text-[#94A3B8] italic text-center">
            Tip: Bright, glowing patches on the Tamper Heatmap highlight spliced text or edited pixels.
          </p>
        </div>

        {/* Right Column (6 cols): 4 Core Forensic Checks & Extracted Data */}
        <div className="lg:col-span-6 space-y-4">

          {/* 4 Core Forensic Checks Card */}
          <div className="bg-[#151F32] border border-[#23334A] rounded-2xl p-5 shadow-sm">
            <h3 className="text-xs sm:text-sm font-bold text-[#E5EDF7] mb-3 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-[#06B6D4]" />
              AI Forensic Checks Breakdown
            </h3>

            <div className="space-y-2.5">

              {/* Check 1: Tampering & Splicing */}
              <div className="p-3 rounded-xl bg-[#0B1120] border border-[#23334A] flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold text-[#E5EDF7]">1. Digital Tamper & Splicing</p>
                  <p className="text-[11px] text-[#94A3B8]">
                    {isTampered
                      ? tamperIssues.map(i => i.title).join(", ")
                      : "Uniform compression levels (No digital splicing found)"}
                  </p>
                </div>
                <span className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${
                  isTampered
                    ? "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30"
                    : "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30"
                }`}>
                  {isTampered ? "TAMPERED" : "PASS"}
                </span>
              </div>

              {/* Check 2: Checksum & Format Validation */}
              <div className="p-3 rounded-xl bg-[#0B1120] border border-[#23334A] flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold text-[#E5EDF7]">2. Document Number & Checksum</p>
                  <p className="text-[11px] text-[#94A3B8]">
                    {isFormatValid
                      ? "Passed official mathematical algorithm & layout check"
                      : (formatIssues.length > 0 ? formatIssues[0].title : "Failed number pattern or checksum")}
                  </p>
                </div>
                <span className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${
                  isFormatValid
                    ? "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30"
                    : "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30"
                }`}>
                  {isFormatValid ? "VALID" : "INVALID"}
                </span>
              </div>

              {/* Check 3: Image Quality & Glare */}
              <div className="p-3 rounded-xl bg-[#0B1120] border border-[#23334A] flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold text-[#E5EDF7]">3. Image Quality & Focus</p>
                  <p className="text-[11px] text-[#94A3B8]">
                    {hasQualityDefects
                      ? qualityIssues.map(i => i.title).join(", ")
                      : "Sharp focus, balanced lighting, no heavy glare"}
                  </p>
                </div>
                <span className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${
                  hasQualityDefects
                    ? "bg-[#F59E0B]/15 text-[#F59E0B] border-[#F59E0B]/30"
                    : "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30"
                }`}>
                  {hasQualityDefects ? "DEFECTS" : "CLEAR"}
                </span>
              </div>

              {/* Check 4: Portrait & Face */}
              <div className="p-3 rounded-xl bg-[#0B1120] border border-[#23334A] flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold text-[#E5EDF7]">4. Face Portrait Verification</p>
                  <p className="text-[11px] text-[#94A3B8]">
                    {faceOk
                      ? "Photo present and verified on ID document"
                      : (faceIssues[0]?.title || "Face photo missing or obscured")}
                  </p>
                </div>
                <span className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${
                  faceOk
                    ? "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30"
                    : "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30"
                }`}>
                  {faceOk ? "PASS" : "FAIL"}
                </span>
              </div>

            </div>
          </div>

          {/* Extracted Details Card */}
          <div className="bg-[#151F32] border border-[#23334A] rounded-2xl p-5 shadow-sm">
            <h3 className="text-xs sm:text-sm font-bold text-[#E5EDF7] mb-3 flex items-center gap-2">
              <FileCheck className="w-4 h-4 text-[#06B6D4]" />
              Extracted Document Details
            </h3>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1.5 border-b border-[#23334A]">
                <span className="text-[#94A3B8]">Document Type:</span>
                <span className="font-bold text-[#E5EDF7]">{result.document_type || 'Unknown'}</span>
              </div>

              <div className="flex justify-between py-1.5 border-b border-[#23334A]">
                <span className="text-[#94A3B8]">Document Number:</span>
                <span className="font-mono font-bold text-[#06B6D4]">
                  {isMasked ? maskedNumber : rawNumber}
                </span>
              </div>

              {details.full_name && (
                <div className="flex justify-between py-1.5 border-b border-[#23334A]">
                  <span className="text-[#94A3B8]">Holder Name:</span>
                  <span className="font-semibold text-[#E5EDF7]">{details.full_name}</span>
                </div>
              )}

              {details.dob && (
                <div className="flex justify-between py-1.5 border-b border-[#23334A]">
                  <span className="text-[#94A3B8]">Date of Birth:</span>
                  <span className="font-semibold text-[#E5EDF7]">{details.dob}</span>
                </div>
              )}

              {/* Cross-check status if available */}
              {crossChecks.name_match !== undefined && crossChecks.name_match !== null && (
                <div className="flex justify-between py-1.5 border-b border-[#23334A]">
                  <span className="text-[#94A3B8]">Name Cross-Check:</span>
                  <span className={`font-bold ${crossChecks.name_match ? 'text-[#22C55E]' : 'text-[#EF4444]'}`}>
                    {crossChecks.name_match ? 'MATCH' : 'MISMATCH'}
                  </span>
                </div>
              )}
            </div>
          </div>

        </div>

      </div>

      {/* Action Buttons Bar */}
      <div className="bg-[#151F32] border border-[#23334A] rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-md">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onScreenAnother}
            className="px-5 py-2.5 bg-[#06B6D4] hover:bg-[#0891B2] text-[#0B1120] font-black rounded-xl text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition active:scale-[0.99]"
          >
            <RotateCcw className="w-4 h-4 stroke-[2.5]" />
            Verify Another Document
          </button>

          <button
            type="button"
            onClick={handlePrint}
            className="px-4 py-2.5 bg-[#0B1120] border border-[#23334A] hover:border-[#06B6D4] text-[#E5EDF7] rounded-xl text-xs sm:text-sm font-semibold flex items-center gap-2 transition"
          >
            <Printer className="w-4 h-4 text-[#06B6D4]" />
            Print Report
          </button>
        </div>

        <button
          type="button"
          onClick={onDeleteDocument}
          className="px-4 py-2.5 bg-[#0B1120] border border-[#EF4444]/40 hover:bg-[#EF4444]/10 text-[#EF4444] rounded-xl text-xs sm:text-sm font-semibold flex items-center gap-2 transition"
        >
          <Trash2 className="w-4 h-4" />
          Delete Record
        </button>
      </div>

    </div>
  );
}
