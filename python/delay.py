import threading
import time

class Delay:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.running = False  # Track if a repeating interval is running
        self.args = args
        self.kwargs = kwargs

    def set_timeout(self, delay_time):
        """Execute the function after a delay."""
        timer = threading.Timer(delay_time, self.function, self.args, self.kwargs)
        timer.start()

    def set_interval(self, interval_time):
        """Execute the function at regular intervals."""
        def interval_runner():
            while self.running:
                self.function()
                time.sleep(interval_time / 1000)  # Convert ms to seconds

        if not self.running:
            self.running = True
            thread = threading.Thread(target=interval_runner, daemon=True)
            thread.start()

    def stop_interval(self):
        """Stop a running interval."""
        self.running = False

