from flask import Flask, render_template, request, jsonify
import pandas as pd
from analysis import plot_fhr_uc, calculate_fhr_epochs, detect_uc_peaks

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('data.csv')

# Convert 'Time(ms)' to seconds for further calculations
data['Time(s)'] = data['Time(ms)'] / 1000

@app.route('/')
def index():
    # Render the homepage
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Perform FHR and UC analysis
    plot_fhr_uc(data)  # This function will save the plots, so no need to return them.
    avg_bpm, pulse_intervals = calculate_fhr_epochs(data)
    peak_info = detect_uc_peaks(data)
    
    # Return the analysis results
    return jsonify({
        'avg_bpm': avg_bpm,
        'pulse_intervals': pulse_intervals,
        'peak_info': peak_info
    })

if __name__ == '__main__':
    app.run(debug=True)

