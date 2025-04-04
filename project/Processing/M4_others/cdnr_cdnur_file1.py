import pandas as pd

def fetch_cdnr_cdnur_func(all_data_dict):
    try:
        this_key = all_data_dict["pre_processing"]["M1_gstr1"]["extract_gstr1_file2_json"]

        df = pd.DataFrame(all_data_dict["pre_processing"]["M1_gstr1"]["extract_gstr1_file2_json"])
        pd.set_option('display.float_format', '{:.2f}'.format)

        #Step 2
        for sec, index_name in [('CDNR', 'Registered'), ('CDNUR', 'Un_Registered')]:
            df_filtered = df[df['sec_nm'] == sec][['ttl_val', 'ttl_tax']].copy()

            df_filtered.columns = ['Invoice value in review period', 'Taxable Value']
            df_filtered['Notes'] = range(1, len(df_filtered) + 1)
            df_filtered['Invoices'] = df_filtered['Notes']
            df_filtered['% Invoice in review period'] = 0
            df_filtered['%Invoices tax in review period'] = 0
            df_filtered.index = pd.RangeIndex(start=1, stop=len(df_filtered) + 1, step=1)
            df_filtered.index.name = index_name
            column_order = ['Notes', 'Invoices',
                             '% Invoice in review period','Invoice value in review period',
                            '%Invoices tax in review period','Taxable Value']


            df_filtered=df_filtered[column_order]
            all_data_dict["processing"]["M4_others"]["fetch_cdnr_cdnur_file2"][index_name]=df_filtered




    except Exception as e:
        return False


