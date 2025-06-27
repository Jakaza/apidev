const path = require('path')
const { spawn } = require('child_process')
const os = require('os')

function runPythonScanner(projectPath) {
    return new Promise((resolve, reject) => {
        const platform = os.platform(); // 'win32', 'darwin', 'linux'
        let scannerPath;

        if (platform === 'win32') {
            scannerPath = path.join(__dirname, '..', 'scan', 'dist', 'scan-win.exe');
        } else if (platform === 'darwin') {
            scannerPath = path.join(__dirname, '..', 'scan', 'dist', 'scan-mac');
        } else if (platform === 'linux') {
            scannerPath = path.join(__dirname, '..', 'scan', 'dist', 'scan-linux');
        } else {
            return reject(new Error(`Unsupported platform: ${platform}`));
        }

        const pythonProcess = spawn(scannerPath, [projectPath])
        let output = ''
        let errorOutput = ''
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString()
        })
        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString()
        })
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return reject(new Error(`python scanner existed with code ${code}\n${errorOutput}`))
            }

            try {
                const parsed = JSON.parse(output)
                resolve(parsed)
            } catch (error) {
                reject(new Error(`Failed to parse JSON from scanner:\n${output}\nError: ${error.message}`))
            }
        })

        pythonProcess.on('error', (err) => {
            reject(new Error(`Failed to start Python process ${err.message}`))
        })

    })
}

module.exports = runPythonScanner