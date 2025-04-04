
from project.Pre_processing.M3_gstr3.fetch_gstr3_file1 import *
from project.Pre_processing.M3_gstr3.extract_gstr3_file2 import *


def central_gstr3_func(all_data_dict):
    try:
        print("in central gstr3")
        if (fetch_gstr3_func(all_data_dict) == True):
            if (extract_gstr3_func(all_data_dict) == True):
                return True
            else:
                return (False, "Failed at extract_gstr3_func")
        else:return (False, "Failed at fetch_gstr3_func")

    except Exception as e:
         return False