# main.py
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import threading

from training_loop import start_training_thread
from auto_rewrite import start_auto_rewrite_thread
from watchdog import start_watchdog_thread

app = FastAPI()

# بدء المكونات الذكية في الخلفية
trainer = start_training_thread()
start_auto_rewrite_thread()
start_watchdog_thread(trainer)

app.mount("/static", StaticFiles(directory="static"), name="static")

html_content = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/>
<title>نظام التداول الذكي</title>
<style>
  body { background: radial-gradient(circle at center, #0b0f1a, #1a2030); color: #c0c8e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  #chat { height: 400px; overflow-y: auto; border: 1px solid #394a7f; padding: 10px; background: #121c3d; }
  #input { width: 80%; padding: 10px; border-radius: 5px; border: none; }
  #send { padding: 10px; border-radius: 5px; background: #1e2a57; color: #c0c8e0; border: none; cursor: pointer; }
  #performance { margin-top: 10px; font-size: 1.2em; }
  #container { max-width: 800px; margin: auto; }
  .msg { margin: 5px 0; padding: 5px; border-radius: 4px; }
  .user
