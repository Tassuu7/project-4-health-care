/**
 * AegisCare Enterprise - Diagnostic Laboratory Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (document.getElementById("labQueueTable")) {
    await loadLabQueue();
  }
});

async function loadLabQueue() {
  try {
    const res = await AegisCare.request("/lab/queue");
    const tbody = document.querySelector("#labQueueTable tbody");
    if (!tbody) return;

    tbody.innerHTML = res.data.map(o => `
      <tr>
        <td><strong>${o.order_number}</strong></td>
        <td>Patient #${o.patient_id}</td>
        <td><span class="badge ${o.priority === 'STAT' ? 'badge-danger' : 'badge-primary'}">${o.priority}</span></td>
        <td><span class="badge badge-warning">${o.status}</span></td>
        <td>
          <button class="btn btn-sm btn-primary" onclick="openResultEntryModal(${o.id})">Enter Results</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}
