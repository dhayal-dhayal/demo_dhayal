import os
import json
import pandas as pd
from collections import defaultdict

import pandas as pd
from collections import defaultdict

# def convert_to_month_range(period_str):
#     """
#     Convert MM-YYYY period string to month range like 'Mar 2020 - Apr 2021'.
#     """
#     try:
#         # Convert the period string into a datetime object
#         start_date = pd.to_datetime(period_str, format='%m-%Y')
#         end_date = start_date.replace(year=start_date.year + 1)  # Adjust to the next year for range

#         # Format to 'Month Year' format
#         start_month = start_date.strftime("%b %Y")
#         end_month = end_date.strftime("%b %Y")

#         return f"{start_month} - {end_month}"
#     except ValueError as e:
#         print(f"Error converting period: {period_str}, {e}")
#         return period_str

def process_gstr3_subfunc3(df_gstr3):
    gross_turnover = 0
    net_turnover = 0
    liability_payable = 0
    liability_paid = 0
    
    
    osup_rows = df_gstr3[df_gstr3['Supply Type'].isin(['OSUP_DET', 'OSUP_ZERO', 'OSUP_NIL_EXMP', 'OSUP_NONGST'])| (df_gstr3['Category'] == 'INTER_STATE_SUPPLY')]
    for index, row in osup_rows.iterrows():
        net_turnover += row.get('Taxable Value', 0)# Iterate over each row in the dataframe for gross turnover, net turnover 
        gross_turnover += row.get('Taxable Value', 0)
        if row['Supply Type'] == 'INTER_STATE_SUPPLY':
            gross_turnover += row.get('IGST Amount', 0)
        if row['Supply Type'] == 'OSUP_DET':
            gross_turnover += sum(row.get(col, 0) for col in [ 'IGST Amount', 'CGST Amount', 'SGST Amount', 'CESS Amount'])

        # Calculate Liability Payable by summing relevant columns
    liability_payable += df_gstr3[df_gstr3['Transaction Description'].isin(['Reverse Charge', 'Other than Reverse Charge'])][['IGST Tax', 'CGST Tax', 'SGST Tax', 'CESS Tax']].sum().sum()
    liability_payable += osup_rows[['IGST Amount', 'CGST Amount', 'SGST Amount', 'CESS Amount']].sum().sum()
    
    # Calculate Liability Paid for 'TX_PAYMENT' rows
    liability_paid = df_gstr3[df_gstr3['Category'] == 'TAX_PAID_ITC'][['s_pds', 'i_pds', 'cs_pdcs', 'c_pdi','c_pdc']].sum().sum()

    return gross_turnover, net_turnover, liability_payable, liability_paid


def process_gstr2_subfunc2(df_gstr2):
    """
    Process GSTR-2B data from DataFrame and calculate gross purchase, net purchase, credit/debit, and recurring totals.
    """
    gross_purchase = net_purchase = credit_debit = 0.0
    gross_purchase = df_gstr2['Invoice Value'].sum()
    net_purchase = df_gstr2['Taxable Value'].sum()
    credit_debit = df_gstr2[(df_gstr2['Type'] == 'cdnr') & (df_gstr2['Source'] == 'docdata')]['Total Docs'].sum()
    invoice_count = len(df_gstr2)
    num_suppliers = df_gstr2['GSTIN'].nunique()
    
    recurring_suppliers = df_gstr2.groupby('GSTIN')['Supplier Period'].nunique().reset_index()
    recurring_suppliers = recurring_suppliers[recurring_suppliers['Supplier Period'] > 1]
    recurring_df = df_gstr2[df_gstr2['GSTIN'].isin(recurring_suppliers['GSTIN'])]
    total_recurring_value = recurring_df['Invoice Value'].sum()  # or use 'Taxable Value' if needed

    return gross_purchase, net_purchase, credit_debit, num_suppliers, invoice_count, total_recurring_value

