from flask import request
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_core.output_parsers import StrOutputParser
import json, requests, sqlite3,re

def query():
    if request.method == 'POST':
        
        # Get essential information from request.
        vectordb_name = request.form.get('vectordb_name')
        if not vectordb_name:
            return 'Input Vectordb name'
        
        namespace = request.form.get('namespace')
        print("this is namespace===>",namespace)
        prompt = request.form.get('prompt')
        if not prompt:
            return 'Input prompt'
        
        model_max_array_lenth = int(request.form.get('model_max_array_lenth'))
        if not model_max_array_lenth:
            return 'Input max array lenth of the model'
        
        model_max_number_token = int(request.form.get('model_max_number_token'))
        if not model_max_number_token:
            return 'Input max number token of the model'
        
        model_temperature = float(request.form.get('model_temperature'))
        if not model_temperature:
            return 'Input model temperature'
        
        model_max_string_token_length = int(request.form.get('model_max_string_token_length'))
        if not model_max_string_token_length:
            return 'Input max string token length of the model'
        model_name = ['roberta-base', 'all-MiniLM-L6-v2', 'squeezebert/squeezebert-uncased']
        
        deliver = ""
        for model in model_name:

            embedding_function = SentenceTransformerEmbeddings(model_name=model)
            ChromaDB = Chroma(persist_directory=f"./Databases/{model}", embedding_function=embedding_function)

            retriever = ChromaDB.as_retriever(search_type="similarity", search_kwargs={"k": 1000})
            retrieved_docs = retriever.invoke(prompt)
            number = 0
            for para in retrieved_docs:
                if not namespace == "":
                    if para.metadata['namespace'] == namespace and para.metadata['vectordb_name'] == vectordb_name:
                        deliver += para.page_content
                else:
                    if para.metadata['vectordb_name'] == vectordb_name:
                        deliver += para.page_content
                number += 1
                if number == 4:
                    break
        print("this is deliver====>", deliver)
        if deliver == "":
            return 'Empty Database'
        
        deliver_prompt = f"As a seasoned data analyst, please answer users' question based on {deliver}. Users' question:{prompt}.\nanswer:"

        # Use LLM endpoint
        url = "http://91.201.5.33:8000/query_chatgpt"

        payload = json.dumps({
            "prompt": deliver_prompt,
            "model_args": {
                "max_array_length": model_max_array_lenth,
                "max_number_tokens": model_max_number_token,
                "temperature": model_temperature,
                "max_string_token_length": model_max_string_token_length
            },
            "response_schema": {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "Output"
                    }
                },
                "required": [
                    "response"
                ]
            }
        })

        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        response = requests.request("POST", url, headers=headers, data=payload)
        
        return response.text
    
    return "OK"