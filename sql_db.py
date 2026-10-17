
import os
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from langchain.tools import tool
import re


class SQLtoLLM:
    def __init__(self, path_db:str):
        self.db = path_db

    def connect_to_db (self):
        """Conexão com o banco de dados SQL"""
        try:
            con = sqlite3.connect(database=self.db)
            cursor = con.cursor()
        except:
            print(f"Erro na conexão com o banco de dados {self.db}")

    #@tool
    def list_tables (self) -> list:
        """Esta função lista as tabelas que compõem o banco de dados SQL"""
        try:
            con = sqlite3.connect(database=self.db)
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            self.list_tables_ = [row[0] for row in cursor.fetchall()]
            return self.list_tables_
        finally:
            con.close()

    #@tool
    def list_columns_db (self, table_name:str) -> list:
        """ Executa a query e retorna uma lista contendo as colunas
        que compõem a tabela"""
        try:
            con = sqlite3.connect(database=self.db)
            cursor = con.cursor()
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)) #placeholder
            schema_row = cursor.fetchall()
            if schema_row:
                list_schema = [row for row in schema_row] # retorna uma tupla, em que a primeira posição é uma string
            list_columns = re.findall(pattern=r'".*"', string=list_schema[0][0])
            return list_columns
        finally:
            con.close()

    #@tool
    def sql_query(self, query:str) -> list:
        """ Executa a query no banco de dados"""
        try:
            con = sqlite3.connect(database=self.db)
            cursor = con.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()

            if not query_result:
                return (
                    f"ALERTA: A query executada com sucesso, mas retornou NENHUM resultado (lista vazia []).\n"
                    f"Query testada: {query}\n"
                    f"Instrução: Revise os filtros utilizados (como cláusulas WHERE, strings com LIKE ou operadores de igualdade).\n"
                    f"Verifique as colunas de texto existentes e tente gerar uma nova abordagem de consulta corrigida."
                )
            else:
                return query_result # a saída é uma lista de tuplas
        
        except Exception as e:
            return f"Erro na consulta: {e}"
        finally:
            con.close()

    #@tool
    def sql_query_checker(self, query:str) -> str:
        """Use this tool to double check if your query is correct before executing it.
        Always use this tool before executing a query with sql_db_query!"""
        import llm
    
        trigger_prompt = """{query}
            Double check the sqlite query above for common mistakes, including:
            - Using NOT IN with NULL values
            - Using UNION when UNION ALL should have been used
            - Using BETWEEN for exclusive ranges
            - Data type mismatch in predicates
            - Properly quoting identifiers
            - Using the correct number of arguments for functions
            - Casting to the correct data type
            - Using the proper columns for joins
            - If the command DELETE is present, return the message *COMANDO PROIBIDO!*

            If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

            Output the final SQL query only.

            SQL Query: """.format(query=query) # pois não é uma f-string, assim, .format substitui o texto de query em {query}
        llm_class = llm.LLM()
        model = llm_class.get_llm_model()
        response = model.invoke(trigger_prompt)
        return formata_instrucao_sql(response.text)

    def list_tools(self): #Listagem de ferramentas - aqui transforma elas em tools
        tools = [
            tool(self.list_tables), 
            tool(self.list_columns_db),
            tool(self.sql_query),
            tool(self.sql_query_checker)
            ]
        return tools


def formataCsvSimba(uploaded_file):
    df = pd.read_csv(uploaded_file, sep=';', engine='python', on_bad_lines='skip', encoding='ISO-8859-1')

    # Converter a coluna de datas para o formato datetime
    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%d/%m/%Y')

    # Converter as colunas monetárias em formato float
    colunas_monetaria = ['VALOR_TRANSACAO', 'VALOR_SALDO']

    for col in colunas_monetaria:
        df[col] = df[col].str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # colunas como 'strings' exceto 'VALOR_TRANSACAO', 'VALOR_SALDO' e 'DATA_LANCAMENTO'
    categorical_columns = [col for col in df.columns if col not in ['VALOR_TRANSACAO', 'VALOR_SALDO', 'DATA_LANCAMENTO']]
    for column in categorical_columns:
        df[column] = df[column].astype(str)

    return df


def create_sql_db(dataframe: pd.DataFrame, sqlite_path: str, table_name: str = 'extrato'):
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    engine = create_engine(f"sqlite:///{sqlite_path}", echo=False)

    dataframe.to_sql(table_name, engine, if_exists='replace', index=False)
    return engine

def formata_instrucao_sql(sql_string:str) -> str:
    removed_endline = sql_string.replace("\n", " ")

    try:
        position_sql_instruct = re.search(pattern=r"```sql.*```", string=removed_endline).span()
        sql_instruct = removed_endline[position_sql_instruct[0]:position_sql_instruct[1]]
        normalized_sql_instruct = sql_instruct.replace("```sql", "").replace("```", "").strip().split()
        return " ".join(normalized_sql_instruct)

    except AttributeError:
        return removed_endline