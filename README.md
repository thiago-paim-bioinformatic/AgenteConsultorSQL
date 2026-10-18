# Agente Consultor de Banco de Dados SQL

Agente de Inteligência Artificial desenvolvido em Python para consultar bancos de dados SQL por meio de instruções em linguagem natural. A aplicação utiliza um modelo de linguagem (LLM) integrado a ferramentas de acesso ao banco de dados para interpretar solicitações, auxiliar na elaboração de consultas e executar o fluxo de interação definido pelo agente.

## 📌 Funcionalidades

- **Consultas em linguagem natural:** permite solicitar informações do banco de dados sem precisar escrever diretamente comandos SQL.
- **Integração com LLM:** utiliza um modelo de linguagem configurado no módulo `llm.py`.
- **Ferramentas de acesso ao banco:** disponibiliza ao agente as ferramentas implementadas no módulo `sql_db.py`.
- **Prompt de sistema personalizado:** permite definir o comportamento, as instruções e as restrições do agente por meio de um arquivo `.txt`.
- **Configuração do agente:** define um nome, um modelo, as ferramentas disponíveis e o prompt de sistema.
- **Modo interativo:** possibilita realizar várias consultas durante a mesma execução.
- **Execução de consulta única:** permite enviar uma pergunta diretamente pela linha de comando.
- **Identificação de sessão:** utiliza um identificador temporal para agrupar as interações realizadas durante a execução.

## 🏗️ Arquitetura do projeto

O script principal coordena os seguintes módulos:

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Recebe os argumentos da linha de comando e coordena a execução do agente. |
| `sql_db.py` | Gerencia a conexão com o banco de dados e disponibiliza as ferramentas de consulta SQL. |
| `agents.py` | Implementa a configuração e a execução do agente de IA. |
| `llm.py` | Disponibiliza o modelo de linguagem utilizado pelo agente. |
| `system_prompt.txt` | Contém as instruções que orientam o comportamento do agente. |


## ⚙️ Requisitos

- Python 3.10 ou superior, considerando a sintaxe de união de tipos utilizada no script.
- Acesso ao banco de dados SQL que será consultado.
- Modelo de linguagem acessível por meio da configuração de `llm.py`.
- Dependências Python utilizadas pelos módulos do projeto.
- Arquivo de texto com o prompt de sistema.

As dependências específicas devem ser instaladas conforme o arquivo `requirements.txt`.

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/thiago-paim-bioinformatic/AgenteConsultorSQL.git
```

Entre no diretório do projeto:

```bash
cd AgenteConsultorSQL
```

### 2. Crie um ambiente virtual

No Windows, utilizando PowerShell:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências


```bash
pip install -r requirements.txt
```

### 4. Configure o modelo de linguagem

Crie um arquivo `.env` com a seguinte estrutura:

```
BASE_URL_SERVER=<OpenAI compatível>
API_KEY_SERVER=<key>
MODEL_LLM=<model>
```


## 📝 Configuração do prompt de sistema

Crie um arquivo de texto, por exemplo, `system_prompt.txt`, com as instruções que orientarão o agente.

Exemplo ilustrativo:

```text
Você é um agente especializado em consultas a bancos de dados SQL.

Sua função é interpretar as perguntas do usuário e utilizar as
ferramentas disponíveis para obter informações do banco de dados.

Regras:
1. Utilize somente as tabelas e colunas disponibilizadas pelas ferramentas.
2. Não invente resultados ou informações ausentes no banco.
3. Explique os resultados de maneira clara e objetiva.
4. Informe quando não houver dados suficientes para responder.
5. Não execute operações de alteração ou exclusão de dados.
6. Respeite as permissões de acesso e as restrições configuradas.
```


## ▶️ Como executar

O programa recebe os seguintes argumentos:

| Argumento | Obrigatório | Descrição |
|---|---|---|
| `--path_database` | Sim | Caminho absoluto para o banco de dados SQL. |
| `--path_system_prompt` | Sim | Caminho do arquivo `.txt` contendo o prompt de sistema. |
| `--agent_name` | Sim | Nome ou identificador do agente. |
| `--query` | Não | Pergunta em linguagem natural para execução única. Se omitido, inicia o modo interativo. |

### 1. Modo interativo

Execute o programa sem informar o argumento `--query`:

```powershell
python promp_to_sql_query.py `
  --path_database "C:\dados\meu_banco.db" `
  --path_system_prompt "C:\projeto\system_prompt.txt" `
  --agent_name "ConsultorSQL"
```

O agente solicitará perguntas pelo terminal.

Exemplo de interação:

