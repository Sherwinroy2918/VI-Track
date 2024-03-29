import pickle
import threading
from PyQt6.QtCore import QFile
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QPushButton,QLineEdit,QLabel
from mainwindow import Ui_MainWindow  # Import the generated Python code
from backend import Script
from signin import Ui_MainWindow1
from Userwindow import Ui_MainWindow2
from eye_control import CursorController
 
choice="-1"
Backend=Script()
Eye=CursorController()
class MyThread(threading.Thread):
  def __init__(self, method_to_call):
    super().__init__()
    self.method_to_call = method_to_call

  def run(self):
    self.method_to_call()
class MyMainWindow(QMainWindow):

    def retrieve_data(self):
        try:
            # Open the file and retrieve the data using pickle
            with open("data.pkl", "rb") as file:
                data = pickle.load(file)
                
        except FileNotFoundError:
            self.data_label.setText("Data not found.")
        for i in data:
            if(i[0]==self.username and i[1]==self.password):
                return i[2]
        else:
            self.label.setText("The entered username or password does not match.")
            return "-1"
            #self.loginButton.clicked.connect(self.get_input)

    def get_input(self):
        # Retrieve the username and password entered by the user
        global choice
        self.username = str(self.username_edit.text())
        self.password = str(self.password_edit.text())
        
        choice=self.retrieve_data()
        if(choice!="-1"):
            self.close()
            return
        else:
            self.username_edit.clear()
            self.password_edit.clear()
            self.loginButton.clicked.connect(self.get_input)
            return


    def goto_sign_in(self):
        self.login=SignInWindow()
        self.login.show()

        
    def __init__(self):
        super().__init__()
        # Create an instance of the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signinButton=self.findChild(QPushButton,"signinButton")
        self.signinButton.clicked.connect(self.goto_sign_in)

        self.username_edit = self.findChild(QLineEdit, "lineEdit")
        self.password_edit = self.findChild(QLineEdit, "lineEdit_2")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.label = self.findChild(QLabel, "tryagain")

        self.loginButton = self.findChild(QPushButton, "loginButton")

        self.loginButton.clicked.connect(self.get_input)
class SignInWindow(QMainWindow):
    def save_data(self):
        # Get the data from the QLineEdit
        self.username = str(self.username_edit.text())
        self.password = str(self.password_edit.text())
        self.choice=str(self.choice_edit.text())
        with open("data.pkl", "rb") as file:
                data = pickle.load(file)
        data.append([self.username,self.password,self.choice])

        # Open a file for storing the data using pickle
        with open("data.pkl", "wb") as file:
            pickle.dump(data, file)

        self.message.setText("user registered successfully.")
        self.hide()

    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow1()
        self.ui.setupUi(self)

        self.username_edit = self.findChild(QLineEdit, "lineEdit")
        self.password_edit = self.findChild(QLineEdit, "lineEdit_2")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.choice_edit = self.findChild(QLineEdit, "lineEdit_3")
        self.message=self.findChild(QLabel,"message")
        
        


        self.signinButton=self.findChild(QPushButton,"pushButton")
        self.signinButton.clicked.connect(self.save_data)
class UserPage(QMainWindow):
    def terminate(self):
        if(choice!="1"):
            global Backend
            Backend.true=0
        else:
            global Eye
            Eye.true=0
        self.close()
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow2()
        self.ui.setupUi(self)

        
        self.terminate_button=self.findChild(QPushButton,"stopButton")
        self.terminate_button.clicked.connect(self.terminate)
        self.showMinimized()
        
def back():
        global choice
        global Backend
        if(choice=="1"):
            Eye.control_cursor()
            Eye.release()
        elif(choice=="2"):
            Backend.control_hand()
        elif(choice=="3"):
            Backend.control_voice()
        
    


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyMainWindow()
    window.show()
    app.exec()

    thread_1=MyThread(back)
    newwindow=UserPage()
    
    thread_1.start()

    newwindow.show()
    app.exec()

    thread_1.join()
    
    

    sys.exit()

