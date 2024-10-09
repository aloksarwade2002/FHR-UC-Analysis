import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths

# Plot FHR and UC data
def plot_fhr_uc(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Time(s)'], data['Fhr1(BPM)'], label='FHR (bpm)')
    plt.title('FHR over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('FHR (bpm)')
    plt.grid(True)
    plt.legend()
    plt.savefig('static/fhr_plot.png')  # Save in static directory for Flask
    
    plt.figure(figsize=(12, 6))
    plt.plot(data['Time(s)'], data['Uc(TOCO)'], label='Uterine Contractions (TOCO)', color='orange')
    plt.title('UC over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('UC (TOCO)')
    plt.grid(True)
    plt.legend()
    plt.savefig('static/uc_plot.png')  # Save in static directory for Flask

# FHR Epoch Calculation
def calculate_fhr_epochs(data, epoch_duration=3.75):
    num_epochs = int(data['Time(s)'].max() // epoch_duration)
    avg_bpm = []
    pulse_intervals = []
    
    for i in range(num_epochs):
        start_time = i * epoch_duration
        end_time = (i + 1) * epoch_duration
        epoch_data = data[(data['Time(s)'] >= start_time) & (data['Time(s)'] < end_time)]
        
        # Calculate average FHR for the epoch
        avg_fhr = epoch_data['Fhr1(BPM)'].mean()
        avg_bpm.append(avg_fhr)
        
        # Calculate pulse interval in milliseconds
        pulse_interval = (60 / avg_fhr) * 1000 if avg_fhr > 0 else 0
        pulse_intervals.append(pulse_interval)
    
    return avg_bpm, pulse_intervals

# UC Peak Detection
def detect_uc_peaks(data):
    peaks, _ = find_peaks(data['Uc(TOCO)'], height=5)
    peak_width_results = peak_widths(data['Uc(TOCO)'], peaks, rel_height=0.5)
    peak_widths_sec = peak_width_results[0] * 0.25  # Convert to seconds
    
    # Filter peaks with widths > 30 seconds
    wide_peaks = peak_widths_sec[peak_widths_sec > 30]
    average_peak_duration = np.mean(wide_peaks) if len(wide_peaks) > 0 else 0
    
    return {
        'num_wide_peaks': len(wide_peaks),
        'avg_peak_duration': average_peak_duration
    }