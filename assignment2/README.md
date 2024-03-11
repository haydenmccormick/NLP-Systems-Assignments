# NLP Systems Assignment 2

## Description
This project links an SQLite database to the Flask NER service

## Prerequisites
- Python 3.10.12
- A command line

Minimal requirements to run these apps are specified in `requirements.txt`. To install all, run:
```bash
pip install -r requirements.txt
```

## The Flask server
To start:
```bash
python app_flask.py
```

Navigate to `http://localhost:5000` in a web browser to use the service. 
- Entering text into the text box and clicking "Submit Query" will run the SPACY NER and dependency parsing steps, upload the dependency parse to the SQLite server, and navigate to the result page.
- Clicking "Show all relations" will take you to `/relations`, which shows all currently uploaded dependency parses in table format. It also provides the option to delete all currently uploaded dependencies and entities.

The SQLite server consists of two tables:

- `Entities` contains all Named Entities found, as well as entity counts and links to relation IDs representing relations the entity has appeared in:

  | Entity            | Relation | Count |
  |-------------------|----------|-------|
  | week              | 2,7,...  | 10    |

- `Relations` contains all encountered relations, each one with a unique ID value and count:

  | ID | Relation            | Count |
  |----|---------------------|-------|
  | 7  | week advmod earlier | 1     |

Relations are extracted from each entity by accessing the linked ID values in the `Relations` table. All Sqlite tasks are performed in `sqlite_helpers.py`