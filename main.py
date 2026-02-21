import os
from dotenv import load_dotenv
 
# Load environment variables (like OPENAI_API_KEY) from your .env file
load_dotenv()
 
# Import our custom modules from the new architecture
from src.agents.outliner import generate_presentation_json
from src.agents.data_analyst import get_chart_data
from src.tools.chart_maker import create_chart_image
from src.tools.pptx_export import export_to_pptx
 
def main():
    print("🚀 Starting Presentation Agent Orchestrator...\n")
    # --------------------------------------------------------------
    # 1. Get User Input
    # --------------------------------------------------------------
    # You can eventually replace these with user inputs: input("Enter topic: ")
    topic = "Pitch for a new AI-powered CRM"
    context = "We are pitching to retail executives. Focus on how it reduces churn and increases sales."
    slide_count = 5
    # --------------------------------------------------------------
    # 2. Generate the Outline (The Brain)
    # --------------------------------------------------------------
    print(f"🧠 Generating {slide_count}-slide outline for: {topic}")
    presentation_data = generate_presentation_json(topic, context, slide_count)
    # Dictionary to keep track of generated chart images {slide_number: image_path}
    chart_images = {}
 
    # --------------------------------------------------------------
    # 3. Process Data Queries (The Skills)
    # --------------------------------------------------------------
    for slide in presentation_data.slides:
        if slide.layout_type == "chart_and_text" and slide.data_query:
            print(f"\n📊 Analyzing data for Slide {slide.slide_number}: '{slide.data_query}'")
            # A. AI generates the data points
            chart_data = get_chart_data(slide.data_query, context)
            # B. Python renders the chart (saving to the output folder)
            # Assuming you run this script from inside the 'src' directory
            image_filename = f"../output/chart_slide_{slide.slide_number}.png"
            img_path = create_chart_image(chart_data, filename=image_filename)
            # C. Store the path so the exporter can find it later
            chart_images[slide.slide_number] = img_path
            print(f"   ✅ Chart saved to: {img_path}")
 
    # --------------------------------------------------------------
    # 4. Export to PowerPoint (The Exporter)
    # --------------------------------------------------------------
    output_file = "../output/AI_CRM_Pitch.pptx"
    print(f"\n🎬 Exporting presentation to {output_file}...")
    # We pass the chart_images dictionary to the exporter
    export_to_pptx(presentation_data, chart_images, output_filename=output_file)
    print("\n🎉 All done! Check your 'output' folder for the final files.")
 
if __name__ == "__main__":
    main()