def process_gstr1_subfunc1(df_gstr1):
    
    b2b, b2c, export, recurring_sales = 0, 0, 0, 0
    b2b     = df_gstr1[df_gstr1['Section Name'] == 'B2B']['Total Invoice Value'].sum()
    b2c     = df_gstr1[df_gstr1['Section Name'].isin(['B2CL', 'B2CS'])]['Total Invoice Value'].sum()
    export  = df_gstr1[df_gstr1['Section Name'] == 'EXP']['Total Invoice Value'].sum()
    
    recurring_sales = df_gstr1.groupby('Counterparty GSTIN')['Return Period'].nunique().reset_index()
    recurring_sales = recurring_sales[recurring_sales['Return Period'] > 1]
    recurring_df = df_gstr1[df_gstr1['Counterparty GSTIN'].isin(recurring_sales['Counterparty GSTIN'])]
    recurring_sales = recurring_df['Total Invoice Value'].sum()
    return b2b, b2c, export, recurring_sales

def business_sum_func(all_data_dict):
    try:
        # Process GSTR-3B, GSTR-2B, and GSTR-1 data
        gstr3_data = process_gstr3_subfunc3(all_data_dict["preprocessing_data_dict"]["M3_gstr3"]["extract_gstr3b_file2_df"])
        if not gstr3_data:
            print("Failed to process GSTR-3B data.")
            return False

        gstr2_data = process_gstr2_subfunc2(all_data_dict["preprocessing_data_dict"]["M2_gstr2"]["extract_gstr2b_file2_df"])
        if not gstr2_data:
            print("Failed to process GSTR-2B data.")
            return False

        gstr1_data = process_gstr1_subfunc1(all_data_dict["preprocessing_data_dict"]["M1_gstr1"]["extract_gstr1_file2_df"])
        if not gstr1_data:
            print("Failed to process GSTR-1 data.")
            return False

        gross_turnover, net_turnover, payable, paid = gstr3_data
        print(f"Gross Turnover: {gross_turnover}, Net Turnover: {net_turnover}, Payable: {payable}, Paid: {paid}")
        gross_purchase, net_purchase, cd_notes, num_suppliers, invoice_count, recurring_purchases = gstr2_data
        print(f"Gross Purchase: {gross_purchase}, Net Purchase: {net_purchase}, Credit/Debit Notes: {cd_notes}, Suppliers: {num_suppliers}, Invoice Count: {invoice_count}, Recurring Purchases: {recurring_purchases}")
        b2b, b2c, export, recurring_sales = gstr1_data

        gross_margin = gross_turnover - gross_purchase
        gross_margin_pct = (gross_margin / gross_turnover * 100) if gross_turnover else 0
        recurring_sales_pct = (recurring_sales / gross_turnover * 100) if gross_turnover else 0
        recurring_purchases_pct = (recurring_purchases / gross_purchase * 100) if gross_purchase else 0

        summary = {
            "Sales": "",
            "Gross Turnover": [gross_turnover],
            "Net Turnover": [net_turnover],
            "Recurring Sales": [recurring_sales],
            "Recurring Sales %": [f"{recurring_sales_pct:.2f}%"],
            "B2B Sales": [b2b],
            "B2C Sales": [b2c],
            "Export Sales": [export],
            "Purchases": "",
            "Gross Purchase": [gross_purchase],
            "Net Purchase": [net_purchase],
            "Recurring Purchases": [recurring_purchases],
            "Recurring Purchases %": [f"{recurring_purchases_pct:.2f}%"],
            "Liability Payable": [payable],
            "Liability Paid": [paid],
            "Credit/Debit Notes": [cd_notes],
            "Gross Margin": [gross_margin],
            "Gross Margin %": [f"{gross_margin_pct:.2f}%"],
            "Invoices": [invoice_count],
            "Suppliers": [num_suppliers]
        }

        df_summary = pd.DataFrame(summary)
        print(df_summary.T.to_string(index=True), '\n')
        all_data_dict["processing_data_dict"]["M1_primary"]["business_summary"] = df_summary.T.to_dict(orient='records')
        print ("Business summary processed successfully.")  
        return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False
