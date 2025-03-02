import requests
from django.shortcuts import render
from django.http import JsonResponse

def send_to_flask(request):
    response_data = None  # Default empty response
    error_message = None   # Store any error messages
    if request.method == 'POST':
        name = request.POST.get("name")
        flask_url = "http://127.0.0.1:5000/process-data"
        
        try:
            response = requests.post(flask_url, json={"name": name}, timeout=5)  # Set timeout
            response.raise_for_status()  # Raise error for 4xx/5xx responses
            
            response_data = response.json()  # Get processed data from Flask
        except requests.Timeout:
            error_message = "The server took too long to respond. Please try again later."
        except requests.ConnectionError:
            error_message = "Could not connect to the server. Please check your connection."
        except requests.HTTPError as err:
            error_message = f"API returned an error: {err.response.status_code}"
        except Exception as e:
            error_message = f"Something went wrong: {str(e)}"

    return render(request, 'hospital/example.html', {"response_data": response_data, "error_message": error_message})


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
    