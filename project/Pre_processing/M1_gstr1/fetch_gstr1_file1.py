import json

def fetch_gstr1_func(all_data_dict):
    try:
        print("in fetch gstr 1")
        this_key = all_data_dict["pre_processing"]["M1_gstr1"]["fetch_gstr1_file1_json"]
        with open(this_key) as file:
            data = json.load(file)
        all_data_dict["pre_processing"]["M1_gstr1"]["fetch_gstr1_file1_json"]=data
        return True


    except Exception as e:
        print(e)
        return False

