from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock data
mock_prices = {
    'AAPL': 150.00,
    'GOOG': 2800.00,
    'TSLA': 700.00,
    'AMZN': 3300.00
}

# Mock portfolio
portfolio = {
    'cash': 10000.00,
    'stocks': {}
}

@app.route('/')
def index():
    return render_template('index.html', prices=mock_prices, portfolio=portfolio)

@app.route('/buy', methods=['POST'])
def buy():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    price = mock_prices[symbol]
    total_cost = price * quantity

    if total_cost > portfolio['cash']:
        return "Not enough cash!", 400

    portfolio['cash'] -= total_cost
    portfolio['stocks'][symbol] = portfolio['stocks'].get(symbol, 0) + quantity

    return redirect(url_for('index'))

@app.route('/sell', methods=['POST'])
def sell():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])

    if symbol not in portfolio['stocks'] or portfolio['stocks'][symbol] < quantity:
        return "Not enough shares!", 400

    price = mock_prices[symbol]
    total_income = price * quantity

    portfolio['cash'] += total_income
    portfolio['stocks'][symbol] -= quantity

    if portfolio['stocks'][symbol] == 0:
        del portfolio['stocks'][symbol]

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()