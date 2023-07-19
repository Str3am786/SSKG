
# Scientific Software Knowledge Graphs (SSKG)
README IN PROGRESS
## Introduction

This tool verifies the link between a scientific paper and a software repository. It accomplishes this by locating the URL of the software repository within the scientific paper. It then extracts the repository's metadata to find any URLs associated with scientific papers and checks if they lead back to the original paper. If a bidirectional link is established, it marks it as "bidirectional".

## Dependencies
- Python 3.9

## Usage

 Install the required dependencies by running:
```
pip install -r requirements.txt
```
Highly recommended steps:  

```text
somef configure
```
You will be asked to provide:

* A GitHub authentication token [**optional, leave blank if not used**], which SOMEF uses to retrieve metadata from GitHub. If you don't include an authentication token, you can still use SOMEF. However, you may be limited to a series of requests per hour. For more information, see [https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)

* The path to the trained classifiers (pickle files). If you have your own classifiers, you can provide them here. Otherwise, you can leave it blank


### The repository is divided into 3 directories: 

	1.  Apis
	2.  Pdf_info_extractor
	3.  Modelado

### Api's
The directory is organized into subdirectories corresponding to the API of each tool utilized: GitHub, Zenodo, OpenAire, and OpenAlex.
These API's extract the necessary DOI's and are processed by [api_doi_collector.py](./apis/api_doi_collector.py) which leaves the transformed and filtered DOI's within ``doi_filtered.csv``, with the first column being the DOI and the second the provenance.

[Arxiv_downloader.py](./apis/arxiv_downloader.py) takes the ``doi_filtered.csv`` and downloads the PDF file if a arxiv ID is found within the  ``doi_filtered.csv`` DOI field. If no arxivID is found, the DOI is added to the ``dois_not_arxiv.csv``.

The DOI's within ``dois_not_arxiv.csv`` are then used within [oa_url_pdf_extractor.py](./apis/oa_url_pdf_extractor.py) which locates a unpaywall url and creates a new csv: ``doi_not_arxiv_with_pdf_url.csv`` with the DOI, unpaywall url and other information.

Finally, all pdf's are downloaded through: [oa_pdf_downloader.py](./apis/oa_pdf_downloader.py) generating a download list.



To view an example please refer to [dois.ipynb](./apis/dois.ipynb)

### Pdf_info_extractor
After the PDF files have been downloaded to the ``pdf_info_extractor/data_pdf/`` directory, we can proceed with extracting the GitHub URLs. To accomplish this, we utilize either GROBID or Tika as part of the tool.

The URL extraction process is performed by the ``pipeline.py`` script, which selects either Tika or GROBID based on the user's preference. It extracts the URLs from each PDF file and generates a separate text file for each PDF within the ``./data_github_urls`` directory. These text files are then passed to SOMEF, which generates a JSON file containing metadata for the repositories.

To execute the pipeline, make sure you are in the ``pdf_info_extractor`` directory.

### Modelado (Modelling)

Once the code_urls have been extracted and the repositories downloaded.  We can the proceed to check whether or not the pdf/software repository is "Bi-directional". This is done by using bidireccional.py 



## License

This project is licensed under the [MIT License](LICENSE).


