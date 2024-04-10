# Create the cosmosdb DB and container
az cosmosdb sql database create -a $COSMOS_ACCT -g $RG -n $COSMOS_DB
az cosmosdb sql container create --account-name $COSMOS_ACCT --database-name $COSMOS_DB --resource-group $RG --name facts --partition-key-path "/Id"


