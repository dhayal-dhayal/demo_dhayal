import pandas as pd

def extract_others_func(all_data_dict):
    try :
        print("in extract others_gstr")
        fetch_key = all_data_dict["pre_processing"]["M4_others"]["fetch_others_file1_json"]
        main_data = fetch_key["data"]["data"]["EFiledlist"]
        df = pd.DataFrame(main_data)

        # Convert 'Month' to a proper date format before sorting
        df['sorted_date'] = pd.to_datetime(df['ret_prd'], format='%m%Y')

        # Sort by 'sorted_date'
        df = df.sort_values(by='sorted_date')

        # Convert 'sorted_date' to the desired "MM YYYY" format
        df['ret_prd'] = df['sorted_date'].dt.strftime('%b %Y')
        df['dof'] = pd.to_datetime(df['dof'], format='%d-%m-%Y', errors='coerce')

        def calculate_delay_days(row):
            if row['status'] == "Filed":  # Only calculate if 'status' is "Filed"
                due_date = pd.to_datetime(f"11 {row['ret_prd']}", format='%d %b %Y')
                return max((row['dof'] - due_date).days, 0)  # Return delay days
            return 0

        result_df = pd.DataFrame({
            "Month": df["ret_prd"],
            "GSTR-1": df.apply(
                lambda row: f"Filed {row['dof'].strftime('%d-%m-%Y')}" if row["status"] == "Filed" and pd.notna(
                    row["dof"]) else "Not Filed", axis=1),
            "Delay Days": df.apply(calculate_delay_days, axis=1)
        })

        result_df = result_df.reset_index(drop=True)
        all_data_dict["pre_processing"]["M4_others"]["extract_others_file2_df"]=result_df

        return True

    except Exception as e:
        print("Error in fetch_gstr1_file1.py :", e)