from object_creator.pipeline import *
from object_creator.doi_to_metadata import *
from object_creator.downloaded_to_paperObj import *
from modelling.bidirectionality import *
from object_creator.paper_obj_utils import *

output_directory = "/Users/pingamax2/Documents"  # output path
dois_txt = "./test/dois.txt"  # path to txt of dois

if __name__ == '__main__':
    print()
    # dois_txt_to_bidir_json(dois_txt=dois_txt, output_dir=output_directory)
    # dois_txt_to_unidir_json(dois_txt=dois_txt, output_dir=output_directory)
    #pipeline_single_unidir("10.3233/SW-223135","./DELETE")
    #doi_to_metaJson("10.1007/978-3-319-68204-4_9","./")
    #dwnlddJson_to_paperJson("./oa_metadata.json","./")
    #from_papers_json_to_bidir("./processed_metadata.json","./")
