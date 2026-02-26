import webview
import http.server
import socketserver
import os
import sys
import threading
import json
import webbrowser
import shutil 

# ================= 配置 =================
IS_FRAMELESS = True
PORT = 8001
# =======================================

# 1. 获取内部静态资源路径
def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

# 2. 获取外部持久化数据路径
def get_user_data_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    lizi_dir = os.path.join(base_dir, 'lizi')
    if not os.path.exists(lizi_dir):
        os.makedirs(lizi_dir)
        
    return os.path.join(lizi_dir, 'index.html')

#持久化数据
USER_INDEX_PATH = get_user_data_path()

if not os.path.exists(USER_INDEX_PATH):
    bundled_index = get_asset_path('index.html')
    if os.path.exists(bundled_index):
        shutil.copy(bundled_index, USER_INDEX_PATH)

os.chdir(os.path.dirname(USER_INDEX_PATH))

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

# API
class Api:
    def start_server(self):
        return server_instance.start()

    def stop_server(self):
        return server_instance.stop()

    def read_index(self):
        try:
            with open(USER_INDEX_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def save_index(self, content):
        try:
            with open(USER_INDEX_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False

    def quit_app(self):
        print("正在安全关闭系统...")
        try:
            server_instance.stop()
        except:
            pass
        os._exit(0)

    def open_browser(self):
        webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    api = Api()
    dashboard_path = get_asset_path('dash.html')
        
    gui_window = webview.create_window(
        title='控制台',
        url=f"file://{dashboard_path}",
        width=1200,
        height=800,
        js_api=api,
        frameless=IS_FRAMELESS,
        easy_drag=False,     
        background_color='#000000',
        text_select=True
        )
    gui_window.events.closed += api.quit_app
    
    webview.start(debug=True)