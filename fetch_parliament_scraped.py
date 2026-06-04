import os
import requests
from bs4 import BeautifulSoup

def scrape_committee_evidence(url: str):
    """Scrapes public evidence submissions listed on the UK Parliament committee index."""
    output_folder = "unprocessed_docs"
    os.makedirs(output_folder, exist_ok=True)
    
    headers = {'User-Agent': 'AlgorithmicHarmAuditProject/1.0 (Academic Content Analysis Tool)'}
    
    print(f"Requesting public HTML content from: {url}")
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code != 200:
        print(f"Failed to access page. Status: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Target common structural components containing evidence links or summary items
    evidence_blocks = soup.find_all('div', class_='written-evidence-item') or soup.find_all('li', class_='evidence-list-item')
    
    if not evidence_blocks:
        # Fallback: find standard anchor tags containing evidence reference keywords
        evidence_blocks = [a.find_parent() for a in soup.find_all('a') if 'evidence' in str(a.get('href')).lower()][:15]
        
    if not evidence_blocks:
        print("Could not isolate specific CSS evidence nodes. Scraping paragraph elements instead...")
        evidence_blocks = soup.find_all('p')[:15]

    print(f"Isolating text chunks from {len(evidence_blocks)} page structures...")
    
    for idx, block in enumerate(evidence_blocks, start=1):
        text_payload = block.text.strip()
        if len(text_payload) < 100:  # Skip trivial layout strings or empty blocks
            continue
            
        doc_id = f"UK-PARL-SCRAPE-{idx:03d}"
        file_path = os.path.join(output_folder, f"{doc_id}.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_payload)
            
    print(f"Scrape sequence completed. Text targets written to '{output_folder}/'.")

if __name__ == "__main__":
    # Example target: Work and Pensions Committee inquiry page focusing on benefit systems or fraud detection
    SAMPLE_TARGET = "https://committees.parliament.uk/committee/135/work-and-pensions-committee/news/"
    scrape_committee_evidence(SAMPLE_TARGET)
