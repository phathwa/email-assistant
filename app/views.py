import json
import os
from django.http import HttpRequest
from django.shortcuts import render
import requests


API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000') # Default for local dev

UNIFIED_TEMPLATE_NAME = 'app/assistant.html'

def reply_view(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        sender = request.POST.get('sender', '')
        thread_summary = request.POST.get('thread_summary', '')
        intent = request.POST.get('intent', '')
        tone = request.POST.get('tone', '')

        api_data = {
            'sender': sender,
            'thread_summary': thread_summary,
            'intent': intent,
            'tone': tone
        }
        context.update(api_data)

        # Build the correct API URL using the environment variable
        api_url = f"{API_BASE_URL}/api/generate-reply/"
        
        try:
            response = requests.post(api_url, json=api_data)
            response.raise_for_status() 
            api_response_data = response.json()

            context['reply_subject'] = api_response_data.get('reply_subject')
            context['reply'] = api_response_data.get('body')
            context['full_reply'] = api_response_data.get('full_reply')

        except requests.exceptions.RequestException as e:
            context['error'] = f"Error calling API: {e}"
        except json.JSONDecodeError:
            context['error'] = "Error: Could not decode the response from the API."

    return render(request, UNIFIED_TEMPLATE_NAME, context)

def compose_view(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        recipient = request.POST.get('recipient', '')
        compose_purpose = request.POST.get('compose_purpose', '')
        compose_tone = request.POST.get('compose_tone', '')

        api_data = {
            'recipient': recipient,
            'compose_purpose': compose_purpose,
            'compose_tone': compose_tone,
        }
        context.update(api_data)

        # Build the correct API URL using the environment variable
        api_url = f"{API_BASE_URL}/api/generate-compose/"
        
        try:
            response = requests.post(api_url, json=api_data)
            response.raise_for_status()
            api_response_data = response.json()

            context['reply_subject'] = api_response_data.get('reply_subject')
            context['reply'] = api_response_data.get('body')
            context['full_reply'] = api_response_data.get('full_reply')

        except requests.exceptions.RequestException as e:
            context['error'] = f"Error calling API: {e}"
        except json.JSONDecodeError:
            context['error'] = "Error: Could not decode the response from the API."

    return render(request, UNIFIED_TEMPLATE_NAME, context)
