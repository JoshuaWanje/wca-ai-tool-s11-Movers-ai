## Name
1. Joshua Wanje
2. Susan Odinga
3. Nevyl Cherop
4. Victor Ngundo
5. Elisha Kibichii

# Nairobi & Kiambu Movers Chatbot

A command-line chatbot that collects a customer's moving details (pickup location, destination, house type, and seats) through natural conversation, then calculates and prints a price quote based on real driving distance.

## What it does

1. Chats with the user to collect: pickup location, destination, house type, and seats owned.
2. Once all details are confirmed, it:
   - Geocodes both locations (OpenStreetMap)
   - Calculates driving distance between them (OSRM)
   - Computes a price quote based on the rate card
   - Prints the quote and saves it to movers_quote.txt

## Setup

### 1. Clone the repo

git clone https://github.com/JoshuaWanje/wca-ai-tool-s11-Movers-ai.git
cd wca-ai-tool-s11-Movers-ai


### 2. Create a virtual environment

py -m venv venv


Activate it:
- PowerShell: venv\Scripts\Activate.ps1
- macOS/Linux: source venv/bin/activate

### 3. Install dependencies

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

## Notes

- Pricing constants in movers.py (BASE_FEE, PER_KM, PER_SEAT, MINIMUM) are placeholders — update them to match the real rate card.
- Geocoding and routing use free public APIs (Nominatim, OSRM) — they have rate limits, so avoid hammering them with rapid repeated requests during testing.
-
 
   



  
     
 
