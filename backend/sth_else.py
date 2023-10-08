from sth import *

file_path = 'uploads/a5a12c22-4252-4834-8e1c-5c0605180a73/pokemon.parquet.gzip'
alias = 'tbl_1'


df = get_df(file_path)

# query = """SELECT Name, Attack FROM tbl_1 WHERE "Type 1" iLIKE 'grass' ORDER BY Attack DESC LIMIT 1"""
# query = """SELECT Name, Attack FROM tbl_1 WHERE HP = (SELECT MAX(HP) FROM tbl_1) AND Legendary = true"""
query = """
SELECT Name, HP FROM tbl_1 WHERE HP = (SELECT MAX(HP) FROM tbl_1 WHERE "Type 1" = 'Grass');
"""

result = run_query(df, query, alias)

print(result)

