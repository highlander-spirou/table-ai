import pandas as pd


new_df = pd.read_parquet('./uploads/asd/pokemon.parquet.gzip')
data = new_df.iloc[0:10].to_dict(orient='split')
print(data['columns'])
print(data['data'])