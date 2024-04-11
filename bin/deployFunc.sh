#!/bin/sh

# make soure that env vars are defined
if [ -z "$RG" ]; then
    echo "RG is not defined"
    exit 1
fi

if [ -z "$AOAI_APP" ]; then
    echo "RG is not defined"
    exit 1
fi

cd src/azureFunction

# make the dist directory
mkdir -p dist
# remove old zip files
rm -f dist/aoai.zip

echo "Creating the zip file for the function app"
# Create a zip file of the function code
zip -r dist/aoai.zip *.py host.json requirements.txt local.settings.json


echo "\nDeploying the function app ( This will take several minutes )"

# Deploy the function app
az functionapp deployment source config-zip -g $RG -n $AOAI_APP --src dist/aoai.zip
