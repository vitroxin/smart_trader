# watchdog.py
import time
from evolution import evolve

class Watchdog:
    def __init__(self, trainer):
        self.trainer = trainer
        self.performance_history = []

    def monitor(self):
        while True:
            if len(self.trainer.trader.memory) > 50:
                # تقييم الأداء (مبسط)
                performance = random.random()
                self.performance_history.append(performance)
                print(f"[watchdog] Current performance: {performance:.3f}")

                if performance < 0.3:
                    print("[watchdog] Performance low, evolving model...")
                    evolve(self.trainer.trader)
            time.sleep(300)  # كل 5 دقائق

def start_watchdog_thread(trainer):
    w = Watchdog(trainer)
    t = threading.Thread(target=w.monitor, daemon=True)
    t.start()
