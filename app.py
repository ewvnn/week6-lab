from flask import Flask, jsonify, request

from duckfine import DuckFine

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/fine")
def fine():
    raw_days = request.args.get("days", "")
    try:
        days = int(raw_days)
    except ValueError:
        return jsonify(error="days must be a non-negative integer"), 400
    if days < 0:
        return jsonify(error="days must be a non-negative integer"), 400

    deluxe = request.args.get("deluxe") == "1"
    fee = DuckFine(member_id=None).charge(days, deluxe=deluxe)
    return jsonify(days=days, deluxe=deluxe, fee=fee)


if __name__ == "__main__":
    app.run(debug=True)
