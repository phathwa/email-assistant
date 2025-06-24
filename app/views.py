from django.shortcuts import render

# Create your views here.
def reply_view(request):
    return render(request, 'app/reply.html')

def compose_view(request):
    return render(request, 'app/compose.html')