from download_pdf.download_pipeline import *
import json

with open("./openalex_dois.json") as f:
    list_dois = json.load(f)

for doi in list_dois:
    if not doi:
        pass
    pdf_download_pipeline(doi,"./")
    break