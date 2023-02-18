import akshare as ak
import pandas as pd

stock_board_concept_name_ths_df = ak.stock_board_concept_name_ths()
print(stock_board_concept_name_ths_df)

stock_board_concept_name_ths_df.to_csv('gnbk.csv')

stock_board_concept_name_ths_gp = ak.stock_board_concept_cons_ths("309050")
print(stock_board_concept_name_ths_gp)

