from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json
from apscheduler.schedulers.background import BackgroundScheduler

from engine.analyzer import detect_anomalies
from engine.report_gen import generate_threat_report
from engine.splunk_ingest import fetch_logs_from_splunk
from engine.elk_ingest import fetch_logs_from_elk
from engine.alerts import send_slack_alert
from engine.email_alert import send_email_alert

app = Flask(__name__)
CORS(app)
STORED_ANOMALIES = None
LATEST_REPORT = None

@app.route("/api/upload-logs", methods=["POST"])
def upload_logs():
    logs = request.get_json()
    with open("logs/logs.json", "w") as f:
        json.dump(logs, f, indent=2)
    return jsonify({"message": "Logs uploaded"}), 200

@app.route("/api/analyze", methods=["POST"])
def analyze():
    global STORED_ANOMALIES, LATEST_REPORT
    logs = json.load(open("logs/logs.json"))
    _, anomalies = detect_anomalies(logs)
    STORED_ANOMALIES = anomalies.to_dict(orient="records")
    if not anomalies.empty:
        LATEST_REPORT = generate_threat_report(anomalies)
        msg = f"{len(STORED_ANOMALIES)} anomalies found."
        send_slack_alert(msg)
        send_email_alert("Security Anomalies Detected", LATEST_REPORT)
    else:
        LATEST_REPORT = "✅ No anomalies."
    return jsonify({"status":"done","count": len(STORED_ANOMALIES)}), 200

@app.route("/api/anomalies", methods=["GET"])
def get_anomalies():
    return jsonify({"anomalies": STORED_ANOMIES or [], "report": LATEST_REPORT or ""})

@app.route("/api/fetch-splunk", methods=["POST"])
def fetch_splunk():
    params = request.get_json()
    logs = fetch_logs_from_splunk(**params)
    open("logs/logs.json","w").write(json.dumps(logs, indent=2))
    return jsonify({"message": f"Fetched {len(logs)} logs"}), 200

@app.route("/api/fetch-elk", methods=["POST"])
def fetch_elk():
    params = request.get_json()
    logs = fetch_logs_from_elk(**params)
    open("logs/logs.json","w").write(json.dumps(logs, indent=2))
    return jsonify({"message": f"Fetched {len(logs)} logs"}), 200

def auto_fetch():
    try:
        logs = fetch_logs_from_splunk(**{
            "host":"localhost","port":8089,"username":"admin","password":"pass",
            "query":"search index=*"
        })
        open("logs/logs.json","w").write(json.dumps(logs, indent=2))
        print(f"[AUTO] Pulled {len(logs)} logs")
    except Exception as e:
        print("[AUTO] fetch failed", e)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_fetch, 'interval', minutes=5)
    scheduler.start()
    app.run(debug=True)
