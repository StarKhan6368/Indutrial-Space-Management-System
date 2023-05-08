from ISMS import app
import multiprocessing

def Flask_run():
    app.run(debug=True)
    
if __name__ == "__main__":
    mqtt_to_postgres = multiprocessing.Process(target=mqtt_start)
    flask_app = multiprocessing.Process(target=Flask_run)
    flask_app.start()
    mqtt_to_postgres.start()
    flask_app.join()
    mqtt_to_postgres.join()
    print("App Has Been Terminated")

# if __name__ == "__main__":
#     app.run(debug=True)