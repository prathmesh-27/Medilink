import requests
from django.shortcuts import render
import pandas as pd

# def get_diet(request):
#     if request.method == "POST":
#         selected_nutrients = request.POST.getlist('nutrients')
#         selected_conditions = request.POST.getlist('health_conditions')
#         selected_gender = request.POST.get('gender')
#         selected_type = request.POST.get('diet')
        
#         # Prepare data to send to Flask app
#         data = {
#             'nutrients': selected_nutrients,
#             'health_conditions': selected_conditions,
#             'gender': selected_gender,
#             'foodtype': selected_type,
#         }
#         print(data)
#        # Send POST request to Flask app
#         flask_url = 'http://localhost:5000/diet'  # Change to your Flask app's URL
#         response = requests.post(flask_url, data=data)
        
#         # If the request is successful
#         if response.status_code == 200:
#             df_html = response.text
#             return render(request, 'hospital/other/diet.html', {'df_html': df_html})
#         else:
#             return render(request, 'hospital/error.html', {'message': 'Error communicating with Flask app'})
    
    # return render(request,'hospital/other/diet.html')    

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
        # print(data)
       # Send POST request to Flask app
        flask_url = 'http://localhost:5000/diet'  # Change to your Flask app's URL
                
        try:
            response = requests.post(flask_url,data=data,timeout=10)   # Add timeout to prevent hanging
        
            response.raise_for_status()  # Raise an error for bad HTTP responses (4xx, 5xx)
        
            data = response.json()  # Convert JSON to Python object
  
            return render(request, 'hospital/other/diet.html', {"df_html": data["table"]})

        except requests.exceptions.ConnectionError:
            error_message = "Failed to connect to Flask API. Is it running?"
        except requests.exceptions.Timeout:
            error_message = "The request to Flask API timed out."
        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            error_message = f"An error occurred: {req_err}"
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

        return render(request, "hospital/error.html", {"message": error_message})
    
    return render(request,'hospital/other/diet.html')
    