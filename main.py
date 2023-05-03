import os
import sys

import requests
from PySide6.QtCore import Qt, Slot, Signal, QUrl, QObject, QFile, QIODevice
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineScript
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from ui_MainWindow import Ui_MainWindow

# basedir = os.path.dirname(__file__)
BASE_DIR = '.'

# Debug webengine
DEBUG_PORT = '35588'
DEBUG_URL = 'http://127.0.0.1:%s' % DEBUG_PORT

# Must make sure that the user-agent is latest!
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}


# Copy from: https://riverbankcomputing.com/pipermail/pyqt/2015-August/036346.html
def client_script():
    script = QWebEngineScript()
    qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
    if not qwebchannel_js.open(QIODevice.OpenModeFlag.ReadOnly):
        raise SystemExit(
            'Failed to load qwebchannel.js with error: %s' %
            qwebchannel_js.errorString())
    qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')
    script.setSourceCode(qwebchannel_js)
    script.setName('xxx')
    script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
    script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
    script.setRunsOnSubFrames(True)
    return script


def platform_free_get_path_downloads():
    if sys.platform == 'darwin':
        path_to_downloads = os.path.join(os.path.expanduser('~'), "Downloads")
        return path_to_downloads
    elif sys.platform == 'win32':
        import winreg
        sid = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
        path_to_downloads, _ = winreg.QueryValueEx(sid, '{374DE290-123F-4565-9164-39C4925E467B}')
        sid.Close()
        return path_to_downloads
    else:
        path_to_downloads = '*** Unsupported Platform ***'
        return path_to_downloads


def platform_free_set_wallpaper(full_path):
    if sys.platform == 'darwin':
        from appscript import app, mactypes
        app('Finder').desktop_picture.set(mactypes.File(full_path))
    elif sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 0)


def get_all_supported_url(js_dir):
    urls = []
    for js in os.listdir(js_dir):
        with open(os.path.join(js_dir, js)) as f:
            # First line
            line = f.readline()
            if 'host_url' in line:
                host_urls = line.replace(' ', '').replace('\n', '').replace('//host_url=', '').split(',')
                urls.extend(host_urls)
    return urls


def get_usr_script(host_url, js_dir):
    # TODO cache script to avoid from opening script file repeatedly.
    js_file = ''
    for js in os.listdir(js_dir):
        with open(os.path.join(js_dir, js)) as f:
            line = f.readline()
            if 'host_url' in line:
                urls = line.replace(" ", "").replace('\n', "")
                if host_url in urls:
                    js_file = os.path.join(js_dir, js)
                    # TODO now only one js is supported.
                    break
    if js_file == '':
        return ""

    with open(js_file) as f:
        return f.read()


class CallHandler(QObject):
    progress = Signal(int)

    def __init__(self):
        super().__init__()
        self._save_dir = ''

    @Slot(str, str)
    def set_background(self, url, save_as):
        full_path = os.path.join(self._save_dir, save_as)
        print('call received ' + url + " " + full_path)
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Download picture
            resp = requests.get(url, stream=True, headers=HEADER)
            total_size = int(resp.headers.get('content-length', 0))
            block_size = 1024
            recv_size = 0
            progress_value = 0
            self.progress.emit(0)
            with open(full_path, "wb") as f:
                for data in resp.iter_content(block_size):
                    recv_size += block_size
                    past_value = progress_value
                    progress_value = int(recv_size / total_size * 100)
                    if past_value != progress_value:
                        self.progress.emit(progress_value)
                    f.write(data)
            self.progress.emit(100)

        # Set Background OSX, Windows
        platform_free_set_wallpaper(full_path)

    def set_save_dir(self, save_dir):
        self._save_dir = save_dir


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Basic info
        self._web_url = 'https://bing.wdbyte.com'
        self._usr_info_file = os.path.join(BASE_DIR, "usr.ini")
        self._js_dir = os.path.join(BASE_DIR, 'scripts')
        self._save_dir = os.path.join(platform_free_get_path_downloads(), "wallpaper")

        # User info
        if os.path.exists(self._usr_info_file):
            with open(self._usr_info_file) as f:
                lines = f.readlines()
                for line in lines:
                    if "save_dir" in line:
                        self._save_dir = line.split("=")[-1]

        # Scripts info
        self._urls = get_all_supported_url(self._js_dir)

        # UI Initialization
        self.ui.progressBar.setVisible(False)
        self.ui.urlComboBox.addItems(self._urls)
        self.ui.urlComboBox.setCurrentText(self._web_url)
        self.ui.urlComboBox.currentIndexChanged.connect(self.refresh_url)
        self.ui.saveLineEdit.setText(self._save_dir)
        self.ui.savePushButton.clicked.connect(self.set_save_dir)

        # Browser
        self.ui.webEngineView.loadProgress.connect(self.update_progress_bar)
        self.ui.webEngineView.loadStarted.connect(self.load_started)
        self.ui.webEngineView.loadFinished.connect(self.load_finished)
        self.ui.webEngineView.page().profile().scripts().insert(client_script())

        # Cross-domain Interaction
        self._handler = CallHandler()
        self._handler.set_save_dir(self._save_dir)
        self._handler.progress.connect(self.update_progress_bar)

        self._channel = QWebChannel()
        self._channel.registerObject('handler', self._handler)
        self.ui.webEngineView.page().setWebChannel(self._channel)

        self.ui.webEngineView.load(QUrl(self._web_url))

    @Slot()
    def set_save_dir(self):
        # TODO Check if the returned save directory is legal.
        default = platform_free_get_path_downloads()
        save_dir = os.path.abspath(QFileDialog.getExistingDirectory(self, "Select Directory", default))

        self._save_dir = save_dir
        self._handler.set_save_dir(self._save_dir)
        self.ui.saveLineEdit.setText(self._save_dir)

        with open(self._usr_info_file, "w") as f:
            f.write("save_dir=" + self._save_dir)

    @Slot()
    def refresh_url(self):
        self._web_url = self.ui.urlComboBox.currentText()
        self.ui.webEngineView.load(QUrl(self._web_url))

    @Slot()
    def load_started(self):
        self.update_progress_bar(0)

    @Slot(bool)
    def load_finished(self, ok):
        if ok:
            self.update_progress_bar(100)
            script = get_usr_script(self._web_url, self._js_dir)
            if script == "":
                return
            self.ui.webEngineView.page().runJavaScript(script)

    @Slot(int)
    def update_progress_bar(self, value):
        # To show progress within a complete period, do not forget update with a value more than 100 to finish display.
        if value >= 100:
            self.ui.progressBar.setVisible(False)
        else:
            self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setValue(value)


if __name__ == "__main__":
    # os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT

    app = QApplication(sys.argv)

    with open(os.path.join(BASE_DIR, 'themes/test.qss')) as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
