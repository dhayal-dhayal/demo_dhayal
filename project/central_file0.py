from project import *
from project.Pre_processing.M1_gstr1.central_gstr1_file0 import central_gstr1_func
from project.Pre_processing.M2_gstr2.central_gstr2_file0 import central_gstr2_func
from project.Pre_processing.M3_gstr3.central_gstr3_file0 import *
from project.Pre_processing.M4_others.central_others_file0 import *
from project.Processing.M4_others.get_intra_org_sales_file2 import*


def central_pre_processing_func(all_data_dict):
    try:
        def call_gstr1_func (all_data_dict):
            print("in central file_call_central_gstr1")
            if(central_gstr1_func(all_data_dict)==True):return True
            else:return False
        def call_gstr2_func (all_data_dict):
            print("in central file_call_central_gstr2")
            if(central_gstr2_func(all_data_dict)==True):return True
            else:return False
        def call_gstr3_func (all_data_dict):
            print("in central file_call_central_gstr3")
            if(central_gstr3_func(all_data_dict)==True):return True
            else:return False
        print("in central")

        if (call_gstr1_func(all_data_dict)==True and call_gstr2_func(all_data_dict)==True and call_gstr3_func(all_data_dict)==True):
                if(get_intra_sales_func(all_data_dict)==True):
                     return True

                else:return False
        else:return False

            
        
         


    except Exception as e:
        print(e)
        return False