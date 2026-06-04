import os
import requests

def query_hansard_debates(api_key: str, search_term: str):
    """Queries Hansard parliamentary transcripts via TheyWorkForYou API."""
    output_folder = "unprocessed_docs"
    os.makedirs(output_folder, exist_ok=True)
    
    # API Endpoint for searching parliamentary speeches
    url = "https://www.theyworkforyou.com/api/getDebates"
    
    params = {
        'key': api_key,
        'search': search_term,
        'output': 'json'
    }
    
    print(f"Querying Hansard records for term: '{search_term}'...")
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code != 200:
        print(f"API Error. Status: {response.status_code}")
        return
        
    data = response.json()
    rows = data.get('rows', [])
    
    if not rows:
        print(f"No speech records found for '{search_term}'.")
        return
        
    print(f"Found {len(rows)} statements. Extracting to text records...")
    for idx, speech in enumerate(rows[:20], start=1):  # Cap at 20 results per search term
        speaker = speech.get('speaker', {}).get('name', 'Unknown_MP').replace(" ", "_")
        gid = speech.get('gid', f'speech_{idx}')
        body_text = speech.get('body', '').replace('<b>', '').replace('</b>', '') # Clean HTML tags
        
        doc_id = f"HANSARD-{gid[:20]}_{speaker}"
        
        document_content = f"Speaker: {speech.get('speaker', {}).get('name')}\nContext: {speech.get('parent', {}).get('body')}\n\nSpeech Text:\n{body_text}"
        
        file_path = os.path.join(output_folder, f"{doc_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(document_content)
            
    print(f"Successfully downloaded Hansard records for '{search_term}'.")

if __name__ == "__main__":
    # Retrieve the key from your environment variables
    TWFY_API_KEY = os.environ.get("TWFY_API_KEY")
    
    if not TWFY_API_KEY:
        print("[WARNING] Please export your TWFY_API_KEY to run the live Hansard stream.")
        # Placeholder indicator for your article text:
        print("Skipping download... Add key to execute.")
    else:
        # Example search terms heavily relevant to critical criminology / algorithmic accountability
        query_hansard_debates(TWFY_API_KEY, search_term="facial recognition")
