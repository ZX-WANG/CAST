# CAST - a ChatGPT-based Article Summarization Tool

## Introduction
This is a tool that summarizes articles using ChatGPT. It reads articles in PDF format by `fitz` and summarizes them by OpenAPI of ChatGPT. 

## Preparation

### Initialize venv (Optional)

```bash
python3 -m venv venv
. venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```
### Set ChatGPT OpenAPI key
    
```bash
touch .env
echo [PUT YOUR KEY HERE] > .env
```
## Usage

```bash
python chatgpt_summarizer.py --pdf [PDF FILE] --output-file [OUTPUT FILE] --format [FORMAT] [--single]
```

You can see the help message by `python chatgpt_summarizer.py -h`.

## Configs
You can modify the constants in `chatgpt_summarizer.py` to change the behavior of the summarizer.
```python
SUMMARY_PROMPT = "Summarize the following text:" # Prompt for summarization
MODEL_NAME = 'gpt-3.5-turbo' # Model used for summarization
MODEL_TOKEN_LIMIT = 4096 # Token limit of the model
```