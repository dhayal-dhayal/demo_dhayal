
import pandas as pd

def get_intra_sales_func(all_data_dict):
    try:
        print("in get intra sales")
        this_key = all_data_dict["pre_processing"]["M2_gstr2"]["extract_gstr2_file2_json"]
        df = pd.DataFrame(this_key)
        df = df.drop(columns=['irn','oidt','rsn','typ', 'irngendate','rev','srctyp','ctin','diffprcnt','inum','itcavl','supfildt','oinum','supprd','ntnum','rt','sgst','txval','cgst','igst','pos','cess','num','suptyp'])
        
        # print(df.to_string())
        df['dt'] = pd.to_datetime(df['dt'], format='%d-%m-%Y')  # ✅ Corrected format

        # Sort by date
        df = df.sort_values(by='dt', ascending=True)

        # Convert back to 'MM YYYY' format
        df['dt'] = df['dt'].dt.strftime('%m %Y')

        df = df[df['gst_type'] == 'b2b']
        df = df.reset_index(drop=True)
        result_df = df.groupby('dt', as_index=False)['val'].sum()

        print(result_df.to_string())
        return True

    except Exception as e:
         print("error : ",e)
         return False