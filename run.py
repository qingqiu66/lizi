import webview
import http.server
import socketserver
import os
import sys
import threading
import json
import webbrowser

# ================= 配置 =================
IS_FRAMELESS = True
PORT = 8001
# =======================================

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

WORK_DIR = get_resource_path(".")
os.chdir(WORK_DIR)
gui_window = None

class GuiLogHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        msg = f"[{self.log_date_time_string()}] {format % args}"
        print(msg)

        if gui_window:
            def send_to_gui():
                try:
                    gui_window.evaluate_js(f"addLog({json.dumps(msg)})")
                except Exception as e:
                    print(f"Log send error: {e}")

            threading.Thread(target=send_to_gui, daemon=True).start()

#线程化服务器管理
class ThreadedServer:
    def __init__(self):
        self.server = None
        self.thread = None
        self.is_running = False

    def start(self):
        if self.is_running: return True
        try:
            socketserver.TCPServer.allow_reuse_address = True
            self.server = socketserver.TCPServer(("", PORT), GuiLogHandler)
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            self.is_running = True
            self._log('✅ 服务已启动: http://localhost:8001')
            return True
        except Exception as e:
            self._log(f'❌ 启动失败: {str(e)}')
            return False

    def stop(self):
        if self.server and self.is_running:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            self._log('🛑 服务已停止')
            return True
        return False
    
    def _log(self, msg):
        if gui_window:
            def send():
                try:
                    gui_window.evaluate_js(f"addLog({json.dumps(msg)})")
                except: pass
            threading.Thread(target=send, daemon=True).start()

server_instance = ThreadedServer()

#API
class Api:
    def start_server(self):
        return server_instance.start()

    def stop_server(self):
        return server_instance.stop()

    def read_index(self):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"

    def save_index(self, content):
        try:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
            
    def quit_app(self):
        server_instance.stop()
        if gui_window: gui_window.destroy()
        # 强制退出，防止残留
        os._exit(0)

    #打开浏览器
    def open_browser(self):
        webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    api = Api()
    dashboard_path = os.path.join(WORK_DIR, 'dash.html')
    
    gui_window = webview.create_window(
        title='Console',
        url=f"file://{dashboard_path}",
        width=1200,
        height=800,
        js_api=api,
        frameless=IS_FRAMELESS,
        easy_drag=False,
        background_color='#000000',
        text_select=True
    )
    
    webview.start(debug=True)