from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()  # reads ANTHROPIC_API_KEY from .env

model = ChatAnthropic(model="claude-sonnet-4-20250514")
response = model.invoke("Say 'setup works' and nothing else.")
print(response.content)