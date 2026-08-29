/**
 * AegisCare Enterprise - Authentication & Role Switcher
 */

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username_or_email = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      try {
        const res = await AegisCare.request("/auth/login", {
          method: "POST",
          body: JSON.stringify({ username_or_email, password })
        });

        AegisCare.setToken(res.data.access_token);
        AegisCare.setCurrentUser(res.data.user);
        AegisCare.showToast("Login successful!", "success");

        // Redirect based on role
        const role = res.data.user.role;
        if (role === "DOCTOR" || role === "SPECIALIST") {
          window.location.href = "/doctor-dashboard";
        } else if (role === "TRIAGE_NURSE" || role === "STAFF_NURSE" || role === "HEAD_NURSE") {
          window.location.href = "/nurse-station";
        } else if (role === "ADMIN") {
          window.location.href = "/admin-console";
        } else if (role === "PHARMACIST") {
          window.location.href = "/pharmacy-console";
        } else if (role === "LAB_TECHNICIAN") {
          window.location.href = "/lab-console";
        } else if (role === "BILLING_OFFICER") {
          window.location.href = "/billing-console";
        } else {
          window.location.href = "/patient-portal";
        }
      } catch (err) {
        console.error("Login failed:", err);
      }
    });
  }
});

// Quick demo login helper
function quickLogin(username, password) {
  document.getElementById("username").value = username;
  document.getElementById("password").value = password;
  document.getElementById("loginForm").dispatchEvent(new Event("submit"));
}
