document.addEventListener("DOMContentLoaded", async () => {
    const routesContainer = document.getElementById("routes-container");
    const testFormContainer = document.getElementById("test-form-container");
    const testForm = document.getElementById("test-form");
    const responseBox = document.getElementById("response-box");
  
    const methodSelect = document.getElementById("http-method");
    const routeUrlInput = document.getElementById("route-url");
  
    let selectedRoute = null;
  
    // Fetch scanned routes
    try {
      const res = await fetch('/__apitest/routes');
      const data = await res.json();
  
      if (!data.success) {
        routesContainer.innerText = "❌ Failed to load routes.";
        return;
      }
  
      routesContainer.innerHTML = '';
  
      data.routes.forEach((route, index) => {
        const div = document.createElement("div");
        div.className = "route-item";
        div.innerText = `${route.method} ${route.path}`;
        div.onclick = () => {
          selectedRoute = route;
          methodSelect.value = route.method;
          routeUrlInput.value = route.path;
          testFormContainer.classList.remove("hidden");
          responseBox.textContent = '';
        };
        routesContainer.appendChild(div);
      });
  
    } catch (err) {
      routesContainer.innerText = `Error: ${err.message}`;
    }
  
    // Handle form submission
    testForm.onsubmit = async (e) => {
      e.preventDefault();
  
      const method = methodSelect.value;
      const bodyRaw = document.getElementById("request-body").value;
      let payload = {};
  
      try {
        payload = JSON.parse(bodyRaw || '{}');
      } catch (e) {
        alert("Request body must be valid JSON.");
        return;
      }
  
      try {
        const res = await fetch(routeUrlInput.value, {
          method,
          headers: {
            "Content-Type": "application/json"
          },
          body: ["POST", "PUT", "PATCH"].includes(method) ? JSON.stringify(payload) : undefined
        });
  
        const result = await res.text();
        responseBox.textContent = `Status: ${res.status}\n\n${result}`;
      } catch (err) {
        responseBox.textContent = `❌ Request failed:\n${err.message}`;
      }
    };
  });
  