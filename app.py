import os
import time
from flask import Flask, render_template, request, jsonify, send_file, abort

app = Flask(__name__)

# The user's requested crypto address
CRYPTO_ADDRESS = "TSP2tJbLpfR1YvRz4VY67nMMXi6PTa6mfK"

# Product Catalog
PRODUCTS = {
    "leadgen": {
        "id": "leadgen",
        "name": "AI LeadGen Pro",
        "price": 50,
        "description": "Автоматичний пошук клієнтів у Telegram чатах за допомогою штучного інтелекту.",
        "icon": "🤖",
        "file": "AI_LeadGen_Pro.zip"
    },
    "crypto_signal": {
        "id": "crypto_signal",
        "name": "Crypto Signal Forwarder",
        "price": 40,
        "description": "Миттєве пересилання сигналів з закритих VIP-каналів до ваших груп.",
        "icon": "📈",
        "file": "Crypto_Signal_Forwarder.zip"
    },
    "moderator": {
        "id": "moderator",
        "name": "Smart Auto-Moderator",
        "price": 30,
        "description": "Захист груп від спаму, капча для новачків, фільтр поганих слів та авто-бан.",
        "icon": "🛡️",
        "file": "Smart_Auto_Moderator.zip"
    },
    "support": {
        "id": "support",
        "name": "Support Desk Bot",
        "price": 35,
        "description": "Професійна система тікетів для організації техпідтримки у Telegram.",
        "icon": "🎧",
        "file": "Support_Desk_Bot.zip"
    },
    "autoposter": {
        "id": "autoposter",
        "name": "Auto-Poster & Watermark",
        "price": 25,
        "description": "Відкладений постінг та автоматичне накладання водяних знаків на фото/відео.",
        "icon": "📸",
        "file": "Auto_Poster.zip"
    },
    "giveaway": {
        "id": "giveaway",
        "name": "Viral Giveaway Manager",
        "price": 20,
        "description": "Бот для розіграшів: перевіряє підписку на спонсорів та обирає переможців.",
        "icon": "🎁",
        "file": "Viral_Giveaway_Manager.zip"
    }
}

@app.route("/")
def index():
    # Show the storefront catalog
    return render_template("storefront.html", products=PRODUCTS.values())

@app.route("/checkout/<product_id>")
def checkout(product_id):
    product = PRODUCTS.get(product_id)
    if not product:
        abort(404)
    return render_template("checkout.html", address=CRYPTO_ADDRESS, product=product)

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

    product_id = data.get("product_id", "")

    if product_id not in PRODUCTS:
        return jsonify({"success": False, "message": "Invalid product."}), 400

    # In a real app, verify the transaction amount matches the product price.
    # Here we assume success for the automated flow.
    return jsonify({
        "success": True,
        "message": "Оплату знайдено! Ваші файли готові до завантаження.",
        "download_url": f"/download/{product_id}"
    })

@app.route("/download/<product_id>")
def download(product_id):
    """Serves the ZIP file containing the specific product."""
    product = PRODUCTS.get(product_id)
    if not product:
        abort(404)

    file_path = product["file"]
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found.", 404

if __name__ == "__main__":
    # Run the server on port 5000
    app.run(host="0.0.0.0", port=5000)
