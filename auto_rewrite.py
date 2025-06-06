# auto_rewrite.py
import threading
import time
import os

def rewrite_core_ai():
    # فكرة مبسطة: تحميل core_ai.py، تعديل وتحسين (مثلاً ضبط التعلم، تنظيف)، وإعادة حفظه
    with open('core_ai.py', 'r', encoding='utf-8') as f:
        code = f.read()
    # هنا يمكن استخدام ast لتعديل الكود تلقائياً حسب الحاجة
    improved_code = code.replace('lr=1e-4', 'lr=5e-5')  # مثال تحسين: تقليل معدل التعلم
    
    with open('core_ai.py', 'w', encoding='utf-8') as f:
        f.write(improved_code)
    print("[auto_rewrite] core_ai.py has been improved and rewritten.")

def auto_rewrite_loop():
    while True:
        rewrite_core_ai()
        time.sleep(360)  # كل 6 دقائق

def start_auto_rewrite_thread():
    t = threading.Thread(target=auto_rewrite_loop, daemon=True)
    t.start()
