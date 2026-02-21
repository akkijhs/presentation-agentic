import matplotlib.pyplot as plt
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import AzureChatOpenAI
from pptx.util import Inches
import os
 
# --------------------------------------------------------------
# 1. Define the Data Schema for the Chart
# --------------------------------------------------------------
class ChartData(BaseModel):
    chart_title: str = Field(description="Title of the chart")
    x_labels: List[str] = Field(description="Labels for the X-axis (e.g., ['2023', '2024', '2025'])")
    y_values: List[float] = Field(description="Numerical values for the Y-axis (must match x_labels length)")
    y_axis_label: str = Field(description="What the Y-axis represents (e.g., 'Revenue in Millions')")
 
# --------------------------------------------------------------
# 2. The Data Analyst Agent (Extracts/Creates the Data)
# --------------------------------------------------------------
def get_chart_data(query: str, context: str) -> ChartData:
    print(f"📊 Data Agent is researching: '{query}'...")
    # Initialize the Azure LLM
    llm = AzureChatOpenAI(
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        #azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        temperature=0.2,
        max_retries=2
    )
    structured_llm = llm.with_structured_output(ChartData)
    # In a production app, you would pass web-search results into this context.
    # For now, the LLM will estimate logical data based on the prompt.
    prompt = f"""You are a data analyst. Based on this query: "{query}" and context: "{context}", 
    generate realistic and persuasive data for a bar chart. Keep it to 3-5 data points."""
    return structured_llm.invoke(prompt)
 
# --------------------------------------------------------------
# 3. The Matplotlib Renderer (Turns Data into a PNG)
# --------------------------------------------------------------
def create_chart_image(chart_data: ChartData, filename="temp_chart.png"):
    plt.figure(figsize=(6, 4)) # Standard slide-friendly proportions
    plt.bar(chart_data.x_labels, chart_data.y_values, color='#4F81BD')
    plt.title(chart_data.chart_title)
    plt.ylabel(chart_data.y_axis_label)
    # Save it transparently so it looks clean on any background
    plt.tight_layout()
    plt.savefig(filename, transparent=True, dpi=300)
    plt.close()
    return filename
 
# --------------------------------------------------------------
# 4. Updated Exporter Logic (Embedding the Chart)
# --------------------------------------------------------------
# Inside your previous `export_to_pptx` loop, update Step 6:
 
        # 6. Chart Logic
        # if slide_data.layout_type == "chart_and_text" and slide_data.data_query:
        #     
        #     # A. Agent gets the data
        #     chart_data = get_chart_data(slide_data.data_query, presentation_data.target_audience)
        #     
        #     # B. Python builds the image
        #     img_path = create_chart_image(chart_data)
        #     
        #     # C. Insert into PowerPoint
        #     # We position it on the right side of the slide
        #     left = Inches(5.0)  
        #     top = Inches(2.0)
        #     width = Inches(4.5)
        #     slide.shapes.add_picture(img_path, left, top, width=width