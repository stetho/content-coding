# Content Coding Pipeline for Algorithmic Harm Audit

A robust, enterprise-grade data engineering pipeline that implements academic qualitative content analysis paradigms at scale. By leveraging the **Gemini 2.5 Flash API** alongside **Pydantic structured schemas**, this framework enforces deterministic data validation on unstructured text corpora, transforming qualitative public records into type-safe, auditable relational datasets.

## 🌟 Overview & Philosophy

Modern public administration increasingly relies on automated decision-making (ADM) systems, machine-learning risk scores, and biometric surveillance frameworks. However, when these tools are deployed without multi-disciplinary oversight, they risk perpetuating structural inequality, introducing severe administrative friction, and creating profound democratic accountability vacuums.

To audit these socio-technical governance mechanisms, empirical research requires scale and reproducibility. Traditional qualitative text analysis relies on human researchers manually applying a strict set of rule-based classifications (a **Codebook**) to text—a process prone to cognitive exhaustion and subjectivity.

This repository bridges the gap between **software infrastructure design** and **critical criminology/sociology**. It treats a Large Language Model not as a conversational chatbot, but as a high-throughput, rule-bound data pipeline component. By combining an immutable cryptographic-style codebook context with strict JSON validation boundaries, the system locks down model creativity to produce deterministic, empirical data points out of unstructured political and journalistic prose.

---

## 🏗️ System Architecture

The project implements a decoupling architecture split into three distinct layers:

1. **Ingestion Layer:** Modular data harvesters designed to isolate qualitative narratives from diverse channels (e.g., public sector disclosures, civil society watchdog investigations, select committee transcripts) and land them as uniform `.txt` blocks in a standardized filesystem staging zone (`unprocessed_docs/`).
2. **Orchestration & Transformation Engine (`batch_pipeline.py`):** The programmatic core that establishes connection pooling with the Gemini API, loads the contextual codebook anchor, maps the theoretical definitions to strict data runtime structures, and handles rate-limiting safety valves.
3. **Storage Tier:** Flattens high-dimensional polymorphic nested JSON payloads directly into clean, normalized tabular datasets (`algorithmic_harm_dataset.csv`) optimized for downstream statistical modeling, database ingestion, or BI analytics.

```
[ Automated DOM Scraper ]       [ Global Failure Archives ]
(fetch_parliament_scraped.py)    (generate_mock_docs.py)
            │                               │
            └───────────────┬───────────────┘
                            ▼
                    [ unprocessed_docs/ ]  <── Isolated File Staging Area
                            │
                            ▼
                    [ batch_pipeline.py ]  <── Enforces Pydantic Schema & 0.1 Temp
                            │
                            ▼
              [ Gemini 2.5 Flash Engine ]  <── Deterministic Tokenizer
                            │
                            ▼
             [ algorithmic_harm_dataset.csv ] <── Type-Safe Auditable Relational File
```

---

## 🛠️ Data Modeling & Strict Typologies

To convert unstructured political rhetoric into database rows without absorbing textual bias, complex criminological theories are mapped directly into code as Python native `Literal` enums within a **Pydantic v2** model.

