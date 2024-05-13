from django.shortcuts import render

def my_model_view(request):
    return render(request, 'models/my_model')

def smart_model_view(request):
    return render(request, 'models/smart_model')

def datacheck_view(request):
    return render(request, 'models/datacheck')
