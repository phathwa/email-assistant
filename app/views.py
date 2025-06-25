import json
from django.http import HttpRequest
from django.shortcuts import render
import requests

# The name of your new, unified template file.
# You should rename the 'modern_email_assistant' file to this in your templates folder.
UNIFIED_TEMPLATE_NAME = 'app/assistant.html'

# This view handles the form submission for generating a reply.
def reply_view(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        # 1. Get data from the form submitted to this view
        sender = request.POST.get('sender', '')
        thread_summary = request.POST.get('thread_summary', '')
        intent = request.POST.get('intent', '')
        tone = request.POST.get('tone', '')

        # 2. Prepare the data payload for the API request
        api_data = {
            'sender': sender,
            'thread_summary': thread_summary,
            'intent': intent,
            'tone': tone
        }
        
        # Keep the original form data to display it again if needed
        context.update(api_data)

        # 3. Make a server-side HTTP request to your API endpoint
        api_url = request.build_absolute_uri('/api/generate-reply/')
        
        try:
            response = requests.post(api_url, json=api_data)
            response.raise_for_status() 
            api_response_data = response.json()

            # 4. Add the data from the API response to the template context
            context['reply_subject'] = api_response_data.get('reply_subject')
            context['reply'] = api_response_data.get('body')
            context['full_reply'] = api_response_data.get('full_reply')

        except requests.exceptions.RequestException as e:
            context['error'] = f"Error calling API: {e}"
        except json.JSONDecodeError:
            context['error'] = "Error: Could not decode the response from the API."

    # Render the unified template.
    return render(request, UNIFIED_TEMPLATE_NAME, context)


# This view now handles the form submission for composing a new email.
def compose_view(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        # 1. Get data from the form
        recipient = request.POST.get('recipient', '')
        compose_purpose = request.POST.get('compose_purpose', '')
        compose_tone = request.POST.get('compose_tone', '')

        # 2. Prepare data payload for the API and to re-populate the form
        api_data = {
            'recipient': recipient,
            'compose_purpose': compose_purpose,
            'compose_tone': compose_tone,
        }
        context.update(api_data)

        # 3. Build the API URL and make a server-side HTTP request
        api_url = request.build_absolute_uri('/api/generate-compose/')
        
        try:
            response = requests.post(api_url, json=api_data)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            api_response_data = response.json()

            # 4. Update context with the data from the API response
            context['reply_subject'] = api_response_data.get('reply_subject')
            context['reply'] = api_response_data.get('body')
            context['full_reply'] = api_response_data.get('full_reply')

        except requests.exceptions.RequestException as e:
            context['error'] = f"Error calling API: {e}"
        except json.JSONDecodeError:
            context['error'] = "Error: Could not decode the response from the API."

    # Render the unified template.
    return render(request, UNIFIED_TEMPLATE_NAME, context)
