# Nairobi & Kiambu Movers chatbot — chats to collect trip details, then quotes a price.
# Routed through OpenRouter (sk-or-... key) instead of calling Anthropic directly.
import json, os, sys
import requests
import anthropic

try:
    from dotenv import load_dotenv
    load_dotenv()  # loads OPENROUTER_API_KEY from .env if present
except ImportError:
    pass

API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-sonnet-4-6"  # OpenRouter needs the provider/model format

# Pricing — placeholder rates, edit to match your real rate card.
BASE_FEE = {"Bedsitter": 3000, "1 Bedroom": 5000, "2 Bedroom": 8000, "3 Bedroom": 12000, "4 Bedroom": 16000}
PER_KM, PER_SEAT, MINIMUM = 100, 300, 3500

SYSTEM_PROMPT = """You are a chatbot for a moving company in Nairobi and Kiambu County, Kenya.
Collect, one at a time: pickup location, destination, house type (Bedsitter/1/2/3/4 Bedroom), and seats owned.
Be warm and brief. Map loose phrasing to the closest house type and confirm it.
LOCATION RESTRICTION:
You only provide moving services within Nairobi County and Kiambu County, Kenya.
- The service operates ONLY within Nairobi County and Kiambu County, Kenya.
- BOTH the pickup location AND the destination location MUST be within Nairobi County or Kiambu County.
- NEVER assume that a place is in Nairobi just because it is a Kenyan place name.
- NEVER guess a county when the location is ambiguous or unknown.If the user's pickup or destination is
outside Nairobi County or Kiambu County politely explain that the service currently
only operates within Nairobi and Kiambu County and do not proceed with the booking.

Once all four are confirmed, end with a new line: DATA_READY:{"pickup":"","destination":"","house_type":"","seats":0}
Do not send DATA_READY early."""


def geocode(place):
    # Free OpenStreetMap geocoding, restricted to Kenya.
    r = requests.get("https://nominatim.openstreetmap.org/search",
                      params={"format": "json", "limit": 1, "countrycodes": "ke", "q": f"{place}, Kenya"},
                      headers={"User-Agent": "movers-cli-demo"}, timeout=10).json()
    if not r:
        raise ValueError(f"Location not found: {place}")
    return float(r[0]["lat"]), float(r[0]["lon"])


def driving_km(a, b):
    # Free OSRM routing — driving distance in km.
    url = f"https://router.project-osrm.org/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}"
    data = requests.get(url, params={"overview": "false"}, timeout=10).json()
    if not data.get("routes"):
        raise ValueError("No route found.")
    return data["routes"][0]["distance"] / 1000


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


def chat(client):
    history = [{"role": "assistant", "content": "Hi! I can help you get a moving quote in Nairobi or Kiambu. Where are you moving from?"}]
    print(f"Bot: {history[0]['content']}")

    while True:
        user_text = input("You: ").strip()
        
        if user_text.lower() in ("quit"):
            print("Bot: okay. Have a good day!")
            return
        
        if not user_text:
            print("Bot: Please type something.")
            continue
        history.append({"role": "user", "content": user_text})

        try:
            r = client.messages.create(model=MODEL, max_tokens=400, system=SYSTEM_PROMPT, messages=history)
            reply = "".join(b.text for b in r.content if hasattr(b, "text"))
        except (anthropic.APIError, Exception) as e:
            print(f"Bot: Something went wrong ({e}). Try again.")
            continue

        history.append({"role": "assistant", "content": reply})
        if "DATA_READY:" in reply:
            visible, json_part = reply.split("DATA_READY:", 1)
            if visible.strip():
                print(f"Bot: {visible.strip()}")
            try:
                quote(json.loads(json_part.strip()))
            except json.JSONDecodeError:
                print("Bot: Couldn't read the collected details.")
            break
        print(f"Bot: {reply}")


def main():
    if not API_KEY:
        sys.exit("Set OPENROUTER_API_KEY in a .env file or environment variable.")
    # Same Anthropic SDK, just pointed at OpenRouter's Anthropic-compatible endpoint.
    # NOTE 1: base_url must be "https://openrouter.ai/api" (no trailing /v1) — the
    # Anthropic SDK appends "/v1/messages" itself. Adding "/v1" here causes a
    # double path ("/api/v1/v1/messages") which 404s.
    # NOTE 2: use auth_token=, not api_key=. The SDK sends api_key as an
    # "x-api-key" header, but OpenRouter's endpoint expects the key as a Bearer
    # token in the "Authorization" header, which only auth_token= produces.
    client = anthropic.Anthropic(auth_token=API_KEY, base_url="https://openrouter.ai/api")
    try:
        chat(client)
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()
