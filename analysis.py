import re
import os

import numpy as np
import pandas as pd

WEEKLY_OPTION_PATTERN = r"^[A-Z]*\d{5,}[A-Z]{2}"
WEEKLY_OPTION_CORNER_CASE = r"^[A-Z]*\d{2}[A-Z]{1}\d{3,}[A-Z]{2}"
MONTHLY_OPTION_PATTERN = r"^[A-Z]*\d{2}[A-Z]{3}\d{2,}[A-Z]{2}"

def analyze_trade_counts(trade_counts):

    total_trades = int(sum(trade_counts))
    profit_trades = int(trade_counts.get(True, 0))
    loss_trades = int(trade_counts.get(False, 0))

    profit_trades_pct = round(profit_trades/total_trades*100, 2)
    loss_trades_pct = round(loss_trades/total_trades*100, 2)
    
    trade_summary = f"{profit_trades_pct} % were profitable trades in other words {loss_trades_pct} % of the trades have given you a loss"
    
    tips = ''
    if profit_trades_pct > loss_trades_pct:
        tips = "You're making more Profits than Loss. Focus on winning trades more. Keep up the hustle!"
    elif loss_trades_pct > profit_trades_pct:
        tips = "You're making more Losses than Profits. Cut the loosing trades early. Focus on Stop Loss and Entry critieria"
    
    return {
        'total_trades': total_trades,
        'profit_trades': profit_trades,
        'loss_trades':loss_trades,
        'profit_trades_pct': profit_trades_pct,
        'loss_trades_pct': loss_trades_pct,
        'trade_summary': trade_summary,
        'tips': tips
    }


def find_symbol_details(symbol):
    
    is_option = True
    
    if not (symbol.endswith('CE') or symbol.endswith('PE')):
        is_option = False
    
    weekly_option_match = re.match(WEEKLY_OPTION_PATTERN, symbol)
    weekly_option_corner_case_match = re.match(WEEKLY_OPTION_CORNER_CASE, symbol)
    monthly_option_match = re.match(MONTHLY_OPTION_PATTERN, symbol)
    
    option_type = symbol[-2:]
    option_expiry = "NO_EXPIRY"
    script = re.split(r"\d", symbol)[0]
    
    if weekly_option_match or weekly_option_corner_case_match:
        option_expiry = "WEEKLY"
        
    elif monthly_option_match:
        option_expiry = "MONTHLY"
        
    else:
        print("Could not indentify :", symbol)
    
    return (is_option, option_type, option_expiry, script)


def main(report_filepath:str):

    if not os.path.isfile(report_filepath):
        return "Report does not exists! Please upload the report again!"

    df = pd.read_excel(report_filepath)

    loopup_column = "Symbol"
    column_start = df[df.isin([loopup_column])].dropna(how='all').index[0]

    df_new = pd.read_excel(report_filepath, skiprows=column_start+1)

    filter_cols = [col for col in df_new.columns if not col.startswith('Unnamed')]

    df_new = df_new[filter_cols]
    trade_counts = (df_new['Realized P&L'] > 0).value_counts()

    total_trade_analysis_data = analyze_trade_counts(trade_counts)

    final_report = {
        'total_pnl': float(df_new['Realized P&L'].sum()), 
        'total_pnl_pct': round(float(df_new['Realized P&L Pct.'].sum()), 2),
        'overall': total_trade_analysis_data
    }

    df_new[['OPTION','OPTION_TYPE','EXPIRY_TYPE','SCRIPT']] = pd.DataFrame(
        np.row_stack(
            np.vectorize(find_symbol_details, otypes=['O'])
            (df_new['Symbol'])
        ),
        index=df_new.index
    )

    option_trades = df_new[df_new['OPTION']=='True']

    script_group = option_trades.groupby('SCRIPT')

    script_analysis_data = {}

    for script, script_df in script_group:
        script_trade_counts = (script_df['Realized P&L'] > 0).value_counts()
    
        data = analyze_trade_counts(script_trade_counts)
        script_analysis_data[script] = data

    multi_group = option_trades.groupby(["OPTION_TYPE","EXPIRY_TYPE","SCRIPT"])

    for (option_type, option_expiry, script), grp_df in multi_group:

        grp_trade_counts = (grp_df['Realized P&L'] > 0).value_counts()
        
        data = analyze_trade_counts(grp_trade_counts)
        
        script_analysis_data[script][f"{option_type}_{option_expiry}"] = {
            'pnl': grp_df['Realized P&L'].sum(),
            'pnl_pct': grp_df['Realized P&L Pct.'].sum(),
            'details': data
        }


    final_report['script_analysis'] = script_analysis_data

    return final_report

# res = main('pnl-TG6138.xlsx')

# print()
# print(res)
