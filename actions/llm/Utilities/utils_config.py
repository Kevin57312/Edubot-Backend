from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_BASE = os.environ["OPENAI_API_BASE"] 
OPENAI_MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]