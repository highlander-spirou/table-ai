from sth import *

file_path = 'uploads/22442226-f8b5-4328-a4e0-cf6b197a0136/pokemon.parquet.gzip'
alias = 'tbl_1'


df = get_df(file_path)
schema = get_schema(df)
question_1 = 'Name of the highest HP pokemon that also a Legendary.'

prompt = create_prompt(schema, alias, question_1, "Name, Attack, Type 1")

print(prompt)
