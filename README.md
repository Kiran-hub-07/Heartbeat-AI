Heartbeat AI is an automated, continuous clinical decision support system designed to bridge the gap between critical patient telemetry and immediate clinical action. The system simulates live IoT medical sensors streaming continuous patient vital metrics (Oxygen Saturation, Pulse Rate, Temperature) into a centralized matrix database, instantly calculates an integrated multi-variant patient risk score, and automatically dispatches an urgent out-of-band cellular SMS notification directly to an on-call nurse's phone via the Twilio Cloud Gateway the split-second a patient's vitals deteriorate.

Key Features
Real-Time Patient Monitor UI: A clean, easy-to-read dashboard that polls data asynchronously every 3 seconds without requiring hard browser refreshes.

Multi-Variant Triage Engine: Calculates composite mathematical health hazard weights based on multiple combined vital signs rather than treating single metrics in isolation.

Cloud Telecommunication Routing: Uses standard cellular frequencies via the Twilio API to bypass internet-dependent chat notifications, ensuring mission-critical reliability.

Defensive Fault-Tolerance Fallback: Automatically switches to a mock data array if the underlying spreadsheet database is missing or locked, ensuring the central hospital workstation never goes dark.

Automated Number Normalization: Sanitizes contact inputs dynamically to strictly conform to E.164 international telecom string formatting.

ystem Architecture Workflow
The system operates as an automated reactive feedback loop across four decoupled layers:

Data Layer (patient_data.xlsx): Simulates ward beds feeding live patient metrics directly to an active database.

Application Core Layer (app.py): Built on the Python Flask framework. Reads database inputs via pandas, evaluates triage calculations, and exposes RESTful JSON API endpoints.

View Presentation Layer (index.html): Renders the frontend layout utilizing native JavaScript Fetch mechanisms on a continuous polling loop.

Network Gateway Layer (Twilio API): Securely intercepts dispatch requests and routes immediate notification payloads directly onto global cellular carrier infrastructures.



Triage Risk Evaluation AlgorithmInstead of checking thresholds in a vacuum, the system combines three core vital arrays to form a single clinical hazard evaluation index scoring between 0 and 85:Oxygen Saturation Drop ($SpO_2 < 92\%$): $+40$ Points (High critical risk priority for acute hypoxemia)Tachycardia Spike ($\text{Pulse Rate} > 110\text{ BPM}$): $+25$ PointsFebrile State ($\text{Temperature} > 100^\circ\text{F}$): $+20$ PointsThis composite weighting allows hospital staff to immediately identify multi-symptom critical trends at a single glance.
Tech Stack
Backend Core: Python 3.x, Flask Micro-framework

Data Science Tools: Pandas, OpenPyXL

Frontend Interface: HTML5, CSS3, Asynchronous JavaScript (ES6+ Architecture)

Cloud Infrastructure: Twilio Telecommunication REST API Gateway