```text
==================================================
Agente consultor de banco de dados SQL
==================================================

Prompt do sistema carregado!

Banco de dados carregado!

Configurações do agente finalizada!

> Quais são as tabelas disponíveis no banco?

Executando o agente...aguarde!
```

Após a resposta, o usuário poderá realizar outra consulta.

Para encerrar a execução, digite:

```text
/bye
```

### 2. Execução de uma consulta específica

Para executar apenas uma pergunta, utilize o argumento `--query`:

```powershell
python promp_to_sql_query.py `
  --path_database "C:\dados\meu_banco.db" `
  --path_system_prompt "C:\projeto\system_prompt.txt" `
  --agent_name "ConsultorSQL" `
  --query "Quais são as tabelas disponíveis no banco?"
```

Nesse modo, o agente processa a pergunta informada e encerra o fluxo após a execução.

### 3. Exemplo no Linux

```bash
python promp_to_sql_query.py \
  --path_database "/dados/meu_banco.db" \
  --path_system_prompt "/projeto/system_prompt.txt" \
  --agent_name "ConsultorSQL" \
  --query "Quantos registros existem na tabela clientes?"
```

Os exemplos de caminho pressupõem um banco acessível diretamente pelo processo Python. Se o projeto utilizar outro tipo de banco, informe o caminho ou identificador esperado pela implementação de `sql_db.py`.

## 🔄 Fluxo de execução

O processamento segue estas etapas:

1. **Recepção dos parâmetros:** o programa obtém os caminhos do banco de dados e do prompt, além do nome do agente e da consulta opcional.
2. **Carregamento das instruções:** lê o arquivo de prompt de sistema.
3. **Conexão com o banco:** instancia `SQLtoLLM`, estabelece a conexão e obtém as ferramentas disponíveis.
4. **Configuração do agente:** define o nome, o modelo, as ferramentas e o prompt.
5. **Persistência das configurações:** chama o método `save_agent_settings()`.
6. **Execução:** recebe perguntas em modo interativo ou processa uma única consulta.
7. **Encerramento:** no modo interativo, finaliza quando o usuário informa `/bye`.

## 🔐 Segurança e boas práticas

Como a aplicação pode executar operações por meio de ferramentas conectadas ao banco de dados, recomenda-se:

- Utilizar um usuário de banco com privilégios mínimos, preferencialmente somente leitura.
- Restringir a execução a comandos SQL autorizados.
- Validar as consultas antes da execução.
- Evitar conceder permissões de `INSERT`, `UPDATE`, `DELETE`, `DROP` ou outras operações de alteração quando não forem necessárias.
- Não armazenar senhas, tokens ou chaves de API diretamente no código-fonte.
- Utilizar variáveis de ambiente ou um gerenciador de segredos para credenciais.
- Registrar erros e operações relevantes, evitando expor informações confidenciais nos logs.
- Avaliar limites de tempo de execução e volume de resultados retornados.
- Não considerar as instruções do prompt de sistema como substitutas de controles de acesso implementados no banco e nas ferramentas.

## ⚠️ Limitações conhecidas

- A precisão das respostas depende do modelo de linguagem, das instruções fornecidas e das ferramentas disponíveis.
- O agente pode interpretar incorretamente perguntas ambíguas; os resultados devem ser verificados em aplicações críticas.
- A compatibilidade com diferentes bancos de dados depende da implementação de `sql_db.py`.
- A persistência das configurações depende do comportamento de `save_agent_settings()` em `agents.py`.
- O script cria um identificador de sessão por execução. A continuidade da memória entre execuções depende da implementação do agente.
- O script não demonstra, por si só, mecanismos de autorização, validação de SQL ou tratamento específico de erros de conexão.

## 🛠️ Solução de problemas

### Erro ao conectar ao banco de dados

Verifique se o caminho está correto, se o processo possui permissão de leitura e se o banco é compatível com a implementação de `sql_db.py`.

### Erro ao carregar o modelo

Confira a configuração de `llm.py`, a disponibilidade do servidor de inferência e as credenciais exigidas pelo provedor.

### Erro ao carregar o prompt

Verifique se o arquivo existe, se o caminho informado está correto e se o conteúdo está codificado em UTF-8.

### O agente não consegue consultar uma tabela

Verifique se as ferramentas disponibilizadas por `SQLtoLLM.list_tools()` permitem descobrir o esquema e executar a consulta necessária, além de confirmar as permissões do usuário do banco.


## 👨‍💻 Autor

Desenvolvido por Thiago Paim. 

##  Versão

versão 1.0
---

