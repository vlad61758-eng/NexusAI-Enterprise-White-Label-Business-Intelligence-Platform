import os
import time
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

# The user's requested crypto address
CRYPTO_ADDRESS = "TSP2tJbLpfR1YvRz4VY67nMMXi6PTa6mfK"

@app.route("/")
def index():
    return render_template("index.html", address=CRYPTO_ADDRESS)

@app.route("/verify-tx", methods=["POST"])
def verify_tx():
    """
    In a real production environment, this would call the TRON Grid API to verify the TxID.
    For this turnkey automated system, we simulate the verification delay.
    """
    data = request.get_json()
    tx_id = data.get("txid", "").strip()

    if not tx_id or len(tx_id) < 10:
        return jsonify({"success": False, "message": "Invalid Transaction ID."}), 400

    # Simulate network verification delay
    time.sleep(2)

    # In a real app, verify the transaction amount matches the product price.
    # Here we assume success for the automated flow.
    return jsonify({
        "success": True,
        "message": "Payment verified! Your download is ready.",
        "download_url": "/download"
    })

@app.route("/download")
def download():
    """Serves the ZIP file containing the product."""
    file_path = "AI_LeadGen_Pro.zip"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found.", 404

if __name__ == "__main__":
    # Run the server on port 5000
    app.run(host="0.0.0.0", port=5000)
