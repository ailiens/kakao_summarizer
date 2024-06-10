import os
import zipfile
import imaplib
import email
import dotenv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from openai import OpenAI
from datetime import datetime
from .utils import list_files, read_text_file, list_zip_files, unzip_file, login_to_email, fetch_email_ids, fetch_email_subjects, download_attachments, summarize_text, extract_conversations_by_date

# Load environment variables
dotenv.load_dotenv()
client = OpenAI()
model = "gpt-3.5-turbo"
max_token = 500

email_add = os.getenv("EMAIL")
pwd = os.getenv("PWD")
email = 'FROM "your_email_address"'

def home(request):
    return render(request, 'main/home.html')

def download_emails(request):
    if request.method == 'POST':
        mail = login_to_email(email_add, pwd)
        search_criteria = email
        email_ids = fetch_email_ids(mail, search_criteria)
        email_details = fetch_email_subjects(mail, email_ids)
        mail.logout()
        return render(request, 'main/select_email.html', {'emails': email_details})
    return redirect('home')

def select_email(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        mail = login_to_email(email_add, pwd)
        mail.select('inbox')  # Ensure the mailbox is selected before fetching emails
        download_attachments(mail, email_id, './downloads')  # Remove .encode() to pass email_id as string
        mail.logout()
        return HttpResponse("Attachments downloaded successfully!")
    return redirect('home')

def select_zip(request):
    if request.method == 'GET':
        download_folder = './downloads'
        zip_files = list_zip_files(download_folder)
        return render(request, 'main/select_zip.html', {'zip_files': zip_files})
def unzip_files(request):
    if request.method == 'POST':
        download_folder = './downloads'
        extract_to_folder = './extracted'
        os.makedirs(extract_to_folder, exist_ok=True)
        zip_files = list_zip_files(download_folder)
        return render(request, 'main/select_zip.html', {'zip_files': zip_files})
    return redirect('home')

def extract_zip(request):
    if request.method == 'POST':
        zip_file = request.POST.get('zip_file')
        zip_path = os.path.join('./downloads', zip_file)
        unzip_file(zip_path, './extracted')
        return HttpResponse("Files unzipped successfully!")
    return redirect('home')

def summarize_conversations(request):
    if request.method == 'POST':
        extracted_folder = './extracted'
        files = list_files(extracted_folder)
        return render(request, 'main/select_file.html', {'files': files})
    return redirect('home')

def summarize_file(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        conversations = read_text_file(file_path)
        today = datetime.today().strftime('%Y-%m-%d')
        date_selection = request.POST.get('date', today)
        date_conversations = extract_conversations_by_date(conversations, date_selection)
        if date_conversations:
            summary = summarize_text(date_conversations)
            return render(request, 'main/summary.html', {'summary': summary})
        else:
            return HttpResponse("No conversations found for the selected date.")
    return redirect('home')
