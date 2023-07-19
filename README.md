
  
# Scientific Software Knowledge Graphs (SSKG)  
README IN PROGRESS  
## Introduction  
  
This tool verifies the link between a scientific paper and a software repository. It accomplishes this by locating the URL of the software repository within the scientific paper. It then extracts the repository's metadata to find any URLs associated with scientific papers and checks if they lead back to the original paper. If a bidirectional link is established, it marks it as "bidirectional".  

There is also a "unidirectional" metric, which finds a repository url and see's within the repository if the paper is named.
  
## Dependencies  
- Python 3.9
- Java 8 or above (please see [Tika requirements](https://tika.apache.org))  
  
## Installation  
  
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

### Docker
TODO

## Usage
  
  To see an example of usage please look at [example.ipynb](./example/example.ipynb)
  
### The repository is divided into the following directories:  
  
1. Download_pdf 
2. Metadata_extraction
3. Object_creator  
4. Modelling
5. Prediction
  
### Download_pdf
Pertains to all the downloading of pdfs. 
Downloaded_obj is a representation of downloaded papers which have not been processed yet.

### Metadata_extraction
Encompasses petitions to OpenAlex for fetching the paper's metadata.
MetadataObj contains the metadata from  OpenAlex: doi, arxiv and its title.
Tika scripts to open a pdf and extract its urls are also found witin this module.
PaperObj is created once the downloadedObj's pdf has been processed to locate all its urls. Contains: doi, arxiv, title, file_path, code_urls.
Finally, the necessary functions dowloading a repository and extracting its metadata with SOMEF

### Modelling
Contains all assessment of bidirectionality and unidirectionality. 
Mainly receives a paperObj and a repository_metadata json.

### Object Creator
This is the pipeline broken down into its main parts. Please look at [pipeline.py](./object_creator/pipeline.py) and [example.ipynb](./example/example.ipynb) to view the execution process.

### Prediction
For assessment of the program against its corpus. The corpus can be found within [corpus.csv](./predicition/corpus.csv) and the f1 score obtained bidirectional:  [corpus_eval_bidir.json](./predicition/corpus_eval_bidir.json) and the same for the unidirectional (_unidir)


  
## License  
  
This project is licensed under the [MIT License](LICENSE).