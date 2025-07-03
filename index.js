const express = require("express");
const path = require("path");
const runPythonScanner = require("./lib/python-runner");

function initApiTester(options = {}) {
    const router = express.Router();
    const projectPath = options.projectPath || process.cwd();

    // ✅ Serve static UI
    const staticPath = path.join(__dirname, 'ui', 'public');
    router.use('/__apitest', express.static(staticPath));

    // ✅ Route to return scanned routes
    router.get('/__apitest/routes', async (req, res) => {
        console.log("➡️  Incoming request to /__apitest/routes");
        console.log("🔍 Project path:", projectPath);

        try {
            const routes = await runPythonScanner(projectPath);

            console.log("✅ Routes received from Python:");
            console.log(routes);

            res.json({ success: true, routes: routes.routes });
        } catch (error) {
            console.error("❌ Failed to run Python scanner:", error);
            res.status(500).json({ success: false, error: error.message });
        }
    });

    return router;
}

module.exports = initApiTester;
