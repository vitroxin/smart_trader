# training_loop.py
import time
import threading
import random
from core_ai import MetaRLTrader

class Trainer:
    def __init__(self):
        self.trader = MetaRLTrader()
        self.running = True

    def fetch_data(self):
        # هنا تستخدم API حقيقي (Binance, Yahoo) أو web scraping لتحصيل بيانات السوق
        # مبسط: بيانات عشوائية
        return [random.random() for _ in range(10)]

    def training_step(self):
        state = self.fetch_data()
        action = random.randint(0, 2)  # مثال: random action
        reward = random.random()
        next_state = self.fetch_data()
        self.trader.remember(state, action, reward, next_state)
        self.trader.train()

    def run(self):
        while self.running:
            self.training_step()
            time.sleep(1)

def start_training_thread():
    trainer = Trainer()
    t = threading.Thread(target=trainer.run, daemon=True)
    t.start()
    return trainer
