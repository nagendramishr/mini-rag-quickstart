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

    if not req.params.get('question'):
        return func.HttpResponse(
            "Please pass a question on the query string",
            status_code=400
        )

    if inputDocuments:
        client = AzureOpenAI(
            azure_endpoint = os.getenv("AOAI_ENDPOINT"), 
            api_key=os.getenv("AOAI_KEY"),  
            api_version="2024-02-15-preview"
        )

        #Join all the facts into a single string
        facts = "\n".join([doc.data['fact'] for doc in inputDocuments])                        
           
        message_text = [{"role":"system","content": facts}, 
                        {"role":"user","content": req.params.get('question')}]

        completion = client.chat.completions.create(
            messages = message_text,
            model = os.environ.get("MODEL", "gpt35"),
            temperature = float(os.environ.get("TEMPERATURE", "0.7")), 
            max_tokens = int(os.environ.get("MAX_TOKENS", "800")),
            top_p = float(os.environ.get("TOP_P", "0.95")),
            frequency_penalty = float(os.environ.get("FREQUENCY_PENALTY", "0")),
            presence_penalty = float(os.environ.get("PRESENCE_PENALTY", "0")),
            stop = os.environ.get("STOP", "None")
        )

    return func.HttpResponse(
        "{\"response\": \""+completion.choices[0].message.content+"\"}",
        status_code=200
        )


