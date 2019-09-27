import pandas as pd
from engine.pipes.discover.e_discovery import  get_fields_type

df_input = pd.DataFrame()
out_path = ""

discovery_report = get_fields_type(df_input)
discovery_report.to_excel(out_path, sheet_name='RE0_discovery')

