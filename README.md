# Mini-Rag-Quickstart!

## Background

The goal of this project is to help you get up an running quickly with a build out of a RAG model. Before you dive in, if you're interested in learning more about the RAG model, you can read some of the documentation here:

> - [Hugging Face’s RAG](https://huggingface.co/docs/transformers/model_doc/rag)  documentation provides a detailed explanation of the RAG model and its implementation.
> - [RAG and generative AI](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) - Azure AI Search: This page provides an overview of RAG and its application in Azure AI Search.
> - [IBM’s AI RAG page](https://www.ibm.com/architectures/hybrid/genai-rag) provides a conceptual architecture of a RAG solution, showing the major components and the flow of interactions between them to respond to a user query.
> - [A Simple Guide To Retrieval Augmented Generation Language Models](https://www.smashingmagazine.com/2024/01/guide-retrieval-augmented-generation-language-models/) includes a diagram showing the generator flow in a RAG-based system.
> - [Retrieval augmented generation (RAG) explained](https://www.superannotate.com/blog/rag-explained) provides a simple diagram that shows the process of RAG at the intersection of natural language generation (NLG) and information retrieval (IR).

In general, LLM's are costly to train and customize because training requires very large GPU clusters running for extended periods of time. You can follow this in-dept discussion here:  [Efficient LLM Training](https://arxiv.org/pdf/2104.04473.pdf). The problem is made more complicated if the data is constantly changing.

To overcome the training problem customers can implement the RAG model and overcome many of the problems: 

> - **Access to External Knowledge:** RAG provides LLMs access to external knowledge through documents, resulting in contextually accurate and factual responses.
> - **Cost-Effective:** RAG is more cost-effective than fine-tuning, as it doesn’t require the labeled data and computational resources that come with model training.
> - **Improves Accuracy:** RAG improves the accuracy and contextuality of LLM-generated responses while minimizing factual inaccuracies.
> - **Up-to-Date Information:** RAG ensures that the model has access to the most current, reliable facts.
> - **Transparency:** Users have access to the model’s sources, ensuring that its claims can be checked for accuracy and ultimately trusted.
> - **Control Over Generated Text:** Organizations have greater control over the generated text output.
> - **Reduces Data Leakage:** By grounding an LLM on a set of external, verifiable facts, the model has fewer opportunities to pull information baked into its parameters. This reduces the chances that an LLM will leak sensitive data.
> - **Reduces Need for Continuous Training:** RAG reduces the need for users to continuously train the model on new data and update its parameters as circumstances evolve4.

# Project Overview

The project will allow you to incorporate openAI into 

```mermaid
graph LR
A[Teams]-- 1. Chat --> B{Logic Apps}
B -- 2. --> C(Azure Function)
D[(CosmosDB)] -- 3. --> C
C -- 4. --> E(OpenAI)
C -- 5. Response --> B
B -- 6. Update Chat --> A 
```

|    | Component | Activity |
|----|-----------|----------|
| 1    | Teams     | User enters text in chat|
| 2  |  Logic App | Logic app invokes Azure function |
| 3|| Azure Function | Functions reads contents from cosmosDB |
| 4| Azure Function  | The function dynamically creates the prompt and calls OpenAI |
| 5| Azure Function | The function optionally interacts further with OpenAI but ultimately returns the response to teams  |
|6 | Logic App | The Logic App updates the conversation with the response from OpenAI |

-------------------

## Building it manually
### Create the resources:
#### 1. Create a new Teams channel

Teams will be used as the chat UI for this project.  To keep things simple, create a new team.  We'll use the general channel in this newly created team.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/3805c120-82af-48da-83aa-500f68f50dec)

#### 2. Create a new Logic App

The logic app will be used to shuttle message between the chat and Azure functions.  Create a new Logic in the azure portal.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/6f5c2315-812f-417a-b1b2-3d82973125ab)

#### 3. Create a new Azure Function

The function app will be used to call the OpenAI service.  Create a new instance in the portal using Python 3.11 on Linux using the serverless option.  If you have a different version of python installed locally, choose the version that matches your local system.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/fd2c9000-aff1-434b-835c-a3f836e272e2)

#### 4. Creae a new OpenAI instance 

Now for the LLM magic.  Here we'll create an openAI Instance from the portal.  Note, you will need to apply for access  ( and be accepted ) before you can instance this.  If you don't have access yet, click on [Apply for access](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/83126828-2798-4e98-8889-a39faafa4470)

You will receive an email that you have been granted access.  Once you have that, create a new instance using the S0 tier.  We'll be created a GPT-3 instance later once it has been instantiated.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/d03ef280-afa1-485e-9833-13f60ada2578)

##### Create a LLM deployment 

In the portal navigate to the deployed instance and select "Model deployments" on the left:

<img width="97" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/f6dc7d7d-6a5b-4c28-9562-9abff246c736">

This will ask you to confirm that you're navigating to Azure OpenAI Studio.  Confirm and create a new deployment:

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/58cc84a8-8fb4-490a-930b-5ceef29d1576)

Make a note of your deployment name.  In this case, its called **gpt35**
#### 5. Create a new CosmosDB instance

We'll need some place to keep the data that will be used to generate the response.  We're going to keep it simple and store this information in a cosmosDB.  The cool thing about cosmosDB is that it makes it super easy to connect to AzureFunctions ( More correctly, it's actually Azure functions that makes it easy to read from comsosDB. [And a storage acct, and event hub, and a queue, etc...] )

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/214fa10d-5d8c-4d51-875c-f4b808d4e4b4)

---------------------

## Hooking it up

Overall implementing a Retrieval-Augmented Generation (RAG) model involves several steps.  But it'll take longer to read through these than to do the actual mini-RAG implementation.

> - **Define Use Case:** Start by defining the specific use case for your RAG implementation. Determine the domain or topic for which you want the Large Language Model (LLM) to generate responses augmented by retrieved information.
> - **Select an LLM:** Choose a suitable Large Language Model for your RAG implementation.
> - **Data Collection:** Collect a set of documents, also known as a corpus, that the model will use to retrieve information.
> - **Data Preprocessing:** Transform and enrich the data to make it suitable for model augmentation.
> - **Embedding:** Use an embedding model to convert the source data into a series of vectors that represent the words in the client data.
> - **Vector Database:** Store the generated embeddings in a vector database.
> - **User Query:** Receive a user input and perform a similarity measure between the collection of documents and the user input.
> - **Post-Processing:** Post-process the user input and the fetched document(s). The post-processing is done with an LLM.
> - **Response Generation:** Generate a response based on the user’s query and the retrieved documents.

### Here are the steps:

Use case: We're going to let AOAI answer some basic questions for us about our team members.  We'er going to create 1 sentence at a time in cosmos.
For these, we're going to use the cloud shell ( or your own az cli that is already logged in )

<img width="588" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/b138de44-5a73-442e-9c95-dca6b7890e12">

In the cloud shell, clone this repo so that you have access to the scripts:
```
git clone https://github.com/nagendramishr/mini-rag-quickstart.git
```

Edit the first three lines of bin/setup.sh as shown below with the correct values for your resource group, 

```
>head -5 bin/setup.sh
#!/bin/sh

export RG=aoai-rag 
export COSMOS_ACCT=nvmopenaicosmosdb 
export COSMOS_DB=aoaidb
```

# Modify any facts from data/cosmosdb-facts.txt

The facts in this file were generated via the prompt generator as a test for this exercise.  You can modify these for your own purpose.

# run the setup scripts and upload the facts into the DB

# Create a new CosmosDB container
```
chmod ugo+x bin/*

bin/setup.sh
bin/createDB.sh
bin/insertCosmos.py

```

You should now have a cosmosDB with a noSQL db in it containing the facts from the facts file.

# Upload the sample azure functions code to your instance.

An Azure Function has already been created for you in `src/azureFunction`.  This code needs to be deployed to Azure and then configured with the endpoints for CosmosDB and OpenAI.  

```
broken deploy code here
```

# Create your logic app.

Overall, the logic app has 3 steps.
1. It's triggered when a message appears in teams.  In this step we will need to configure the teams connection and grant access to the logic app.
2. Once a message is received, if the Subject is "Question", the Azure function from the previous step will be called with the users question.
3. The response from the azure function will be uploaded into teams as a reply to the original message.

   ![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/fc311cea-f0e8-41f9-8c37-7b7989b0fbc4)

In the first step, add a trigger: **When a new channel message is added**.  Select the team that was created in step 1 along with the General channel.  You will be asked to login and allow the logic app to connect on your behalf.  For the question **How often fo you want to check for items?**, select once per minute.
![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/9d25e91e-740f-427d-a388-f1bf23d3731d)

Add **condition** as the next action and require that the Message subject is equal to **"Question"**. If up don't do this, the bot will get triggered when it responds to your question and it will respond to its own response.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/a6b2e6a9-87e1-4ce6-ba22-1c20880f312a)

On the true side of the condition, add a **HTTP** action.  This action will call the azure function with a question whose value is the **message body content** that was posted on teams.  For the URL, enter the URL for your azure function.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/fc84af51-b7fe-40aa-ade6-91d46d3fac72)

You can find the URL for your azure function by clicking into the "AskQuestion" function on the Overview page and then clicking **Get Function URL**:
<img width="482" alt="image" src="https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/d53d5487-60bb-41f9-9d5b-459c5f75ca18">

After the HTTP step, add another action: **Reply with a message in channel**.  Here, the important part is to select the message ID from the original question as the message ID for the response.  Also, be sure to include the Body from the HTTP request which contains the BOT's response.

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/eecff9c7-e25d-4c34-b287-3a7c95c07e03)


Now, you can post a message in the teams channel and after a few minutes, you will see a response.
![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/e12e0d46-cde9-4aec-9866-e31785b781b4)

![image](https://github.com/nagendramishr/mini-rag-quickstart/assets/81572024/f6a0d6fd-281d-487d-91fa-dd3a69cd9090)
