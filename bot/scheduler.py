from apscheduler.schedulers.background import BackgroundScheduler
import threading

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.start()


scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.start()
