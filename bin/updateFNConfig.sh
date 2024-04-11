#!/bin/sh

export AOAI_KEY=""
export AOAI_ENDPOINT=""
export MyAccount_COSMOSDB=""
export MODEL="gpt35"



az functionapp config appsettings set --name $AOAI_APP --resource-group $RG \
  --settings "AOAI_KEY=$AOAI_KEY" "AOAI_ENDPOINT=$AOAI_ENDPOINT" "MyAccount_COSMOSDB=$MyAccount_COSMOSDB" "MODEL=$MODEL"


