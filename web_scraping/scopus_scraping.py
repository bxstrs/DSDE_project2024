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

# Function to fetch research papers
def fetch_research_papers(query, max_results=1000, results_per_request=25):
    all_papers = []
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

            # Extract relevant information
            for item in entries:
                paper = {
                    "Title": item.get("dc:title", ""),
                    "Authors": item.get("dc:creator", ""),
                    "Publication Name": item.get("prism:publicationName", ""),
                    "Year": item.get("prism:coverDate", "").split("-")[0],
                    "DOI": item.get("prism:doi", ""),
                    "Citation Count": item.get("citedby-count", 0),
                    "Keywords": item.get("authkeywords", ""),
                    "Abstract": item.get("dc:description", ""),  # Abstract of the paper
                    "Subject Areas": item.get("subj-area-abbrev", []),  # Abbreviated subject areas
                    "Index Terms": item.get("idxterms", ""),  # Index terms
                    "Link": item.get("link", [{}])[0].get("@href", "")  # Link to paper
                }
                all_papers.append(paper)

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
query = query = (
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
df = pd.DataFrame(papers)
df.to_csv(r"C:/desktop/workspace/university/dsde/DSDE_project2024/web_scraping/scopus_trend_2017.csv", index=False)

print(f"Scraped {len(papers)} research papers. Data saved to 'scopus_research_papers.csv'.")


