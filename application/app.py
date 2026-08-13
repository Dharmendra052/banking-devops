from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "application": "Banking Application",
        "status": "UP",
        "version": "v1"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/accounts")
def accounts():
    return jsonify({
        "accounts": [
            {
                "id": 1001,
                "customer": "John",
                "balance": 50000
            },
            {
                "id": 1002,
                "customer": "David",
                "balance": 75000
            }
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
