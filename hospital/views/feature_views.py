import requests
from django.shortcuts import render
from django.http import JsonResponse


def get_diet(request):
    if request.method == "POST":
        selected_nutrients = request.POST.getlist('nutrients')
        selected_conditions = request.POST.getlist('health_conditions')
        selected_gender = request.POST.get('gender')
        selected_type = request.POST.get('diet')
        
        # Prepare data to send to Flask app
        data = {
            'nutrients': selected_nutrients,
            'health_conditions': selected_conditions,
            'gender': selected_gender,
            'foodtype': selected_type,
        }
        print(data)
       # Send POST request to Flask app
        flask_url = 'http://localhost:5000/diet'  # Change to your Flask app's URL
        response = requests.post(flask_url, data=data)
        
        # If the request is successful
        if response.status_code == 200:
            df_html = response.text
            # Optionally, if Flask returns JSON, you can use response.json()
            return render(request, 'hospital/other/diet.html', {'df_html': df_html})
        else:
            return render(request, 'hospital/error.html', {'message': 'Error communicating with Flask app'})
    
    return render(request,'hospital/other/diet.html')    
    