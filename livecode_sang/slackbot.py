from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
from langgraph_workflow import LangGraphWorkflow
from dotenv import load_dotenv
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# 필수 환경 변수 확인
required_env_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET", "SLACK_APP_TOKEN"]
for var in required_env_vars:
    if not os.environ.get(var):
        raise ValueError(f"필수 환경 변수 {var}가 설정되지 않았습니다.")

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

workflow = LangGraphWorkflow()

@app.message(".*")
def message_handler(message, say):
    try:
        user_input = message['text']
        logger.info(f"Received message: {user_input}")
        response = workflow.start({"message": user_input})
        if "message" in response:
            say(response["message"])
        else:
            say("죄송합니다. 응답을 생성하는 데 문제가 발생했습니다.")
    except Exception as e:
        logger.error(f"Error in message handler: {str(e)}", exc_info=True)
        say(f"죄송합니다. 오류가 발생했습니다. 관리자에게 문의해 주세요.")

if __name__ == "__main__":
    try:
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        logger.info("Starting Slack bot...")
        handler.start()
    except Exception as e:
        logger.error(f"Error starting Slack bot: {str(e)}", exc_info=True)
    
#from slack_bolt.adapter.socket_mode import SocketModeHandler
#from slack_bolt import App
#from langgraph_workflow import LangGraphWorkflow
#from dotenv import load_dotenv
#import os
#
#load_dotenv()
#
#app = App(
#    token=os.environ.get("SLACK_BOT_TOKEN"),
#    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
#)
#
#workflow = LangGraphWorkflow()
#
#@app.message(".*")
#def message_handler(message, say):
#    try:
#        user_input = message['text']
#        response = workflow.start({"message": user_input})
#        say(response["message"])
#    except Exception as e:
#        say(f"죄송합니다. 오류가 발생했습니다: {str(e)}")
#
#if __name__ == "__main__":
#    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()



#from slack_bolt.adapter.socket_mode import SocketModeHandler
#from slack_bolt import App
#from langgraph_workflow import LangGraphWorkflow
#from dotenv import load_dotenv
#import os
#from langchain.prompts import ChatPromptTemplate
#from langchain.schema import HumanMessage, SystemMessage
#
#from langchain_openai import ChatOpenAI
#from langchain.prompts import ChatPromptTemplate
#from typing import TypedDict
#import os
#
#from dotenv import load_dotenv
#
#
#
#load_dotenv()
#
#app = App(
#    token=os.environ.get("SLACK_BOT_TOKEN"),
#    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
#)
#
#llm = ChatOpenAI(
#    temperature=0,
#)
#
##당신은 인간과 대화하는 유용한 AI입니다, 답을 모른다면 그냥 모른다고 말하고 지어내지 마세요"
#
#prompt = ChatPromptTemplate.from_messages([
#    SystemMessage(content="당신은 인간과 대화하는 유용한 AI입니다, 답을 모른다면 그냥 모른다고 말하고 지어내지 마세요"),
#    HumanMessage(content="{message}")
#])
#
#chain = prompt | llm
#
#class AgentState(TypedDict):
#    message: str
#    
#def chat_agent(state: AgentState) -> AgentState:
#    result = chain.invoke({"message": state["message"]})
#    state["message"] = result.content
#    return state
#
#workflow = LangGraphWorkflow()
#
#@app.message(".*")
#def message_handler(message, say):
#    user_input = message['text']
#    formatted_prompt = prompt.format(message=user_input)
#    response = workflow.start({"message": formatted_prompt})
#    say(response["message"])
#
#
## Start your app
#if __name__ == "__main__":
#    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
#