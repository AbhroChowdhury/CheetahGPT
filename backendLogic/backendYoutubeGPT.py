from llama_index import VectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import json
import openai
from llama_index.memory import ChatMemoryBuffer
from llama_hub.youtube_transcript import YoutubeTranscriptReader

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# read the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

loader = YoutubeTranscriptReader()

print("Please enter a youtube video link: ")
YTlink = input()

documents = loader.load_data(ytlinks=[YTlink])

index = VectorStoreIndex.from_documents(documents)

memory = ChatMemoryBuffer.from_defaults(token_limit=50)

chat_engine = index.as_chat_engine(chat_mode='context', memory=memory, system_prompt="You are a chat bot, able to have normal interactions. You will have be given the transcript of a youtube video; Users will ask questions pertaining to this youtube video. You will help them")

print("Please enter a question (type exit to leave):")
userInput = ''

while userInput != 'exit':
    userInput = input()
    response = chat_engine.chat(userInput)
    print(f"YoutubeGPT: {response}")