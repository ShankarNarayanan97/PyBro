# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 18:19:05 2020

@author: S Shankar Narayanan
"""

import os # This is done to link files in HDD to program

import sys # Think of this as a pre-built package to use passive system functions

# Here I'm importing the PyQt5 library which is kind of a high-level binding to enable multi-level functionalities.

from PyQt5.QtCore import * # This is the main sub-library for PyQt5
from PyQt5.QtWidgets import * # This is the module to use Widgets
from PyQt5.QtGui import * # This is the main GUI container to display the widgets
from PyQt5.QtWebEngineWidgets import * # This is the module for the Browser
from PyQt5.QtPrintSupport import * # As the name suggest, this is used to link locally connected printers to print the web-page

# Notice that I have used * while importing. This is done to import all the modules present in them.

# Now the way I'm going to build the browser is that I'm going to make use of OOP to faciliate easier deployment and for scalability.

class AboutDialog(QDialog): # This is the drop down for displaying the program's developer information whcih takes in a value which we pass it
    def __init__(self, *args, **kwargs): # This is the constructor taking 2 parameters, *args which takes a dynamic input and 
                                        # **kwargs which takes a dynamic input with key-value pairs like a dictionary
                                        
        super(AboutDialog, self).__init__(*args, **kwargs) # super() is used to inherit properties of parent class.

        QBtn = QDialogButtonBox.Ok  # Here we are importing the class for widget import.
        self.buttonBox = QDialogButtonBox(QBtn)
        
        # I'm putting 2 functions whether to accept or reject the request
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

                  

        layout = QVBoxLayout() # Here I'm importing the class to design the GUI layout

        title = QLabel("         Made by \n S Shankar Narayanan")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png'))) # As i mentioned earlier, os module is used to link the file in my
                                                                            # HDD to the value of 'images'
        layout.addWidget(logo) # Adding the widget to the main layout

        layout.addWidget(QLabel("Version 1.0")) 


        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter) # This loop is to make sure the layout is unwavered by the elements

        layout.addWidget(self.buttonBox)

        self.setLayout(layout) # I'm now commiting the changes.
        
        
 # Now I'm going to repeaat the same for the other modules.       
        
        
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs) # The usual stuff
        
        # Now im am going to give functionality to the browser

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation") # Adding URL Navigator to the component
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)
        
        # Adding component to provide BACK button functionality

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self) 
        back_btn.setStatusTip("Back to previous page") 
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back()) # BACK functionality linkage
        navtb.addAction(back_btn) # Commiting the changes
        
        
        # Adding component to provide FORWARD button functionality

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward()) # FORWARD functionality linkage
        navtb.addAction(next_btn) # Commiting the changes
        
        # Adding component to provide RELOAD button functionality

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload()) # RELOAD functionality linkage
        navtb.addAction(reload_btn) # Commiting the changes
        
        # Adding component to provide HOME button functionality

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home) # RELOAD functionality linkage
        navtb.addAction(home_btn) # Commiting the changes

        navtb.addSeparator() # Now I'm adding a seperator 

        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png'))) 
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url) # Giving function to the property
        navtb.addWidget(self.urlbar)
        
        # Adding component to provide HOME button functionality

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self) # STOP functionality linkage
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        
        # Repeating the same for the other components

        file_menu = self.menuBar().addMenu("&File") 

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About PyBro ", self)
        about_action.setStatusTip("Find out more about S Shankar Narayanan")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_pybrowser_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            " My Homepage", self)
        navigate_pybrowser_action.setStatusTip("Go to my Homepage")
        navigate_pybrowser_action.triggered.connect(self.navigate_pybrowser)
        help_menu.addAction(navigate_pybrowser_action)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage') # Adding HOMEPAGE functionality

        self.show()

        self.setWindowTitle("PyBro")
        self.setWindowIcon(QIcon(os.path.join('images', 'browser_title.png')))
        
    def add_new_tab(self, qurl=None, label="Blank"): # This is the main function to add a new tab

        if qurl is None:
            qurl = QUrl('') # To prevent any unintended request

        browser = QWebEngineView() # Importing browser module
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)


        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title())) # To change the title once a succesfull request is done

    def tab_open_doubleclick(self, i): # This is the main function to add double click functionality
        if i == -1:  # No tab under the click
            self.add_new_tab()
            
    # Repeating the same for other pertinent functionalities

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i) # This is done to avoid unnecessary memory usage.

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s -S Shankar Narayanan" % title)

    def navigate_pybrowser(self):
        self.tabs.currentWidget().setUrl(QUrl("https://github.com/ShankarNarayanan97")) # My GITHUB homepage

    def about(self):
        dlg = AboutDialog() # Routing to main 
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)") # This is the functionality to open saved web pages in .htm and .html format

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)") # Same as above

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com")) # To provide a default homepage, felt google is better

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https': # To provide more secure functionality, similair to HTTPS Everywhere extension
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("PyBro")
app.setOrganizationName("PyBro")
app.setOrganizationDomain("http://shankarnarayanan.me/?reqp=1&reqr=")

window = MainWindow()

app.exec_()

