const path = require('path')
const {spawn} = require('child_process')

function runPythonScanner(projectPath){
    return new Promise((resolve, reject)=>{
    const scannerPath = path.join(__dirname, '..', 'scan', 'scan.py');
    const pythonProcess = spawn('python', [scannerPath, projectPath])
    let output = ''
    let errorOutput = ''
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString()
    })
    pythonProcess.stderr.on('data', (data)=>{
        errorOutput += data.toString()
    })
    pythonProcess.on('close', (code)=>{
        if(code !== 0){
            return reject(new Error(`python scanner existed with code ${code}\n${errorOutput}`))
        }

        try {
            const parsed = JSON.parse(output)
            resolve(parsed)
        } catch (error) {
            reject(new Error(`Failed to parse JSON from scanner:\n${output}\nError: ${error.message}`))
        }
    })

    pythonProcess.on('error', (err)=>{
        reject(new Error(`Failed to start Python process ${err.message}`))
    })
    
    })
}

module.exports = runPythonScanner