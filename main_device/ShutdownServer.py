from shutdown import plug_off
import logging
from logging.handlers import RotatingFileHandler
import os
import threading
from flask import Flask, request, jsonify

LOGDIR = '/var/log/weather_station'
os.makedirs(LOGDIR, exist_ok=True)

app = Flask(__name__)

# --- Loggeri ---
class ComponentFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "component"):
            record.component = record.name
        return super().format(record)

def make_logger(name, path, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = RotatingFileHandler(path, maxBytes=5*1024*1024, backupCount=5)
        fmt = '%(asctime)s %(levelname)s %(name)s %(component)s: %(message)s'
        formatter = ComponentFormatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

connections_logger = make_logger(
    'weather.shutdown',
    os.path.join(LOGDIR, 'shutdown.log'),
    level=logging.INFO
)

connections_logger.info('Shutdown server started', extra={'component': 'shutdown'})

# --- Shutdown thread ---
def _start_shutdown_thread():
    def worker():
        try:
            connections_logger.info("Shutdown thread: aloitetaan plug_off-sekvenssi")
            plug_off()
        except Exception:
            connections_logger.exception("Shutdown thread: virhe plug_off-sekvenssissä")
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# --- HTTP endpoint ---
@app.route("/shutdown", methods=["POST"])
def http_shutdown():
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        connections_logger.exception("Virhe lukemassa JSONia")
        return jsonify({"ok": False, "error": "invalid_json"}), 400

    if data.get("cmd") != "shutdown":
        return jsonify({"ok": False, "error": "invalid_cmd"}), 400

    connections_logger.info("HTTP shutdown: vastaanotettu, käynnistetään sekvenssi")
    _start_shutdown_thread()
    return jsonify({"ok": True, "message": "shutdown started"}), 202

# --- Käynnistys ---
def run_shutdown_server():
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == "__main__":
    run_shutdown_server()
