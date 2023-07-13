from download_pdf.download_pipeline import pdf_download_pipeline
from download_pdf.downloaded_obj import DownloadedObj
import os

def metadata_to_downloaded(metadataObj, output_dir):
    """
    @Param metdataObj metadata object will be used to download the pdf
    @Param output_dir output directory to where the pdf will be downloaded
    ----
    :returns
    downloaded Object, which has a filename and filepath
    """
    #takes metadata and downloads the pdf
    if not metadataObj:
        return None
    file_path = pdf_download_pipeline(doi=metadataObj.doi,output_directory=output_dir)
    file_name = os.path.basename(file_path)
    return DownloadedObj(title=metadataObj.title,doi=metadataObj.doi,arxiv=metadataObj.arxiv,file_name=file_name,file_path=file_path)