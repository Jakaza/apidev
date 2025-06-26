const runScanner = require('./lib/python-runner.js')

runScanner('./examples/basic-app')
.then((routes)=>{
    console.log(`Routes found:${routes} `)
})
.catch((err)=>{
    console.log(`Error running scanner: ${err.message}`); 
})