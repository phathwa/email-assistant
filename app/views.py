import json
from django.http import HttpRequest
from django.shortcuts import render
import requests

from api.views import generate_reply

# Create your views here.
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
        #    You must provide the full URL to your running Django server's API endpoint.
        #    This URL might change depending on your environment (development/production).
        api_url = request.build_absolute_uri('/api/generate-reply/')
        
        try:
            # The 'json' parameter automatically sets the Content-Type header to application/json
            response = requests.post(api_url, json=api_data)
            
            # Check if the API call was successful
            response.raise_for_status() 

            # 4. Get the JSON data from the API response
            api_response_data = response.json()

            # 5. Add the data from the API response to the template context
            context['reply_subject'] = api_response_data.get('reply_subject')
            context['reply'] = api_response_data.get('body')
            context['full_reply'] = api_response_data.get('full_reply')

        except requests.exceptions.RequestException as e:
            # Handle potential network errors or bad responses from the API
            context['error'] = f"Error calling API: {e}"
        except json.JSONDecodeError:
            context['error'] = "Error: Could not decode the response from the API."

    # Render the template with the context, which will be empty on GET
    # and populated on a successful POST.
    return render(request, 'app/reply.html', context)

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

    return render(request, 'app/compose.html', context)