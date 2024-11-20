from calculations import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    plot_url = None
    S = K = T = r = sigma = option_type = model = N = None
    if request.method == 'POST':
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])
        option_type = request.form['option_type']
        model = request.form['model']
        if model == 'black_scholes':
            price = black_scholes(S, K, T, r, sigma, option_type)
        elif model == 'binomial':
            N = int(request.form['N'])
            price = binomial_option_pricing(S, K, T, r, sigma, N, option_type)
        plot_url = plot_lognormal(S, r, sigma, T)
    return render_template('index.html', price=price, plot_url=plot_url, S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type, model=model, N=N)

if __name__ == '__main__':
    app.run()