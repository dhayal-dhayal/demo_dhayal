from project.Pre_processing.M1_gstr1 import *
from project.Pre_processing.M1_gstr1.fetch_gstr1_file1 import *
from project.Pre_processing.M1_gstr1.extract_gstr1_file2 import *


def central_gstr1_func(all_data_dict):
    try:
        print("in central gstr1")
        if (fetch_gstr1_func(all_data_dict) == True):
            if (extract_gstr1_func(all_data_dict) == True):
                return True
            else:
                return (False, "Failed at extract_gstr1_func")

    except Exception as e:
         return False
