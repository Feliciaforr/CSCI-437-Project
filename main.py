import subprocess
import time

if __name__ == "__main__":
    processes = []

    try:
    
        update_runner = subprocess.Popen(["python", "backend/market/update_runner.py"])
        processes.append(update_runner)


        time.sleep(1) 
        backend_app = subprocess.Popen(["python", "backend/app.py"])
        processes.append(backend_app)
        
        time.sleep(1)
        alert_runner = subprocess.Popen(["python", "backend/alerts/alert_runner.py"])
        processes.append(alert_runner)

        time.sleep(20) 
        main_app = subprocess.Popen(["python", "gui/MainApp.py"])
        processes.append(main_app)

       
        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        print("Shutting down processes...")
        for p in processes:
            p.terminate()