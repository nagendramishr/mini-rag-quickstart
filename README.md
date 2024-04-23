# Mini-Rag-Quickstart!

## Background

The goal of this project is to help you get up and running quickly with a build out of a RAG model. You can skip to the actual build out below or if you're interested in learning more about the RAG model, you can read some of the documentation here:

> - [Hugging Face’s RAG](https://huggingface.co/docs/transformers/model_doc/rag)  documentation provides a detailed explanation of the RAG model and its implementation.
> - [RAG and generative AI](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) - Azure AI Search: This page provides an overview of RAG and its application in Azure AI Search.
> - [IBM’s AI RAG page](https://www.ibm.com/architectures/hybrid/genai-rag) provides a conceptual architecture of a RAG solution, showing the major components and the flow of interactions between them to respond to a user query.
> - [A Simple Guide To Retrieval Augmented Generation Language Models](https://www.smashingmagazine.com/2024/01/guide-retrieval-augmented-generation-language-models/) includes a diagram showing the generator flow in a RAG-based system.
> - [Retrieval augmented generation (RAG) explained](https://www.superannotate.com/blog/rag-explained) provides a simple diagram that shows the process of RAG at the intersection of natural language generation (NLG) and information retrieval (IR).

In general, RAG is a way to overcome the need to constantly train and retrain a Large Language Model. Imagine a neural network with 200 billion nodes with each node connected to the others. These LLM's are the engine in generative AI, but they are very expensive to train because they require a lot of computation to build. ( Think large GPU clusters running complex calculations for a long time.) This is so computationally expensive that keeping up with new data or customizing becomes cost prohibitive. You can learn more about it in this in-depth description here:  [Efficient LLM Training](https://arxiv.org/pdf/2104.04473.pdf). .

Customers who implement the RAG model can not only solve the training issues, but they also gain the following benefits:   

> - **Access to External Knowledge:** RAG provides LLMs access to external knowledge through documents, resulting in contextually accurate and factual responses.
> - **Cost-Effective:** RAG is more cost-effective than fine-tuning, as it doesn’t require the labeled data and computational resources that come with model training.
> - **Improves Accuracy:** RAG improves the accuracy and contextuality of LLM-generated responses while minimizing factual inaccuracies.
> - **Up-to-Date Information:** RAG ensures that the model has access to the most current, reliable facts.
> - **Transparency:** Users have access to the model’s sources, ensuring that its claims can be checked for accuracy and ultimately trusted.
> - **Control Over Generated Text:** Organizations have greater control over the generated text output.
> - **Reduces Data Leakage:** By grounding an LLM on a set of external, verifiable facts, the model has fewer opportunities to pull information baked into its parameters. This reduces the chances that an LLM will leak sensitive data.
> - **Reduces Need for Continuous Training:** RAG reduces the need for users to continuously train the model on new data and update its parameters as circumstances evolve4.

# Project Overview

This project will allow you to build a RAG implementation by incorporating **Azure OpenAI** and **CosmosDB** into a **Teams Channel**.  In this implementation, you will be able to ask questions about sample data uploaded into the database via a **Teams** chat.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/1ae8c7c6-fc72-485a-85e5-701f696339fb)


| Component | Activity |
|-----------|----------|
|Teams     | User enters text in chat|
| Logic App | Logic app invokes Azure function.  Once the call to the function completes, the App injects the response back into the chat as a response. |
|Azure Function | Functions reads contents from cosmosDB, creates the prompt and calls OpenAI.  After receiving the response from OpenAI, the function perform additional computation before responding to the Logic App. |
| CosmosDB | Contains the data that will be used to augment the chat request |
|  OpenAI | The hosted LLM that is responsible for processing the enhanced request and formulating a response.  |
-------------------
## Prerequisites

You will need the following in order to run through this quickstart:

1. An Azure subscription with the ability to create Azure resources: ( Resource Group, Logic App, Azure Function, CosmosDB and Azure OpenAI ).
2. Access to the OpenAI offering in Azure. [ You can request access if you do not have it.](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
3. A computer with VS Code installed on it:  [Windows / Mac](https://code.visualstudio.com/download)  -  [wsl](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode).
4. [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#install-the-azure-functions-core-tools) installed on the computer.
5. Python 3.11 or 3.10. 

## Building it manually
### Create the resources:
#### 1. Create a new Teams channel

Teams will be used as the chat UI for this project.  To keep things simple, create a new team. Once created, we'll use it's general channel for the entry point into RAG.

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/3805c120-82af-48da-83aa-500f68f50dec" width="500">


#### 2. Create a new Logic App

The **Logic App** will be used to shuttle message between the **Teams** chat and **Azure Functions**.  Create a new **Logic App** in the **Azure Portal**.

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/6f5c2315-812f-417a-b1b2-3d82973125ab" width="500">

#### 3. Create a new Azure Function

The **Azure Function** app will be used to call the **OpenAI** service and is we will implement the RAG model.  Create a new instance in the portal using Python 3.11 on Linux using the serverless option.  We'll need to deploy this from you laptop so If you have a different version of python installed locally, choose the version that matches your local system.

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/fd2c9000-aff1-434b-835c-a3f836e272e2" width="500">

#### 4. Create a new OpenAI instance

Now for the LLM magic.  Here we'll create an **OpenAI** Instance from the portal.  Note, you will need to apply for access  ( and be accepted ) before you can instantiate this.  If you don't have access yet, click on [Apply for access](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/83126828-2798-4e98-8889-a39faafa4470" width="400">

You will receive an email that you have been granted access.  Once you have that, create a new instance using the S0 tier.  We’ll create the GPT-3 instance in the next step.

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/d03ef280-afa1-485e-9833-13f60ada2578" width="500">


##### Create a LLM deployment 

In the portal navigate to the deployed instance and select "Model deployments" on the left:

<img width="200" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/f6dc7d7d-6a5b-4c28-9562-9abff246c736">

This will ask you to confirm that you're navigating to **Azure OpenAI Studio**.  Confirm and create a new deployment:

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/58cc84a8-8fb4-490a-930b-5ceef29d1576" width="400">

Make a note of this deployment name, the endpoint and key. You will need these when you configure your **Azure Function** settings.  In the example above, the deployment name is called **gpt35**.


#### 5. Create a new CosmosDB instance

Now we'll need a place to keep the data that will be used to generate the enhanced prompt.  We're going to store this information in **CosmosDB**.  The cool thing about **CosmosDB** is that it very easy to connect to **Azure Functions**.  **Azure Functions** has a lot of different bindings including **SQL** but it's slightly less complex to read from **CosmosDB**.  ( You can watch [this video](https://www.youtube.com/watch?v=4d71whuKqNM&t=8s&ab_channel=AzureAppModernization) for more details on connecting CosmosDB. )

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/214fa10d-5d8c-4d51-875c-f4b808d4e4b4" width="500">

---------------------

## Stitching it all together

Overall implementing a Retrieval-Augmented Generation (RAG) model involves several steps.  They are detailed below.  In our implementation, we're doing all the steps except for the: Embedding and Vector Database steps.  After you finish implementation, try to identify where each of these steps are performed.

> - **Define Use Case:** Start by defining the specific use case for your RAG implementation. Determine the domain or topic for which you want the Large Language Model (LLM) to generate responses augmented by retrieved information.
> - **Select an LLM:** Choose a suitable Large Language Model for your RAG implementation.
> - **Data Collection:** Collect a set of documents, also known as a corpus, that the model will use to retrieve information.
> - **Data Preprocessing:** Transform and enrich the data to make it suitable for model augmentation.
> - **Embedding:** Use an embedding model to convert the source data into a series of vectors that represent the words in the client data.
> - **Vector Database:** Store the generated embeddings in a vector database.
> - **User Query:** Receive a user input and perform a similarity measure between the collection of documents and the user input.
> - **Post-Processing:** Post-process the user input and the fetched document(s). The post-processing is done with an LLM.
> - **Response Generation:** Generate a response based on the user’s query and the retrieved documents.

### Uploading the data:

In our implementation, we are going to ingest sample data and layer it on top of the general knowledge the LLM already knows about.  We will then use **Azure OpenAI** to answer questions about the combined data.  This repo already has the source data as 1 sentence for each fact but you can tune it if you like.

In order to ingest the sample data, we're going to use the Cloud Shell ( or your own az cli that is already logged in )

<img width="650" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/b138de44-5a73-442e-9c95-dca6b7890e12">

In the cloud shell, clone this repo so that you have access to the scripts:

```
git clone https://github.com/nagendramishr/mini-rag-quickstart.git
```

Edit the first three variables of bin/setup.sh as shown below with the correct values for the resources your created. 

```
>head -5 bin/setup.sh
#!/bin/sh

export RG=aoai-rag 
export COSMOS_ACCT=nvmopenaicosmosdb 
export AOAI_APP=nvmaoai-teams
```

#### Modify any facts from data/cosmosdb-facts.txt

As stated earlier, the sample facts are stored in this file: `data/cosmosdb-facts.txt`. They were generated via the prompt generator as a test for this exercise.  You can modify the prompt and generate your own facts or add additional lines to the data.  The prompt is contained in `data/datagen_prompt.txt` and you can simply cut and paste it into bing chat to generate a new response set.

### Run the setup scripts and upload the facts into the DB

#### Create a new CosmosDB container
```
chmod ugo+x bin/*

source bin/setup.sh
bin/createDB.sh
bin/insertCosmos.py

```

Your **cosmosDB** instance should now be updated with the contents of the data file.  You can use the data explorer to validate or update the facts in the **Azure Portal**.

<img width="1117" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/57330179-4f4e-4406-8a59-2b8787230059">

### Deploying the Azure Function:

#### Get your local environment ready

The source code for an Azure Function has already been created for you in `src/azureFunction`.  This code needs to be deployed to **Azure** and then configured with the endpoints for **CosmosDB** and **OpenAI**.  

Since you will be doing development in this code for your homework, it will be best to open it up in VS Code locally on your local machine.  For this part, you will need to install Python and the [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#install-the-azure-functions-core-tools)    You will also need the following VSCode extensions installed:

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/32fb63a4-d068-49ee-a5ba-81844a56e124" width="350">
<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/2eafb8db-7c7f-4ac0-9ca8-aa9a32077818" width="350">


Once installed, clone the repo locally and navigate to the src/azureFunction folder.

Clone the code locally and source setup.sh:
```
> git clone https://github.com/nagendramishr/mini-rag-quickstart.git
> cd mini-rag-quickstart
> source bin/setup.sh
```


Open up **VS Code** to the ``src/azureFunctions`` folder that you cloned locally.  Your **VS Code Explorer** section should look like this:

<img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/252e4c7e-1fc3-4874-a293-de06954ec1fb" width="200">


#### Deploying the code

Deploy your code is built into VSCode.  If you want to know more about deploying from VS code you can watch [this video](https://www.youtube.com/watch?v=-W2utG3CCrs&t=3s&ab_channel=AzureAppModernization).

1. Type `Ctrl-Shift-P`  and select **Azure Functions: Deploy to Function App...**.
2. Select your subscription
3. Select your function app
4. Confirm that you want to deploy the function
5. Verify that the code was deployed by looking for the function in the **Azure Portal**

<img width="1013" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/710ce730-091d-46aa-9b72-426acc821b0c">

If you do not see the function `AskQuestion`, than the deployment did not succeed ( or it is still uploading ).  

#### Configure the Azure Function

Now that your function code has been deployed, you next need to configure it so that it knows about your **CosmosDB** and **OpenAI** endpoints.

Edit the contents of bin/updateFNConfig.sh

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/73cd59c0-5cec-46ba-9b66-756c83fe4a30)

Note: The `AOAI_KEY` and `AOAI_ENDPOINT` are listed on the Azure Portal:

<img width="323" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/a42f03d0-3fb7-4794-9ff7-dec87f218411">

The `MyAccount_COSMOSDB` variable shuld be defined with the value of `$COSMOS_CONNSTR`. You can also grab it from the portal as well:

<img width="287" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/61e0fe88-bcdb-4afa-bf67-c5f8763090e7">


Now run the update script to configure the values in your Azure Function.

```
bin/updateFNConfig.sh
```

You may have to restart your Azure function, but it should now be up and running.  You are ready to connect it to the **Logic App**.

### Create your Logic App.

Overall, the logic app has 3 steps.
1. It gets triggered when a message appears in Teams.  In this step we will need to configure the teams connection and grant access to the **Logic App**.
2. Once a message is received, if the Subject is "Question", the Azure function from the previous step will be called with the users question.
3. The response from the **Azure Function** will be uploaded into **Teams** as a reply to the original message.

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/fc311cea-f0e8-41f9-8c37-7b7989b0fbc4" width="400">

In the first step, add a trigger: **When a new channel message is added**.  Select the team that was created in step 1 along with the General channel.  You will be asked to login and allow the **Logic App** to connect on your behalf.  For the question **How often do you want to check for items?**, select once per minute.

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/9d25e91e-740f-427d-a388-f1bf23d3731d" width="500">

Add **Condition** as the next action and require that the Message Subject is equal to **"Question"**. If up don't do this, the bot will get triggered when it responds to your question and it will respond to its own response.

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/a6b2e6a9-87e1-4ce6-ba22-1c20880f312a" width="500">

On the **True** side of the condition, add an **HTTP** action.  This action will call the **Azure Function** with a question whose value is the **message body content** that was posted on teams.  For the URL, enter the URL for your **Azure Function**.

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/fc84af51-b7fe-40aa-ade6-91d46d3fac72" width="500">

You can find the URL for your **Azure Function** by clicking into the "AskQuestion" function on the Overview page and then clicking **Get Function URL**:

<img width="550" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/d53d5487-60bb-41f9-9d5b-459c5f75ca18">

After the HTTP step, add another action: **Reply with a message in channel**.  Here, the important part is to select the message ID from the original question as the message ID for the response.  Also, be sure to include the Body from the HTTP request which contains the BOT's response.

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/eecff9c7-e25d-4c34-b287-3a7c95c07e03" width="500">


# Testing the RAG Model:

Now that the data has been upload and your **Azure** services configured, you can test the solution by posting a message in the teams channel and after a few minutes, you will see a response.

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/e12e0d46-cde9-4aec-9866-e31785b781b4" width="600">

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/f6a0d6fd-281d-487d-91fa-dd3a69cd9090" width="800">

   <img src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/199b9c18-f14d-4096-9318-c46b6a8e76b9" width="800">

