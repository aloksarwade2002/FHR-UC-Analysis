document.addEventListener('DOMContentLoaded', function() {
    // Fetch analysis results using an AJAX call
    fetch('/analyze', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Display the results on the page
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <h3>FHR Analysis</h3>
            <p>Average FHR (bpm): ${data.avg_bpm.join(', ')}</p>
            <p>Pulse Intervals (ms): ${data.pulse_intervals.join(', ')}</p>

            <h3>UC Peak Analysis</h3>
            <p>Number of wide peaks: ${data.peak_info.num_wide_peaks}</p>
            <p>Average peak duration: ${data.peak_info.avg_peak_duration} seconds</p>
        `;
    })
    .catch(error => console.error('Error fetching analysis:', error));
});
