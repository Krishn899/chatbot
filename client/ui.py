import sys
from pathlib import Path

import streamlit as st
from langchain_core.messages import HumanMessage

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from server.main import chatmodel


if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input=st.chat_input('Type here')
thread_id='1'
config={'configurable':{'thread_id':thread_id}}
if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    
    with st.chat_message('assistant'):
            ai_message=st.write_stream(
                    message_chunk.content for message_chunk,metadata in chatmodel.stream(
                        {'messages':[HumanMessage(content=user_input)]},
                        config=config,
                        stream_mode='messages'
                    )
                )
            
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})