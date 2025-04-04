from project.Pre_processing.M4_others.fetch_others_file1_json import *
from project.Pre_processing.M4_others.extract_others_file2 import *


def central_others_func(all_data_dict):
    try:
        print("in central others")
        if (fetch_others_func(all_data_dict) == True):
            if (extract_others_func(all_data_dict) == True):
                return True
            else:
                print( "Failed at extract_gstr1_func")
                return False

    except Exception as e:
        print(e)
        return (False)