/**
 * AegisCare Enterprise - Nurse Station & Triage Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (document.getElementById("triageQueueTable")) {
    await loadTriageQueue();
    await loadBedMatrix();
  }
});

async function loadTriageQueue() {
  try {
    const res = await AegisCare.request("/triage/queue");
    const tbody = document.querySelector("#triageQueueTable tbody");
    if (!tbody) return;

    tbody.innerHTML = res.data.map(t => `
      <tr>
        <td><span class="badge badge-esi-${t.triage_level}">ESI ${t.triage_level}</span></td>
        <td><strong>${t.triage_number}</strong></td>
        <td>Patient #${t.patient_id}</td>
        <td>${t.chief_complaint}</td>
        <td>${t.assigned_zone}</td>
        <td>${t.pain_score}/10</td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

async function loadBedMatrix() {
  try {
    const res = await AegisCare.request("/wards/beds/available");
    const container = document.getElementById("bedMatrixContainer");
    if (!container) return;

    container.innerHTML = res.data.map(b => `
      <div class="bed-card available">
        <strong>${b.identifier}</strong>
        <p class="text-muted" style="font-size:11px;">${b.ward} - Rm ${b.room}</p>
        <span class="badge badge-success mt-1">Ready</span>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}
