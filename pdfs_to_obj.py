from object_creator.downloaded_to_paperObj import dwnlddJson_to_paperJson
from object_creator.pdf_to_downloaded import pdfs_to_downloaded_Json
from object_creator.pipeline import from_papers_json_to_unidir

path_json = pdfs_to_downloaded_Json("/home/kg/PDFs")
paper_json = dwnlddJson_to_paperJson("../test/pdfs/pdf_metadata.json", "../test/pdfs")
from_papers_json_to_unidir(paper_json,"/home/kg")