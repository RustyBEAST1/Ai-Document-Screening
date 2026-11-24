import React, { useState, useRef, useEffect } from 'react';
import {
  UploadCloud,
  FileText,
  X,
  ChevronDown,
  ChevronRight,
  ShieldCheck,
  Camera,
  RotateCw,
  Clipboard,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Play
} from 'lucide-react';

const SUPPORTED_DOCUMENTS = [
  "Aadhaar Card",
  "PAN Card",
  "Driving Licence",
  "Voter ID Card",
  "Passport"
];

const SAMPLE_DOCS = [
  // 1. Aadhaar Card
  {
    id: "sample-aadhaar-clean",
    label: "Clean Aadhaar Card",
    tag: "Authentic",
    type: "Aadhaar Card",
    badgeColor: "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30",
    desc: "Valid 12-digit number passing Verhoeff checksum with original layout."
  },
  {
    id: "sample-aadhaar-tampered",
    label: "Tampered Aadhaar",
    tag: "Fraudulent",
    type: "Aadhaar Card",
    badgeColor: "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30",
    desc: "Spliced number with noise artifacts failing mathematical Verhoeff check."
  },
  // 2. PAN Card
  {
    id: "sample-pan-clean",
    label: "Clean PAN Card",
    tag: "Authentic",
    type: "PAN Card",
    badgeColor: "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30",
    desc: "Valid 10-char format with 4th char 'P' (Individual) and official headers."
  },
  {
    id: "sample-pan-tampered",
    label: "Tampered PAN Card",
    tag: "Fraudulent",
    type: "PAN Card",
    badgeColor: "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30",
    desc: "Edited Date of Birth with digital tampering and invalid entity code 'X'."
  },
  // 3. Driving Licence
  {
    id: "sample-dl-clean",
    label: "Clean Driving Licence",
    tag: "Authentic",
    type: "Driving Licence",
    badgeColor: "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30",
    desc: "Valid Sarathi RTO format (DL04 2021) with sharp portrait and chip graphic."
  },
  {
    id: "sample-dl-blurry",
    label: "Blurry Driving Licence",
    tag: "Suspicious",
    type: "Driving Licence",
    badgeColor: "bg-[#F59E0B]/15 text-[#F59E0B] border-[#F59E0B]/30",
    desc: "Poor camera focus and flash glare preventing reliable validation."
  },
  // 4. Voter ID Card
  {
    id: "sample-voter-clean",
    label: "Clean Voter ID",
    tag: "Authentic",
    type: "Voter ID Card",
    badgeColor: "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30",
    desc: "Valid ECI EPIC format (3 letters + 7 digits) with official headers."
  },
  {
    id: "sample-voter-tampered",
    label: "Irregular Voter ID",
    tag: "Fraudulent",
    type: "Voter ID Card",
    badgeColor: "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30",
    desc: "Non-standard EPIC format (VTR9874X2) and spliced photo box seam."
  },
  // 5. Passport
  {
    id: "sample-passport-clean",
    label: "Clean Passport",
    tag: "Authentic",
    type: "Passport",
    badgeColor: "bg-[#22C55E]/15 text-[#22C55E] border-[#22C55E]/30",
    desc: "Valid Republic of India passport with 2-line ICAO Doc 9303 MRZ."
  },
  {
    id: "sample-passport-mismatch",
    label: "Fake Passport",
    tag: "Fraudulent",
    type: "Passport",
    badgeColor: "bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30",
    desc: "Missing portrait photo and failing ICAO Doc 9303 MRZ checksum."
  }
];

