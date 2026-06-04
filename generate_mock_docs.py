import os

def create_mock_research_corpus():
    output_folder = "unprocessed_docs"
    os.makedirs(output_folder, exist_ok=True)
    
    # A curated set of highly realistic qualitative scenarios mapping to our criminology domain
    corpus = {
        "UK-HO-BORDER-01": (
            "An investigation into the Home Office e-gates rollout at London Heathrow revealed a hidden "
            "automation bias within the passport verification algorithm. The machine-learning model, trained "
            "predominantly on high-contrast European passport photos, demonstrated a 14% higher rejection rate "
            "for passengers with darker skin tones and non-Western naming conventions. When individual travelers "
            "attempted to appeal their automated detention, border agents stated they had no administrative visibility "
            "into the 'black box' system scoring matrix, creating a permanent accountability gap where travelers "
            "were held in custody without clear procedural recourse."
        ),
        "UK-DWP-FRAUD-02": (
            "The Department for Work and Pensions expanded its automated fraud detection algorithms to cross-reference "
            "banking transaction history for Universal Credit applicants over the age of 50. Internal communications "
            "confirm that the system flagged thousands of valid care payments as 'undisclosed illicit income' due to "
            "an error in the algorithmic classification rules. Senior officials defense argued that while the system "
            "produced occasional errors, sweeping automation was an absolute necessity to prevent fraud at scale and "
            "protect public revenue, normalizing a high rate of severe administrative friction for vulnerable claimants."
        ),
        "UK-MET-SURVEILLANCE-03": (
            "Civil liberties groups launched a legal challenge against regional police forces deploying automated "
            "Live Facial Recognition vans during public political demonstrations. The continuous biometric scanning "
            "of crowds led to a distinct chilling effect, where community advocates explicitly altered their public "
            "behaviors or avoided attending legal assemblies entirely due to fear of automated misidentification and "
            "subsequent wrongful arrest by the state apparatus."
        ),
        "UK-COUNCIL-HOUSING-04": (
            "A local council implemented an AI-driven predictive allocation system to triage applications for social "
            "housing support. Critical analysis showed that the model's underlying scoring rules penalized applicants "
            "from specific postcodes characterized by historic underinvestment, effectively turning the resource "
            "allocation software into a mechanism of punitive resource extraction that locked marginalized families "
            "out of state support infrastructure."
        )
    }
    
    print(f"Populating '{output_folder}/' directory with clean qualitative research texts...")
    
    for doc_id, text in corpus.items():
        file_path = os.path.join(output_folder, f"{doc_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f" Created: {doc_id}.txt")
        
    print("\nLocal corpus successfully generated! You are ready to run the batch pipeline.")

if __name__ == "__main__":
    create_mock_research_corpus()
