import gradio as gr
import math
import matplotlib.pyplot as plt
import io


def calculate_pipe_diameter(flow_rate, velocity):
    # Convert flow rate from liters/sec to m^3/sec
    flow_rate_m3s = flow_rate / 1000

    # Area = Q / V
    area = flow_rate_m3s / velocity

    # Diameter = sqrt(4 * A / pi)
    diameter_m = math.sqrt(4 * area / math.pi)

    # Convert to mm
    diameter_mm = diameter_m * 1000
    return round(diameter_mm, 2), diameter_m


def plot_pipe(diameter_m):
    fig, ax = plt.subplots()
    circle = plt.Circle((0.5, 0.5), diameter_m / 2, color='blue', alpha=0.3)
    ax.add_patch(circle)
    ax.set_aspect('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f"Pipe Diameter: {round(diameter_m*1000, 2)} mm")
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def pipe_size_app(flow_rate, velocity):
    diameter_mm, diameter_m = calculate_pipe_diameter(flow_rate, velocity)
    img_buf = plot_pipe(diameter_m)
    return diameter_mm, img_buf


iface = gr.Interface(
    fn=pipe_size_app,
    inputs=[
        gr.Number(label="Flow Rate (liters/sec)"),
        gr.Number(label="Permissible Velocity (m/sec)")
    ],
    outputs=[
        gr.Number(label="Recommended Pipe Diameter (mm)"),
        gr.Image(type="pil", label="Pipe Visualization")
    ],
    title="Pipe Size Helper",
    description="Enter the flow rate and permissible velocity to get the recommended pipe diameter and a visualization."
)

if __name__ == "__main__":
    iface.launch()