```python
from typing import Literal
from pydantic import BaseModel, Field

HarmTypology = Literal[
    "DISCRIMINATORY_PROFILING",  # Biased targeting, high false-positives, unequal error rates
    "ACCOUNTABILITY_GAP",       # "Black box" opaque logic, no human oversight, unreviewable decisions
    "CHILLING_EFFECT",          # Over-surveillance modifying public behavior or suppressing legal rights
    "RESOURCE_EXTRACTION",      # Automation used to punitively restrict welfare, housing, or state aid
    "SYSTEMIC_NORMALISATION"     # Officials accepting technical flaws as a necessary trade-off for speed
]

TargetedDomain = Literal["POLICING", "WELFARE_BENEFITS", "BORDER_CONTROL", "LOCAL_GOVERNMENT"]

class AlgorithmicHarmRecord(BaseModel):
    document_id: str = Field(description="Unique identifier for the source document.")
    primary_domain: TargetedDomain = Field(description="The branch of the state apparatus deploying the automated system.")
    dominant_harm_type: HarmTypology = Field(description="The primary sociological or structural harm identified.")
    impacted_demographic: list[str] = Field(description="Protected characteristics or marginalized groups explicitly identified as bearing the cost.")
    state_rationalisation: str = Field(description="The justification or defense offered by state actors for deploying the tool.")
    severity_index: Literal["LOW", "MEDIUM", "HIGH"] = Field(description="Scale of structural impact and rights violations.")
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* A valid Google AI Studio API Key (Free tier works perfectly)

### 1. Environment Setup & Dependency Installation
Isolate your workspace dependencies by spinning up a clean virtual environment:

```bash
# Clone the repository
git clone [https://github.com/stetho/content-coding.git](https://github.com/stetho/content-coding.git)
cd content-coding

# Initialize a custom named virtual environment
python3 -m venv algorithmic_harm_env

# Activate the environment
# On macOS/Linux:
source algorithmic_harm_env/bin/activate
# On Windows (PowerShell):
# .\\algorithmic_harm_env\\Scripts\\Activate.ps1

# Upgrade pip and install validated production requirements
pip install --upgrade pip
pip install google-genai pydantic beautifulsoup4 requests
```

### 2. Configure Your Environment Variables
The official Google GenAI SDK looks implicitly for a system environment variable named `GEMINI_API_KEY`. Avoid hardcoding credentials into scripts.

```bash
# Linux/macOS
export GEMINI_API_KEY="AIzaSyYourActualAPIKeyHere..."

# Windows (Command Prompt)
set GEMINI_API_KEY="AIzaSyYourActualAPIKeyHere..."

# Windows (PowerShell)
"$env:GEMINI_API_KEY="AIzaSyYourActualAPIKeyHere..."
```

### 3. Generate the Qualitative Staging Corpus
To bypass brittle public web application firewalls during testing, execute the mock data synthesizer to inject realistic, highly localized socio-technical narratives into your workspace:

```bash
python generate_mock_docs.py
```
*This command will create the `unprocessed_docs/` folder and populate it with four distinct case studies spanning DWP welfare fraud scorecards, Home Office automated border e-gates, metropolitan live facial recognition deployments, and algorithmic social housing triage.*

### 4. Execute the Ingestion and Coding Pipeline
Execute the master orchestration engine to process the staging directory sequentially through the validated AI infrastructure:

```bash
python batch_pipeline.py
```

### Expected Output Logs
```text
Initializing Content Coding Test...
Found 4 documents to analyze. Starting pipeline...
[1/4] Processing: UK-HO-BORDER-01... Success ✅
[2/4] Processing: UK-DWP-FRAUD-02... Success ✅
[3/4] Processing: UK-MET-SURVEILLANCE-03... Success ✅
[4/4] Processing: UK-COUNCIL-HOUSING-04... Success ✅

Pipeline complete! Dataset successfully saved to: algorithmic_harm_dataset.csv
```

---

## 📊 Sample Pipeline Transformation

### Unstructured Source Text Input (`UK-DWP-FRAUD-02.txt`)
> *"...Internal communications confirm that the system flagged thousands of valid care payments as 'undisclosed illicit income' due to an error in the algorithmic classification rules. Senior officials defense argued that while the system produced occasional errors, sweeping automation was an absolute necessity to prevent fraud at scale and protect public revenue, normalizing a high rate of severe administrative friction for vulnerable claimants."*

### Deterministic JSON Target Output (Generated Programmatically)
```json
{
  "document_id": "UK-DWP-FRAUD-02",
  "primary_domain": "WELFARE_BENEFITS",
  "dominant_harm_type": "SYSTEMIC_NORMALISATION",
  "impacted_demographic": ["Universal Credit applicants over the age of 50"],
  "state_rationalisation": "sweeping automation was an absolute necessity to prevent fraud at scale and protect public revenue",
  "severity_index": "HIGH"
}
```

The runtime flattens this schema into a persistent row inside `algorithmic_harm_dataset.csv`, transforming prose into clean, filterable database fields.

---

## 🔒 Architectural Engineering Highlights

* **Zero-Cost Rigorous Research Pattern:** Demonstrates how researchers and institutions can build a high-fidelity algorithmic auditing engine on a budget using `gemini-2.5-flash`'s competitive latency profile and extensive free tier.
* **Deterministic Configuration Guardrails:** The pipeline locks model temperature at `0.1` and passes descriptive codebook parameters directly into the configuration. This minimizes semantic drift, enforces strict type conformity across large batches, and eliminates hallucinated output schemas.
* **Network Fault & Rate Resilience:** Includes programmatic pacing variables (`time.sleep`) and structured exception handling routines, ensuring the processing orchestration manages systemic execution spikes gracefully without crashing midway through heavy data loops.

---

## 📄 License
This project is open-source and licensed under the MIT License.

