import azure.functions as func
import datetime
import json
import logging
import os
from openai import AzureOpenAI

app = func.FunctionApp()

@app.function_name(name="AskQuestion")
@app.route(route="AskQuestion", auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(arg_name="inputDocuments", 
                     database_name="aoaidb",
                     container_name="facts",
                     connection="MyAccount_COSMOSDB")
def test_function(inputDocuments: func.DocumentList, req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if inputDocuments:
        client = AzureOpenAI(
            azure_endpoint = os.getenv("AOAI_ENDPOINT"), 
            api_key=os.getenv("AOAI_KEY"),  
            api_version="2024-02-15-preview"
        )

        #Join all the facts into a single string
        facts = "\n".join([doc.data['fact'] for doc in inputDocuments])                        
           
        message_text = [{"role":"system","content": facts}, 
                        {"role":"user","content": "Who is most qualified to work on functions"}]

        completion = client.chat.completions.create(
            model="gpt35",
            messages = message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

    return func.HttpResponse(
        completion.choices[0].message.content,
        status_code=200
        )


