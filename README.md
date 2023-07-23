
# AI relavent paper feed and reading tool using GPT

## Introduction

The purpose of this project is to create a tool that can help researchers and enthusiasts in the field of Artificial 
Intelligence (AI) to keep up with the latest research papers and articles. The tool will use the GPT (Generative 
Pre-trained Transformer) model to summarize and provide key insights from the papers and articles.

## Usage

### Set Environment Variable for your API keys
To use the package, you need to first setup your API keys in your environment variables. 

For Windows
1. run the following in the cmd prompt, replacing <yourkey> with your API key
```commandline
setx OPENAI_API_KEY "<yourkey>"
setx NOTION_API_KEY "<yourkey>"
```
2. This will apply to future cmd prompt window, so you will need to open a new one to use that variable with curl.
You can validate that this variable has been set by opening a new cmd prompt window and typing in 
```commandline
echo %OPENAI_API_KEY
```

For MacOS and Linux
1. we write environment variables to `.bash_profile.` 
```commandline
echo "export OPENAI_API_KEY='yourkey'" >> ~/.bash_profile
echo "export NOTION_API_KEY='yourkey'" >> ~/.bash_profile
```
2. Update the shell with the new variable:
```commandline
source ~/.bash_profile
```
3. Confirm that you have set your environment variable using the following command. 
```commandline
echo $OPENAI_API_KEY
echo $NOTION_API_KEY
```


## Objectives

The objectives of this project are as follows:

- Develop a web application that can fetch and store AI research papers and articles from various sources.
- Integrate the GPT model to summarize and provide key insights from the papers and articles.
- Feed Daily paper update with summaries to user every day in the morning.
- Translate the summaries into different language for readers using GPT models.
- Provide a user-friendly interface for users to search, filter and read the summarized papers and articles.
- Implement a feedback system where users can rate the quality of the summaries provided by the GPT model.

## Methodology

The following steps will be taken to achieve the objectives of the project:

1. Data collection: The web application will fetch AI research papers and articles from various sources such as arXiv, 
IEEE, and ACM Digital Library.
    -  We can start with arXiv and extend to paied libraries
    -  Fetch paper using one of the following options or combinations
        -  keyword
        -  author name
        -  relative topic
        -  paper name
        -  url
        -  conference
2. Data preprocessing: The fetched articles will be preprocessed to remove noise and irrelevant information.
    -  We will parse the paper into different sections and
    -  We will also extract the important figures with its caption from the paper and return it to user
3. GPT model integration: The preprocessed articles will be fed into the GPT model to generate summaries and key 
insights.
    -  fed each section of the paper to GPT model one by one and get the insights
    -  We will extract the main methodology of the paper
    -  We will list useful reference 
4. Summarized articles storage: The summarized articles will be stored in a database for easy retrieval and access.
5. User interface development: A user-friendly interface will be developed for users to search, filter and read the 
summarized articles.
6. Feedback system implementation: A feedback system will be implemented where users can rate the quality of the 
summaries provided by the GPT model.