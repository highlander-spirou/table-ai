import duckdb
from services.tables import get_table_meta
from jinja2 import Environment
from template import template
from errors import *
from cohere import Client
import re
from ChainExecutor import ChainExecutor
import networkx as nx

API_KEY = 'vSULf5lQOyNZ9mUaOFjIuMlwmYkbafZikmXtH8c1'
env = Environment()
prompt_tmpl = env.from_string(template)
co = Client(API_KEY)


def get_df(file_path):
    try:
        df = duckdb.read_parquet(file_path)
        print('df fetched')
        return df
    except Exception:
        raise FileNotExisted


def get_schema(df):
    print('schema fetched')
    return get_table_meta(df)


def create_prompt(schema, alias, question):
    print('create prompt')
    return prompt_tmpl.render(
        table_alias=alias, schema=schema, question=question)


def get_query_suggestion(prompt):
    try:
        response = co.generate(prompt, model='command-nightly',
                               max_tokens=544, temperature=0)

        sql_query = re.findall(
            r'```([^```]*)```', response.generations[0].text)[0]

        if 'sql' in sql_query:
            sql_query = sql_query.split('\n')[1]

        sql_query = sql_query
        full_explain = response.generations[0].text
        print('sql generated')
        return sql_query, full_explain
    except Exception:
        raise CohereNotResponse


def run_query(df, sql_query, alias):
    try:
        result = df.query(alias, sql_query)
        result = result.fetchall()
        print('queried')
        return result
    except Exception:
        raise RunQueryFail(query=sql_query)


def fix_table_name(s, alias):
    """
    Fix common cohere prompt where it sometimes refer alias as `table`
    """
    if 'table' in s:
        return s.replace('table', alias)
    else:
        return s


def fix_space_contained_table(q, schema):
    column_names = [i[0] for i in schema if " " in i[0]]
    q2 = q
    for i in column_names:
        if i in q:
            q2 = q2.replace(i, f'"{i}"')

    return q2



if __name__ == "__main__":
    file_path = 'uploads/22442226-f8b5-4328-a4e0-cf6b197a0136/pokemon.parquet.gzip'
    df = get_df(file_path)
    schema = get_schema(df)
    alias = 'tbl_1'
    q = """SELECT Name, Attack FROM tbl_1 WHERE Type 1 = 'Grass' ORDER BY Attack DESC LIMIT 1"""
    q2 = fix_table_name(q, alias)
    q2 = fix_space_contained_table(q2, schema)

    result = run_query(df, q2, alias)
    print(result)
    question_1 = 'Name of the highest HP pokemon that also a Legendary. Display the Name and HP column'


    ai_flow = ChainExecutor()
    ai_flow.add_node(get_df, args={"file_path": file_path}) \
        .add_node(get_schema) \
        .add_node(create_prompt, args={'alias': alias, 'question': question_1}) \
        .add_node(get_query_suggestion) \
        .add_node(fix_table_name) \
        .add_node(fix_space_contained_table) 

    ai_flow.add_edge_from_node_order()

    ai_flow.add_node(run_query, args={'alias': alias})

    # Establish connection between `run_query` and `get_df`
    ai_flow.add_edge('get_df', 'run_query', arg_index=0)

    # Establish connection between `run_query` and `get_query_suggestion`
    ai_flow.add_edge('get_query_suggestion', 'run_query', result_index=0, arg_index=1)

    try:
        # Ask the first question
        ai_flow.execute()
        first_result = ai_flow.get_node_result('run_query')

        # Ask the second question
        ai_flow.update_node_args('create_prompt', args={'question': 'Name of the highest Attack pokemon that also a Grass type. Display the Name and Attack column'})
        ai_flow.execute()
        second_result = ai_flow.get_node_result('run_query')

        print('first', first_result)
        print('second', second_result)

    except RunQueryFail as e:
        print(e.query)
