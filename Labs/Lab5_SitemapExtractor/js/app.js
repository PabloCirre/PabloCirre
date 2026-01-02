/**
 * Sitemap Extractor Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('sitemap-url');
    const extractBtn = document.getElementById('extract-btn');
    const urlCountMsg = document.getElementById('url-count');
    const consoleOutput = document.getElementById('console-output');
    const statusLight = document.getElementById('status-light');
    const consoleLight = document.getElementById('console-light');
    const downloadTxtBtn = document.getElementById('download-txt');
    const downloadZipBtn = document.getElementById('download-zip');
    const processStatus = document.getElementById('process-status');

    let extractedUrls = [];

    const log = (message, type = 'info') => {
        const line = document.createElement('div');
        line.className = `line ${type}`;
        line.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        consoleOutput.appendChild(line);
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    };

    const setStatus = (status, lightClass = 'on') => {
        processStatus.textContent = `STATUS: ${status.toUpperCase()}`;
        statusLight.className = `light ${lightClass}`;
        consoleLight.className = `light ${lightClass}`;
    };

    extractBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) {
            log('Error: URL is required.', 'error');
            return;
        }

        // Reset UI
        extractedUrls = [];
        urlCountMsg.textContent = '0';
        downloadTxtBtn.disabled = true;
        downloadZipBtn.disabled = true;
        setStatus('extracting', 'processing');
        log(`Starting extraction for: ${url}`);

        try {
            const response = await fetch('extract.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (data.error) {
                log(`Error: ${data.error}`, 'error');
                setStatus('error', 'error');
            } else if (data.success) {
                extractedUrls = data.urls;
                urlCountMsg.textContent = data.count;
                log(`Success: Found ${data.count} URLs.`, 'success');
                setStatus('complete', 'on');
                
                downloadTxtBtn.disabled = false;
                downloadZipBtn.disabled = false;
                document.getElementById('export-light').className = 'light on';
            }
        } catch (error) {
            log(`Fatal Error: ${error.message}`, 'error');
            setStatus('error', 'error');
        }
    });

    // TXT Download Logic
    downloadTxtBtn.addEventListener('click', () => {
        if (extractedUrls.length === 0) return;
        
        const blob = new Blob([extractedUrls.join('\n')], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sitemap_urls.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        log('TXT file downloaded.', 'success');
    });

    // ZIP Download Logic (Using an external library or a PHP helper if zip.js is not available)
    // For simplicity in this lab environment, we can use a separate PHP script or a small JS library.
    // I'll implement a basic ZIP generation using a lightweight approach if possible, but for a 
    // lab, generating it server-side or using a blob-to-zip lib is better.
    // Let's use a dynamic approach: create the ZIP in PHP and return the binary.
    
    downloadZipBtn.addEventListener('click', async () => {
        if (extractedUrls.length === 0) return;
        
        log('Generating ZIP package...');
        setStatus('zipping', 'processing');

        try {
            // We can send the URLs back to a zip helper or just reuse extract.php if we want
            // but for better UX, let's just use JS to trigger a "download-as-zip" if we had JSZip.
            // Alternative: The PHP extract.php can already have the ZIP ready or we make a zip.php.
            
            // Re-fetching with a zip flag is one way
            const response = await fetch('zip_helper.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls: extractedUrls })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'sitemap_urls.zip';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                log('ZIP package downloaded.', 'success');
                setStatus('complete', 'on');
            } else {
                log('Error generating ZIP.', 'error');
                setStatus('error', 'error');
            }
        } catch (error) {
            log(`ZIP Error: ${error.message}`, 'error');
            setStatus('error', 'error');
        }
    });
});
