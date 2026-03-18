from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent

load_dotenv()  # reads ANTHROPIC_API_KEY from .env

# --- TOOLS ---
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together. Use this when you need to multiply."""
    return a * b

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together. Use this when you need to add."""
    return a + b

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# --- MODEL ---
model = ChatAnthropic(model="claude-sonnet-4-20250514")
tools = [multiply, add, wikipedia]

# --- AGENT ---
agent = create_react_agent(model, tools)


# --- RUN ---
response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is 7 times the population of Rome?"}]}
)

# Print the final response
for message in response["messages"]:
    print(f"\n--- {message.type} ---")
    print(message.content)


"""
# Alternative code for interactive questions:
# --- RUN ---
user_input = input("\nAsk the agent something: ")

response = agent.invoke(
    {"messages": [{"role": "user", "content": user_input}]}
)

# Print the final response
for message in response["messages"]:
    print(f"\n--- {message.type} ---")
    print(message.content)
"""


"""
Final output:

--- human ---
What is 7 times the population of Rome?

--- ai ---
[{'text': "I'll help you find 7 times the population of Rome. First, let me look up Rome's current population.", 'type': 'text'}, {'id': 'toolu_01T3fNmbrhrM7gSGjzrmR4HR', 'caller': {'type': 'direct'}, 
'input': {'query': 'Rome population'}, 'name': 'wikipedia', 'type': 'tool_use'}]

--- tool ---
Page: Rome
Summary: Rome is the capital city and most populated comune (municipality) of Italy. It is also the administrative centre of the Lazio region and of the Metropolitan City of Rome. 
A special comune named Roma Capitale with a population of 2.7 million in an area of 1,287.36 km2 (497.1 mi2), Rome is the third most populous city in the European Union by population within city limits. 
The Metropolitan City of Rome Capital, with a population of 4.2 million, is the most populous metropolitan city in Italy. Its metropolitan area is the third-most populous within Italy. 
Rome is located in the central-western portion of the Italian Peninsula, within Lazio (Latium), along the shores of the Tiber Valley. 
Vatican City (the smallest country in the world and headquarters of the worldwide Catholic Church under the governance of the Holy See) is an independent country inside the city boundaries of Rome, 
the only existing example of a country within a city. Rome is often referred to as the "City of Seven Hills" due to its geography, and also as the "Eternal City". 
Rome is generally considered to be one of the cradles of Western civilization and Western Christian culture, and the centre of the Catholic Church.
Rome's history spans 28 centuries. While Roman mythology dates the founding of Rome at around 753 BC, the site has been inhabited for much longer, making it a major human settlement 
for over three millennia and one of the oldest continuously occupied cities in Europe. The city's early population originated from a mix of Latins, Etruscans, and Sabines. 
Eventually, the city successively became the capital of the Roman Kingdom, the Roman Republic and the Roman Empire, and is regarded by many as the first-ever Imperial city and metropolis. 
It was first called The Eternal City (Latin: Urbs Aeterna; Italian: La Città Eterna) by the Roman poet Tibullus in the 1st century BC, and the expression was also taken up by Ovid, Virgil, and Livy. 
Rome is also called Caput Mundi (Capital of the World).
After the fall of the Empire in the west, which marked the beginning of the Middle Ages, Rome slowly fell under the political control of the Papacy, and in the 8th century, 
it became the capital of the Papal States, which lasted until 1870. Beginning with the Renaissance, almost all popes since Nicholas V (1447–1455)
pursued a coherent architectural and urban programme over four hundred years, aimed at making the city the artistic and cultural centre of the world.
In this way, Rome first became one of the major centres of the Renaissance and then became the birthplace of both the Baroque style and Neoclassicism. 
Famous artists, painters, sculptors, and architects made Rome the centre of their activity, creating masterpieces throughout the city. 
In 1871, Rome became the capital of the Kingdom of Italy, which, in 1946, became the Italian Republic. It hosted the Summer Olympics in 1960.
In 2019, Rome was the 14th most visited city in the world with 8.6 million tourists, the third most visited city in the European Union, and the most popular tourist destination in Italy. 
Its historic centre is listed by UNESCO as a World Heritage Site. 
Rome is also the seat of several specialised agencies of the United Nations, such as the Food and Agriculture Organization, the World Food Programme, and the International Fund for Agricultural Development. 
The city also hosts the Secretariat of the Parliamentary Assembly of the Union for the Mediterranean, as well as the headquarters of several Italian multinational companies 
such as Eni, Enel, TIM, Leonardo, and banks such as BNL. Numerous companies are based within Rome's EUR business district, such as the luxury fashion house Fendi located in the Palazzo della Civiltà Italiana. 
The presence of renowned international brands in the city has made Rome an important centre of fashion and design, and the Cinecittà Studios have been the set of many Academy Award–winning movies.

Page: History of Rome
Summary: The history o
(NOTICE: The WikipediaAPIWrapper truncates results, this is why "The history o" doesn't end.)

--- ai ---
[{'text': "Based on the Wikipedia information, Rome (the municipality/comune) has a population of 2.7 million. Now I'll multiply this by 7.", 'type': 'text'}, {'id': 'toolu_011j4RYAyEbUpvMLXYzwCefj', 'caller': {'type': 'direct'}, 'input': {'a': 2700000, 'b': 7}, 'name': 'multiply', 'type': 'tool_use'}]

--- tool ---
18900000.0

--- ai ---
7 times the population of Rome is **18,900,000** (or 18.9 million).

This calculation is based on Rome's municipal population of 2.7 million people. Note that Rome also has a larger metropolitan area with 4.2 million people - if you were interested in that figure instead, 7 times the metropolitan population would be 29.4 million.
"""