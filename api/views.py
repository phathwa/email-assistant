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
    if request.method == 'POST':
        is_json = request.content_type == 'application/json'

        try:
            data = json.loads(smart_str(request.body)) if is_json else request.POST
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

        Please generate a thoughtful, clear email reply and do not use em dash.
        """

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_content},
                ],
                stream=False
            )
            full_reply = response.choices[0].message.content.strip()
        except Exception as e:
            if is_json:
                return JsonResponse({'error': str(e)}, status=500)
            return render(request, 'api/home.html', {
                'reply_error': f"Error generating reply: {e}",
                'sender': sender,
                'thread_summary': thread_summary,
                'intent': intent,
                'tone': tone,
            })

        subject_match = re.match(r'^\s*\*\*?Subject:\*\*?\s*(.+)', full_reply, re.IGNORECASE | re.MULTILINE)
        subject = subject_match.group(1).strip() if subject_match else ''
        body = re.sub(r'^\s*\*\*?Subject:\*\*?.*\n?', '', full_reply, count=1, flags=re.IGNORECASE | re.MULTILINE).strip()
        
        if is_json:
            return JsonResponse({
                'sender': sender,
                'thread_summary': thread_summary,
                'intent': intent,
                'tone': tone,
                'reply_subject': subject,
                'body': body,
                'full_reply': full_reply,
            })

        return render(request, 'api/home.html', {
            'sender': sender,
            'thread_summary': thread_summary,
            'intent': intent,
            'tone': tone,
            'reply_subject': subject,
            'reply': body,
            'full_reply': full_reply,
        })

    return render(request, 'api/home.html')


@csrf_exempt
def generate_compose(request):
    if request.method == 'POST':
        is_json = request.content_type == 'application/json'

        try:
            data = json.loads(smart_str(request.body)) if is_json else request.POST
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
                ],
                stream=False
            )
            full_reply = response.choices[0].message.content.strip()
        except Exception as e:
            if is_json:
                return JsonResponse({'error': str(e)}, status=500)
            return render(request, 'api/home.html', {
                'compose_error': f"Error composing email: {e}",
                'recipient': recipient,
                'compose_purpose': purpose,
                'compose_tone': tone,
            })

        # Extract subject from first line
        subject_match = re.match(r'^\s*\*\*?Subject:\*\*?\s*(.+)', full_reply, re.IGNORECASE | re.MULTILINE)
        subject = subject_match.group(1).strip() if subject_match else ''

        # Remove subject line
        body = re.sub(r'^\s*\*\*?Subject:\*\*?.*\n?', '', full_reply, count=1, flags=re.IGNORECASE | re.MULTILINE).strip()

        if is_json:
            return JsonResponse({
                'recipient': recipient,
                'compose_purpose': purpose,
                'compose_tone': tone,
                'reply_subject': subject,
                'body': body,
                'full_reply': full_reply,
            })

        return render(request, 'api/home.html', {
            'recipient': recipient,
            'compose_purpose': purpose,
            'compose_tone': tone,
            'reply_subject': subject,
            'reply': body,
            'full_reply': full_reply,
        })

    return render(request, 'api/compose-email.html')
