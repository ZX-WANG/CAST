import argparse
import fitz
import pandas as pd

from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file
import openai
SUMMARY_PROMPT = "Summarize the following text:"
MODEL_NAME = "gpt-3.5-turbo"
MODEL_TOKEN_LIMIT = 4096

# Suffix for every format defined
suffix_dict = {
    'excel': 'xlsx',
    'csv': 'csv'
}

def write_to_file(data, file, format):
    if format == 'excel':
        data.to_excel(file, index = None)
    elif format == 'csv':
        data.to_csv(file, sep='\t', encoding='utf-8', index=None)
    else:
        raise Exception("Invalid format")

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser("Summarize a PDF file with ChatGPT")
    arg_parser.add_argument("--pdf", type=str, required=True, help="Path to the PDF file")
    arg_parser.add_argument("--format", type=str, choices=['excel', 'csv'], required=True, help="Format for the output file")
    arg_parser.add_argument("--single", action='store_true', help="Complete the summary in a whole conversation with CHatGPT.\nIf set to false, a new conversation will be started for each page.")
    arg_parser.add_argument("--output-file", type=str, help="Path to the output file")
    args = arg_parser.parse_args()
    
    data_list = []
    conversation = []
    with fitz.open(args.pdf) as doc:
        for page in tqdm(doc):
            text = page.get_text()
            model_text = text
            if len(text) > MODEL_TOKEN_LIMIT:
                print("Text too long for model, truncating to 4096 tokens")
                model_text = text[:MODEL_TOKEN_LIMIT]
            current_conversation = [
                    {"role": "user", "content": SUMMARY_PROMPT},
                    {"role": "user", "content": model_text}
                ]
            conversation.extend(current_conversation)
            response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages= conversation if args.single else current_conversation, 
            )
            summary = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": summary})
            data_list.append({'page': page.number, 'text': text, 'summary': summary})
    data = pd.DataFrame(data_list)
    output_file = args.output_file if args.output_file else f"summary.{suffix_dict[args.format]}"
    write_to_file(data, output_file, args.format)