#Nairobi & Kiambu Movers chatbot — chats to collect trip details, then quotes a price.
# Uses OpenRouter's standard chat/completions endpoint directly (no Anthropic SDK needed).
#
# TEAM SKELETON — each function below is owned by one person (see comments).
# Fill in only your own function(s). Don't edit anyone else's section.

import json, os, sys
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()  # loads OPENROUTER_API_KEY from .env if present
except ImportError:
    pass

API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-sonnet-4.6"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ============================================================
# TASK 3 (Pricing & Quote) — pricing constants
# TODO: replace placeholder rates with the real rate card.
# ============================================================
BASE_FEE = {"Bedsitter": 3000, "1 Bedroom": 5000, "2 Bedroom": 8000, "3 Bedroom": 12000, "4 Bedroom": 16000}
PER_KM, PER_SEAT, MINIMUM = 100, 300, 3500


# ============================================================
# TASK 1 (AI & Prompt Engineering)
# TODO: write the full system prompt and implement ask_ai().
# ============================================================
SYSTEM_PROMPT = """TODO: write the system prompt here.
It should instruct the bot to collect pickup location, destination, house type,
and seats owned — one at a time — then end with a DATA_READY: line containing
the collected details as JSON."""


def ask_ai(history):
    # TODO: send history to OpenRouter and return the assistant's reply text.
    # Hint: POST to OPENROUTER_URL with the API_KEY in headers and SYSTEM_PROMPT
    # plus history in the messages list. Use r.raise_for_status() to catch errors.
    raise NotImplementedError("ask_ai() not implemented yet — Task 1")


# ============================================================
# TASK 2 (Location & Distance)
# TODO: implement geocoding and distance calculation.
# ============================================================
def geocode(place):
    # TODO: look up (lat, lon) for place using a geocoding API (e.g. Nominatim),
    # restricted to Kenya. Raise ValueError if the place isn't found.
    raise NotImplementedError("geocode() not implemented yet — Task 2")


def driving_km(a, b):
    # TODO: given two (lat, lon) tuples, return driving distance in km
    # (e.g. using OSRM's routing API). Raise ValueError if no route is found.
    raise NotImplementedError("driving_km() not implemented yet — Task 2")


# ============================================================
# TASK 3 (Pricing & Quote) — quote logic
# TODO: compute and display/save the price quote.
# ============================================================
def quote(data):
    # TODO: use geocode() + driving_km() to get distance, then calculate:
    #   base fee (from BASE_FEE by house_type) + distance charge + seat charge,
    #   with a MINIMUM floor. Print the breakdown and save it to movers_quote.txt.
    raise NotImplementedError("quote() not implemented yet — Task 3")


# ============================================================
# TASK 4 (Chat Loop & Error Handling)
# TODO: implement the interactive chat loop and program entry point.
# ============================================================
def chat():
    # TODO: greet the user, loop taking input, call ask_ai(), handle errors,
    # and when the reply contains "DATA_READY:", parse the JSON and call quote().
    raise NotImplementedError("chat() not implemented yet — Task 4")


def main():
    if not API_KEY:
        sys.exit("Set OPENROUTER_API_KEY in a .env file or environment variable.")
    try:
        chat()
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()