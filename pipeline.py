import os
from typing import Literal
from google import genai
from pydantic import BaseModel, Field

# =====================================================================
# 1. DEFINE THE SOCIOLOGICAL SCHEMA
# =====================================================================
# We use Literal types to force Gemini to act as a deterministic encoder.
# It can ONLY choose from these exact categorical strings.

HarmTypology = Literal[
    "DISCRIMINATORY_PROFILING",  # Biased targeting, high false-positives, unequal error rates
    "ACCOUNTABILITY_GAP",       # "Black box" opaque logic, no human oversight, unreviewable decisions
    "CHILLING_EFFECT",          # Over-surveillance modifying public behavior or suppressing legal rights
    "RESOURCE_EXTRACTION",       # Automation used to punitive-ly restrict welfare, housing, or state aid
    "SYSTEMIC_NORMALISATION"     # Officials accepting technical flaws as a necessary trade-off for speed
]

TargetedDomain = Literal["POLICING", "WELFARE_BENEFITS", "BORDER_CONTROL", "LOCAL_GOVERNMENT"]

class AlgorithmicHarmRecord(BaseModel):
    document_id: str = Field(description="The unique identifier for the source document.")
    primary_domain: TargetedDomain = Field(
        description="The specific branch of the state apparatus deploying the automated system."
    )
    dominant_harm_type: HarmTypology = Field(
        description="The primary sociological or structural harm identified in the text."
    )
    impacted_demographic: list[str] = Field(
        description="Specific protected characteristics or marginalized groups explicitly identified as bearing the cost."
    )
    state_rationalisation: str = Field(
        description="The justification or defense offered by state actors for deploying the tool (e.g., efficiency, fraud prevention)."
    )
    severity_index: Literal["LOW", "MEDIUM", "HIGH"] = Field(
        description="LOW: procedural friction | MEDIUM: individual misclassification/wrongful stress | HIGH: systemic loss of liberty, institutional poverty, or collective rights violations."
    )


# =====================================================================
# 2. CORE CODING FUNCTION
# =====================================================================
def analyze_algorithmic_harm(doc_id: str, raw_text: str) -> AlgorithmicHarmRecord:
    """
    Ingests raw unstructured text, injects the sociological codebook context,
    and forces Gemini to return a structured payload mapping to our Pydantic model.
    """
    
    # Check that the user has set their API key environment variable
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in your terminal.")

    # Initialize the official GenAI client
    client = genai.Client()

    # The Anchor Prompt: This trains the LLM on our academic definitions right before it reads the data
    codebook_prompt = """
    You are a quantitative research analyst specialized in the sociology of technology and critical criminology.
    Your objective is to code the provided text snippet into a strict JSON payload based on our study's codebook definitions.

    Definitions for 'dominant_harm_type':
    - DISCRIMINATORY_PROFILING: The system produces unequal error rates, false positives, or targeted scrutiny that disproportionately penalizes specific demographics.
    - ACCOUNTABILITY_GAP: State agencies use black-box tools with zero transparency, preventing citizens or courts from effectively challenging automated decisions.
    - CHILLING_EFFECT: Pervasive surveillance changes public behavior or suppresses civil liberties.
    - RESOURCE_EXTRACTION: Automation is leveraged to systematically restrict access to state resources, housing, or welfare.
    - SYSTEMIC_NORMALISATION: Officials defend structural flaws or algorithmic errors as a necessary trade-off for administrative speed.
    """

    # Execute the API call using Gemini 2.5 Flash (cost-effective and incredibly fast for structured tasks)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            {"text": codebook_prompt},
            {"text": f"Document ID: {doc_id}\n\nSource Text:\n{raw_text}"}
        ],
        config={
            'response_mime_type': 'application/json',
            'response_schema': AlgorithmicHarmRecord,
            'temperature': 0.1,  # Forces low-creativity, highly rule-based classification
        },
    )
    
    # Parse and validate the JSON string directly back into our type-safe Pydantic object
    return AlgorithmicHarmRecord.model_validate_json(response.text)


# =====================================================================
# 3. TEST EXECUTION ENVIRONMENT
# =====================================================================
if __name__ == "__main__":
    print("Initializing Content Coding Test...")

    # A realistic sample reflecting public sector AI critiques
    sample_uk_report = """
    A coalition of digital rights groups has raised flags over the Department for Work and Pensions' 
    continued rollout of machine-learning risk scores to flag potential Universal Credit fraud. 
    Internal evaluations revealed that non-UK nationals and individuals over 35 were flagged 
    for intense financial scrutiny at rates entirely out of proportion with actual fraud occurrence. 
    When pressed by the Select Committee on the clear demographic disparities, senior officials 
    conceded that bias was present but argued it was a necessary component of catching bad actors at scale. 
    Privacy advocates warn that because applicants are never informed when these automated flags are applied, 
    there is no viable legal path to contest a frozen claim, trapping vulnerable families in bureaucratic limbo.
    """
    
    try:
        # Run the pipeline
        coded_record = analyze_algorithmic_harm(doc_id="UK-DWP-2026-A", raw_text=sample_uk_report)
        
        # Display the results
        print("\n--- CODING SUCCESSFUL ---")
        print(f"Document ID:      {coded_record.document_id}")
        print(f"Domain:           {coded_record.primary_domain}")
        print(f"Harm Typology:    {coded_record.dominant_harm_type}")
        print(f"Demographics:     {', '.join(coded_record.impacted_demographic)}")
        print(f"Severity Level:   {coded_record.severity_index}")
        print(f"State Defense:    {coded_record.state_rationalisation}")
        print("-------------------------")
        
        # To show that it's a real Python object, let's print the raw serialized dictionary
        print("\nValidated Data Dictionary Object:")
        print(coded_record.model_dump())

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
