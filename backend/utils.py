def get_table_list(client: Client):
    return [split_parquet(i) for i in listdir(f'uploads/{client.server_cookie}')]

def get_table_meta(df):
    # df = duckdb.read_parquet(file_path)
    return [(i[0], i[1]) for i in df.description]



def analyze_df(df):
    col_type = df.dtypes.to_dict()
    null_counts = df.isnull().sum().to_dict()

    a = {}
    for index in col_type.keys():
        a[index] = (str(col_type[index]), null_counts[index])
    return a


class LongTask:
    def __init__(self, file_path, question) -> None:
        self.file_path = file_path
        self.question = question
        self.alias = 'tbl_1'

        # Placeholder attributes
        self.df = None
        self.schema = None
        self.prompt = None
        self.sql_query = None
        self.full_explain = None
        self.result = None

    def get_df(self):
        try:
            print(self.file_path)
            self.df = duckdb.read_parquet(self.file_path)
        except Exception:
            raise FileNotExisted

    def get_schema(self):
        self.schema = get_table_meta(self.df)

    def create_prompt(self):
        self.prompt = prompt_tmpl.render(
            table_alias=self.alias, schema=self.schema, question=self.question)

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
        except Exception:
            raise CohereNotResponse

    def run_query(self):
        try:
            result = self.df.query(self.alias, self.sql_query)
            self.result = result.fetchall()
        except Exception:
            print('raising')
            raise RunQueryFail(query=self.sql_query)

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.get_df()
        self.get_schema()
        self.create_prompt()
        await self.get_query_suggestion()
        self.run_query()
        return self.result