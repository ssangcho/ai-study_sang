from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_community.tools import DuckDuckGoSearchRun

class DuckDuckGoAgent:
	def __init__(self):
		self.prompt = ChatPromptTemplate.from_messages([
			("system", "당신은 인간과 대화하는 유용한 AI입니다, 답을 모른다면 그냥 모른다고 말하고 지어내지 마세요"),
			("human", "{message}"),
		])
		self.llm = ChatOpenAI(temperature=0)
		self.chain = self.prompt | self.llm 
		print("DuckDuckGoAgent가 생성되었습니다.")
			
	def invoke (self, message) -> AIMessage:
		search = DuckDuckGoSearchRun()
		search_result = search.invoke(message)
		print(search_result)
		# return AIMessage(content=search_result)
		return self.chain.invoke(f"{message}\n 다음 검색결과를 참고하여 답해줘 {search_result}")

