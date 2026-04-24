import sys
import requests
if len(sys.argv) !=2:
    sys.exit("Missing command-line argument")

try:
    n = float(sys.argv[1])
except ValueError:
    sys.exit("Invalid number")

try:
    response = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=abcd1234xyz")
    data = response.json()
    price_string = data["data"]["priceUsd"]
    price_float = float(price_string)
except requests.RequestException:
    sys.exit("API request failed")
except (KeyError, ValueError):
    sys.exit("Error processing data")

total_cost = n * price_float

formatted_total = f"${total_cost:,.4f}"
print(formatted_total)