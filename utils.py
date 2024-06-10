import os
import zipfile
import imaplib
import email
import dotenv
from openai import OpenAI
from datetime import datetime

dotenv.load_dotenv()
client = OpenAI()
model = "gpt-4o" #"gpt-3.5-turbo"
max_token = 500

email_add = os.getenv("EMAIL")
pwd = os.getenv("PWD")

def list_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def list_zip_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.zip')]

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f'Extracted {zip_path} to {extract_to}')

def login_to_email(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')  # Ensure the inbox is selected after login
    return mail

def fetch_email_ids(mail, search_criteria):
    mail.select('inbox')
    status, messages = mail.search(None, search_criteria)
    if status != 'OK':
        print("Failed to search emails.")
        return []
    email_ids = messages[0].split()
    return email_ids

def fetch_email_subjects(mail, email_ids):
    email_details = []
    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        if status != 'OK':
            print(f"Failed to fetch email ID: {e_id.decode()}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        email_subject = msg['subject']
        if email_subject.startswith('=?'):
            email_subject = email.header.decode_header(email_subject)
            email_subject = ' '.join([str(t[0], t[1] or 'utf-8') if isinstance(t[0], bytes) else t[0] for t in email_subject])
        email_details.append((e_id.decode(), email_subject))  # Decode email_id for proper string handling
    return email_details

def download_attachments(mail, email_id, download_folder='./downloads'):
    status, msg_data = mail.fetch(email_id, '(RFC822)')  # Pass email_id directly as string
    if status != 'OK':
        print(f"Failed to fetch email ID: {email_id}")
        return
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    email_subject = msg['subject']
    if email_subject.startswith('=?'):
        email_subject = email.header.decode_header(email_subject)
        email_subject = ' '.join([str(t[0], t[1] or 'utf-8') if isinstance(t[0], bytes) else t[0] for t in email_subject])
    print(f'Email ID: {email_id} | Subject: {email_subject}')
    os.makedirs(download_folder, exist_ok=True)
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            filepath = os.path.join(download_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            print(f'Attachment downloaded: {filepath}')

def summarize_text(text, model=model, max_tokens=300):
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Use proper Korean, answer in the style of kindergarten teacher, gentle and enthusiastic. "
                                          "If there is an schedule or appointment please write the at the end of setence for letting me know."
                                          "You must answered by Korean."},
            {"role": "user", "content": f"Summarize the following conversation:\n\n{text}"}
        ],
        max_tokens=max_tokens,
        stream=True,
    )
    summary = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            summary += content
    return summary.strip()

def extract_conversations_by_date(conversations, date):
    lines = conversations.split('\n')
    date_conversations = [line for line in lines if line.startswith(date)]
    return '\n'.join(date_conversations)
