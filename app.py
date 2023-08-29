from flask import Flask, render_template, request, jsonify
from llama_index import VectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import json
import openai
from llama_index.memory import ChatMemoryBuffer


app = Flask(__name__)

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# read the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Reddit credentials
reddit_client_id = os.environ.get("REDDIT_CLIENT_ID")
reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.environ.get("REDDIT_USER_AGENT")
reddit_username = os.environ.get("REDDIT_USERNAME")
reddit_password = os.environ.get("REDDIT_PASSWORD")

# Loading Reddit reader from LlamaHub
RedditReader = download_loader('RedditReader')

@app.route('/redditGPT', methods=['POST'])
def process_reddit_request():
    data = request.get_json()  # Get data from the JSON request
    subreddit = data.get('subreddit')
    keywords = data.get('keywords')
    question = data.get('question')

    print("Received data:")
    print("Subreddit:", subreddit)
    print("Keywords:", keywords)
    print("Question:", question)


    # Loading appropriate subreddit data and storing it as indexes
    loader = RedditReader()
    documents = loader.load_data(subreddits=[subreddit], search_keys=keywords, post_limit=17)
    index = VectorStoreIndex.from_documents(documents)

    memory = ChatMemoryBuffer.from_defaults(token_limit=50)

    chat_engine = index.as_chat_engine(chat_mode='context', memory=memory, system_prompt="You are a chat bot, able to have normal interactions. You have access to a few reddit posts based on what the user filtered. You will answer any query the user has in relation to these reddit posts. The user will ask a question in which you can usually find/derive an answer from the reddit posts.")

    response = chat_engine.chat(question)

    print("GPT Response:", response)

    response_data = {
        "gpt_response": response.response  # Access the response text
    }

    return jsonify(response_data)

@app.route('/redditGPT')
def render_redditGPT():
    return render_template('redditGPT.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redditGPT')
def redditGPT():
    return render_template('redditGPT.html')

@app.route('/youtubeGPT')
def youtubeGPT():
    return render_template('youtubeGPT.html')

@app.route('/wikipediaGPT')
def wikipediaGPT():
    return render_template('wikipediaGPT.html')

@app.route('/csvGPT')
def csvGPT():
    return render_template('csvGPT.html')

@app.route('/documentGPT')
def documentGPT():
    return render_template('documentGPT.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
