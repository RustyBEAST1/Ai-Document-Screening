import React from 'react';
import { AlertCircle, Shield } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <footer className="mt-12 pt-6 border-t border-[#23334A] text-xs text-[#94A3B8]">
      <div className="p-4 bg-[#151F32] border border-[#23334A] rounded-xl flex items-start gap-3">
        <AlertCircle className="w-4 h-4 text-[#06B6D4] flex-shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong className="text-[#E5EDF7]">Verification Notice:</strong> This AI system provides preliminary fraud and tampering screening. It is designed to assist verifiers and does not replace official government identity databases or human review.
        </p>
      </div>
      <div className="flex flex-col sm:flex-row items-center justify-between gap-2 mt-4 text-[11px] text-[#94A3B8]">
        <span>AEGIS AI • Fake Identity & Document Screener</span>
        <span>Secured with Verhoeff D5, Error Level Analysis (ELA) & OCR</span>
      </div>
    </footer>
  );
}
