from object_creator.pipeline import *

output_directory = "/Users/pingamax2/Documents" #output path
dois_txt = "./test/dois.txt" #path to txt of dois
if __name__ == '__main__':
    dois_txt_to_bidir_json(dois_txt=dois_txt,output_dir=output_directory)
    dois_txt_to_unidir_json(dois_txt=dois_txt,output_dir=output_directory)