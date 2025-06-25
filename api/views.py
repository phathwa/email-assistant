from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.encoding import smart_str
import os
import json
import re
from openai import OpenAI

DEESEE_API_KEY = os.getenv('DEESEE_API_KEY', 'sk-df27d79c16c04faa83067921d7f81c42')
client = OpenAI(api_key=DEESEE_API_KEY, base_url="https://api.deepseek.com")

def home(request):
    return render(request, 'api/home.html')

@csrf_exempt
def generate_reply(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(smart_str(request.body))
        sender = data.get('sender', '')
        thread_summary = data.get('thread_summary', '')
        intent = data.get('intent', '')
        tone = data.get('tone', '')
    except Exception as e:
        return JsonResponse({'error': f'Invalid input: {e}'}, status=400)

    system_message = "You are a helpful assistant that generates context-driven email replies."
    user_content = f"""
    Sender: {sender}
    Email Summary: {thread_summary}
    Reply Intent: {intent}
    Tone: {tone}

    Please generate a thoughtful, clear email reply and do not use em dash. The reply must start with the subject line, like this: 'Subject: Your Subject Here'.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_content},
            ]
        )
        full_reply = response.choices[0].message.content.strip()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # --- UPDATED LOGIC ---
    # This method is more robust for separating the subject and body.
    lines = full_reply.split('\n')
    subject = ''
    body = ''

    # Check if the first line looks like a subject line.
    if lines and lines[0].lower().strip().startswith('subject:'):
        # Extract the subject text from the first line.
        subject_line = lines[0]
        subject = subject_line[subject_line.find(':')+1:].strip()
        
        # The body is all subsequent lines, joined together.
        body = '\n'.join(lines[1:]).strip()
    else:
        # If no "Subject:" line is found, treat the whole response as the body.
        subject = 'No Subject Generated'
        body = full_reply

    return JsonResponse({
        'reply_subject': subject,
        'body': body,
        'full_reply': full_reply,
    })

@csrf_exempt
def generate_compose(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(smart_str(request.body))
        recipient = data.get('recipient', '')
        purpose = data.get('compose_purpose', '')
        tone = data.get('compose_tone', '')
    except Exception as e:
        return JsonResponse({'error': f'Invalid input: {e}'}, status=400)

    system_message = "You are a helpful assistant that composes professional emails from scratch, including the subject line."
    user_content = f"""
    Recipient: {recipient}
    Purpose: {purpose}
    Tone: {tone}

    Please compose a complete email, including a suggested subject line. Start with 'Subject:' on the first line. Do not use em dash.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_content},
            ]
        )
        full_reply = response.choices[0].message.content.strip()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # --- UPDATED LOGIC ---
    # This method is more robust for separating the subject and body.
    lines = full_reply.split('\n')
    subject = ''
    body = ''

    # Check if the first line looks like a subject line.
    if lines and lines[0].lower().strip().startswith('subject:'):
        # Extract the subject text from the first line.
        subject_line = lines[0]
        subject = subject_line[subject_line.find(':')+1:].strip()
        
        # The body is all subsequent lines, joined together.
        body = '\n'.join(lines[1:]).strip()
    else:
        # If no "Subject:" line is found, treat the whole response as the body.
        subject = 'No Subject Generated'
        body = full_reply

    return JsonResponse({
        'reply_subject': subject,
        'body': body,
        'full_reply': full_reply,
    })
