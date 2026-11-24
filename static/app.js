// AI Fake Identity & Document Screening System - Frontend Controller

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const documentTypeSelect = document.getElementById("documentTypeSelect");
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const filePreviewBar = document.getElementById("filePreviewBar");
  const selectedFileName = document.getElementById("selectedFileName");
  const selectedFileSize = document.getElementById("selectedFileSize");
  const btnRemoveFile = document.getElementById("btnRemoveFile");
  const btnStartScreening = document.getElementById("btnStartScreening");

  // Optional Cross-Check
  const toggleCrossCheck = document.getElementById("toggleCrossCheck");
  const crossCheckPanel = document.getElementById("crossCheckPanel");
  const crossCheckIcon = document.getElementById("crossCheckIcon");
  const inputName = document.getElementById("inputName");
  const inputDob = document.getElementById("inputDob");
  const inputDocNumber = document.getElementById("inputDocNumber");

  // Sample Buttons
  const sampleChips = document.querySelectorAll(".sample-chip");

  // Sections
  const uploadSection = document.getElementById("uploadSection");
  const scannerSection = document.getElementById("scannerSection");
  const scannerStatusText = document.getElementById("scannerStatusText");
  const scannerStepText = document.getElementById("scannerStepText");
  const resultSection = document.getElementById("resultSection");

  // Result Elements
  const resultBanner = document.getElementById("resultBanner");
  const resRiskLevel = document.getElementById("resRiskLevel");
  const resShortMessage = document.getElementById("resShortMessage");
  const resConfidence = document.getElementById("resConfidence");
  const resDocType = document.getElementById("resDocType");
  const resRiskScore = document.getElementById("resRiskScore");
  const gaugeFill = document.getElementById("gaugeFill");
  const resRecommendation = document.getElementById("resRecommendation");
  const resIssuesCount = document.getElementById("resIssuesCount");
  const resIssuesList = document.getElementById("resIssuesList");

  // Details Table
  const tdDocType = document.getElementById("tdDocType");
  const tdDocNumber = document.getElementById("tdDocNumber");
  const btnToggleMask = document.getElementById("btnToggleMask");
  const tdName = document.getElementById("tdName");
  const tdDob = document.getElementById("tdDob");
  const tdGender = document.getElementById("tdGender");
  const tdFormatNotes = document.getElementById("tdFormatNotes");
  const tdSecurityFeatures = document.getElementById("tdSecurityFeatures");

  // Previews
  const tabOriginal = document.getElementById("tabOriginal");
  const tabEla = document.getElementById("tabEla");
  const imgDocumentPreview = document.getElementById("imgDocumentPreview");
  const imgElaPreview = document.getElementById("imgElaPreview");
  const viewHelpText = document.getElementById("viewHelpText");

  // Actions
  const btnScreenAnother = document.getElementById("btnScreenAnother");
  const btnDeleteDocument = document.getElementById("btnDeleteDocument");

  // History Modal
  const btnOpenHistory = document.getElementById("btnOpenHistory");
  const btnCloseHistory = document.getElementById("btnCloseHistory");
  const historyModal = document.getElementById("historyModal");
  const historyList = document.getElementById("historyList");

  // State
  let currentFile = null;
  let activeSampleId = null;
  let currentScreeningResult = null;
  let isNumberMasked = true;

  // 1. File Selection & Drag-and-Drop
  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  function handleFileSelected(file) {
    currentFile = file;
    activeSampleId = null;
    selectedFileName.textContent = file.name;
    selectedFileSize.textContent = formatBytes(file.size);
    filePreviewBar.style.display = "flex";
    dropzone.style.display = "none";
    validateForm();
  }

  btnRemoveFile.addEventListener("click", (e) => {
    e.stopPropagation();
    currentFile = null;
    activeSampleId = null;
    fileInput.value = "";
    filePreviewBar.style.display = "none";
    dropzone.style.display = "block";
    validateForm();
  });

  // 2. Document Type Change
  documentTypeSelect.addEventListener("change", () => {
    validateForm();
  });

  function validateForm() {
    const hasDocType = Boolean(documentTypeSelect.value);
    const hasFile = Boolean(currentFile || activeSampleId);
    btnStartScreening.disabled = !(hasDocType && hasFile);
  }

  // 3. Optional Cross-Check Accordion
  toggleCrossCheck.addEventListener("click", () => {
    const isOpen = crossCheckPanel.classList.toggle("open");
    crossCheckIcon.style.transform = isOpen ? "rotate(90deg)" : "rotate(0deg)";
  });

  // 4. One-Click Sample Document Selector
  sampleChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const sampleId = chip.getAttribute("data-sample");
      activeSampleId = sampleId;
      currentFile = null;

      // Auto-set the document type for the selected sample
      if (sampleId.includes("aadhaar")) {
        documentTypeSelect.value = "Aadhaar Card";
      } else if (sampleId.includes("pan")) {
        documentTypeSelect.value = "PAN Card";
      } else if (sampleId.includes("dl")) {
        documentTypeSelect.value = "Driving Licence";
      } else if (sampleId.includes("passport")) {
        documentTypeSelect.value = "Passport";
      }

      selectedFileName.textContent = `Pre-loaded Sample (${chip.querySelector("span").textContent})`;
      selectedFileSize.textContent = "Test Data";
      filePreviewBar.style.display = "flex";
      dropzone.style.display = "none";
      validateForm();

      // Trigger screening directly
      startScreeningFlow();
    });
  });

  // 5. Start Screening Flow
  btnStartScreening.addEventListener("click", startScreeningFlow);

  async function startScreeningFlow() {
    const docType = documentTypeSelect.value;
    if (!docType || (!currentFile && !activeSampleId)) {
      alert("Please select a document type and upload a document.");
      return;
    }

    // Switch to scanner animation
    uploadSection.style.display = "none";
    resultSection.style.display = "none";
    scannerSection.style.display = "block";

    // Animated scanner steps
    const steps = [
      { status: "Analyzing Document Quality...", step: "Inspecting resolution, focus sharpness, glare, and shadows..." },
      { status: "Executing Forensic Forensics...", step: "Running Error Level Analysis (ELA) for digital splicing..." },
      { status: "Inspecting Photo & Security Borders...", step: "Detecting facial biometric zone and boundary seams..." },
      { status: "Extracting OCR Text & Formats...", step: "Validating checksum algorithms, MRZ syntax, and official keywords..." },
      { status: "Synthesizing Risk Score...", step: "Finalizing risk evaluation and actionable recommendations..." }
    ];

    let stepIndex = 0;
    const interval = setInterval(() => {
      stepIndex++;
      if (stepIndex < steps.length) {
        scannerStatusText.textContent = steps[stepIndex].status;
        scannerStepText.textContent = steps[stepIndex].step;
      }
    }, 450);

    try {
      let data;
      const uName = inputName.value.trim();
      const uDob = inputDob.value.trim();
      const uDocNo = inputDocNumber.value.trim();

      if (activeSampleId) {
        // Query sample endpoint
        const params = new URLSearchParams();
        if (uName) params.append("user_name", uName);
        if (uDob) params.append("user_dob", uDob);
        if (uDocNo) params.append("user_number", uDocNo);
        const queryStr = params.toString() ? `?${params.toString()}` : "";

        const res = await fetch(`/api/screen-sample/${activeSampleId}${queryStr}`, {
          method: "POST"
        });
        if (!res.ok) {
          let errText = "Failed to screen sample document.";
          try {
            const errData = await res.json();
            errText = errData.detail || errText;
          } catch (_) {
            errText = `Backend connection failed (HTTP ${res.status}). Please ensure 'python run.py' is running on port 8000.`;
          }
          throw new Error(errText);
        }
        data = await res.json();
      } else {
        // Multipart upload
        const formData = new FormData();
        formData.append("file", currentFile);
        formData.append("document_type", docType);
        if (uName) formData.append("user_name", uName);
        if (uDob) formData.append("user_dob", uDob);
        if (uDocNo) formData.append("user_number", uDocNo);

        const res = await fetch("/api/screen", {
          method: "POST",
          body: formData
        });
        if (!res.ok) {
          let errText = "Document screening failed.";
          try {
            const errData = await res.json();
            errText = errData.detail || errText;
          } catch (_) {
            errText = `Backend connection failed (HTTP ${res.status}). Please ensure 'python run.py' is running on port 8000.`;
          }
          throw new Error(errText);
        }
        data = await res.json();
      }

      clearInterval(interval);
      setTimeout(() => {
        renderScreeningResults(data);
      }, 500);

    } catch (err) {
      clearInterval(interval);
      alert("Error: " + err.message);
      scannerSection.style.display = "none";
      uploadSection.style.display = "block";
    }
  }

  // 6. Render Results Screen
  function renderScreeningResults(data) {
    currentScreeningResult = data;
    scannerSection.style.display = "none";
    resultSection.style.display = "block";

    const risk = (data.risk_level || "low").toLowerCase();
    const score = data.risk_score || 0;

    // Banner styling
    resultBanner.className = `result-banner risk-${risk}`;
    resRiskLevel.textContent = `${data.risk_level} Risk`;
    resShortMessage.textContent = data.short_message;
    resConfidence.textContent = `${data.confidence}%`;
    resDocType.textContent = data.document_type;
    resRiskScore.textContent = score;

    // Gauge circle stroke animation
    // Radius 40 -> circumference = 2 * PI * 40 ≈ 251.2
    const circumference = 251.2;
    const offset = circumference - (score / 100) * circumference;
    gaugeFill.style.strokeDashoffset = offset;

    if (risk === "low") {
      gaugeFill.style.stroke = "#10b981";
    } else if (risk === "medium") {
      gaugeFill.style.stroke = "#f59e0b";
    } else {
      gaugeFill.style.stroke = "#ef4444";
    }

    // Recommendation card
    resRecommendation.textContent = data.recommendation;

    // Detected Issues List
    resIssuesCount.textContent = (data.issues || []).length;
    resIssuesList.innerHTML = "";

    if (!data.issues || data.issues.length === 0) {
      resIssuesList.innerHTML = `
        <div style="text-align: center; padding: 24px 12px; color: #10b981;">
          <p style="font-weight: 700; font-size: 1.05rem;">No Suspicious Anomalies Detected</p>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">
            The document passed all tamper, blur, glare, and mathematical checksum screenings.
          </p>
        </div>
      `;
    } else {
      data.issues.forEach((iss) => {
        const item = document.createElement("div");
        const sev = (iss.severity || "info").toLowerCase();
        item.className = `issue-item sev-${sev}`;
        item.innerHTML = `
          <div style="flex: 1;">
            <div class="issue-header">
              <span class="issue-badge badge-${sev}">${sev}</span>
              <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">[${iss.category || "General"}]</span>
              <h4 class="issue-title">${escapeHtml(iss.title)}</h4>
            </div>
            <p class="issue-desc">${escapeHtml(iss.description)}</p>
          </div>
        `;
        resIssuesList.appendChild(item);
      });
    }

    // Extracted Details
    const details = data.extracted_details || {};
    tdDocType.textContent = data.document_type;
    
    isNumberMasked = true;
    updateMaskedNumberDisplay(details.document_number_masked, details.document_number_raw);

    tdName.textContent = details.full_name || "Not extracted";
    tdDob.textContent = details.dob || "Not extracted";
    tdGender.textContent = details.gender || "N/A";
    tdFormatNotes.textContent = details.format_notes || (details.format_valid ? "Valid Syntax" : "Format Discrepancy");

    const securityItems = [];
    if (details.qr_detected) securityItems.push("QR Scanned");
    if (details.mrz_detected) securityItems.push("MRZ Detected");
    if (details.detected_keywords && details.detected_keywords.length > 0) {
      securityItems.push(`${details.detected_keywords.length} Official Headers`);
    }
    tdSecurityFeatures.textContent = securityItems.length > 0 ? securityItems.join(" • ") : "No special features verified";

    // Previews & ELA
    if (data.preview_url) {
      imgDocumentPreview.src = data.preview_url;
      imgDocumentPreview.style.display = "block";
    }
    if (data.ela_url) {
      imgElaPreview.src = data.ela_url;
      tabEla.style.display = "inline-block";
    } else {
      tabEla.style.display = "none";
    }

    // Default to Original Masked Preview
    switchPreviewTab("original");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // 7. Toggle Number Masking
  btnToggleMask.addEventListener("click", () => {
    isNumberMasked = !isNumberMasked;
    const details = currentScreeningResult?.extracted_details || {};
    updateMaskedNumberDisplay(details.document_number_masked, details.document_number_raw);
  });

  function updateMaskedNumberDisplay(masked, raw) {
    if (!tdDocNumber) return;
    if (isNumberMasked) {
      tdDocNumber.textContent = masked || "Protected / None";
      btnToggleMask.textContent = "👁️ Reveal";
    } else {
      tdDocNumber.textContent = raw || masked || "None";
      btnToggleMask.textContent = "🔒 Mask";
    }
  }

  // 8. Preview Tab Switching
  tabOriginal.addEventListener("click", () => switchPreviewTab("original"));
  tabEla.addEventListener("click", () => switchPreviewTab("ela"));

  function switchPreviewTab(tab) {
    if (tab === "original") {
      tabOriginal.classList.add("active");
      tabEla.classList.remove("active");
      imgDocumentPreview.style.display = "block";
      imgElaPreview.style.display = "none";
      viewHelpText.textContent = "* Sensitive fields are masked in previews for privacy.";
    } else {
      tabEla.classList.add("active");
      tabOriginal.classList.remove("active");
      imgDocumentPreview.style.display = "none";
      imgElaPreview.style.display = "block";
      viewHelpText.textContent = "* ELA Heatmap: High-contrast white/bright anomalies indicate digital splicing or altered text.";
    }
  }

  // 9. Screen Another Document
  btnScreenAnother.addEventListener("click", () => {
    resultSection.style.display = "none";
    scannerSection.style.display = "none";
    uploadSection.style.display = "block";

    // Reset fields
    currentFile = null;
    activeSampleId = null;
    currentScreeningResult = null;
    fileInput.value = "";
    filePreviewBar.style.display = "none";
    dropzone.style.display = "block";
    inputName.value = "";
    inputDob.value = "";
    inputDocNumber.value = "";
    validateForm();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // 10. Delete Document (Privacy Purge)
  btnDeleteDocument.addEventListener("click", async () => {
    if (!currentScreeningResult || !currentScreeningResult.id) return;
    
    const confirmDelete = confirm(
      "Are you sure you want to delete this document?\n\nThis will permanently purge the uploaded scan and all extracted screening records from the server."
    );
    if (!confirmDelete) return;

    try {
      const res = await fetch(`/api/screening/${currentScreeningResult.id}`, {
        method: "DELETE"
      });
      if (res.ok) {
        alert("Document scan and associated screening records have been permanently purged.");
        btnScreenAnother.click();
      } else {
        alert("Failed to delete document from server.");
      }
    } catch (e) {
      alert("Error deleting file: " + e.message);
    }
  });

  // 11. History Modal
  btnOpenHistory.addEventListener("click", async () => {
    historyModal.classList.add("open");
    historyList.innerHTML = `<p style="text-align: center; color: var(--text-muted); padding: 24px;">Loading previous screenings...</p>`;
    
    try {
      const res = await fetch("/api/history?limit=30");
      if (!res.ok) throw new Error("Could not load history");
      const records = await res.json();

      if (!records || records.length === 0) {
        historyList.innerHTML = `<p style="text-align: center; color: var(--text-muted); padding: 24px;">No screenings recorded yet.</p>`;
        return;
      }

      historyList.innerHTML = "";
      records.forEach((r) => {
        const item = document.createElement("div");
        item.className = "history-item";
        const risk = (r.risk_level || "low").toLowerCase();
        const dateStr = new Date(r.created_at).toLocaleString();

        item.innerHTML = `
          <div>
            <div style="font-weight: 700; font-size: 0.95rem;">${escapeHtml(r.document_type)}</div>
            <div style="font-size: 0.78rem; color: var(--text-muted);">${dateStr} • ${escapeHtml(r.filename)}</div>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <span class="chip-tag tag-${risk}">${r.risk_level} (${r.risk_score}/100)</span>
            <button class="btn-mask-toggle btn-view-hist" data-id="${r.id}">View</button>
          </div>
        `;
        historyList.appendChild(item);
      });

      // Attach click to view details
      historyList.querySelectorAll(".btn-view-hist").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          e.stopPropagation();
          const id = btn.getAttribute("data-id");
          historyModal.classList.remove("open");
          loadPreviousScreening(id);
        });
      });

    } catch (e) {
      historyList.innerHTML = `<p style="text-align: center; color: #ef4444; padding: 24px;">Error: ${e.message}</p>`;
    }
  });

  btnCloseHistory.addEventListener("click", () => {
    historyModal.classList.remove("open");
  });

  historyModal.addEventListener("click", (e) => {
    if (e.target === historyModal) {
      historyModal.classList.remove("open");
    }
  });

  async function loadPreviousScreening(id) {
    try {
      const res = await fetch(`/api/screening/${id}`);
      if (!res.ok) throw new Error("Record not found");
      const data = await res.json();
      uploadSection.style.display = "none";
      renderScreeningResults(data);
    } catch (e) {
      alert("Failed to load screening: " + e.message);
    }
  }

  // Utilities
  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
