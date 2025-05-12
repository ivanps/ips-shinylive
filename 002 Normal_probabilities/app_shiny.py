from shiny import App, ui, render
from scipy.integrate import quad
from math import exp

app_ui = ui.page_fluid(
    ui.h1("Normal Probability Calculator"),
    ui.input_numeric("mu", "Mean (μ):", 0, min=-1000, max=1000),
    ui.input_numeric("sigma", "Standard Deviation (σ):", 1, min=0.000001, max=1000),
    ui.input_numeric("x1", "x1 =", -10, min=-1000, max=1000),
    ui.input_numeric("x2", "x2 =", 10, min=-1000, max=1000),
    ui.output_text_verbatim("txt")
)

def normal_pdf(x, mu=0, sigma=1):
    # Compute the pdf for the normal distribution
    return 1 / (sigma * (2 * 3.14159265) ** 0.5) * exp(-((x - mu) ** 2) / (2 * (sigma ** 2)))

def integral_normal_pdf(x1=-10, x2=10, mu=0, sigma=1):
    return quad(normal_pdf, x1, x2, args=(mu, sigma))[0]

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"P({input.x1()} <= X <= {input.x2()}) = {integral_normal_pdf(input.x1(), input.x2(), input.mu(), input.sigma())}"

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()