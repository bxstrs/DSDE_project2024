import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

# API Key and Base URL
API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.elsevier.com/content/search/scopus"
HEADERS = {
    "X-ELS-APIKey": API_KEY,
    "Accept": "application/json"
}

# Load existing records to avoid duplicates
existing_csv = r"C:/desktop/workspace/university/dsde/DSDE_project2024/json_data/information.csv"  # Path to the file with existing records
if os.path.exists(existing_csv):
    existing_records = pd.read_csv(existing_csv)
    existing_dois = set(existing_records['DOI'].str.strip().str.lower())
else:
    existing_dois = set()

# Function to fetch research papers
def fetch_research_papers(query, max_results=2500, results_per_request=25):
    all_papers = []
    unique_dois = set(existing_dois)  # Track DOIs to avoid duplicates
    start = 0

    while len(all_papers) < max_results:
        # Define query parameters
        params = {
            "query": query,
            "sort": "citedby-count",
            "count": results_per_request,
            "start": start,
            "httpAccept": "application/json"
        }

        # Make API request
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()
            entries = data.get("search-results", {}).get("entry", [])

            # Extract and filter unique papers
            for item in entries:
                doi = item.get("prism:doi", "").strip().lower()  # Normalize DOI
                if doi and doi not in unique_dois:  # Add only unique DOIs
                    paper = {
                        "Title": item.get("dc:title", ""),
                        "Authors": item.get("dc:creator", ""),
                        "Publication Name": item.get("prism:publicationName", ""),
                        "Year": item.get("prism:coverDate", "").split("-")[0],
                        "DOI": doi,
                        "Citation Count": item.get("citedby-count", 0),
                        "Keywords": item.get("authkeywords", ""),
                        "Abstract": item.get("dc:description", ""),
                        "Subject Areas": item.get("subj-area-abbrev", []),
                        "Index Terms": item.get("idxterms", ""),
                        "Link": item.get("link", [{}])[0].get("@href", "")
                    }
                    all_papers.append(paper)
                    unique_dois.add(doi)  # Track new DOI

            # Update start index for next batch
            start += results_per_request

            # Break if no more results
            if len(entries) < results_per_request:
                break
        else:
            print(f"Error {response.status_code}: {response.text}")
            break

        # Respect API rate limits
        time.sleep(1)  # Wait 1 second between requests

    return all_papers

# Query and Fetch Papers
query = (
    'PUBYEAR > 2017 AND PUBYEAR < 2024 AND ('
    'TITLE("engineering") OR TITLE("machine learning") OR TITLE("data science") OR '
    'TITLE("economic") OR TITLE("sustainability") OR TITLE("cryptocurrency")'
    'OR TITLE("financial markets") OR TITLE("digital transformation")' 
    'OR TITLE("robotics") OR TITLE("internet of things") OR TITLE("IoT") '
    'OR TITLE("AI") OR TITLE("artificial intelligence") OR TITLE("machine learning") '
    'OR TITLE("sustainability") OR TITLE("renewable energy") OR TITLE("smart cities") ' 
    ')'
)

papers = fetch_research_papers(query, max_results=2500)

# Save to CSV
output_csv = r"C:/desktop/workspace/university/dsde/DSDE_project2024/web_scraping/scopus_trend_2018-2023.csv"
df = pd.DataFrame(papers)
df.to_csv(output_csv, index=False)

print(f"Scraped {len(papers)} unique research papers. Data saved to '{output_csv}'.")
