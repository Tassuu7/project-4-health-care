/**
 * AegisCare Enterprise - Client Core Runtime & API Dispatcher
 */

const AegisCare = {
  apiBase: "/api/v1",

  // Authorization token management
  getToken() {
    return localStorage.getItem("aegis_token");
  },

  setToken(token) {
    localStorage.setItem("aegis_token", token);
  },

  getCurrentUser() {
    const userStr = localStorage.getItem("aegis_user");
    return userStr ? JSON.parse(userStr) : null;
  },

  setCurrentUser(user) {
    localStorage.setItem("aegis_user", JSON.stringify(user));
  },

  logout() {
    localStorage.removeItem("aegis_token");
    localStorage.removeItem("aegis_user");
    window.location.href = "/login";
  },

  // HTTP Fetch Wrapper with Authorization Bearer header
  async request(endpoint, options = {}) {
    const url = endpoint.startsWith("http") ? endpoint : `${this.apiBase}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {})
    };

    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, { ...options, headers });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || data.message || "An error occurred");
      }
      return data;
    } catch (err) {
      AegisCare.showToast(err.message, "error");
      throw err;
    }
  },

  // Toast Notifications
  showToast(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }
};

// Modal helpers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}
