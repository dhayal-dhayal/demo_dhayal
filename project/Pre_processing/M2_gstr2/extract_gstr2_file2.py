import json
import pandas as pd

def extract_gstr2_func(all_data_dict):
    try:
        fetch_key = all_data_dict["pre_processing"]["M2_gstr2"]["fetch_gstr2_file1_json"]
        print("in extract gstr2")
        # Locate 'b2b' inside 'docdata'
        main_data = fetch_key['data']['data']['data']
        b2b_data = (main_data.get('docdata', {}).get('b2b',[]))
        gst_types = ['b2b', 'b2ba']
        df_list = []
        for gst_type in gst_types:
            gst_data = (
                    main_data.get('docdata', {}).get(gst_type, []) +
                    main_data.get('cp_sum', {}).get(gst_type, [])
                     )
            if any('inv' in entry for entry in gst_data):
                temp_df = pd.json_normalize(
                gst_data,
                record_path=['inv'],
                meta=['ctin', 'trdnm', 'supfildt', 'supprd'],
                errors='ignore'
                )
            else:
                temp_df = pd.DataFrame(gst_data)

            temp_df.insert(0, 'gst_type', gst_type)
            if 'items' in temp_df.columns:
                items_df = pd.json_normalize(temp_df['items'].explode())
                temp_df = temp_df.drop(columns=['items']).reset_index(drop=True)
                temp_df = pd.concat([temp_df, items_df], axis=1)
            df_list.append(temp_df)

        final_df = pd.concat(df_list, ignore_index=True)

        records = []
        for cdnr_entry in main_data["docdata"]["cdnr"]:
            common_fields = {
                "gst_type": "cdnr",
                "trdnm": cdnr_entry["trdnm"],
                "supfildt": cdnr_entry["supfildt"],
                "supprd": cdnr_entry["supprd"],
                "ctin": cdnr_entry["ctin"],
            }
            for nt in cdnr_entry["nt"]:
                nt_data = common_fields.copy()  # Copy common fields for each row
                # Add only non-list values from nt
                nt_data.update({k: v for k, v in nt.items() if not isinstance(v, list)})
                records.append(nt_data)


        df_cdnr = pd.DataFrame(records)
        df_combined = pd.concat([final_df, df_cdnr], ignore_index=True)
        df_final = df_combined.where(pd.notnull(df_combined), None)

        all_data_dict["pre_processing"]["M2_gstr2"]["extract_gstr2_file2_json"] = df_final
        return True

    except Exception as e:
        print("Error in extract_gstr2_file1.py :", e)