import pandas as pd


new_df = pd.read_parquet('./uploads/asd_9168024629/pokemon.parquet.gzip')
data = new_df.iloc[0:10].to_dict(orient='split')
exec("print(data)")