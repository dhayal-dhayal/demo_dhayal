import json
import pandas as pd


def fetch_others_func(all_data_dict):
    try:
        print("in fetch_others_gstr")
        this_key = all_data_dict["pre_processing"]["M4_others"]["fetch_others_file1_json"]
        with open(this_key) as file:
            data = json.load(file)
        all_data_dict["pre_processing"]["M4_others"]["fetch_others_file1_json"] = data
        return True

    except Exception as e:
        print("Error in fetch_gstr1_file1.py :", e)
