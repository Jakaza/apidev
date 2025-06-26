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
        try {
            const routes = await runPythonScanner(projectPath);
            res.json({ success: true, routes });
        } catch (error) {
            console.error("❌ Failed to run Python scanner:", error);
            res.status(500).json({ success: false, error: error.message });
        }
    });

    return router;
}

module.exports = initApiTester;
