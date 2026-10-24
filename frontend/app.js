// Confirm the backend is reachable and show which model it is configured for.
async function checkHealth() {
  const statusEl = document.getElementById("status");
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    statusEl.textContent = `Backend conectado · modelo ${data.model}`;
    statusEl.className = "ok";
  } catch (err) {
    statusEl.textContent = "No se pudo conectar con el backend.";
    statusEl.className = "error";
  }
}

checkHealth();
