import threading
import schedule
import datetime

def update_weather():
	# 여기에 update code 작성
	current_time = datetime.datetime.now().time()
	print("Current time:", current_time)
	print("type:", type(current_time))
	print("str:", str(current_time))
	return
	
def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

def schedule_thread():
	while True:
		schedule.run_pending()


def scheduling_data_update():
	schedule.every().hour.at(":00").do(run_threaded, update_weather)
	schedule.every().hour.at(":30").do(run_threaded, update_weather)
	thread = threading.Thread(target=schedule_thread)
	thread.start()