import sql_db as sql
import agents as ag
#import agents_graph as ag
import llm
import argparse
import datetime
from langchain_core.globals import set_debug

def sql_consultor(path_database:str, 
                  path_system_prompt:str, 
                  agent_name:str, 
                  query:str | None=None):

    set_debug(False)
    session = str(datetime.datetime.now().timestamp())

    print("="*50)
    print("\nAgente consultor de banco de dados SQL\n")
    print("="*50)

    with open (file=path_system_prompt, mode='r', encoding='utf-8') as fh:
        lines = fh.readlines()
        system_prompt = " ".join(lines)
    print("\nPrompt do sistema carregado!\n")

    obj = sql.SQLtoLLM(path_db=path_database)
    obj.connect_to_db()
    tools = obj.list_tools()
    print("\nBanco de dados carregado!\n\n")

    agente = ag.Agent()
    agente.set_name_agent(name=agent_name)
    agente.set_model(model=llm.LLM().get_llm_model())
    agente.set_tools(tools=tools)
    agente.set_system_prompt(prompt=system_prompt)
    agente.save_agent_settings()
    print("\nConfigurações do agente finalizada!")

    if query == None:
        while True:
            print("\n\n")
            print("*" * 100)
            print(f"* Informe interação de usuário para gerar consulta ao banco de dados:\n\n* {path_database}\n\n* ou digite '/bye' para sair...\n")
            print("*" * 100)
            print("\n")

            user_prompt = input("> ")

            if user_prompt == "/bye":
                break
            else:
                print("\n\nExecutando o agente...aguarde!\n")
                agente.run_agent(user_prompt=user_prompt, session=session)
            
            print("\n")
            print("-" * 100)
    else:
        print("\n\nExecutando o agente...aguarde!\n")
        agente.run_agent(user_prompt=query, session=session)
                    
        print("\n")
        print("-" * 100)

def main():
    parser = argparse.ArgumentParser(description="Agente consultor de banco de dados SQL")
    parser.add_argument('--path_database',
                        type=str,
                        required=True,
                        help='Informe o caminho absoluto para o banco de dados SQL')
    parser.add_argument('--path_system_prompt',
                        type=str,
                        required=True,
                        help='Carregue o arquivo .txt contendo o prompt do sistema')
    parser.add_argument('--agent_name',
                        type=str,
                        required=True,
                        help='Informe identificador para o agente')
    parser.add_argument('--query',
                            type=str,
                            required=False,
                            help='Informe uma consulta em texto livre - somente se não for consulta interativa com o agente')
    
    args = parser.parse_args()


    sql_consultor(path_database=args.path_database,
                  path_system_prompt=args.path_system_prompt,
                  agent_name=args.agent_name,
                  query=args.query)

if __name__ == '__main__':
    main()