import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
 
# Import the Pydantic schema from your schemas folder
from src.schemas.presentation import PresentationOutline
 
def generate_presentation_json(topic: str, context: str, slide_count: int) -> PresentationOutline:
    """
    Takes a topic and context, and uses Azure OpenAI to generate a structured presentation outline.
    """
    # 1. Initialize the Azure LLM
    # LangChain automatically pulls AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT from your .env
    llm = AzureChatOpenAI(
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        #azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        temperature=0.2,
        max_retries=2
    )
    # 2. Bind the Pydantic schema to force strict structured output
    structured_llm = llm.with_structured_output(PresentationOutline)
 
    # 3. Create the Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert presentation designer and storyteller. 
        Your job is to take a user's topic and context, and outline a highly persuasive, 
        logical presentation. 
        Keep slide text concise (people don't read walls of text).
        Put the detailed explanations in the speaker notes.
        If a slide requires data visualization or proof, assign it the 'chart_and_text' layout 
        and write a clear 'data_query' for a web searcher to find the stats."""),
        ("user", "Topic: {topic}\nContext: {context}\nNumber of Slides: {slide_count}")
    ])
 
    # 4. Build the chain and execute
    chain = prompt | structured_llm
    print(f"🧠 Outliner Agent is structuring {slide_count} slides for: '{topic}'...")
    result = chain.invoke({
        "topic": topic,
        "context": context,
        "slide_count": slide_count
    })
    return result
 
# --------------------------------------------------------------
# Optional: Quick local testing block
# --------------------------------------------------------------
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Load your .env variables
    test_topic = "Pitch for a new AI-powered CRM"
    test_context = "Pitching to retail executives. Focus on reducing churn."
    print("Testing Outliner Agent with Azure OpenAI...\n")
    try:
        outline = generate_presentation_json(test_topic, test_context, 3)
        print("\n✅ Success! Here is the structured output:\n")
        print(outline.model_dump_json(indent=2))
    except Exception as e:
        print(f"\n❌ Error connecting to Azure: {e}")