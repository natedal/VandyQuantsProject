import matplotlib
import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering
import matplotlib.pyplot as plt
import io
import base64


def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculates the Black-Scholes option price.

    Parameters:
    - S: Current stock price
    - K: Strike price
    - T: Time to expiration in years
    - r: Risk-free interest rate
    - sigma: Volatility of the underlying asset
    - option_type: 'call' or 'put'

    Returns:
    - Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return price

def plot_lognormal(S, r, sigma, T):
    mu = (r - 0.5 * sigma ** 2) * T + np.log(S)
    sigma_t = sigma * np.sqrt(T)
    s = np.linspace(0.01 * S, 3 * S, 500)
    pdf = (1 / (s * sigma_t * np.sqrt(2 * np.pi))) * \
          np.exp(- (np.log(s) - mu) ** 2 / (2 * sigma_t ** 2))

    fig, ax = plt.subplots()
    ax.plot(s, pdf)
    ax.set_xlabel('Stock Price at Expiration')
    ax.set_ylabel('Probability Density')
    ax.set_title('Lognormal Distribution of Stock Price at Expiration')

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    fig.savefig(pngImage, format='png')
    pngImage.seek(0)
    pngData = base64.b64encode(pngImage.getvalue()).decode('ascii')
    plt.close(fig)  # Close the figure to free up memory
    return pngData

def binomial_option_pricing(S, K, T, r, sigma, N, option_type='call'):
    """
    Calculates the Binomial option price.

    Parameters:
    - S: Current stock price
    - K: Strike price
    - T: Time to expiration in years
    - r: Risk-free interest rate
    - sigma: Volatility of the underlying asset
    - N: Number of time steps
    - option_type: 'call' or 'put'

    Returns:
    - Option price
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # Initialize asset prices at maturity
    ST = np.zeros(N + 1)
    for i in range(N + 1):
        ST[i] = S * (u ** (N - i)) * (d ** i)
    
    # Initialize option values at maturity
    if option_type == 'call':
        option_values = np.maximum(0, ST - K)
    elif option_type == 'put':
        option_values = np.maximum(0, K - ST)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Backward induction to calculate option price
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            option_values[i] = (p * option_values[i] + (1 - p) * option_values[i + 1]) * discount

    return option_values[0]