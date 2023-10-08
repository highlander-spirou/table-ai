import duckdb
import re
from cohere import AsyncClient
from jinja2 import Environment
from template import template
from errors import *
from typing import Literal
from ChainExecutor import ChainExecutor

API_KEY = 'vSULf5lQOyNZ9mUaOFjIuMlwmYkbafZikmXtH8c1'
env = Environment()
prompt_tmpl = env.from_string(template)


def show_table(file_path, page, limit):
    offset_page = page - 1
    tbl = f"read_parquet('{file_path}')"
    offset = limit * offset_page
    data = duckdb.execute(
        f"SELECT * FROM {tbl} LIMIT ? OFFSET ?", [limit, offset]).df()
    data = data.fillna('N/A').to_dict('split')
    return data


def get_table_meta(df):
    return [(i[0], i[1]) for i in df.description]



class AITask:
    """
    Core logic of the website.

    Run in an resumable manners
    """
    def __init__(self, file_path, question) -> None:
        self.file_path = file_path
        self.question = question

        # Placeholder attributes
        self.df = None
        self.schema = None
        self.prompt = None
        self.sql_query = None
        self.full_explain = None
        self.result = None

        # static variables (eternal uses only)
        self._alias = 'tbl_1'
        self.STAGE: Literal['INIT', 'DF GOT', 'AI ASKED', 'SQL RAN'] = 'INIT'


    def get_df(self):
        try:
            self.df = duckdb.read_parquet(self.file_path)
            self.STAGE = 'DF GOT'
        except Exception:
            raise FileNotExisted

    def _get_schema(self):
        self.schema = get_table_meta(self.df)

    def _create_prompt(self):
        self.prompt = prompt_tmpl.render(
            table_alias=self._alias, schema=self.schema, question=self.question)

    async def get_query_suggestion(self):
        try:
            async with AsyncClient(API_KEY) as co:
                response = await co.generate(self.prompt, model='command-nightly',
                                             max_tokens=544, temperature=0)

            sql_query = re.findall(
                r'```([^```]*)```', response.generations[0].text)[0]

            if 'sql' in sql_query:
                sql_query = sql_query.split('\n')[1]

            self.sql_query = sql_query
            self.full_explain = response.generations[0].text
            self.STAGE = 'AI ASKED'
        except Exception:
            raise CohereNotResponse

    def run_query(self):
        try:
            result = self.df.query(self._alias, self.sql_query)
            self.result = result.fetchall()
            self.STAGE = 'SQL RAN'
        except Exception:
            raise RunQueryFail(query=self.sql_query)

    async def __call__(self):
        self.get_df()
        self._get_schema()
        self._create_prompt()
        await self.get_query_suggestion()
        self.run_query()
        return self.result