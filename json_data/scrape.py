import json
import glob
import os
import pandas as pd

year_list = ['2018', '2019', '2020', '2021', '2022', '2023']
informations = []

for year in year_list:
    #path of raw data
    folder_path = f'C:/CEDT/Semester_3/2110403/project_data/{year}'
    file_list = glob.glob(f'{folder_path}/*')
    file_list = [os.path.normpath(file_path) for file_path in file_list]
    for file_path in file_list:
        try:
            file_path = file_path.replace("\\", "/")
            with open(file_path, 'r', encoding='utf-8') as file:
                print(f'{file_path} is in progress...')
                data = json.load(file)
                coredata = data['abstracts-retrieval-response']['coredata']

                info = {
                    "Title": coredata.get("dc:title", ""),
                    "Authors": ", ".join([author.get("ce:indexed-name", "") for author in coredata.get("dc:creator", {}).get("author", [])]),
                    "Publication Name": coredata.get("prism:publicationName", ""),
                    "Year": coredata.get("prism:coverDate", "").split("-")[0],
                    "DOI": coredata.get("prism:doi", ""),
                    "Citation Count": int(coredata.get("citedby-count")) if coredata.get("citedby-count") is not None else 0,
                    "Keywords": "; ".join([kw.get("$", "") for kw in data.get("authkeywords", {}).get("author-keyword", [])]),
                    "Abstract": coredata.get("dc:description", ""),
                    "Subject Areas": "; ".join([sa.get("$", "") for sa in data.get("subject-areas", {}).get("subject-area", [])]),
                    "Index Terms": "; ".join([term.get("$", "") for term in data.get("idxterms", {}).get("mainterm", [])]),
                    "Link": coredata.get("link", [{}])[-1].get("@href", "")  # Get the last link
                }
                informations.append(info)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing file {file_path}: {e}")

if informations:
    title = pd.DataFrame(informations)
    #path of exported file
    output_path2 = 'C:/CEDT/Semester_3/2110403/project_data/information.csv'
    title.to_csv(output_path2, index=False, encoding='utf-8')
    print(f'Information data successfully exported to {output_path2}')
else:
    print('No Information data to export')
