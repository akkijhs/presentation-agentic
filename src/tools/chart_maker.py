import os
import matplotlib.pyplot as plt
 
# Import the Pydantic schema from your schemas folder
from src.agents.data_analyst import ChartData
 
def create_chart_image(chart_data: ChartData, filename: str = "../output/temp_chart.png") -> str:
    """
    Takes structured ChartData and renders a bar chart using Matplotlib.
    Saves the chart as a transparent PNG so it blends perfectly into PowerPoint slides.
    """
    # 1. Ensure the output directory exists so the script doesn't crash on save
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"🎨 Chart Maker is rendering: '{chart_data.chart_title}'...")
 
    # 2. Set up the figure with slide-friendly proportions (Width, Height in inches)
    fig, ax = plt.subplots(figsize=(6, 4))
    # 3. Create the bar chart
    # Using a clean, professional corporate blue color
    bars = ax.bar(chart_data.x_labels, chart_data.y_values, color='#4F81BD', edgecolor='none')
    # 4. Add labels and title
    ax.set_title(chart_data.chart_title, fontsize=14, pad=15, fontweight='bold')
    ax.set_ylabel(chart_data.y_axis_label, fontsize=11, labelpad=10)
    # 5. Clean up the aesthetics (Remove top and right borders for a modern look)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    # Add subtle grid lines behind the bars to make values easier to read
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    # Ensure bars sit on top of the grid lines
    for bar in bars:
        bar.set_zorder(3)
 
    # 6. Save the image with high resolution and a transparent background
    plt.tight_layout()
    plt.savefig(
        filename, 
        transparent=True, # Crucial for PowerPoint integration
        dpi=300           # High resolution so it doesn't look pixelated on big screens
    )
    # Free up memory to prevent slowdowns if generating massive decks
    plt.close(fig)
    return filename
 
# --------------------------------------------------------------
# Optional: Quick local testing block
# --------------------------------------------------------------
if __name__ == "__main__":
    # Create mock data mimicking what the LLM would output
    mock_data = ChartData(
        chart_title="Projected Revenue Growth",
        x_labels=["Q1", "Q2", "Q3", "Q4"],
        y_values=[1.2, 2.5, 3.8, 5.1],
        y_axis_label="Revenue ($M)"
    )
    print("Testing Chart Maker tool...\n")
    try:
        # Save it into the output folder relative to this script
        test_filename = "../../output/test_chart.png"
        saved_path = create_chart_image(mock_data, filename=test_filename)
        print(f"\n✅ Success! Chart saved to: {os.path.abspath(saved_path)}")
    except Exception as e:
        print(f"\n❌ Error generating chart: {e}")