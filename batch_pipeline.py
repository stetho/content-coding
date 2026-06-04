import os
import time
import csv
from typing import Literal
from google import genai
from pydantic import BaseModel, Field

# =====================================================================
# 1. THE ARCHITECTURE (SCHEMA & DEFINITIONS)
# =====================================================================
HarmTypology = Literal[
    "DISCRIMINATORY_PROFILING", "ACCOUNTABILITY_GAP", 
    "CHILLING_EFFECT", "RESOURCE_EXTRACTION", "SYSTEMIC_NORMALISATION"
]

TargetedDomain = Literal["POLICING", "WELFARE_BENEFITS", "BORDER_CONTROL", "LOCAL_GOVERNMENT"]

class AlgorithmicHarmRecord(BaseModel):
    document_id: str
    primary_domain: TargetedDomain
    dominant_harm_type: HarmTypology
    impacted_demographic: list[str]
    state_rationalisation: str
    severity_index: Literal["LOW", "MEDIUM", "HIGH"]


# =====================================================================
# 2. CORE RUNTIME ENGINE
# =====================================================================
def analyze_algorithmic_harm(doc_id: str, raw_text: str) -> AlgorithmicHarmRecord:
    """Sends a single text payload to Gemini using strict Pydantic schemas."""
    client = genai.Client()

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

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            {"text": codebook_prompt},
            {"text": f"Document ID: {doc_id}\n\nSource Text:\n{raw_text}"}
        ],
        config={
            'response_mime_type': 'application/json',
            'response_schema': AlgorithmicHarmRecord,
            'temperature': 0.1, 
        },
    )
    return AlgorithmicHarmRecord.model_validate_json(response.text)


# =====================================================================
# 3. BATCH PROCESSING WRAPPER
# =====================================================================
def run_batch_pipeline(input_folder: str, output_csv: str):
    """Loops through a directory of text files, processes them, and writes a CSV."""
    
    # Ensure the input directory actually exists
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"Created empty directory: '{input_folder}/'")
        print("Please drop some sample .txt files in there and re-run the script.")
        return

    # Find all text files in the folder
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    
    if not all_files:
        print(f"No .txt files found in '{input_folder}/'. Add files to process them.")
        return

    print(f"Found {len(all_files)} documents to analyze. Starting pipeline...")
    
    results = []

    for idx, file_name in enumerate(all_files, start=1):
        file_path = os.path.join(input_folder, file_name)
        doc_id = os.path.splitext(file_name)[0]  # Use file name without extension as Doc ID
        
        print(f"[{idx}/{len(all_files)}] Processing: {file_name}...", end="", flush=True)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()

            # Execute API Analysis
            record = analyze_algorithmic_harm(doc_id=doc_id, raw_text=raw_text)
            
            # Convert Pydantic object to a flat dictionary for easy CSV output
            flat_record = record.model_dump()
            # Convert the list of demographics into a single comma-separated string for the CSV column
            flat_record['impacted_demographic'] = ", ".join(flat_record['impacted_demographic'])
            
            results.append(flat_record)
            print(" Success ✅")
            
            # Rate limiting safety valve: sleep for 2 seconds to respect Gemini Free Tier limits
            time.sleep(2)
            
        except Exception as e:
            print(f" FAILED ❌ (Error: {e})")
            print("Continuing to next file...")

    # Write the results out to disk as a structured CSV dataset
    if results:
        fieldnames = ["document_id", "primary_domain", "dominant_harm_type", "impacted_demographic", "state_rationalisation", "severity_index"]
        
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            
        print(f"\nPipeline complete! Dataset successfully saved to: {output_csv}")
    else:
        print("\nPipeline finished but zero documents were successfully processed.")


if __name__ == "__main__":
    # Define our inputs and outputs
    INPUT_DIR = "unprocessed_docs"
    OUTPUT_FILE = "algorithmic_harm_dataset.csv"
    
    run_batch_pipeline(input_folder=INPUT_DIR, output_csv=OUTPUT_FILE)
