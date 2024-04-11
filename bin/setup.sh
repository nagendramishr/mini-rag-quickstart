#!/bin/bash

export RG=aoai-rag                    # The name of the resource group for the quick start
export COSMOS_ACCT=nvmaoaidb          # The name of the Cosmos account
export AOAI_APP=nvmaoai-teams         # The name of the function app

## DO NOT CHANGE THE VALUES BELOW
export COSMOS_DB=aoaidb               

## Calculated values
export COSMOS_KEY=`az cosmosdb keys list --name $COSMOS_ACCT --resource-group $RG --type keys | jq -r '.primaryMasterKey'`
export COSMOS_CONNSTR="AccountEndpoint=https://$COSMOS_ACCT.documents.azure.com:443/;AccountKey=$COSMOS_KEY;"

# install the cosmos module
pip install azure-cosmos



