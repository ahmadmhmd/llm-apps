# main.py
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain_cerebras.chat_models import ChatCerebras
from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from windows_use.agent import Agent
from dotenv import load_dotenv

load_dotenv()

# llm = ChatGoogleGenerativeAI(model='gemini-flash-lite-latest', temperature=0.2)
# llm=ChatCerebras(api_key=os.getenv("CEREBRAS_API_KEY"), model="gpt-oss-120b", temperature=0.2)
llm=ChatOllama(model='qwen3-vl:235b-cloud')
instructions=['We have Claude Desktop, Perplexity and ChatGPT App installed on the desktop so if you need any help, just ask your AI friends.']
agent = Agent(instructions=instructions,llm=llm,use_vision=True)
query=input("Enter your query: ")
agent_result=agent.invoke(query=query)
print(agent_result.content)