from pydantic import BaseModel, Field
from typing import List, Literal
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
 
# --------------------------------------------------------------
# 1. Define the Structured Schema (The "Blueprint")
# --------------------------------------------------------------
 
class Slide(BaseModel):
    slide_number: int = Field(description="The sequential number of the slide.")
    layout_type: Literal[
        "title_slide", 
        "title_and_content", 
        "two_column", 
        "chart_and_text"
    ] = Field(description="The suggested visual layout for this slide.")
    title: str = Field(description="The main headline of the slide. Should be punchy.")
    bullets: List[str] = Field(description="3 to 5 key points or sentences for the slide body.")
    speaker_notes: str = Field(description="Detailed script for the presenter to read.")
    data_query: str = Field(
        default="", 
        description="If layout is 'chart_and_text', describe what data needs fetching. Otherwise leave blank."
    )
 
class PresentationOutline(BaseModel):
    presentation_title: str = Field(description="The overall title of the deck.")
    target_audience: str = Field(description="Who this presentation is for.")
    slides: List[Slide] = Field(description="The sequence of slides.")
 
# --------------------------------------------------------------
# 2. Set Up the AI Agent
# --------------------------------------------------------------
 
def generate_presentation_json(topic: str, context: str, slide_count: int) -> PresentationOutline:
    # Initialize the LLM (Requires OPENAI_API_KEY in your environment variables)
    # We use a model with strong reasoning to ensure good narrative flow.
    llm = AzureChatOpenAI(
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        #azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        temperature=0.2,
        max_retries=2
    )

    response = llm.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # NOT model name
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
    # Bind the Pydantic schema to the LLM so it strictly outputs our format
    structured_llm = response.with_structured_output(PresentationOutline)
 
    # Create the Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert presentation designer and storyteller. 
        Your job is to take a user's topic and context, and outline a highly persuasive, 
        logical presentation. 
        Keep slide text concise (people don't read walls of text).
        Put the detailed explanations in the speaker notes.
        If a slide requires data validation, assign it the 'chart_and_text' layout and write a data_query."""),
        ("user", "Topic: {topic}\nContext: {context}\nNumber of Slides: {slide_count}")
    ])
 
    # Build the chain and execute
    chain = prompt | structured_llm
    print(f"🧠 Agent is thinking and structuring {slide_count} slides...")
    result = chain.invoke({
        "topic": topic,
        "context": context,
        "slide_count": slide_count
    })
    return result
 
# --------------------------------------------------------------
# 3. Test the Agent
# --------------------------------------------------------------
 
if __name__ == "__main__":
    test_topic = "Pitch for a new AI-powered CRM"
    test_context = "We are pitching to retail executives. Focus on how it reduces churn and increases sales."
    # Run the agent
    presentation_data = generate_presentation_json(test_topic, test_context, slide_count=5)
    # Output the structured JSON
    print("\n✅ Presentation Generated Successfully:\n")
    print(presentation_data.model_dump_json(indent=2))