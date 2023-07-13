
from utils.regex import is_filename_doi, str_to_arxivID
from
import os.path
import json

#WARNING this is for adrians pdfs

def adrian_to_doi(file_name):
    '''
    tries to find the doi within a pdf
    Input
    :returns
    doi
    '''

    #adrian had changed the "/" for a "_"
    possible_ID = file_name.replace(".pdf","")


def adrian_to_downloaded(file_name):
    '''
    Uses Adrians File naming system.
    arxiv are as is
    doi's have the following replaced: "/" for a "_"
    '''
    possible_ID = file_name.replace(".pdf", "")
    if str_to_arxivID(possible_ID):
        #TODO
        pass
    possible_ID = possible_ID.replace("_","/")
    if (doi:= is_filename_doi(possible_ID)):
        return doi_to_paperDict(doi)


def adrian_pdfs_2Meta(directory):
    result = {}
    list = os.listdir(directory)
    for file in list:
        if (meta:= adrian_to_downloaded(file)):
            key = next(iter(meta.keys()))
            meta[key]["file_name"] = file
            meta[key]["file_path"] = os.path.join(directory,file)
            result.update(meta)
    return result

def adrian_pdfs_2Json(directory):
    dictJson = adrian_pdfs_2Meta(directory)
    if not dictJson:
        return None
    output_path = directory + "/" +  "pdfMetadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dictJson, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path
