#Nairobi & Kiambu Movers chatbot — chats to collect trip details, then quotes a price.
# Uses OpenRouter's standard chat/completions endpoint directly (no Anthropic SDK needed).

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
# TASK 3 ELISHA- (Pricing & Quote) — pricing constants
# ============================================================
BASE_FEE = {"Bedsitter": 3000, "1 Bedroom": 5000, "2 Bedroom": 8000, "3 Bedroom": 12000, "4 Bedroom": 16000}
PER_KM, PER_SEAT, MINIMUM = 100, 300, 3500


# ====================================================
# TASK 1 (AI & Prompt Engineering)
<<<<<<< HEAD
=======
# write the full system prompt and implement ask_ai().
# ============================================================
>>>>>>> fb97e1212c22ea4704e77c1ee7c68e60af555ff2
SYSTEM_PROMPT = """You are a helpful Nairobi and Kiambu movers assistant.

LOCATION RESTRICTION:
You only provide moving services within Nairobi County and Kiambu County, Kenya.
If the user's pickup or destination is outside Nairobi County or Kiambu County,
politely explain that the service currently only operates within Nairobi and Kiambu County and 
do not proceed with the booking.

Your job is to gather the information needed for a moving quote, one field at a time.
Ask only for the next missing detail and do not request multiple pieces of information in the same message.

Follow this order strictly:
1. Ask for the pickup location.
2. Ask for the destination.
3. Ask for the house type.
4. Ask for the number of seats owned.

Rules:
- Keep replies short, friendly, and conversational.
- If the user gives more than one item at once, acknowledge the information received and ask only for the missing field.
- Accept common variations for house types such as Bedsitter, 1 Bedroom, 2 Bedroom, 3 Bedroom, and 4 Bedroom.
- Treat seats owned as an integer number.
- Once all four details are known, respond with a brief confirmation and then end the message with a line exactly in this format:
DATA_READY: {"pickup_location": "...", "destination": "...", "house_type": "...", "seats_owned": 0}
- Do not add extra JSON blocks or markdown fences.
- The final line must be valid JSON and include all collected details.
"""


def ask_ai(history):
    """Send the conversation to OpenRouter and return the model reply text."""
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Nairobi Movers Chatbot",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + history,
        "temperature": 0.2,
        "max_tokens": 400,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


# ============================================================
# TASK 2 (Location & Distance)
 # This replaces geocode() and driving_km() in movers.py.
# Covers suggestions 1-4 from the task guide:
#  1. Bias results toward Nairobi/Kiambu with a viewbox
#  2. Cache repeated lookups
#  3. Handle Nominatim/OSRM rate limits gracefully (retry once after a short delay)
#  4. Verify the result is actually within Nairobi/Kiambu (check address components)
import time

_geocode_cache = {}
# Rough bounding box covering Nairobi + Kiambu counties (min_lon, min_lat, max_lon, max_lat)
_NAIROBI_KIAMBU_VIEWBOX = "36.60,-1.45,37.10,-0.95"

# Counties Nominatim should report back, to confirm the match is actually local
_VALID_COUNTIES = {"nairobi", "kiambu"}


def geocode(place):
    """Look up (lat, lon) for a place name, biased toward Nairobi/Kiambu, with caching,
    rate-limit retry, and a check that the result is really in Nairobi/Kiambu."""
    key = place.strip().lower()
    if key in _geocode_cache:
        return _geocode_cache[key]

    params = {
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "ke",
        "viewbox": _NAIROBI_KIAMBU_VIEWBOX,
        "bounded": 1,
        "addressdetails": 1,
        "q": f"{place}, Kenya",
    }
    headers = {"User-Agent": "movers-cli-demo"}

    for attempt in range(2):  # try once, then retry once if rate-limited
        resp = requests.get("https://nominatim.openstreetmap.org/search",
                             params=params, headers=headers, timeout=10)
        if resp.status_code == 429 and attempt == 0:
            time.sleep(2)  # brief pause before retrying
            continue
        resp.raise_for_status()
        results = resp.json()
        break
    else:
        results = []

    if not results:
        raise ValueError(f"Location not found: {place}")

    match = results[0]
    address = match.get("address", {})
    county = (address.get("county") or address.get("state") or "").lower().replace(" county", "")
    if county and not any(valid in county for valid in _VALID_COUNTIES):
        raise ValueError(f"'{place}' seems to be outside Nairobi/Kiambu (matched: {county}).")

    result = (float(match["lat"]), float(match["lon"]))
    _geocode_cache[key] = result
    return result


