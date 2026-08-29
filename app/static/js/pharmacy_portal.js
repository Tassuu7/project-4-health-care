/**
 * AegisCare Enterprise - Pharmacy & Drug Dispensing Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (document.getElementById("medicationInventoryTable")) {
    await loadInventory();
  }
});

async function loadInventory() {
  try {
    const res = await AegisCare.request("/prescriptions/medications");
    const tbody = document.querySelector("#medicationInventoryTable tbody");
    if (!tbody) return;

    tbody.innerHTML = res.data.map(m => `
      <tr>
        <td><code>${m.drug_code}</code></td>
        <td><strong>${m.brand_name}</strong> (${m.generic_name})</td>
        <td>${m.dosage_form} - ${m.strength}</td>
        <td>${m.current_stock_quantity} units</td>
        <td>$${m.unit_price.toFixed(2)}</td>
        <td>
          <button class="btn btn-sm btn-secondary" onclick="openRestockModal(${m.id})">Restock</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}
