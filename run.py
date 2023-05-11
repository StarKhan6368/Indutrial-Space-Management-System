from ISMS import app
from mqtt_to_postgres import mqtt_start
import multiprocessing
    
if __name__ == "__main__":
    mqtt_to_postgres = multiprocessing.Process(target=mqtt_start)
    flask_app = multiprocessing.Process(target=app.run, args=("0.0.0.0", 5000))
    flask_app.start()
    mqtt_to_postgres.start()
    flask_app.join()
    mqtt_to_postgres.join()
    print("App Has Been Terminated")
    
# if __name__ == "__main__":
#     app.run("0.0.0.0", 5000, debug=True)