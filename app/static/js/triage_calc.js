/**
 * AegisCare Enterprise - Emergency Severity Index (ESI) Real-Time Calculator
 */

const TriageCalculator = {
  evaluate() {
    const isResus = document.getElementById("triageResus")?.checked || false;
    const isHighRisk = document.getElementById("triageHighRisk")?.checked || false;
    const pain = parseInt(document.getElementById("triagePain")?.value || "0", 10);
    const resources = parseInt(document.getElementById("triageResources")?.value || "1", 10);
    const hr = parseInt(document.getElementById("triageHR")?.value || "80", 10);
    const spo2 = parseFloat(document.getElementById("triageSpO2")?.value || "98");

    let level = 5;
    let label = "Level 5 - Non-Urgent";
    let colorClass = "esi-5";

    if (isResus) {
      level = 1;
      label = "Level 1 - Resuscitation (Immediate Life Threat)";
      colorClass = "esi-1";
    } else if (isHighRisk || pain >= 8 || spo2 < 92 || hr > 130 || hr < 40) {
      level = 2;
      label = "Level 2 - Emergent (High Risk / Danger Vitals)";
      colorClass = "esi-2";
    } else if (resources >= 2) {
      level = 3;
      label = "Level 3 - Urgent (Multiple Resources)";
      colorClass = "esi-3";
    } else if (resources === 1) {
      level = 4;
      label = "Level 4 - Less Urgent (Single Resource)";
      colorClass = "esi-4";
    }

    const display = document.getElementById("triageResultBox");
    if (display) {
      display.className = `triage-score-display ${colorClass}`;
      display.innerHTML = `<h3>${label}</h3><p>Calculated ESI Score: <strong>Level ${level}</strong></p>`;
    }
  }
};
