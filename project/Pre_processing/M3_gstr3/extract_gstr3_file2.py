import json
import pandas as pd

def extract_gstr3_func(all_data_dict):
    try:
        print("in extract gstr 3")
        fetch_key = all_data_dict["pre_processing"]["M3_gstr3"]["fetch_gstr3_file1_json"]
        # print("Extracting JSON data to DataFrame...\n")
        data = fetch_key["data"]["data"]
        main_data = fetch_key['data']['data']

        #  Inter-State Supplies DataFrames ,  #  Unregistered details
        unreg_details_df = pd.DataFrame(main_data['inter_sup']['unreg_details']) ##ok
        unreg_details_df.index.name = "unregistered_details"

        # itc avl, net, rev and inelg
        itc_elg =main_data["itc_elg"]
        dfs = [pd.DataFrame(itc_elg[k]).assign(category=k) if isinstance(itc_elg[k], list) else
               pd.DataFrame([itc_elg[k]]).assign(category=k, ty="NET") for k in itc_elg]
        df_itc= pd.concat(dfs, ignore_index=True)
        df_itc.index.name = "itc_eligible"

        # sup details
        sup_details =  main_data["sup_details"]
        df_sup_details = pd.DataFrame.from_dict(sup_details, orient='index').reset_index()
        df_sup_details.rename(columns={'index': 'category'}, inplace=True)
        df_sup_details.index.name = "supply_deatils"

        tx_pmt = main_data["tx_pmt"]
        df_tx_pditc = pd.DataFrame([tx_pmt["pditc"]]).assign(category="pditc")
        tx_py = main_data["tx_pmt"]["tx_py"]
        df_tx_py = pd.DataFrame(tx_pmt["tx_py"]).assign(category="tx_py")

        combined_df = pd.concat([unreg_details_df, df_sup_details, df_itc, df_tx_pditc,df_tx_py], ignore_index=True)
        combined_df = combined_df.drop(columns=["sgst", "cgst", "cess", "igst"], errors="ignore")
        combined_df = combined_df.astype(object).where(pd.notna(combined_df), None)

        all_data_dict["pre_processing"]["M3_gstr3"]["extract_gstr3_file2_df"] = combined_df
        return True

    except Exception as e:
        print("Error in fetch_gstr2_file1.py :", e)