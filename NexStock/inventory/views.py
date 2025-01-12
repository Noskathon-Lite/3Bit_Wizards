from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'pages-contact.html')

def forms_layouts(request):
    return render(request, 'forms-layouts.html')

def tables_data(request):
    return render(request, 'tables-data.html')

def charts_chartjs(request):
    return render(request, 'charts-chartjs.html')

def users_profile(request):
    return render(request, 'users-profile.html')

def pages_register(request):
    return render(request, 'pages-register.html')

def pages_login(request):
    return render(request, 'pages-login.html')

def update_element(request):
    if request.method == 'POST':
        element_id = request.POST.get('element_id')
        # Process your element update logic here
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def get_element(request, element_id):
    # Fetch element data based on element_id
    # Replace with your actual model and logic
    data = {
        'element_id': element_id,
        # Add other element data
    }
    return JsonResponse(data)