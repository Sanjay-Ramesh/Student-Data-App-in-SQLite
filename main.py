from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
QGridLayout, QLineEdit, QPushButton, QMainWindow, QMenu, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon

import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons\\add.png"),"Add student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons\\search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Menu", 
                                              "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements
        toolbar =  QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action) 

        # Create statusbar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)


        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)
    
    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog1 = SearchDialog()
        dialog1.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Search Widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Search")
        layout.addWidget(self.student_name)

        # Add a search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
                                (name,))
        rows = list(result)
        print(rows)
        items = main_windows.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_windows.table.item(item.row(), 1).setSelected(True)

            cursor.close()
            connection.close()
        

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Student Name Widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Combo Box Course
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add Mobile 
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_windows.load_data()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from the selected row
        index = main_windows.table.currentRow()
        student_name = main_windows.table.item(index, 1).text()

        # Get id from selected row 
        self.student_id = main_windows.table.item(index, 0).text()

        # Add Student Name Widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Combo Box Course
        course_name = main_windows.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add Mobile 
        mobile = main_windows.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def update(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), 
                         self.course_name.itemText(self.course_name.currentIndex()), 
                          self.mobile.text(), 
                          self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_windows.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        # Get selected row index and student id
        index = main_windows.table.currentRow() 
        student_id = main_windows.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_windows.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Good")
        confirmation_widget.setText("The Record was deleted successfully")
        confirmation_widget.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
This app was created during the course "The Python Mega Course".
Feel free to modify and reuse this app.
"""
        self.setText(content)


app = QApplication(sys.argv)        
main_windows = MainWindow()
main_windows.show()
main_windows.load_data()
sys.exit(app.exec())