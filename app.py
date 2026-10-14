from flask import Flask, jsonify, render_template_string, request

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


# Part 3: the fine-checker page that members actually use
PAGE = """<!doctype html>
<title>QuackLoan fine checker</title>
<h1>QuackLoan fine checker</h1>
<form>
  <label>Days late <input name="days" type="number" min="0"></label>
  <label><input name="deluxe" type="checkbox" value="1">
    Deluxe duck</label>
  <button>Check fine</button>
</form>
{% if fee is not none %}
<p role="status">Your fine is ${{ "%.2f" % fee }}</p>
{% endif %}
"""


@app.get("/")
def checker():
    days = request.args.get("days", type=int)
    deluxe = request.args.get("deluxe") == "1"
    fee = None
    if days is not None and days >= 0:
        fee = DuckFine("quote").charge(days, deluxe=deluxe)
    return render_template_string(PAGE, fee=fee)


if __name__ == "__main__":
    app.run(debug=True)
