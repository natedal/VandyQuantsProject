from calculations import *;

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    plot_url = None
    if request.method == 'POST':
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])
        option_type = request.form['option_type']
        price = black_scholes(S, K, T, r, sigma, option_type)
        plot_url = plot_lognormal(S, r, sigma, T)
    return render_template('index.html', price=price, plot_url=plot_url)


if __name__ == '__main__':
    app.run()