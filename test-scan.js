const runScanner = require('./lib/python-runner.js');

// Test the scanner with better error handling and output
async function testScanner() {
    console.log('🔍 Testing API Route Scanner...');
    console.log('=' * 40);

    try {
        const result = await runScanner('./examples/basic-app');

        console.log('✅ Scanner executed successfully!');
        console.log(`📊 Results:`, JSON.stringify(result, null, 2));

        // Extract routes if the result is structured
        const routes = result.routes || result;
        const stats = result.stats;

        if (Array.isArray(routes)) {
            console.log(`\n📍 Found ${routes.length} route(s):`);
            routes.forEach((route, index) => {
                console.log(`  ${index + 1}. ${route.method} ${route.path}`);
                if (route.file) {
                    console.log(`     📄 File: ${route.file}`);
                }
                if (route.expected_inputs && Object.keys(route.expected_inputs).length > 0) {
                    console.log(`     📥 Expected inputs:`, route.expected_inputs);
                }
                if (route.framework) {
                    console.log(`     🔧 Framework: ${route.framework}`);
                }
            });
        } else {
            console.log('⚠️  No routes array found in result');
        }

        if (stats) {
            console.log(`\n📈 Statistics:`);
            console.log(`  Files scanned: ${stats.scanned_files}`);
            console.log(`  Errors: ${stats.errors?.length || 0}`);
        }

    } catch (err) {
        console.error('❌ Error running scanner:', err.message);
        console.error('Stack trace:', err.stack);

        // Additional debugging info
        console.log('\n🔍 Debug info:');
        console.log('- Make sure the Python executable exists in scan/dist/');
        console.log('- Check that ./examples/basic-app directory exists');
        console.log('- Verify the executable has proper permissions');
    }
}

// Run the test
testScanner();