from llama_index import VectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import json
import openai
from llama_index.memory import ChatMemoryBuffer

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# read the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# reddit credentials
reddit_client_id = os.environ.get("REDDIT_CLIENT_ID")
reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.environ.get("REDDIT_USER_AGENT")
reddit_username = os.environ.get("REDDIT_USERNAME")
reddit_password = os.environ.get("REDDIT_PASSWORD")

# loading reddit reader from LlamaHub
RedditReader = download_loader('RedditReader')

# allow user to specify what subreddits they want
subredditChoice = input("Please enter the name of the SubReddit you'd like to query: ")
subreddits = [subredditChoice]

searchkeyChoice1 = input("Please enter a keyword to narrow down the search: ")
searchkeyChoice2 = input("Please enter another keyword to narrow down the search: ")
search_keys = [searchkeyChoice1, searchkeyChoice2]

print("Thank you, please wait as we process your request!")

# will need to change accordingly; the higher this number the more accurate the answer will be
# however, the higher the number = more data to embed, which will cost me more via openAI API
post_limit = 17

# loading appropriate subreddit data, and storing it as indexes
loader = RedditReader()
documents = loader.load_data(subreddits=subreddits, search_keys=search_keys, post_limit=post_limit)
index = VectorStoreIndex.from_documents(documents)

memory = ChatMemoryBuffer.from_defaults(token_limit=50)

chat_engine = index.as_chat_engine(chat_mode='context', memory=memory, system_prompt="You are a chat bot, able to have normal interactions. You have access to a few reddit posts based on what the user filtered. You will answer any query the user has in relation to these reddit posts. The user will ask a question in which you can usually find/derive an answer from the reddit posts.")

print("Please enter a question (type exit to leave):")
userInput = ''

while userInput != 'exit':
    userInput = input()
    response = chat_engine.chat(userInput)
    print(f"GPTReddit: {response}")