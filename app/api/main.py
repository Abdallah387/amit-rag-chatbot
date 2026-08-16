 
# TODO: Set up FastAPI app for the chatbot API
# TODO: Implement /chat endpoint to handle user queries
# TODO: Implement /chat/history endpoint to retrieve chat history
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'RAG Chatbot API running'}

#chatpot