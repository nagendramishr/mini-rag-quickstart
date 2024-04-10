#!/usr/bin/python3

from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import uuid
import sys
import json

# COSMOS_KEY and COSMOS_ACCT are set as environment variables defined in setup.sh

# Initialize Cosmos Client
url = "https://" + os.environ['COSMOS_ACCT'] + ".documents.azure.com:443/"
key = os.environ.get('COSMOS_KEY')

client = CosmosClient(url, credential=key)

# Select database
database_name = os.environ['COSMOS_DB'] 
database = client.get_database_client(database_name)

# Select container
container_name = 'facts'
container = database.get_container_client(container_name)


def insert_item(container, fact):


    # generate a guid
    item_id = str(uuid.uuid4())
    # Insert item
    item_body = {
        "id": item_id,
        "fact": fact
    }

    #print(f"Inserting item {item_body}")
    container.upsert_item(body=item_body)

fopen = open('data/cosmosdb-facts.txt', 'r')
lines = fopen.readlines()

for line in lines:
    print(line)
    insert_item(container, line)
