# 🧪 apidev — Express API Testing Middleware with Built-in UI

**apidev** is a Postman-style API testing system that integrates directly into your Express application. It auto-detects all your routes using a Python-based scanner and provides a beautiful in-browser UI to test them — no extra config or external tools required.

---

## ✨ Features

- ✅ Instantly discover all Express routes using static code analysis
- ✅ Simple middleware setup — no config required
- ✅ In-browser UI to test GET, POST, PUT, DELETE, PATCH
- ✅ Add custom headers and body inputs
- ✅ Color-coded HTTP methods for quick visibility
- ⚠️ Requires Python installed *(binaries coming soon)*

---

---

## 🔮 Roadmap

| Feature                                    | Status        |
| ------------------------------------------ | ------------- |
| Auto-detect routes using static scanner    | ✅ Completed   |
| Simple in-browser testing UI               | ✅ Completed   |
| Add body and headers to test requests      | ✅ Completed   |
| Static route listing with HTTP method tags | ✅ Completed   |
| Precompiled scanner binaries (Windows)     | 🔄 In Progress |
| Full route (http://...) detection          | 🔄 In Progress |
| Query/body/params detection                | 🔄 In Progress |
| Precompiled scanner binaries (Linux)       | 🔜 Next        |
| React/Vite-based advanced UI               | 🧭 Planned     |
| cURL/Postman export                        | 🧭 Planned     |
| Request history & environment variables    | 🧭 Planned     |

---



## 📦 Installation

```bash
npm install apidev
```

---

## 🚀 Quick Start

### 1. Use the middleware in your Express app

```js
const express = require("express");
const initApiTester = require("apidev");

const app = express();
app.use(express.json());

// Register your routes here
// app.use('/api', require('./routes/api'))

// Mount the API tester
app.use(initApiTester());

app.listen(3000, () => console.log("Running on http://localhost:3000"));
```

### 2. Open the Test UI

Visit [http://localhost:3000/__apitest](http://localhost:3000/__apitest)  
You’ll see all your detected routes — test them directly.

---

## 📁 Project Structure (Overview)

```
express-api-tester/
│
├── package.json               # NPM config and dependencies
├── index.js                   # Main middleware entry point
│
├── lib/                       # JavaScript helper modules
│   └── python-runner.js       # Spawns the Python scanner from Node.js
│
├── scan/                      # Python scanner logic
│   ├── scan.py                # Entry point for scanning a project
│   └── parser/                # Parsing logic for Express routes
│       ├── route_extractor.py
│       └── utils.py
│
├── bin/                       # (Planned) Python scanner compiled for each OS
│   ├── scan-win.exe           # Windows (coming soon)
│   ├── scan-mac               # macOS binary (coming soon)
│   └── scan-linux             # Linux binary (coming soon)
│
├── ui/                        # Web-based API Testing Interface
│   ├── public/                # HTML/JS/CSS UI (current version)
│   └── app/                   # (Planned) React/Vite version
│
├── routes/                    # Internal Express routes for UI + data
│   └── apitest.routes.js
│
├── docs/                      # API scan examples and documentation
│   └── api-output-example.json
│
├── examples/                  # Sample Express app to test apidev locally
│   └── basic-app/
│       └── app.js
│
└── README.md                  # You are here
```

---

## 🧪 How It Works

1. `apidev` statically scans your Express project with `scan.py`
2. It collects all `app.get(...)`, `router.post(...)`, etc.
3. Detected routes are sent to the browser interface
4. The UI lets you test endpoints with optional body and headers

---

## ⚙ Requirements

- Node.js v14 or newer
- Python 3.6+ *(temporarily required for scanning)*


## 📘 Example Output

```json
[
  {
    "method": "POST",
    "path": "/users",
    "file": "routes/user.js"
  },
  {
    "method": "GET",
    "path": "/products/:id",
    "file": "routes/product.js"
  }
]
```

---

## 🧪 Test Locally

A full example is included under `examples/basic-app`.

```bash
cd examples/basic-app
node app.js
```

Then visit:  
[http://localhost:3000/__apitest](http://localhost:3000/__apitest)

---

## 🤝 Notes for Contributors

We welcome contributors who want to improve or extend **apidev**. This project is actively evolving, and your input is valuable. Before submitting a pull request, please read the following notes:

### 🧠 Philosophy

- Keep the middleware integration **lightweight and simple**
- Ensure everything works **locally without external services**
- Follow the existing file structure and module separation
- Focus on **developer-first experience** and fast feedback loops

### 🧪 How You Can Help

- Improve the Python scanner to better detect:
  - `req.params`, `req.query`, and `req.body`
  - Imported route handlers (`router.get('/', handler)`)
- Add binary support (`bin/scan-win.exe`, etc.) so Python is optional
- Enhance the UI with:
  - Authorization header helpers
  - Response formatting and collapsible sections
  - Export to cURL/Postman
- Help design the future `React/Vite` version in `ui/app/`

### ⚙ Development Guidelines

- Test changes using the demo app:
  ```bash
  node examples/basic-app/app.js
  ```
- Python debug output:
  ```python
  print("Debug message", file=sys.stderr)
  ```
- JavaScript debug output:
  ```js
  console.log("Debug message")
  ```

### 🔒 What Not to Add (Yet)

- No telemetry, network requests, or user tracking
- No third-party auth integrations (keep it local)
- No database dependencies

---

## 👨‍💻 Author

**Jakaza**  
Built with ❤️ for devs who test fast and ship clean.

---

## 🛡 License

[MIT](./LICENSE)