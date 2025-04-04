import json


def fetch_gstr3_func(all_data_dict):
    try:
        print("in fetch gstr3")
        this_key = all_data_dict["pre_processing"]["M3_gstr3"]["fetch_gstr3_file1_json"]
        with open(this_key) as file:
            data = json.load(file)
        all_data_dict["pre_processing"]["M3_gstr3"]["fetch_gstr3_file1_json"] = data
        return True


    except Exception as e:
        print("Error in fetch_gstr2_file1.py :", e)