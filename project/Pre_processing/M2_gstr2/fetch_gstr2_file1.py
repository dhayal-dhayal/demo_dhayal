import json


def fetch_gstr2_func(all_data_dict):
    try:
        print("in vfetch gstr 2")
        this_key = all_data_dict["pre_processing"]["M2_gstr2"]["fetch_gstr2_file1_json"]
        with open(this_key) as file:
            data = json.load(file)

        all_data_dict["pre_processing"]["M2_gstr2"]["fetch_gstr2_file1_json"] = data
        return True


    except Exception as e:
        print("Error in fetch_gstr2_file1.py :", e)