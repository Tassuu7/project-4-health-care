/**
 * AegisCare Enterprise - Physician Clinical Workbench Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (document.getElementById("doctorQueueTable")) {
    await loadDoctorQueue();
  }
});

async function loadDoctorQueue() {
  try {
    const res = await AegisCare.request("/appointments?today_only=true");
    const tbody = document.querySelector("#doctorQueueTable tbody");
    if (!tbody) return;

    if (!res.data || res.data.length === 0) {
      tbody.innerHTML = "<tr><td colspan='6' class='text-center text-muted'>No appointments scheduled today.</td></tr>";
      return;
    }

    tbody.innerHTML = res.data.map(appt => `
      <tr>
        <td><strong>${appt.appointment_number}</strong></td>
        <td>Patient #${appt.patient_id}</td>
        <td>${new Date(appt.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
        <td>${appt.chief_complaint}</td>
        <td><span class="badge badge-primary">${appt.status}</span></td>
        <td>
          <button class="btn btn-sm btn-primary" onclick="openConsultationModal(${appt.id}, ${appt.patient_id})">Consult</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

function openConsultationModal(apptId, patientId) {
  document.getElementById("consultApptId").value = apptId;
  document.getElementById("consultPatientId").value = patientId;
  openModal("consultationModal");
}
