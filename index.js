const express = require("express");
const req = require("express");
const path = require("path");
const runPythonScanner = require(".lib/python-runner");

function initApiTester(options = {}) {
    const router = express.Router();
    // serve static UI
    const staticPath = path.join(__dirname, 'ui' , 'public');
    router.use('/__apitest', express.static(staticPath));

    router.get('__apitest/routes', async (req , res) => {
        try{
            const routes = await runPythonScanner(projectPath)
            res.json({success: true, routes})
        }catch(error){
            console.error("Failed to run python scanner:", error)
            res.status(500).json({success: false, "error": error.message})
        }
    })
}

module.exports = initApiTester;