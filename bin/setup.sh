#!/bin/bash

export RG=aoai-rag
export COSMOS_ACCT=nvmaoaidb
export COSMOS_DB=aoaidb

export COSMOS_KEY=`az cosmosdb keys list --name $COSMOS_ACCT --resource-group $RG --type keys | jq -r '.primaryMasterKey'`

# install the cosmos module
pip install azure-cosmos



