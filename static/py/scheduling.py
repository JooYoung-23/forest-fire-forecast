import threading
import schedule
from update_weather import update_weather
	
def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

def schedule_thread():
	while True:
		schedule.run_pending()


def scheduling_data_update():
	
	schedule.every().hour.at(":40").do(run_threaded, update_weather)
	thread = threading.Thread(target=schedule_thread)
	thread.start()