import subprocess
import time

# Start Flask server
flask_process = subprocess.Popen(["python", "flask_api/run.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Wait a bit to avoid port conflicts (optional)
time.sleep(2)

# Start Django server
django_process = subprocess.Popen(["python", "manage.py", "runserver"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Print output from both processes
try:
    while True:
        output_f = flask_process.stdout.readline()
        output_d = django_process.stdout.readline()
        
        if output_f:
            print(f"[Flask] {output_f.strip()}")
        if output_d:
            print(f"[Django] {output_d.strip()}")
        
        if not output_f and not output_d:
            break
except KeyboardInterrupt:
    flask_process.terminate()
    django_process.terminate()
    print("\nServers stopped.")

