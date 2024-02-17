# NLP Systems Assignment 1

## Description
This project implements several RESTful APIs and web servers for NER and dependency parsing.

## Prerequisites
- Python 3.10.12
- A command line

Minimal requirements to run these apps are specified in `requirements.txt`. To install all, run:
```bash
pip install -r requirements.txt
```

## FastAPI
To start:
```bash
uvicorn app_fastapi:app --reload
```
The server can be accessed at `http:/127.0.0.1:8000`. To send a GET request:

```bash
curl -X GET http:/127.0.0.1:8000/[route]
```

To send a POST request:


```bash
curl -X POST http:/127.0.0.1:8000/[route] \
       -H 'accept: application/json' \
       -H 'Content-Type: application/json' \
       -d@input.json 
```

(To run using a .txt file instead of a json file, just replace the last line with `-d '{"text": "'"$(cat input.txt)"'"}'`)

### Routes:

- `/` 
  - GET: Return a summary of service
  - POST: Return the text and entities
- `/ner`
  - POST: Return named entities of input
- `/dep`
  - POST: Return dependency relations of input

Each route also accepts a pretty parameter (e.g. `curl http://127.0.0.1:8000?pretty=true`). This renders the output in a more human-readable format.


## Flask
To start:
```bash
python app_flask.py
```

Navigate to `http://localhost:5000` in a web browser to use the service. Entering a sentence into the text box will produce a displaCy NER visualization and all dependency relations of the input.

## Streamlit
To start:
```bash
streamlit run app_streamlit.py
```
Navigate to `http://localhost:8501` in a web browser to use the service. Enter text in the box to show NLP analysis of your input. The website consists of two pages:

- entities: Shows all entities and word frequencies detected by Spacy NER.
- dependencies: Shows all dependencies in table and graph form.