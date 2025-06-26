document.addEventListener("DOMContentLoaded", async () => {
  const routesContainer = document.getElementById("routes-container");
  const testFormContainer = document.getElementById("test-form-container");
  const testForm = document.getElementById("test-form");
  const responseBox = document.getElementById("response-box");

  const methodInput = document.getElementById("http-method");
  const routeUrlInput = document.getElementById("route-url");

  const headersContainer = document.getElementById("headers-container");
  const addHeaderBtn = document.getElementById("add-header-btn");

  let selectedRoute = null;

  // Helper to add a new header row
  function addHeaderRow(key = '', value = '') {
    const row = document.createElement("div");
    row.className = "header-row";

    const keyInput = document.createElement("input");
    keyInput.type = "text";
    keyInput.placeholder = "Header Key";
    keyInput.value = key;

    const valueInput = document.createElement("input");
    valueInput.type = "text";
    valueInput.placeholder = "Header Value";
    valueInput.value = value;

    const removeBtn = document.createElement("button");
    removeBtn.textContent = "✕";
    removeBtn.onclick = () => row.remove();

    row.appendChild(keyInput);
    row.appendChild(valueInput);
    row.appendChild(removeBtn);

    headersContainer.appendChild(row);
  }

  // Add initial header row
  addHeaderRow();
  addHeaderBtn.onclick = () => addHeaderRow();

  // Fetch scanned routes
  try {
    const res = await fetch('/__apitest/routes');
    const data = await res.json();

    if (!data.success) {
      routesContainer.innerText = "❌ Failed to load routes.";
      return;
    }

    routesContainer.innerHTML = '';

    data.routes.forEach((route) => {
      const div = document.createElement("div");

      div.className = `route-item method-${route.method.toLowerCase()}`;
      div.innerHTML = `
        <span class="method-tag">${route.method}</span>
        <span class="route-path">${route.path}</span>
      `;


      div.onclick = () => {
        selectedRoute = route;
        methodInput.value = route.method;
        routeUrlInput.value = route.path;
        testFormContainer.classList.remove("hidden");
        responseBox.textContent = '';
      };
      routesContainer.appendChild(div);
    });
  } catch (err) {
    routesContainer.innerText = `❌ Error: ${err.message}`;
  }

  // Handle form submission
  testForm.onsubmit = async (e) => {
    e.preventDefault();

    const method = methodInput.value;
    const url = routeUrlInput.value;

    let bodyPayload = {};
    let headersPayload = {};

    // Parse body
    try {
      const bodyRaw = document.getElementById("request-body").value.trim();
      bodyPayload = bodyRaw ? JSON.parse(bodyRaw) : {};
    } catch (e) {
      alert("❌ Invalid JSON in Body field.");
      return;
    }

    // Collect headers from dynamic rows
    document.querySelectorAll(".header-row").forEach(row => {
      const inputs = row.querySelectorAll("input");
      const key = inputs[0].value.trim();
      const value = inputs[1].value.trim();
      if (key) {
        headersPayload[key] = value;
      }
    });

    // Send request
    try {
      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          ...headersPayload
        },
        body: ["POST", "PUT", "PATCH"].includes(method) ? JSON.stringify(bodyPayload) : undefined
      });

      const resultText = await res.text();
      responseBox.textContent = `Status: ${res.status}\n\n${resultText}`;
    } catch (err) {
      responseBox.textContent = `❌ Request failed:\n${err.message}`;
    }
  };
});
