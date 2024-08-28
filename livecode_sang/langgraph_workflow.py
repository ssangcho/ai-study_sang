import logging
from typing import Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agent_state import AgentState
from chat_agent import ChatAgent
from duckduckgo_agent import DuckDuckGoAgent
from agent_selector import AgentSelector

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangGraphWorkflow:
    def __init__(self):
        self.workflow = StateGraph(AgentState)
        self._setup_workflow()
        self.app = self.workflow.compile()

    def _setup_workflow(self):
        self.workflow.add_node("agent_selector", self.agent_selector)
        self.workflow.add_node("chat_agent", LangGraphWorkflow.chat_agent)
        self.workflow.add_node("search_agent", LangGraphWorkflow.search_agent)
        
        self.workflow.set_entry_point("agent_selector")
        
        self.workflow.add_conditional_edges(
            "agent_selector", 
            self.agent_selector_router,
            {
                "chat_agent": "chat_agent", 
                "search_agent": "search_agent",
                "end": END
            }
        )

        self.workflow.add_edge("chat_agent", END)
        self.workflow.add_edge("search_agent", END)

    def start(self, state: AgentState) -> AgentState:
        logger.info(f"Starting workflow with message: {state['message']}")
        try:
            result = self.app.invoke(state)
            logger.info(f"Workflow result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in workflow: {str(e)}")
            return {"message": "An error occurred during processing."}

    @staticmethod
    def agent_selector(state: AgentState) -> AgentState:
        logger.info("Selecting agent...")
        try:
            selector = AgentSelector()
            result = selector.process(state["message"])
            state["agent_name"] = result["agent_name"]
            state["args"] = result["args"]
            logger.info(f"Selected agent: {state['agent_name']}")
            return state
        except Exception as e:
            logger.error(f"Error in agent selection: {str(e)}")
            state["agent_name"] = "error"
            state["args"] = {"message": "An error occurred during agent selection."}
            return state

    @staticmethod
    def chat_agent(state: AgentState) -> AgentState:
        logger.info("Executing chat agent...")
        try:
            agent = ChatAgent()
            message = state.get("args", {}).get("message", state["message"])
            result = agent.invoke(message)
            state["message"] = result.content
            logger.info(f"Chat agent response: {state['message']}")
            return state
        except Exception as e:
            logger.error(f"Error in chat agent: {str(e)}", exc_info=True)
            state["message"] = "An error occurred during chat processing."
            return state

    @staticmethod
    def search_agent(state: AgentState) -> AgentState:
        logger.info("Executing search agent...")
        try:
            agent = DuckDuckGoAgent()
            content = state.get("args", {}).get("content", state["message"])
            result = agent.invoke(content)
            state["message"] = result.content
            logger.info(f"Search agent response: {state['message']}")
            return state
        except Exception as e:
            logger.error(f"Error in search agent: {str(e)}", exc_info=True)
            state["message"] = "An error occurred during search processing."
            return state

    @staticmethod
    def agent_selector_router(state: AgentState) -> Literal["chat_agent", "search_agent", "end"]:
        agent = state["agent_name"]
        
        if agent == "Chat":
            return "chat_agent"
        elif agent == "Search":
            return "search_agent"
        else:
            return "end"
  
# 이전에 만든건데 필요하다면 복구해도 좋아.
#class LangGraphWorkflow:
#	def __init__(self):
#		self.workflow = StateGraph(AgentState)
#		self.workflow.add_node("agent_selector", self.agent_selector)
#		self.workflow.add_node("chat_agent", self.chat_agent)
#		self.workflow.add_node("search_agent", self.search_agent)
#		
#		self.workflow.set_entry_point("agent_selector")
#		
#		self.workflow.add_conditional_edges(
#			"agent_selector", 
#			self.agent_selector_router, {
#        "chat_agent": "chat_agent", 
#        "search_agent":"search_agent",
#        "not_relevant": END
#      }
#		)
#
#		self.workflow.add_edge("chat_agent", END)
#		self.workflow.add_edge("search_agent", END)
#
#		self.app = self.workflow.compile()
#
#		with open('langgraph.png', 'wb') as file:
#			file.write(self.app.get_graph().draw_mermaid_png())
#
#	def start(self, state: AgentState) -> AgentState:
#		return self.app.invoke(state)
#	
#	def agent_selector(self, state: AgentState) -> AgentState:
#		print("Selecting agent...")
#		selector = AgentSelector()
#		result = selector.process(state["message"])
#		state["agent_name"] = result.tool_calls[0]["name"]
#		state["args"] = result.tool_calls[0].get("args", {})
#		return state
#	
#	def chat_agent(self, state: AgentState) -> AgentState:
#		print("chat_agent")
#		agent = ChatAgent()
#		result = agent.invoke(state)
#		state["message"] = result.content
#		return state
#
#	def search_agent(self, state: AgentState) -> AgentState:
#		print("search_agent")
#		agent = DuckDuckGoAgent()
#		result = agent.process(state["message"])
#		state["message"] = result.content
#		return state
#
#def agent_selector_router(self, state: AgentState) -> Literal["chat_agent", "search_agent", "not_relevant"]:
#        agent = state["agent_name"]
#        
#        if agent == "Chat":
#            return "chat_agent"
#        elif agent == "Search":
#            return "search_agent"
#        else:
#            return "not_relevant"

#
#	def agent_selector_router(self, state: AgentState) -> Literal["chat_agent", "search_agent","not_relevant"]:
#		# agent = state["agent_name"]
#		# Llm을 호출해서 결과를 받아서 agent를 결정하는 로직
#		agent = "search_agent"
#		# agent = "no agent"
#
#		if agent == "chat":
#			return "chat_agent"
#		elif agent == "search_agent":
#			return "search_agent"	
#		else:
#			return "not_relevant"
#