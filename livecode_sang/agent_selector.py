import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Chat(BaseModel):
    """chatbot용 api를 호출합니다."""
    message: str = Field(..., description="대화 내용")

class Search(BaseModel):
    """search api를 호출합니다."""
    content: str = Field(..., description="search 내용")

class AgentSelector:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
          ("system", "제공한 내용에 대해서 사용가능한 Agent를 선택하여 결과를 돌려주는 ai입니다"),
          ("human", "{message}"),
        ])
        self.llm = ChatOpenAI(temperature=0)
        self.tools = [Chat, Search]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.chain = self.prompt | self.llm_with_tools 

    def process(self, message: str) -> Dict[str, Any]:
        try:
            result = self.chain.invoke({"message": message})
            logger.info("Agent selection raw result: %s", result)
            
            if hasattr(result, 'tool_calls') and result.tool_calls:
                tool_call = result.tool_calls[0]
                return {
                    "agent_name": tool_call['name'],
                    "args": tool_call['args']
                }
            elif hasattr(result, 'content'):
                return {
                    "agent_name": "not_relevant",
                    "args": {"message": result.content}
                }
            else:
                return {
                    "agent_name": "not_relevant",
                    "args": {"message": message}
                }
        except Exception as e:
            logger.error(f"Error in agent selection: {str(e)}", exc_info=True)
            return {
                "agent_name": "error",
                "args": {"message": "An error occurred during agent selection."}
            }
                    
                
            
            
            
            
#from langchain_openai import ChatOpenAI
#from langchain.prompts import ChatPromptTemplate
#from pydantic import BaseModel, Field
#
#class Chat(BaseModel):
#    """chatbot용 api를 호출합니다."""
#    message: str = Field(..., description="대화 내용")
#
#class Search(BaseModel):
#    """search api를 호출합니다."""
#    content: str = Field(..., description="search 내용")
#
#class AgentSelector:
#    def __init__(self):
#        self.prompt = ChatPromptTemplate.from_messages([
#          ("system", "제공한 내용에 대해서 사용가능한 Agent를 선택하여 결과를 돌려주는 ai입니다"),
#          ("human", "{message}"),
#        ])
#        self.llm = ChatOpenAI(temperature=0)
#        self.tools = [Chat, Search]
#        self.llm_with_tools = self.llm.bind_tools(self.tools)
#        
#        self.chain = self.prompt | self.llm_with_tools 
#
#    def process(self, message) -> dict:
#        result = self.chain.invoke({"message": message})
#        print("Agent selection raw result:", result)
#        
#        if hasattr(result, 'tool_calls') and result.tool_calls:
#            tool_call = result.tool_calls[0]
#            return {
#                "agent_name": tool_call.name,
#                "args": tool_call.args
#            }
#        else:
#            return {
#                "agent_name": "not_relevant",
#                "args": {"message": result.content if hasattr(result, 'content') else message}
#            }