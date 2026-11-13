"""Generate synthetic customer records containing both valid and invalid fields."""
import csv
import random
from pathlib import Path

random.seed(19)
OUTPUT = Path("messy_contacts.csv")
names = ["Amina Yusuf", "Ethan Cole", "Sara Ahmed", "Noah Reed", "Maya Shah"]
countries = ["US", "GB", "PK", "DE", "CA"]
rows = []

for number in range(1, 81):
    name = random.choice(names)
    email = f"person{number}@example.com"
    age = str(random.randint(18, 70))
    country = random.choice(countries)
    if number % 9 == 0:
        email = "not-an-email"
    if number % 11 == 0:
        age = "unknown"
    if number % 13 == 0:
        name = " "
    if number % 17 == 0:
        country = ""
    rows.append({"customer_id": f"U{number:04d}", "name": name, "email": email, "age": age, "country": country})

# Add one duplicate ID to demonstrate duplicate-ID validation.
rows.append(rows[2].copy())

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["customer_id", "name", "email", "age", "country"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {OUTPUT} with {len(rows)} data rows.")