def driving_km(a, b):
    """Return driving distance in km between two (lat, lon) tuples, using OSRM."""
    url = f"https://router.project-osrm.org/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}"

    for attempt in range(2):  # try once, then retry once if rate-limited
        resp = requests.get(url, params={"overview": "false"}, timeout=10)
        if resp.status_code == 429 and attempt == 0:
            time.sleep(2)
            continue
        resp.raise_for_status()
        data = resp.json()
        break
    else:
        data = {}

    if not data.get("routes"):
        raise ValueError("No route found.")
    return data["routes"][0]["distance"] / 1000


# ============================================================
# TASK 3(ELISHA) (Pricing & Quote) — quote logic
# ============================================================
 Pricing — placeholder rates, edit to match your real rate card.
BASE_FEE = {"Bedsitter": 3000, "1 Bedroom": 5000, "2 Bedroom": 8000, "3 Bedroom": 12000, "4 Bedroom": 16000}
PER_KM, PER_SEAT, MINIMUM = 100, 300, 3500
def quote(data):
    # Geocode, get distance, compute price, print + save. All errors caught here.
    try:
        km = driving_km(geocode(data["pickup"]), geocode(data["destination"]))
    except (requests.RequestException, ValueError) as e:
        print(f"Could not calculate distance: {e}")
        return

    base = BASE_FEE.get(data["house_type"], BASE_FEE["1 Bedroom"])
    dist_charge, seat_charge = round(km * PER_KM), data["seats"] * PER_SEAT
    total = max(base + dist_charge + seat_charge, MINIMUM)

    lines = [f"Distance: {km:.1f} km", f"Base fee ({data['house_type']}): KES {base:,}",
              f"Distance charge: KES {dist_charge:,}", f"Seats charge: KES {seat_charge:,}", f"TOTAL: KES {total:,}"]
    print("\n" + "\n".join(lines))
    with open("movers_quote.txt", "w", encoding="utf-8") as f:
        f.write(f"{data['pickup']} -> {data['destination']} | {data['house_type']}, {data['seats']} seats\n")
        f.write("\n".join(lines))
    print("Saved to movers_quote.txt")
   


# ============================================================
# TASK 4 (Chat Loop & Error Handling)
#  Covers suggestions from the task guide:
#  1. "quit"/"exit" command
#  2. "restart" command
#  3. Conversation length limit (avoid runaway loops / API costs)
#  4. Better JSON error recovery (ask the AI to resend instead of giving up)
# ============================================================
MAX_TURNS = 50
# ============================================================
def chat():
    """Run the interactive chat loop that collects details and triggers a quote."""
    history = [{"role": "assistant", "content": "Hi! I can help you gkiet a moving quote in Nairobi or Kiambu. Where are you moving from?"}]
    print(f"Bot: {history[0]['content']}")
    turns = 0

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() in ("quit", "exit"):
            print("Bot: Okay, ending the chat. Have a good day!")
            return

        if user_text.lower() == "restart":
            history = [{"role": "assistant", "content": "Sure, let's start over. Where are you moving from?"}]
            print(f"Bot: {history[0]['content']}")
            turns = 0
            continue

        if not user_text:
            print("Bot: Please type something.")
            continue

        turns += 1
        if turns > MAX_TURNS:
            print("Bot: This conversation is getting long — let's restart to keep things on track.")
            history = [{"role": "assistant", "content": "Where are you moving from?"}]
            turns = 0
            continue

        history.append({"role": "user", "content": user_text})

        try:
            reply = ask_ai(history)
        except requests.HTTPError as e:
            print(f"Bot: API error ({e.response.status_code}): {e.response.text[:200]}")
            continue
        except requests.RequestException as e:
            print(f"Bot: Connection problem ({e}). Try again.")
            continue

        history.append({"role": "assistant", "content": reply})

        if "DATA_READY:" in reply:
            visible, json_part = reply.split("DATA_READY:", 1)
            if visible.strip():
                print(f"Bot: {visible.strip()}")
            try:
                quote(json.loads(json_part.strip()))
                return
            except json.JSONDecodeError:
                # Ask the AI to resend the data instead of giving up entirely
                history.append({"role": "user",
                                 "content": "That JSON didn't come through correctly. Please resend the DATA_READY line with valid JSON."})
                print("Bot: Sorry, something went wrong reading the details — let me try that again.")
                continue

        print(f"Bot: {reply}")


def main():
    """Entry point: check for an API key, then start the chat loop."""
    if not API_KEY:
        sys.exit("Set OPENROUTER_API_KEY in a .env file or environment variable.")
    try:
        chat()
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()
