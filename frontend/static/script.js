document.addEventListener('DOMContentLoaded', function() {
    const singleUrlForm = document.getElementById('singleUrlForm');
    const batchUrlForm = document.getElementById('batchUrlForm');
    const resultsContent = document.getElementById('resultsContent');

    // Single URL Analysis
    if (singleUrlForm) {
        singleUrlForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const url = document.getElementById('url').value;
            if (!url) return;

            resultsContent.innerHTML = '<div>Analyzing URL...</div>';

            try {
                const response = await fetch('http://127.0.0.1:8001/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url })
                });

                const result = await response.json();
                resultsContent.innerHTML = '<h3>Results</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                addExportButton(result, 'resultsContent');
                
            } catch (error) {
                resultsContent.innerHTML = '<div>Error: ' + error.message + '</div>';
            }
        });
    }

    // Batch URL Analysis
    if (batchUrlForm) {
        batchUrlForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const urls = document.getElementById('urls').value
                .split('\n')
                .map(url => url.trim())
                .filter(url => url);

            if (!urls.length) return;

            resultsContent.innerHTML = '<div>Analyzing ' + urls.length + ' URLs...</div>';

            try {
                const results = [];
                for (let i = 0; i < urls.length; i++) {
                    resultsContent.innerHTML = '<div>Processing: ' + (i+1) + '/' + urls.length + '</div>';
                    
                    const response = await fetch('http://127.0.0.1:8001/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ url: urls[i] })
                    });
                    
                    const result = await response.json();
                    results.push(result);
                }
                
                resultsContent.innerHTML = '<h3>Batch Results</h3><pre>' + JSON.stringify(results, null, 2) + '</pre>';
                results.forEach((result, index) => addExportButton(result, 'resultsContent'));
                
            } catch (error) {
                resultsContent.innerHTML = '<div>Error: ' + error.message + '</div>';
            }
        });
    }
});

    // Add export button functionality
    function addExportButton(resultData, containerId) {
        const container = document.getElementById(containerId);
        const exportBtn = document.createElement('button');
        exportBtn.textContent = 'Export to PDF';
        exportBtn.style.cssText = 'margin: 10px; padding: 8px 16px; background: #007cba; color: white; border: none; cursor: pointer;';
        
        exportBtn.onclick = async function() {
            try {
                const response = await fetch('http://127.0.0.1:8001/export-pdf', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(resultData)
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'analysis_report.pdf';
                    a.click();
                    window.URL.revokeObjectURL(url);
                } else {
                    alert('PDF export failed');
                }
            } catch (error) {
                alert('Export error: ' + error.message);
            }
        };
        
        container.appendChild(exportBtn);
    }

