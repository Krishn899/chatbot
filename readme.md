we are using langchain and langgraph to make a intelligent chatbot with memory and rag.

i am using huggingface to acess free llm model, the model i will be using for this particular project is "google/gemma-4-31B-it".

for ui i am using streamlit, we are using session state dictionary it is a special dictionary in streamlit which doesnt refresh each time we press enter in streamlit this help us in storing chat history for that seesion of user, may implement a better alternative in future for this