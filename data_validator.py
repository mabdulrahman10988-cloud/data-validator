"""Validate customer CSV records and split valid and invalid rows."""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
REQUIRED = ["customer_id", "name", "email", "age", "country"]


def validate_row(row, seen_ids):
    """Return a list of problems found in one record."""
    problems = []
    customer_id = (row.get("customer_id") or "").strip()
    name = (row.get("name") or "").strip()
    email = (row.get("email") or "").strip()
    age_text = (row.get("age") or "").strip()
    country = (row.get("country") or "").strip().upper()

    for field in REQUIRED:
        if not (row.get(field) or "").strip():
            problems.append(f"missing_{field}")

    if email and not EMAIL_PATTERN.match(email):
        problems.append("invalid_email")

    if age_text:
        try:
            age = int(age_text)
            if age < 18 or age > 100:
                problems.append("age_out_of_range")
        except ValueError:
            problems.append("age_not_integer")

    if country and not re.fullmatch(r"[A-Z]{2}", country):
        problems.append("country_code_must_be_2_letters")

    if customer_id and customer_id in seen_ids:
        problems.append("duplicate_customer_id")
    elif customer_id:
        seen_ids.add(customer_id)

    return problems


def main():
    parser = argparse.ArgumentParser(description="Check required fields, email, age, country code and duplicate IDs.")
    parser.add_argument("input", nargs="?", default="messy_contacts.csv", help="Input CSV path")
    parser.add_argument("--prefix", default="validation", help="Output file prefix")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}. Run: python generate_data.py")

    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise SystemExit("The input CSV has no header row.")
        missing_columns = [name for name in REQUIRED if name not in reader.fieldnames]
        if missing_columns:
            raise SystemExit(f"Missing required columns: {', '.join(missing_columns)}")
        rows = list(reader)
        fieldnames = list(reader.fieldnames)

    valid_rows = []
    invalid_rows = []
    issue_counts = Counter()
    seen_ids = set()

    for row in rows:
        cleaned = {key: (value or "").strip() for key, value in row.items()}
        cleaned["country"] = cleaned["country"].upper()
        problems = validate_row(cleaned, seen_ids)
        if problems:
            cleaned["validation_errors"] = ";".join(problems)
            invalid_rows.append(cleaned)
            issue_counts.update(problems)
        else:
            valid_rows.append(cleaned)

    valid_path = Path(f"{args.prefix}_valid.csv")
    invalid_path = Path(f"{args.prefix}_invalid.csv")
    report_path = Path(f"{args.prefix}_report.json")

    with valid_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_rows)

    invalid_fields = fieldnames + ["validation_errors"]
    with invalid_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=invalid_fields)
        writer.writeheader()
        writer.writerows(invalid_rows)

    report = {
        "input_file": str(input_path),
        "total_rows": len(rows),
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalid_rows),
        "issue_counts": dict(sorted(issue_counts.items())),
        "validation_rules": [
            "all required fields must be present",
            "email must have a basic name@domain.tld shape",
            "age must be an integer from 18 through 100",
            "country must be a two-letter code",
            "customer_id must be unique",
        ],
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Total rows: {len(rows)}")
    print(f"Valid rows: {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")
    print(f"Saved: {valid_path}, {invalid_path}, {report_path}")


if __name__ == "__main__":
    main()
