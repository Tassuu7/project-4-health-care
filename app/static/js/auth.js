/**
 * AegisCare Enterprise - Authentication & Role Switcher
 */

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const submitBtn = loginForm.querySelector("button[type='submit']");
      const originalText = submitBtn.innerHTML;
      
      const usernameInput = document.getElementById("username");
      const passwordInput = document.getElementById("password");
      
      const username_or_email = usernameInput.value.trim();
      const password = passwordInput.value;

      if (!username_or_email || !password) {
        AegisCare.showToast("Please enter both username and password", "warning");
        return;
      }

      submitBtn.disabled = true;
      submitBtn.innerHTML = "Signing in...";

      try {
        const res = await AegisCare.request("/auth/login", {
          method: "POST",
          body: JSON.stringify({ username_or_email, password })
        });

        AegisCare.setToken(res.data.access_token);
        AegisCare.setCurrentUser(res.data.user);
        AegisCare.showToast(`Welcome, ${res.data.user.first_name}! Redirecting...`, "success");

        // Redirect based on user role
        const role = res.data.user.role;
        setTimeout(() => {
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
        }, 500);
      } catch (err) {
        console.error("Login failed:", err);
        AegisCare.showToast(err.message || "Invalid credentials", "error");
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }
});

// Quick demo login helper
function quickLogin(username, password) {
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  if (usernameInput && passwordInput) {
    usernameInput.value = username;
    passwordInput.value = password;
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.dispatchEvent(new Event("submit"));
    }
  }
}
