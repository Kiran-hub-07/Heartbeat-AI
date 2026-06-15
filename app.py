import os
import pandas as pd
from flask import Flask, render_template, jsonify, request
from twilio.rest import Client  # Handles the cellular network connection

app = Flask(__name__)

EXCEL_FILE = 'patient_data.xlsx'

# ==============================================================================
# 🔑 TWILIO NETWORK CREDENTIALS
# Paste your keys directly from your Twilio Console dashboard!
# ==============================================================================
TWILIO_ACCOUNT_SID = 'AC585c19109386349c620c2a92ab249ee7'
TWILIO_AUTH_TOKEN  = 'c2f88fc44f1be0299bbda13a9f56adb9'

# ⚠️ PLACE YOUR VIRTUAL TWILIO ASSIGNED PHONE NUMBER HERE (Include the country code prefix, e.g., '+1...')
TWILIO_NUMBER      = '+1 972 823 1269'  


# ==============================================================================
# 🧮 CLINICAL RISK ENGINE (MULTI-VARIANT TRIAGE MATRIX)
# ==============================================================================
def calculate_patient_risk(patient):
    """
    Analyzes multiple vital signs combined to calculate a cumulative risk score.
    Weights are assigned for abnormal SpO2, Heart Rate, and Temperature values.
    """
    score = 0
    
    try:
        # Safely extract and convert spreadsheet entries to numeric values
        spo2 = int(patient.get('SpO2', 100))
        hr = int(patient.get('HeartRate', 70))
        temp = float(patient.get('Temperature', 98.6))
        
        # Apply proportionate mathematical weights based on clinical metrics
        if spo2 < 92: 
            score += 40
        if hr > 110: 
            score += 25
        if temp > 100: 
            score += 20
            
    except (ValueError, TypeError):
        # Fallback safety if a cell contains corrupted data or an empty string
        pass
        
    return score


# ==============================================================================
# 📊 DATABASE READ & FALLBACK HANDLERS
# ==============================================================================
def get_mock_fallback_data():
    """Returns baseline dummy data if the patient spreadsheet is missing or locked."""
    return [
        {
            "PatientID": "P101", 
            "PatientName": "John Doe", 
            "SpO2": 96, 
            "HeartRate": 72, 
            "Temperature": 98.4, 
            "FloorChargeNurse": "Nurse Michael", 
            "NursePhone": "+919342375559"
        },
        {
            "PatientID": "P102", 
            "PatientName": "Jane Smith", 
            "SpO2": 89, 
            "HeartRate": 115, 
            "Temperature": 101.2, 
            "FloorChargeNurse": "Nurse Michael", 
            "NursePhone": "+919342375559"
        }
    ]

def get_patients_from_excel():
    """Reads patient telemetry straight from the Excel worksheet database."""
    if not os.path.exists(EXCEL_FILE):
        return get_mock_fallback_data()
        
    try:
        df = pd.read_excel(EXCEL_FILE)
        if df.empty:
            return get_mock_fallback_data()
            
        # Normalize column formats automatically to strip out spaces or case anomalies
        df.columns = df.columns.str.replace(' ', '').str.replace('_', '')
        
        # Safely convert dataframe rows to a standard Python dictionary list
        patients = df.to_dict(orient='records')
        return patients
    except Exception as e:
        print(f"Excel reading exception caught: {e}")
        return get_mock_fallback_data()


# ==============================================================================
# 🌐 CORE APPLICATION ROUTE ENDPOINTS
# ==============================================================================
@app.route('/')
def index():
    """Renders the main central clinical telemetry dashboard UI interface."""
    return render_template('index.html')


@app.route('/api/patients')
def get_patients():
    """Fetches records from the Excel file and appends computed risk profiles."""
    patients = get_patients_from_excel()
    
    # Injects the computed clinical weight index directly into each patient object JSON payload
    for p in patients:
        p['RiskScore'] = calculate_patient_risk(p)
        
    return jsonify(patients)


@app.route('/api/alert/<patient_id>', methods=['POST'])
def trigger_alert(patient_id):
    """
    Intercepts dynamic critical events and executes an instant outbound 
    cellular SMS routing gateway notification to the designated handler.
    """
    patients = get_patients_from_excel()
    patient = next((p for p in patients if str(p.get('PatientID')) == str(patient_id)), None)
    
    if not patient:
        return jsonify({"status": "error", "message": "Patient record target not located on current floor matrix."}), 404
        
    raw_phone = str(patient.get('NursePhone', '')).strip()
    if not raw_phone:
        return jsonify({"status": "error", "message": "No active contact payload associated with this clinical handler."}), 400
        
    # Automatically normalization check: attaches country code prefix (+91) if missing
    nurse_phone = raw_phone if raw_phone.startswith('+') else f"+91{raw_phone}"
    
    # Calculate current risk context metrics for message reporting
    risk_score = calculate_patient_risk(patient)
    
    # Compose the clinical emergency payload message context string
    alert_message = (
        f"🚨 HEARTBEAT AI EMERGENCY TELEMETRY BREACH\n\n"
        f"Patient: {patient.get('PatientName', 'Unknown')}\n"
        f"Room ID: {patient.get('PatientID', 'N/A')}\n"
        f"Current Vitals: SpO2 {patient.get('SpO2')}% | HR {patient.get('HeartRate')} BPM\n"
        f"Computed Risk Evaluation Index Score: {risk_score}/85\n\n"
        f"Immediate clinical onsite handler intervention required."
    )
    
    try:
        # Initialize the Twilio Network Engine Pipeline
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Dispatch message across cellular infrastructure
        message = client.messages.create(
            body=alert_message,
            from_=TWILIO_NUMBER,
            to=nurse_phone
        )
        
        return jsonify({
            "status": "success", 
            "message": f"Clinical route established! Notification sent to handler at {nurse_phone}",
            "sid": message.sid
        })
        
    except Exception as err:
        # Return clean error string feedback directly to our dashboard alert window interface
        return jsonify({
            "status": "error", 
            "message": f"Twilio gateway communication error instance returned: {str(err)}"
        }), 500


if __name__ == '__main__':
    # Run the microservice server locally on Port 5000 with live execution tracking
    app.run(debug=True, port=5000)
