import uuid
import streamlit as st
from server.main import chatmodel
from langchain_core.messages import HumanMessage,AIMessage

def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    CONFIG={'configurable':{'thread_id':thread_id}}
    return chatmodel.get_state(config=CONFIG).values['messages']

def change_mssg_format(messages):
    temp_mssg=[]
    for message in messages:
        if isinstance(message,HumanMessage):
            role='user'
        else:
            role='assistant'
        temp_mssg.append({'role':role,'content':message.content})
    return temp_mssg