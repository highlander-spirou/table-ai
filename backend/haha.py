import pandas as pd

df = pd.read_csv('./store/sth.csv')
df.to_parquet('./uploads/haha.parquet.gzip', compression='gzip')

new_df = pd.read_parquet('./uploads/haha.parquet.gzip')
print(new_df)
