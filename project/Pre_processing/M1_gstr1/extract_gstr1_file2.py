import pandas as pd
import json

def extract_gstr1_func(all_data_dict):
    try:
        print("in extract gstr")
        df = pd.DataFrame()
        fetch_key = all_data_dict["pre_processing"]["M1_gstr1"]["fetch_gstr1_file1_json"]

        for item in fetch_key["data"]["data"]["sec_sum"]:
            new_data = []  # empt to store values for the curnt obj
            base_data = item.copy()  # Copy the parent object

            # separate keys that contain list-type values
            for key, value in item.items():
                if isinstance(value, list):  # If key has a list, normalise it
                    for sub_item in value:
                        base_data.pop(key, None)

                        if "cpty_sum" in sub_item and isinstance(sub_item["cpty_sum"], list):
                            for cpty_item in sub_item["cpty_sum"]:
                                row = sub_item.copy()  # Copy current row
                                row.pop("cpty_sum", None)  # Remove nested list key
                                row.update(cpty_item)  # Merge `cpty_sum` into the row
                                new_data.append(row)  # Add new row
                        else:
                            new_data.append(sub_item)
                    break
            new_data.append(base_data)
            # print(new_data)
            temp_df = pd.json_normalize(new_data, sep="split")  # Normalize original
            # Append to df
            df = pd.concat([df, temp_df], ignore_index=True)

        df = df.bfill().astype(object).where(pd.notna(df), None)
        df["sec_nm"] = df["sec_nm"].fillna(df["typ"])
        df.drop(columns=["typ"], inplace=True)
        df['sec_nm'] = df['sec_nm'].bfill()
        all_data_dict["pre_processing"]["M1_gstr1"]["extract_gstr1_file2_json"]=df
        return True

    except Exception as e:
        return False