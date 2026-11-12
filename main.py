#!/usr/bin/env python

import sys
from browser_config import *
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
        self.open_address("about:newtab")
        
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
            path = Path(__file__).parent / "pages" / (address.split(":")[1] + ".html")
            self.open_file(str(path))
        else:
            if not ("." in address):
                self.browser.setUrl(QUrl.fromUserInput("duckduckgo.com/" + address))
            self.browser.setUrl(QUrl.fromUserInput(self.address_bar.text()))
    def open_file(self, path):
        self.browser.load(QUrl.fromLocalFile(path))
    def open_address(self, address):
        # opens address as string
        self.address_bar.setText(address)
        self.navigate()
    def update_address(self, url):
        self.address_bar.setText(url.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    with open(STYLESHEET, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    
    sys.exit(app.exec())
