from .business_summary_file1 import *
from .return_status_file2 import *

def central_processing_M1_func(all_data_dict):
    try:
        business_summary = business_sum_func(all_data_dict)
        if not business_summary:
                print("❌ Error: Could not fetch JSON data.")
                return False

        return_status = get_return_status(all_data_dict)  
        if not return_status:
                print("❌ Error: Data extraction failed.")
                return False 
        
        return True     

    except Exception as e:
        print(f"Error in central_processing_M1: {e}")
        return False