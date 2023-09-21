import pandas as pd


new_df = pd.read_parquet('./uploads/asd/pokemon.parquet.gzip')
print(new_df)
