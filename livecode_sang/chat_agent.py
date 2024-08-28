from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

class ChatAgent:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 인간과 대화하는 유용한 AI입니다, 답을 모른다면 그냥 모른다고 말하고 지어내지 마세요"),
            ("human", "{message}"),
        ])

        self.llm = ChatOpenAI(temperature=0)
        self.chain = self.prompt | self.llm

    def invoke(self, message) -> AIMessage:
        return self.chain.invoke(message)
        