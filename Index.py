from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon 
import sys
import sqlite3

db = sqlite3.connect("app.db")
cr = db.cursor()

cr.execute(
    "CREATE TABLE IF NOT EXISTS Students (Student_ID INTEGER PRIMARY KEY, Student_Name TEXT)")
cr.execute(
    "CREATE TABLE IF NOT EXISTS Attendance (Student_Name TEXT, Attend_Times INTEGER, Student_ID INTEGER)")

cr.execute("CREATE TABLE IF NOT EXISTS Admins (Username TEXT PRIMARY KEY, Password TEXT)")

try:
    cr.execute("INSERT INTO Admins (Username, Password) VALUES (?, ?)", ("Mohamed", "admin"))
    db.commit()  
except sqlite3.IntegrityError:
    pass

db.commit()


# Login
def validate_admin():
    username = Username.text().strip()
    password = Password.text().strip()

    if not username or not password:
        QtWidgets.QMessageBox.warning(Admin_Login_Window, "Error", "Both Username And Password Are Required!")
        return

    cr.execute("SELECT * FROM Admins WHERE Username = ? AND Password = ?", (username, password))
    admin = cr.fetchone()
    if admin:
        QtWidgets.QMessageBox.information(Admin_Login_Window, "Login Successful", f"Welcome {username}")
        Edit_Window.show()
        Admin_Login_Window.close()
    else:
        QtWidgets.QMessageBox.warning(Admin_Login_Window, "Login Failed", "Invalid Username Or Password!")


# Attend
def mark_attendance():
    student_name = Student_Name.text().strip().capitalize()
    student_id = Student_ID.text().strip()

    if not student_name or not student_id:
        QtWidgets.QMessageBox.warning(Main_Window, "Input Error", "Both Fields Are Required!")
        return

    cr.execute("SELECT * FROM Students WHERE Student_ID = ? AND Student_Name = ?", (student_id, student_name))
    student = cr.fetchone()
    if student:
        cr.execute("SELECT * FROM Attendance WHERE Student_ID = ?", (student_id,))
        attendance = cr.fetchone()
        if attendance:
            cr.execute("UPDATE Attendance SET Attend_Times = Attend_Times + 1 WHERE Student_ID = ?", (student_id,))
        else:
            cr.execute("INSERT INTO Attendance (Student_Name, Attend_Times, Student_ID) VALUES (?, ?, ?)", (student_name, 1, student_id))
            QtWidgets.QMessageBox.information(Main_Window, "Success", "Attendance Marked successfully!")
    else:
        str1 = """Make Sure You Have Write Your Name As It Added Or Check Your ID"""
        QtWidgets.QMessageBox.warning(Main_Window, "Student Not Found ", (str1) )


# Add
def add_student():
    student_name = Student_Name_Edit.text().strip().capitalize()
    student_id = Student_ID_Edit.text().strip()

    if not student_name or not student_id:
        QtWidgets.QMessageBox.warning(Edit_Window, "Error", "Both Fields Are Required!")
        return

    try:
        cr.execute("INSERT INTO Students (Student_ID, Student_Name) VALUES (?, ?)", (student_id, student_name))
        QtWidgets.QMessageBox.information(Edit_Window, "Success", "Student Added Successfully!")
        db.commit()  
    except sqlite3.IntegrityError:
        QtWidgets.QMessageBox.warning(Edit_Window, "Error", "This ID Has been Used Try Another ID.")


# Remove
def remove_student():
    student_id = Student_ID_Edit.text().strip()
    student_name = Student_Name_Edit.text().strip()

    if not student_id or not student_name:
        QtWidgets.QMessageBox.warning(Edit_Window, "Error", "Both Fields Are Required!")
        return

    cr.execute("DELETE FROM Students WHERE Student_ID = ? AND Student_Name = ?", (student_id, student_name))
    cr.execute("DELETE FROM ATTENDANCE WHERE Student_ID = ? AND Student_Name = ?", (student_id, student_name))
    if cr.rowcount > 0:
        QtWidgets.QMessageBox.information(Edit_Window, "Success", "Student Removed Successfully!")
        db.commit()  
    else:
        QtWidgets.QMessageBox.warning(Edit_Window, "Error", "Student Not Found.")


# Students Data Window
def view_students():

    table = QtWidgets.QTableWidget(Students_Window)
    table.setGeometry(20, 20, 1500, 800)
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Attends Times'])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    cr.execute("SELECT Student_ID, Student_Name, Attend_Times FROM Attendance")
    students = cr.fetchall()
    table.setRowCount(len(students))
    for row_idx, (student_id, student_name, Attend_Times) in enumerate(students):
        table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(student_id)))
        table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(student_name))
        table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(Attend_Times)))

    Students_Window.showMaximized()




###########################################################################################################################################
###########################################################################################################################################
###########################################################################################################################################


# Interface

qtw = QtWidgets.QApplication(sys.argv)
Main_Window = QtWidgets.QMainWindow()
Admin_Login_Window = QtWidgets.QMainWindow()
Edit_Window = QtWidgets.QMainWindow()
Students_Window = QtWidgets.QMainWindow()


# Main Window

