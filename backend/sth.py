import duckdb
from services.tables import get_table_meta
from jinja2 import Environment
from template import template
from errors import *
from cohere import Client
import re
from ChainExecutor import ChainExecutor
import networkx as nx
from typing import Optional

API_KEY = 'vSULf5lQOyNZ9mUaOFjIuMlwmYkbafZikmXtH8c1'
env = Environment()
prompt_tmpl = env.from_string(template)
co = Client(API_KEY)


def get_df(file_path):
    try:
        df = duckdb.read_parquet(file_path)
        return df
    except Exception:
        raise FileNotExisted


def get_schema(df):
    return get_table_meta(df)


def create_prompt(schema, alias, question, select: Optional[str] = None):
    return prompt_tmpl.render(
        table_alias=alias, schema=schema, question=question, select=select)


def get_cohere_suggestion(prompt):
    try:
        response = co.generate(prompt, model='command-nightly',
                               max_tokens=544, temperature=0)

        full_explain = response.generations[0].text
        return full_explain
    except Exception:
        raise CohereNotResponse


def get_query_from_suggestion(suggestion):
    sql_query = re.findall(r'```([^```]*)```', suggestion)[0]

    if 'sql' in sql_query:
        sql_query = sql_query.split('\n')[1]

    return sql_query


def run_query(df, sql_query, alias):
    try:
        result = df.query(alias, sql_query)
        result = result.fetchall()
        return result
    except Exception:
        raise RunQueryFail(query=sql_query)


def fix_table_name(s, alias):
    """
    Fix common cohere prompt where it sometimes refer alias as `table`
    """
    if 'table' in s:
        new_str = s.replace('table', alias)
        return new_str
    else:
        return s


def fix_space_contained_table(q, schema):
    print('table fix query', q)
    column_names = [i[0] for i in schema if " " in i[0]]
    q2 = q
    for i in column_names:
        if i in q:
            q2 = q2.replace(i, f'"{i}"')

    return q2


class AIFlow:
    """
    Main logic of the program. Using Chain Executor to generate SQL, run them with duckdb, 
    and provide way to manual fix and resume if error occurs

    This class is an event-driven that acts on the change of `question` state. 
    """

    def __init__(self, file_path: str, alias: str) -> None:
        self.ai_flow = ChainExecutor()
        self.fix_flow = ChainExecutor()

        # External dependency (Static)
        self.file_path = file_path
        self.alias = alias

        # post_init
        self.__construct_ai_flow()

    def __construct_ai_flow(self):
        """
        Constructing `ChainExecutor` graph
        """
        self.ai_flow.add_node(get_df, args={"file_path": self.file_path}) \
            .add_node(get_schema) \
            .add_node(create_prompt, args={"alias": self.alias}) \
            .add_node(get_cohere_suggestion) \
            .add_node(get_query_from_suggestion) \

        self.ai_flow.add_edge_from_node_order()

        self.ai_flow.add_node(run_query, args={'alias': alias})

        self.ai_flow.add_edge('get_df', 'run_query', arg_index=0) \
            .add_edge('get_query_from_suggestion', 'run_query', arg_index=1)

    def __construct_error_flow(self):
        """
        Construction of automatic error fixing flow. This flow is dependant on the state `question` 
        and must be post init after `ai_flow` (reliant on `ai_flow`'s `get_schema` node)
        """
        self.fix_flow.add_node(fix_table_name, args={'alias': self.alias}) \
            .add_node(fix_space_contained_table, args={'schema': self.ai_flow.get_node_result('get_schema')})

        self.fix_flow.add_edge_from_node_order()

    def __auto_fix_query(self, falsey_query):
        print(f'Error found on query:\n{falsey_query}')
        if len(self.fix_flow.g.nodes) == 0:
            self.__construct_error_flow()

        self.fix_flow.update_node_args(
            'fix_table_name', args={'s': falsey_query})
        self.fix_flow.execute()
        return self.fix_flow.get_node_result('fix_space_contained_table')

    def manual_run_query(self, query):
        df = self.ai_flow.get_node_result('get_df')
        return run_query(df, query, self.alias)

    def answer_question(self, question, select: Optional[str] = None):
        """
        Update `question` state and run `ai_flow`
        """
        try:
            self.ai_flow.update_node_args(
                'create_prompt', args={'question': question, 'select': select})
            self.ai_flow.execute()
            return self.ai_flow.get_node_result('run_query')

        except FileNotExisted:
            print('Error, table collapse')

        except CohereNotResponse:
            print('Cohere AI not responding')

        except RunQueryFail as e:

            falsey_query = e.query
            corrected_query = self.__auto_fix_query(falsey_query)
            print('corrected query', corrected_query)
            return self.manual_run_query(corrected_query)


if __name__ == "__main__":
    file_path = 'uploads/22442226-f8b5-4328-a4e0-cf6b197a0136/pokemon.parquet.gzip'
    alias = 'tbl_1'
    question_1 = 'Name of the highest HP pokemon that also a Legendary.'
    select_1 = 'Name, Attack'
    question_2 = 'Name of the highest Attack pokemon that also a Grass type.'
    select_2 = 'Name, Attack'

    ai_flow = AIFlow(file_path, alias)

    answer1 = ai_flow.answer_question(question_1, select=select_1)
    print('answer 1', answer1)

    
    answer2 = ai_flow.answer_question(question_2, select=select_2)
    print('answer 2', answer2)

    query_1 = f"""SELECT Name, "Type 1" FROM {alias} WHERE "Type 1" = 'Grass' ORDER BY Attack DESC LIMIT 2"""

    answer3 = ai_flow.manual_run_query(query_1)
    print(answer3)
