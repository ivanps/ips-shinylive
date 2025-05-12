from shiny import App, ui, render
from scipy.integrate import quad
from math import exp
import matplotlib.pyplot as plt
import io
from shiny.types import ImgData

app_ui = ui.page_fluid(
    ui.h1("Normal Probability Calculator"),
    ui.input_numeric("mu", "Mean (μ):", 0, min=-1000, max=1000),
    ui.input_numeric("sigma", "Standard Deviation (σ):", 1, min=0.000001, max=1000),
    ui.input_numeric("x1", "x1 =", -10, min=-1000, max=1000),
    ui.input_numeric("x2", "x2 =", 10, min=-1000, max=1000),
    ui.output_text_verbatim("txt"),
    ui.output_plot("plot")  
)

def normal_pdf(x, mu=0, sigma=1):
    # Compute the pdf for the normal distribution
    return 1 / (sigma * (2 * 3.14159265) ** 0.5) * exp(-((x - mu) ** 2) / (2 * (sigma ** 2)))

def integral_normal_pdf(x1=-10, x2=10, mu=0, sigma=1):
    return quad(normal_pdf, x1, x2, args=(mu, sigma))[0]

# Function to plot the normal PDF and highlight the area between x1 and x2
def plot_normal_pdf(x1=-10, x2=10, mu=0, sigma=1):
    # Define the range for x values
    x = [mu - 4 * sigma + (8 * sigma / 999) * i for i in range(1000)]
    y = [normal_pdf(xi, mu, sigma) for xi in x]
    
    # Plot the normal PDF
    plt.plot(x, y, label='Normal PDF')
    
    # Fill the area between x1 and x2
    x_fill = [x1 + (x2 - x1) / 999 * i for i in range(1000)]
    y_fill = [normal_pdf(xi, mu, sigma) for xi in x_fill]
    plt.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='Area between x1 and x2')
    
    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title(f'Normal Distribution (mean={mu}, std dev={sigma})')
    plt.legend()
    
    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"P({input.x1()} <= X <= {input.x2()}) = {integral_normal_pdf(input.x1(), input.x2(), input.mu(), input.sigma())}"

    @output
    @render.plot
    def plot() -> ImgData:
        # Generate the plot and return it
        return plot_normal_pdf(input.x1(), input.x2(), input.mu(), input.sigma())

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()