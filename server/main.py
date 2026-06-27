import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()
HF_API = os.getenv('hf_api')


def build_model() -> ChatHuggingFace:
    llm = HuggingFaceEndpoint(
        repo_id='google/gemma-4-31B-it',
        huggingfacehub_api_token=HF_API,
    )
    return ChatHuggingFace(llm=llm)


model = build_model()


class ChatModel(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat(state: ChatModel) -> ChatModel:
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}


checkpointer = MemorySaver()
graph = StateGraph(ChatModel)

graph.add_node('chat', chat)
graph.add_edge(START, 'chat')
graph.add_edge('chat', END)

chatmodel = graph.compile(checkpointer=checkpointer)


def run_cli() -> None:
    thread_id = '1'
    print('welcome to our platform, to end the conversation just enter bye')
    while True:
        user_message = input('user message: ')
        print(f'user: {user_message}')

        if user_message.strip().lower() in ['exit', 'bye', 'quit']:
            break

        config = {'configurable': {'thread_id': thread_id}}
        response = chatmodel.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)
        print('AI: ', response['messages'][-1].content)


if __name__ == '__main__':
    run_cli()