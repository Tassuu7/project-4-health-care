/**
 * AegisCare Enterprise - Patient Self-Service Portal Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  const user = AegisCare.getCurrentUser();
  if (document.getElementById("patientAppointmentsList")) {
    await loadPatientDashboardData();
  }
});

async function loadPatientDashboardData() {
  try {
    const res = await AegisCare.request("/appointments?patient_id=1");
    const container = document.getElementById("patientAppointmentsList");
    if (!container) return;

    if (!res.data || res.data.length === 0) {
      container.innerHTML = "<p class='text-muted'>No upcoming appointments.</p>";
      return;
    }

    container.innerHTML = res.data.map(a => `
      <div class="timeline-item">
        <div class="timeline-bullet"></div>
        <h4>${new Date(a.start_time).toLocaleDateString()} at ${new Date(a.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</h4>
        <p><strong>Reason:</strong> ${a.chief_complaint}</p>
        <span class="badge badge-primary">${a.status}</span>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}
