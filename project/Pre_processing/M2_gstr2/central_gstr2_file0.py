
from project.Pre_processing.M2_gstr2.fetch_gstr2_file1 import *
from project.Pre_processing.M2_gstr2.extract_gstr2_file2 import *


def central_gstr2_func(all_data_dict):
    try:
        print("in central gstr2")
        if (fetch_gstr2_func(all_data_dict) == True):
            if (extract_gstr2_func(all_data_dict) == True):
                return True
            else:
                return (False, "Failed at extract_gstr2_func")

    except Exception as e:
         return False