Main_Window.setWindowTitle('Attendance System')
Main_Window.setWindowIcon(QtGui.QIcon('Attendance System\App Icon.png'))
Main_Window.setGeometry(700, 300, 400, 500)


# Admin Button

Admin_Button = QtWidgets.QPushButton('Admin', Main_Window)
Admin_Button.move(290, 25)
Admin_Button.clicked.connect(Admin_Login_Window.show)
Admin_Button.clicked.connect(Main_Window.close)


# Student Name

ST_Label = QtWidgets.QLabel('Student Name', Main_Window)
ST_Label.setGeometry(75, 120, 200, 32)
ST_Label.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px;')

Student_Name = QtWidgets.QLineEdit(Main_Window)
Student_Name.setGeometry(75, 150, 250, 32)
Student_Name.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px; border-radius: 5px;')
Student_Name.setPlaceholderText('Three-Part Name')


# Student ID

ST_ID_Label = QtWidgets.QLabel('Student ID', Main_Window)
ST_ID_Label.setGeometry(75, 190, 200, 32)
ST_ID_Label.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px;')

Student_ID = QtWidgets.QLineEdit(Main_Window)
Student_ID.setGeometry(75, 220, 250, 32)
Student_ID.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px; border-radius: 5px;')
Student_ID.setPlaceholderText('Enter A Number')


# Attend Button

Attend_Button = QtWidgets.QPushButton('Attend', Main_Window)
Attend_Button.move(250, 275)
Attend_Button.clicked.connect(mark_attendance)


# Admin Login Window

Admin_Login_Window.setWindowTitle('Login')
Admin_Login_Window.setWindowIcon(QtGui.QIcon('Attendance System\App Icon.png'))
Admin_Login_Window.setGeometry(700, 300, 400, 500)


# Username

US = QtWidgets.QLabel('Username', Admin_Login_Window)
US.setGeometry(75, 120, 200, 32)
US.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px;')

Username = QtWidgets.QLineEdit(Admin_Login_Window)
Username.setGeometry(75, 150, 250, 32)
Username.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px; border-radius: 5px;')


# Password

Pass = QtWidgets.QLabel('Password', Admin_Login_Window)
Pass.setGeometry(75, 190, 200, 32)
Pass.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px;')

Password = QtWidgets.QLineEdit(Admin_Login_Window)
Password.setGeometry(75, 220, 250, 32)
Password.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px; border-radius: 5px;')


# Login Button

Login_Button = QtWidgets.QPushButton('Login', Admin_Login_Window)
Login_Button.move(250, 275)
Login_Button.clicked.connect(validate_admin)


# Edit Window

Edit_Window.setWindowTitle('Edit')
Edit_Window.setWindowIcon(QtGui.QIcon('Attendance System\App Icon.png'))
Edit_Window.setGeometry(700, 300, 400, 500)


# Student Name

ST_Label_Edit = QtWidgets.QLabel('Student Name', Edit_Window)
ST_Label_Edit.setGeometry(75, 120, 200, 32)
ST_Label_Edit.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px;')

Student_Name_Edit = QtWidgets.QLineEdit(Edit_Window)
Student_Name_Edit.setGeometry(75, 150, 250, 32)
Student_Name_Edit.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px; border-radius: 5px;')
Student_Name_Edit.setPlaceholderText('Three-Part Name')


# Student ID

ST_ID_Label_Edit = QtWidgets.QLabel('Student ID', Edit_Window)
ST_ID_Label_Edit.setGeometry(75, 190, 200, 32)
ST_ID_Label_Edit.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px;')

Student_ID_Edit = QtWidgets.QLineEdit(Edit_Window)
Student_ID_Edit.setGeometry(75, 220, 250, 32)
Student_ID_Edit.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 20px; border-radius: 5px;')
Student_ID_Edit.setPlaceholderText('Enter A Number')


# Add Button

Add_Button = QtWidgets.QPushButton('Add', Edit_Window)
Add_Button.move(100, 275)
Add_Button.setToolTip('Add Student')
Add_Button.clicked.connect(add_student)


# Remove Button

Remove_Button = QtWidgets.QPushButton('Remove', Edit_Window)
Remove_Button.move(200, 275)
Remove_Button.setToolTip('Remove Student')
Remove_Button.clicked.connect(remove_student)


# Student Data Window

Students_Window.setWindowTitle('View Students')
Students_Window.setWindowIcon(QtGui.QIcon('Attendance System\App Icon.png'))
Students_Window.setGeometry(700, 300, 900, 600)


# Button to View Students Data

View_Students_Button = QtWidgets.QPushButton('View Students', Edit_Window)
View_Students_Button.move(150, 325)
View_Students_Button.setToolTip('View All Students')
View_Students_Button.clicked.connect(view_students)


# Go Back To Attend Window

Attend_Button = QtWidgets.QPushButton('Attend', Edit_Window)
Attend_Button.move(290, 25)
Attend_Button.setToolTip('Go Back To Attend')
Attend_Button.clicked.connect(Edit_Window.close)
Attend_Button.clicked.connect(Main_Window.show)

Main_Window.show()
qtw.exec_()
db.commit()
db.close()
