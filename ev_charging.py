
import threading
import time


class EVChargingSystem:

    def __init__(self):
        self.total_chargers = 3

        # Counting semaphore
        self.charger_semaphore = threading.Semaphore(3)

        # Mutex lock
        self.charger_lock = threading.Lock()

        self.chargers = ["Available"] * 3
        self.total_requests = 0
        self.events = []

    def add_event(self, message):
        with self.charger_lock:
            self.events.insert(0, message)
            self.events = self.events[:10]

    def request_ev(self):

        with self.charger_lock:
            self.total_requests += 1
            ev_id = self.total_requests

        self.add_event(f"EV {ev_id} requested charging")

        thread = threading.Thread(
            target=self.charge_ev,
            args=(ev_id,)
        )

        thread.start()

    def charge_ev(self, ev_id):

        self.charger_semaphore.acquire()
        charger_id = None

        try:
            with self.charger_lock:

                for i in range(self.total_chargers):
                    if self.chargers[i] == "Available":
                        self.chargers[i] = "Charging"
                        charger_id = i + 1
                        break

            self.add_event(
                f"EV {ev_id} started charging at Charger {charger_id}"
            )

            time.sleep(20)

            with self.charger_lock:
                self.chargers[charger_id - 1] = "Completed"

            self.add_event(f"EV {ev_id} completed charging")

            time.sleep(1)

            with self.charger_lock:
                self.chargers[charger_id - 1] = "Released"

            self.add_event(f"Charger {charger_id} released")

            time.sleep(1)

            with self.charger_lock:
                self.chargers[charger_id - 1] = "Available"

            self.add_event(f"Charger {charger_id} is available")

        finally:
            self.charger_semaphore.release()

    def get_snapshot(self):

        with self.charger_lock:
            return {
                "chargers": self.chargers.copy(),
                "total_requests": self.total_requests,
                "active_sessions": self.chargers.count("Charging"),
                "available_chargers": self.chargers.count("Available"),
                "events": self.events.copy()
            }


# Create the charging system
system = EVChargingSystem()
