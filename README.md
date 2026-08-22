## Name
1. Joshua Wanje
2. Susan Odinga
3. Nevyl Cherop
4. Victor Ngundo
5. Elisha Kibichii

# Nairobi & Kiambu Movers Chatbot

A command-line chatbot that collects a customer's moving details (pickup location, destination, house type, and seats) through natural conversation, then calculates and prints a price quote based on real driving distance between the two locations.built with python using openstrap for geocoding and the open router API for natural language conversation

## What it does

1. Chats with the user to collect: pickup location, destination, house type, and seats owned.
2. Once all details are confirmed, it:
   - Geocodes both locations (OpenStreetMap)
   - Calculates driving distance between them (OSRM)
   - Computes a price quote based on the rate card
   - Prints the quote and saves it to movers_quote.txt

## how to set up

### 1. Cloning the repo
By using the command prompt

git clone https://github.com/JoshuaWanje/wca-ai-tool-s11-Movers-ai.git
cd wca-ai-tool-s11-Movers-ai


### 2. Create a virtual environment

py -m venv venv


Activate it:
- PowerShell: venv\Scripts\Activate.ps1
- macOS/Linux: source venv/bin/activate

### 3. Install dependencies
how to install:
pip install -r requirements.txt


### 4. Set up your API key
Copy .env.example to a new file named .env:

copy .env.example .env

Then open .env and replace the placeholder with your real OpenRouter API key:

OPENROUTER_API_KEY=your_actual_key_here


*Never commit .env* — it's already listed in .gitignore. Each person on the team should use their own key, or a shared one agreed on privately (not in the repo).

## Running it


py movers.py


Chat with the bot in the terminal. It'll ask for your pickup location, destination, house type, and seats, then generate a quote.

## Team workflow

We're working in a team of 5 — to avoid overwriting each other's changes, everyone works on their own branch and merges via Pull Request.

1. Before starting work, update your local main:
   
   git checkout main
   git pull origin main
   
2. Create your own branch:
   
   git checkout -b yourname-feature
   
3. Make your changes, then commit and push:
   
   git add .
   git commit -m "Describe what you changed"
   git push -u origin yourname-feature
   
4. Open a Pull Request on GitHub to merge into main. Get a teammate to review before merging.
5. Don't push directly to main.

## Project structure

| File | Owner | Covers |
|---|---|---|
| SYSTEM_PROMPT, ask_ai() | Person 1 | AI conversation logic |
| geocode(), driving_km() | Person 2 | Location & distance |
| quote(), pricing constants | Person 3 | Pricing & quote output |
| chat(), main() | Person 4 | Chat loop & error handling |
| .env.example, requirements.txt, this README | Person 5 | Setup, docs, integration testing |

## SYSTEM_PROMPT AND ASK_AI() REPORT

## 1. SYSTEM_PROMPT

The SYSTEM_PROMPT gives instructions to the Movers AI chatbot. It controls how the chatbot communicates
with customers and tells it what information to collect.
The chatbot collects four details: pickup location, destination, house type, and seats owned. It asks one
question at a time and, after collecting all the information, returns the details using DATA_READY in JSON
format.
## SYSTEM_PROMPT = """
You are a moving services assistant.
Collect the following details from the customer:
1. Pickup location
2. Destination
3. House type

## 4. Number of seats owned

Rules:
- Ask for only one detail at a time.
- Wait for the customer's response before asking the next question.
- Do not ask for information that has already been provided.
- Keep the conversation simple and professional.
When all the required information has been collected, respond with:
DATA_READY:
{
"pickup_location": "<pickup location>",
"destination": "<destination>",
"house_type": "<house type>",
"seats_owned": "<number of seats>"
}
"""
## 2. ASK_AI()

The ask_ai() function connects the chatbot to the AI model. It sends the conversation and the system
instructions to the model and returns the AI-generated response.
def ask_ai(messages):
response = client.models.generate_content(
model="gemini-2.5-flash",
contents=messages,
config={
"system_instruction": SYSTEM_PROMPT
}
)
return response.text

## 3. HOW THE SYSTEM WORKS

1. The customer sends a message requesting moving services.
2. The ask_ai() function receives the conversation.
3. The SYSTEM_PROMPT tells the AI what information to collect.
4. The chatbot asks one question at a time.
5. The customer provides the required information.
6. After all four details are collected, the chatbot returns DATA_READY.
7. The information is returned in JSON format.
4. EXAMPLE
Bot: What is your pickup location?
Customer: Nairobi
Bot: What is your destination?
Customer: Kiambu
Bot: What type of house are you moving from?
Customer: Three bedroom
Bot: How many seats do you own?
Customer: 7
DATA_READY:
{
"pickup_location": "Nairobi",
"destination": "Kiambu",
"house_type": "Three bedroom",
"seats_owned": "7"
}
## 5. CONCLUSION

The SYSTEM_PROMPT controls the chatbot's behavior, while ask_ai() connects the conversation to the AI
model. Together, they allow the Movers AI chatbot to collect customer moving information in a simple,
organized, and in structured way