export default function UploadScreen({ onStartScreening, onSelectSample }) {
  const [docType, setDocType] = useState("");
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showCrossCheck, setShowCrossCheck] = useState(false);
  const [crossCheck, setCrossCheck] = useState({ name: "", dob: "", docNumber: "" });
  const [pasteNotice, setPasteNotice] = useState(false);

  // Camera State
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [cameraError, setCameraError] = useState(null);

  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  // Generate preview URL when file changes
  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    if (file.type && file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setPreviewUrl(null);
    }
  }, [file]);

  // Global Clipboard Paste Listener (Ctrl+V)
  useEffect(() => {
    const handlePaste = (e) => {
      if (e.clipboardData && e.clipboardData.items) {
        for (let item of e.clipboardData.items) {
          if (item.type.startsWith("image/")) {
            const pastedFile = item.getAsFile();
            if (pastedFile) {
              setFile(pastedFile);
              setPasteNotice(true);
              setTimeout(() => setPasteNotice(false), 3500);
              break;
            }
          }
        }
      }
    };
    window.addEventListener("paste", handlePaste);
    return () => window.removeEventListener("paste", handlePaste);
  }, []);

  const handleFile = (f) => {
    if (f) setFile(f);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  // Rotate Image 90 degrees
  const handleRotateImage = () => {
    if (!file || !previewUrl) return;
    const img = new Image();
    img.src = previewUrl;
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = img.height;
      canvas.height = img.width;
      const ctx = canvas.getContext("2d");
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.rotate((90 * Math.PI) / 180);
      ctx.drawImage(img, -img.width / 2, -img.height / 2);

      canvas.toBlob((blob) => {
        if (blob) {
          const rotatedFile = new File([blob], file.name || "rotated_id.jpg", {
            type: file.type || "image/jpeg"
          });
          setFile(rotatedFile);
        }
      }, file.type || "image/jpeg", 0.95);
    };
  };

  // Start Camera
  const openCamera = async () => {
    setIsCameraOpen(true);
    setCameraError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 1920 }, height: { ideal: 1080 } }
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      setCameraError("Camera unavailable or permission denied: " + err.message);
    }
  };

  // Close Camera
  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
  };

  // Capture Photo
  const capturePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        const photoFile = new File([blob], `camera_scan_${Date.now()}.jpg`, { type: "image/jpeg" });
        setFile(photoFile);
        closeCamera();
      }
    }, "image/jpeg", 0.95);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!docType || !file) return;
    onStartScreening({
      file,
      documentType: docType,
      ...crossCheck
    });
  };

  const handleSampleClick = (sample) => {
    setDocType(sample.type);
    onSelectSample(sample.id, sample.type, crossCheck);
  };

  const isValid = Boolean(docType && file);

  return (
    <div className="space-y-6">

      {/* Clipboard Paste Banner */}
      {pasteNotice && (
        <div className="p-3 bg-[#06B6D4]/15 border border-[#06B6D4]/40 rounded-xl text-[#06B6D4] text-xs font-semibold flex items-center gap-2">
          <Clipboard className="w-4 h-4" />
          Document image captured from clipboard (Ctrl+V)!
        </div>
      )}

      {/* Main Scanner Card */}
      <div className="bg-[#151F32] border border-[#23334A] rounded-2xl shadow-xl p-5 sm:p-7">
        
        <div className="flex items-center justify-between pb-5 border-b border-[#23334A] mb-6">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#06B6D4]/15 border border-[#06B6D4]/30 flex items-center justify-center text-[#06B6D4]">
              <UploadCloud className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-bold text-[#E5EDF7]">
                Document Scanner & Analysis
              </h2>
              <p className="text-xs text-[#94A3B8]">
                Instant fraud, tampering, and checksum verification
              </p>
            </div>
          </div>
          <span className="hidden sm:inline-flex text-[11px] font-semibold text-[#94A3B8] px-2.5 py-1 bg-[#0B1120] border border-[#23334A] rounded-full">
            5 Indian ID Types
          </span>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Step 1: Document Type */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs sm:text-sm font-bold text-[#E5EDF7] flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#06B6D4]/20 text-[#06B6D4] flex items-center justify-center text-[11px] font-black">
                  1
                </span>
                Select Document Type <span className="text-[#EF4444]">*</span>
              </label>
              <span className="text-[11px] text-[#94A3B8]">Required</span>
            </div>

            <div className="relative">
              <select
                value={docType}
                onChange={(e) => setDocType(e.target.value)}
                className="w-full px-4 py-3 bg-[#0B1120] border border-[#23334A] rounded-xl text-[#E5EDF7] text-sm font-medium focus:outline-none focus:border-[#06B6D4] focus:ring-1 focus:ring-[#06B6D4] appearance-none cursor-pointer transition"
              >
                <option value="" disabled className="text-[#94A3B8]">
                  Choose document type to verify...
                </option>
                {SUPPORTED_DOCUMENTS.map((d) => (
                  <option key={d} value={d} className="bg-[#151F32] text-[#E5EDF7]">
                    {d}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-[#94A3B8] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>

          {/* Step 2: Upload Area */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs sm:text-sm font-bold text-[#E5EDF7] flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#06B6D4]/20 text-[#06B6D4] flex items-center justify-center text-[11px] font-black">
                  2
                </span>
                Upload Document Scan or Photo <span className="text-[#EF4444]">*</span>
              </label>
              <span className="text-[11px] text-[#94A3B8]">Ctrl+V to paste</span>
            </div>

            {!file ? (
              <div
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
                onDragLeave={() => setIsDragOver(false)}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-2xl p-6 sm:p-8 text-center cursor-pointer transition-all ${
                  isDragOver
                    ? "border-[#06B6D4] bg-[#06B6D4]/10"
                    : "border-[#23334A] bg-[#0B1120]/70 hover:border-[#06B6D4]/50 hover:bg-[#0B1120]"
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*,.pdf"
                  className="hidden"
                  onChange={(e) => e.target.files && handleFile(e.target.files[0])}
                />

                <div className="w-14 h-14 mx-auto mb-3 bg-[#06B6D4]/10 text-[#06B6D4] border border-[#06B6D4]/20 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/10">
                  <UploadCloud className="w-7 h-7" />
                </div>

                <p className="text-sm sm:text-base font-bold text-[#E5EDF7] mb-1">
                  Click to choose file or drag & drop here
                </p>

                <p className="text-xs text-[#94A3B8] max-w-sm mx-auto mb-4">
                  Accepts JPG, PNG, WEBP or PDF. Make sure all corners and text are clear.
                </p>

                {/* Camera Button */}
                <div className="flex items-center justify-center gap-3">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      openCamera();
                    }}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-[#151F32] border border-[#23334A] hover:border-[#06B6D4] hover:text-[#06B6D4] rounded-xl text-xs font-semibold text-[#E5EDF7] transition"
                  >
                    <Camera className="w-4 h-4 text-[#06B6D4]" />
                    Use Camera
                  </button>
                </div>
              </div>
            ) : (
              <div className="p-4 bg-[#0B1120] border border-[#23334A] rounded-2xl space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-center gap-3 overflow-hidden">
                    {previewUrl ? (
                      <div className="relative w-16 h-12 bg-black rounded-lg overflow-hidden flex-shrink-0 border border-[#23334A]">
                        <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
                      </div>
                    ) : (
                      <div className="w-12 h-12 bg-[#06B6D4]/15 text-[#06B6D4] rounded-lg flex items-center justify-center flex-shrink-0">
                        <FileText className="w-6 h-6" />
                      </div>
                    )}
                    <div className="overflow-hidden">
                      <p className="text-sm font-bold text-[#E5EDF7] truncate">{file.name}</p>
                      <p className="text-xs text-[#94A3B8]">
                        {(file.size / (1024 * 1024)).toFixed(2)} MB • Ready to verify
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {previewUrl && (
                      <button
                        type="button"
                        onClick={handleRotateImage}
                        className="px-3 py-1.5 bg-[#151F32] border border-[#23334A] hover:border-[#06B6D4] rounded-lg text-xs font-semibold text-[#E5EDF7] flex items-center gap-1.5 transition"
                      >
                        <RotateCw className="w-3.5 h-3.5 text-[#06B6D4]" />
                        Rotate 90°
                      </button>
                    )}

                    <button
                      type="button"
                      onClick={() => setFile(null)}
                      className="px-3 py-1.5 bg-[#151F32] border border-[#EF4444]/40 hover:bg-[#EF4444]/10 text-[#EF4444] rounded-lg text-xs font-semibold flex items-center gap-1 transition"
                    >
                      <X className="w-3.5 h-3.5" />
                      Remove
                    </button>
                  </div>
                </div>

                {previewUrl && (
                  <div className="w-full bg-[#070B14] rounded-xl overflow-hidden max-h-56 flex items-center justify-center p-2 border border-[#23334A]">
                    <img src={previewUrl} alt="Preview" className="max-h-52 max-w-full object-contain rounded" />
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Optional Cross-Check Drawer */}
          <div className="pt-1">
            <button
              type="button"
              onClick={() => setShowCrossCheck(!showCrossCheck)}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-[#06B6D4] hover:text-[#22D3EE] transition"
            >
              <ChevronRight className={`w-3.5 h-3.5 transition-transform ${showCrossCheck ? "rotate-90" : ""}`} />
              Optional: Enter Person Details to Cross-Check
            </button>

            {showCrossCheck && (
              <div className="mt-3 p-4 bg-[#0B1120] border border-[#23334A] rounded-xl grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-[#94A3B8] mb-1">Holder Name</label>
                  <input
                    type="text"
                    placeholder="e.g. Arun Kumar"
                    value={crossCheck.name}
                    onChange={(e) => setCrossCheck({ ...crossCheck, name: e.target.value })}
                    className="w-full px-3 py-2 text-xs bg-[#151F32] border border-[#23334A] rounded-lg text-[#E5EDF7] focus:outline-none focus:border-[#06B6D4]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#94A3B8] mb-1">Date of Birth</label>
                  <input
                    type="text"
                    placeholder="DD/MM/YYYY"
                    value={crossCheck.dob}
                    onChange={(e) => setCrossCheck({ ...crossCheck, dob: e.target.value })}
                    className="w-full px-3 py-2 text-xs bg-[#151F32] border border-[#23334A] rounded-lg text-[#E5EDF7] focus:outline-none focus:border-[#06B6D4]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#94A3B8] mb-1">Document Number</label>
                  <input
                    type="text"
                    placeholder="e.g. Aadhaar / PAN / DL / Passport"
                    value={crossCheck.docNumber}
                    onChange={(e) => setCrossCheck({ ...crossCheck, docNumber: e.target.value })}
                    className="w-full px-3 py-2 text-xs bg-[#151F32] border border-[#23334A] rounded-lg text-[#E5EDF7] focus:outline-none focus:border-[#06B6D4]"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Primary Submit Button */}
          <button
            type="submit"
            disabled={!isValid}
            className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm sm:text-base flex items-center justify-center gap-2.5 transition-all ${
              isValid
                ? "bg-[#06B6D4] hover:bg-[#0891B2] text-[#0B1120] font-black cursor-pointer shadow-lg shadow-cyan-500/25 active:scale-[0.99]"
                : "bg-[#23334A] text-[#94A3B8]/60 cursor-not-allowed"
            }`}
          >
            <ShieldCheck className="w-5 h-5 stroke-[2.5]" />
            Verify Document
          </button>

        </form>
      </div>

      {/* 1-Click Interactive Test Samples */}
      <div className="bg-[#151F32] border border-[#23334A] rounded-2xl p-5 sm:p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="w-4 h-4 text-[#06B6D4]" />
          <h3 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-[#E5EDF7]">
            Quick Test Cases (1-Click Demo)
          </h3>
        </div>
        <p className="text-xs text-[#94A3B8] mb-4">
          Click any card to instantly test genuine passes and fraud detection algorithms:
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {SAMPLE_DOCS.map((s) => (
            <div
              key={s.id}
              onClick={() => handleSampleClick(s)}
              className="p-3.5 bg-[#0B1120] border border-[#23334A] hover:border-[#06B6D4]/60 rounded-xl cursor-pointer transition flex flex-col justify-between hover:bg-[#1A263D] group"
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-1.5">
                  <span className="text-[10px] text-[#06B6D4] font-semibold uppercase tracking-wider">
                    {s.type.replace(" Card", "")}
                  </span>
                  <span className={`text-[10px] font-extrabold px-1.5 py-0.5 rounded-full border ${s.badgeColor}`}>
                    {s.tag}
                  </span>
                </div>
                <h4 className="text-xs sm:text-sm font-bold text-[#E5EDF7] group-hover:text-[#06B6D4] transition mb-1">
                  {s.label}
                </h4>
                <p className="text-[11px] text-[#94A3B8] leading-snug">
                  {s.desc}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-[#23334A] flex items-center justify-between text-[11px] text-[#06B6D4] font-semibold">
                <span>Run Test</span>
                <Play className="w-3 h-3 fill-current" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Web Camera Modal */}
      {isCameraOpen && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#151F32] border border-[#23334A] rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl flex flex-col">
            <div className="px-5 py-3.5 border-b border-[#23334A] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Camera className="w-4 h-4 text-[#06B6D4]" />
                <h4 className="text-sm font-bold text-[#E5EDF7]">Capture Document Photo</h4>
              </div>
              <button onClick={closeCamera} className="p-1 text-[#94A3B8] hover:text-[#E5EDF7] rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 bg-black relative flex items-center justify-center min-h-[300px]">
              {cameraError ? (
                <div className="p-4 text-center text-[#EF4444] text-xs">
                  <AlertTriangle className="w-8 h-8 mx-auto mb-2" />
                  {cameraError}
                </div>
              ) : (
                <>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    className="w-full max-h-[360px] object-cover rounded-xl"
                  />
                  <div className="absolute inset-8 border-2 border-dashed border-[#06B6D4]/60 rounded-xl pointer-events-none flex items-center justify-center">
                    <span className="text-[11px] text-[#06B6D4] bg-[#0B1120]/80 px-2 py-0.5 rounded font-mono">
                      Align ID inside frame
                    </span>
                  </div>
                </>
              )}
            </div>

            <div className="p-4 border-t border-[#23334A] flex items-center justify-between gap-3">
              <button
                type="button"
                onClick={closeCamera}
                className="px-4 py-2 bg-[#0B1120] border border-[#23334A] text-[#94A3B8] hover:text-[#E5EDF7] rounded-xl text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={capturePhoto}
                disabled={Boolean(cameraError)}
                className="px-5 py-2.5 bg-[#06B6D4] hover:bg-[#0891B2] text-[#0B1120] rounded-xl text-xs font-black flex items-center gap-2 shadow-lg shadow-cyan-500/20 disabled:opacity-50"
              >
                <Camera className="w-4 h-4 stroke-[2.5]" />
                Capture Photo
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
