import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QPushButton
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("browser")
        self.resize(800, 600)

        back_button = QPushButton("Back")
        forward_button = QPushButton("Forward")
        reload_button = QPushButton("Reload")

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Search")
        self.address_bar.returnPressed.connect(self.navigate)

        self.browser = QWebEngineView()
        #self.browser.setUrl(QUrl("https://www.google.com"))
        
        back_button.clicked.connect(self.browser.back)
        forward_button.clicked.connect(self.browser.forward)
        reload_button.clicked.connect(self.browser.reload)
        self.browser.urlChanged.connect(self.update_address)

        toolbar = QHBoxLayout()
        toolbar.addWidget(back_button)
        toolbar.addWidget(forward_button)
        toolbar.addWidget(reload_button)
        toolbar.addWidget(self.address_bar)
        
        central_widget = QWidget()

        layout = QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(self.browser)

        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)
        
    def navigate(self):
        address = self.address_bar.text().strip().lower()

        if "about:" in address:
            path = Path(__file__).parent / "pages" / (address.split(":")[0] + ".html")
            self.open_file(str(path))
        else:
            self.browser.setUrl(QUrl.fromUserInput(self.address_bar.text()))
    def open_file(self, path):
        self.browser.load(QUrl.fromLocalFile(path))
    def update_address(self, url):
        self.address_bar.setText(url.toString())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
