from threading import Event
import threading

appointment_submitted = Event()
appointment_submitted = threading.Event()
submitted_data = {}  # Global shared dictionary

history = []  