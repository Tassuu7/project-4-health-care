/**
 * AegisCare Enterprise - Admin Console & HIPAA Audit Trail
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (document.getElementById("auditLogTable")) {
    await loadAuditLogs();
  }
});

async function loadAuditLogs() {
  try {
    const res = await AegisCare.request("/audit/logs?limit=50");
    const tbody = document.querySelector("#auditLogTable tbody");
    if (!tbody) return;

    tbody.innerHTML = res.data.map(l => `
      <tr>
        <td>${new Date(l.timestamp).toLocaleString()}</td>
        <td><strong>${l.username || 'SYSTEM'}</strong> <span class="badge badge-gray">${l.user_role || 'N/A'}</span></td>
        <td><span class="badge badge-primary">${l.action}</span></td>
        <td>${l.resource_type} #${l.resource_id || ''}</td>
        <td><code>${l.ip_address || '127.0.0.1'}</code></td>
        <td>${l.details || ''}</td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}
