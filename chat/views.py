from django.shortcuts import render, redirect
# from .forms import ContactUsForm

# def contact_us(request):
#     if request.method == 'POST':
#         form = ContactUsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('')  # Redirect to a new URL on success
#     else:
#         form = ContactUsForm()
#     return render(request, 'about.html', {'form': form}) ### FIX THIS

def success_view(request):
    return render(request, 'about.html')

def gpt_chat_view(request):
    return render(request, 'collaboration/gpt_chat.html') 

def investor_portal_view(request):
    return render(request, 'collaboration/investor_portal')

