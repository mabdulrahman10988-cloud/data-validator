# Data Validator

A Python command-line tool that checks a customer CSV for missing required values, basic email shape, age range, two-letter country codes, and duplicate customer IDs. It separates valid and invalid records and writes a JSON issue summary.

**Portfolio status:** Independent demonstration using synthetic data. It is not a commissioned client project.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run the demonstration

```bash
python generate_data.py
python data_validator.py
```

Expected files:

- `messy_contacts.csv` — generated synthetic input
- `validation_valid.csv` — rows that passed the checks
- `validation_invalid.csv` — rows with a `validation_errors` column
- `validation_report.json` — counts of each validation issue

## Validate another CSV

```bash
python data_validator.py path/to/contacts.csv --prefix client_check
```

## Rules

1. `customer_id`, `name`, `email`, `age`, and `country` must be present.
2. Email must have a basic `name@domain.tld` structure.
3. Age must be an integer from 18 through 100.
4. Country must be a two-letter code.
5. Customer IDs must be unique.

## Limits

- The email rule checks basic shape only; it does not prove that an email inbox exists.
- The country rule checks two letters only; it does not check a live country-code database.
- Invalid rows are not deleted; they are written to a separate file for review.

## Reproducibility

The generator uses a fixed random seed, so it creates the same sample data each time.

## License

MIT. See `LICENSE` if you add one before public distribution.
