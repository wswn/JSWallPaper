import os
import sys

import requests
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, QFile, QIODevice
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineCore import QWebEngineScript
from PyQt6.QtWebEngineWidgets import QWebEngineView


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


class CallHandler(QObject):
    def __init__(self, progress_bar: QtWidgets.QProgressBar):
        super().__init__()
        self._save_dir = ''
        self._progress_bar = progress_bar

    @pyqtSlot(str, str)
    def set_background(self, url, save_as):
        full_path = os.path.join(self._save_dir, save_as)
        print('call received ' + url + " " + full_path)
        if not os.path.exists(full_path):
            resp = requests.get(url, stream=True)
            total_size = int(resp.headers.get('content-length', 0))
            block_size = 1024
            self._progress_bar.setRange(0, total_size)
            self._progress_bar.setVisible(True)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "wb") as f:
                for data in resp.iter_content(block_size):
                    self._progress_bar.setValue(self._progress_bar.value() + block_size)
                    f.write(data)
            self._progress_bar.setValue(0)
            self._progress_bar.setVisible(False)

        # Set Background OSX, Windows
        platform_free_set_wallpaper(full_path)

    def set_save_dir(self, save_dir):
        self._save_dir = save_dir


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        x, y, w, h = self.geometry().x(), self.geometry().y(), 1280, 720
        self.setGeometry(x, y, w, h)

        # Central Widget
        main_layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)

        # Set Central Widget
        self.setCentralWidget(central_widget)

        # Basic info
        self._usr_info_file = "usr.ini"
        self._web_url = 'https://bing.wdbyte.com'
        self._js_dir = 'scripts/'
        self._save_dir = os.path.join(platform_free_get_path_downloads(), "wallpaper")

        # User info
        if os.path.exists(self._usr_info_file):
            with open(self._usr_info_file) as f:
                lines = f.readlines()
                for line in lines:
                    if "save_dir" in line:
                        self._save_dir = line.split("=")[-1]

        # Scripts info
        self._urls = self.get_all_supported_url()

        # Set Progress bar
        self._progress_bar = QtWidgets.QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFixedHeight(2)
        self._progress_bar.setParent(central_widget)
        self._progress_bar.setVisible(False)

        # Set toolbar
        self._url_label = QtWidgets.QLabel("URL")
        self._url_combo_box = QtWidgets.QComboBox()
        self._url_combo_box.addItems(self._urls)
        self._url_combo_box.setCurrentText(self._web_url)
        self._url_combo_box.currentIndexChanged.connect(self.refresh_url)
        self._url_combo_box.adjustSize()

        tool_url_layout = QtWidgets.QHBoxLayout()
        tool_url_layout.addWidget(self._url_label)
        tool_url_layout.addWidget(self._url_combo_box)

        self._save_dir_button = QtWidgets.QPushButton("Save into")
        self._save_dir_line_edit = QtWidgets.QLineEdit(self._save_dir)

        tool_save_dir_layout = QtWidgets.QHBoxLayout()
        tool_save_dir_layout.addWidget(self._save_dir_button)
        tool_save_dir_layout.addWidget(self._save_dir_line_edit)
        tool_save_dir_layout.setSpacing(5)

        self._save_dir_button.clicked.connect(self.set_save_dir)
        self._save_dir_line_edit.setReadOnly(True)

        tool_layout = QtWidgets.QHBoxLayout()
        tool_layout.addLayout(tool_url_layout)
        tool_layout.addLayout(tool_save_dir_layout)

        main_layout.addLayout(tool_layout)

        # Browser, comment the next line if no debug info is required.
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=0"
        self._browser = QWebEngineView()
        self._browser.loadFinished.connect(self.script_injection)
        self._browser.page().profile().scripts().insert(client_script())

        main_layout.addWidget(self._browser)

        # Interaction
        self._handler = CallHandler(self._progress_bar)
        self._handler.set_save_dir(self._save_dir)

        self._channel = QWebChannel()
        self._browser.page().setWebChannel(self._channel)
        self._channel.registerObject('handler', self._handler)

        self._browser.load(QUrl(self._web_url))

    def get_all_supported_url(self):
        urls = []
        js_dir = self._js_dir
        js_file = ''
        for js in os.listdir(js_dir):
            with open(js_dir + js) as f:
                # First line
                line = f.readline()
                if 'host_url' in line:
                    host_urls = line.replace(' ', '').replace('\n', '').replace('//host_url=', '').split(',')
                    urls.extend(host_urls)
        return urls

    def get_usr_script(self):
        js_dir = self._js_dir
        js_file = ''
        for js in os.listdir(js_dir):
            with open(js_dir + js) as f:
                line = f.readline()
                if 'host_url' in line:
                    urls = line.replace(" ", "").replace('\n', "")
                    if self._web_url in urls:
                        js_file = js_dir + js
                        # TODO now only one js is supported.
                        break
        if js_file == '':
            return """ console.log("No js found")"""

        with open(js_file) as f:
            return f.read()

    @QtCore.pyqtSlot(bool)
    def script_injection(self, ok):
        if ok:
            script = self.get_usr_script()
            self._browser.page().runJavaScript(script)

    @QtCore.pyqtSlot()
    def set_save_dir(self):
        default = platform_free_get_path_downloads()
        save_dir = os.path.abspath(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", default))

        self._save_dir = save_dir
        self._handler.set_save_dir(self._save_dir)
        self._save_dir_line_edit.setText(self._save_dir)

        with open(self._usr_info_file, "w") as f:
            f.write("save_dir=" + self._save_dir)

    @QtCore.pyqtSlot()
    def refresh_url(self):
        self._web_url = self._url_combo_box.currentText()
        self._browser.load(QUrl(self._web_url))

    def resizeEvent(self, event):
        self._progress_bar.setFixedWidth(self.width())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)
    with open('themes/test.qss') as f:
        qApp.setStyleSheet(f.read())
    ui = MainWindow()
    ui.setWindowTitle("WallPaper")
    ui.show()
    sys.exit(qApp.exec())
