from project.central_file0 import *

def main():
    # all_data_dict = r"D:\Spring\Python\demo.json"
    all_data_dict = {"pre_processing":{
                                        "M1_gstr1":{ "fetch_gstr1_file1_json"   : r"D:\Spring\Python\demo.json",

                                                     "extract_gstr1_file2_json" :  "",
                                                     "gstr1_hsn_summary"        :  r"D:\Spring\Python\gstr1_hsn.json",
                                                     },
                                        "M2_gstr2": {"fetch_gstr2_file1_json"   : r"D:\Spring\Python\gstr_2.json",
                                                     "extract_gstr2_file2_json" :  "" },
                                        "M3_gstr3": {"fetch_gstr3_file1_json"   : r"D:\Spring\Python\gstr_3.json",
                                                     "extract_gstr3_file2_df"   : ""  },
                                        "M4_others": {"fetch_others_file1_json"   : r"D:\Spring\Python\track_gst_returns.json",
                                                     "extract_others_file2_df"   : ""  }
                                       },

                     "processing" : {
                                        "M4_others" : {"fetch_cdn_file1"        : " " ,
                                                       "fetch_cdnr_cdnur_file2" : { "Registered"    :  "" ,
                                                                                    "Un_Registered" :  ""
                                                                                   },
                                                       "get_intra_org_sales_file3"  : ""                           
                                                       }
                                    }
                    }

    # print("main")
    if(central_pre_processing_func(all_data_dict)==True):
        print("in main")
        

    # if(central_pre_processing_func(all_data_dict) == True):
    #     print("in main\n", all_data_dict["pre_processing"]["M4_others"]["extract_others_file2_df"])
    

    # if(central_pre_processing_func(all_data_dict)==True):
    #     print("in main\n")
    #     print(all_data_dict["pre_processing"]["M1_gstr1"]["extract_gstr1_file2_json"].head(1).to_string(),"\n"*2)
    #     print(all_data_dict["pre_processing"]["M2_gstr2"]["extract_gstr2_file2_json"].head(1).to_string(),'\n'*2)
    #     print(all_data_dict["pre_processing"]["M3_gstr3"]["extract_gstr3_file2_df"].head(1).to_string())
    # else:print("Failed")


main()
