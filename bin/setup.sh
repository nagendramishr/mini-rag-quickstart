#!/bin/bash

export RG=aoai-rag
export COSMOS_ACCT=nvmaoaidb
export COSMOS_DB=aoaidb
export AOAI_APP=nvmaoai-teams

export COSMOS_KEY=`az cosmosdb keys list --name $COSMOS_ACCT --resource-group $RG --type keys | jq -r '.primaryMasterKey'`
export COSMOS_CONNSTR="AccountEndpoint=https://$COSMOS_ACCT.documents.azure.com:443/;AccountKey=$COSMOS_KEY;"
# install the cosmos module
pip install azure-cosmos



