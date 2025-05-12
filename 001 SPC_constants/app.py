from shiny.express import input, render, ui
from scipy.stats import norm
from scipy.integrate import quad
from scipy.special import gammaln
from numpy import exp

def compute_d2(n):
    def integrand(x):
        return 1 - (1 - norm.cdf(x)) ** n - (norm.cdf(x)) ** n

    result, _ = quad(integrand, -float('inf'), float('inf'))
    return result

def compute_c4(n):
    gamma_ratio = exp(gammaln(n / 2) - gammaln((n - 1) / 2))
    return ((2 / (n - 1))**0.5) * gamma_ratio
    
def f(n, x, y):
    Phi_x = norm.cdf(x)
    Phi_y = norm.cdf(y)
    return 1 - Phi_y**n - (1 - Phi_x) ** n + (Phi_y - Phi_x) ** n
    
def inner_integral(n, y):
    result, _ = quad(lambda x: f(n, x, y), -float('inf'), y)
    return result
    
def compute_d3(n):
    outer_integral_value, _ = quad(lambda y: inner_integral(n, y), -float('inf'), float('inf'))
    result = (2 * outer_integral_value - compute_d2(n)**2)**0.5
    return result

ui.h1("Shewhart control charts constants")
ui.input_numeric("n", "Select the group sample size:", 5, min=2, max=100)

@render.code
def txt():
    return f"c4 = {compute_c4(input.n())}\nd2 = {compute_d2(input.n())}\nd3 = {compute_d3(input.n())}"