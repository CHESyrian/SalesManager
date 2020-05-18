from warnings import filterwarnings
filterwarnings('ignore')
import os
from random import choice
from sys import argv, exit
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QPushButton, QLabel, QLineEdit,\
    QGridLayout, QMessageBox, QToolBar, QAction, QTableWidget, QTableWidgetItem, QTabWidget, QComboBox
import pymysql as SQL


#Main Window in App
class Main_UI(QMainWindow):
# Main Variables in this class.
    def __init__(self, auth_info):
        super(Main_UI, self).__init__()
        self.auth_info    = auth_info
        self.exp_Class    = auth_info['Class']
        self.exp_username = auth_info['username']
        self.exp_password = auth_info['password']
        self.exp_dbname   = auth_info['DBName']
        self.db_conn      = SQL.connect('localhost', auth_info['username'], auth_info['password'], auth_info['DBName'])
        self.full_width   = QApplication.primaryScreen().size().width() - 15
        self.full_height  = QApplication.primaryScreen().size().height() - 68
        self.Main_Grid    = QGridLayout()
        self.toolbar      = QToolBar()
        self.tabwidget    = QTabWidget()
        self.win_icon     = "Resources/sm_logo_icon.ico"   
        self.win_title    = "Sales Manager V1.0 | %s - %s"%(self.exp_Class, self.exp_username)
        self.table_label  = {'clients' :['ID', 'Name', 'Email', 'Username', 'Password', 'Number Phone'],
                             'products':['ID', 'Product Name', 'Quantity', 'Unit Price', 'Product Code'],
                             'requests':['ID', 'Client', 'Product Name', 'Quantity', 'Request Date', 'Status']}
        if self.exp_Class == "Importer":
            self.Importer_UI()
        elif self.exp_Class == "Exporter":
            self.Exporter_UI()

#Eporter Interface
    def Exporter_UI(self):
        self.setGeometry(0, 0, self.full_width, self.full_height)
        self.setWindowTitle(self.win_title)
        self.setWindowIcon(QIcon(self.win_icon))
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(32, 32))
# Tables in Exporter Interface
# Table_1 - clients
        self.table_1   = QTableWidget()
        self.Hheader_1 = self.table_1.horizontalHeader()
        self.Vheader_1 = self.table_1.verticalHeader()
        self.table_1.setAlternatingRowColors(True)
        self.table_1.setColumnCount(6)
        self.Hheader_1.setCascadingSectionResizes(False)
        self.Hheader_1.setSortIndicatorShown(False)
        self.Hheader_1.setStretchLastSection(True)
        self.Vheader_1.setVisible(False)
        self.Vheader_1.setCascadingSectionResizes(False)
        self.Vheader_1.setStretchLastSection(False)
        self.table_1.setHorizontalHeaderLabels(self.table_label['clients'])
# Table_2 - products
        self.table_2   = QTableWidget()
        self.Hheader_2 = self.table_2.horizontalHeader()
        self.Vheader_2 = self.table_2.verticalHeader()
        self.table_2.setAlternatingRowColors(True)
        self.table_2.setColumnCount(5)
        self.Hheader_2.setCascadingSectionResizes(False)
        self.Hheader_2.setSortIndicatorShown(False)
        self.Hheader_2.setStretchLastSection(True)
        self.Vheader_2.setVisible(False)
        self.Vheader_2.setCascadingSectionResizes(False)
        self.Vheader_2.setStretchLastSection(False)
        self.table_2.setHorizontalHeaderLabels(self.table_label['products'])
# Table_3 - requests
        self.table_3 = QTableWidget()
        self.Hheader_3 = self.table_3.horizontalHeader()
        self.Vheader_3 = self.table_3.verticalHeader()
        self.table_3.setAlternatingRowColors(True)
        self.table_3.setColumnCount(6)
        self.Hheader_3.setCascadingSectionResizes(False)
        self.Hheader_3.setSortIndicatorShown(False)
        self.Hheader_3.setStretchLastSection(True)
        self.Vheader_3.setVisible(False)
        self.Vheader_3.setCascadingSectionResizes(False)
        self.Vheader_3.setStretchLastSection(False)
        self.table_3.setHorizontalHeaderLabels(self.table_label['requests'])
# Actions in toolbar
        self.ac_savetable     = QAction(QIcon('Resources/save_as.png'), 'Save Table', self)
        self.ac_addclient     = QAction(QIcon('Resources/add-user-male-64.png'), 'Add Client', self)
        self.ac_updateclient  = QAction(QIcon('Resources/change-user-64.png'), 'Update Client', self)
        self.ac_deleteclient  = QAction(QIcon('Resources/denied-64.png'), 'Delete Client', self)
        self.ac_addproduct    = QAction(QIcon('Resources/add_tag.png'), 'Add Product', self)
        self.ac_updateproduct = QAction(QIcon('Resources/update_tag.png'), 'Update Product', self)
        self.ac_deleteproduct = QAction(QIcon('Resources/remove_tag.png'), 'Delete Product', self)
        self.ac_refreshtable  = QAction(QIcon('Resources/refresh.png'), 'Refresh Table', self)
        self.ac_aboutapp      = QAction(QIcon('Resources/info.png'), 'About App', self)
        self.ac_developerinfo = QAction(QIcon('Resources/developer_info.png'), 'Developer Info', self)
        self.ac_contactus     = QAction(QIcon('Resources/contact_us.png'), 'Contact Us', self)
# Add Actions to toolbar.
        actions = [self.ac_savetable, self.ac_addclient, self.ac_updateclient, self.ac_deleteclient, self.ac_addproduct, 
                   self.ac_deleteproduct, self.ac_updateproduct, self.ac_refreshtable,self.ac_aboutapp, 
                   self.ac_developerinfo]
        for action in actions:
            self.toolbar.addAction(action)
# Set Widgets
        self.tabwidget.addTab(self.table_1, 'clients')
        self.tabwidget.addTab(self.table_2, 'products')
        self.tabwidget.addTab(self.table_3, 'requests')
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.tabwidget)
# Actions Connect
        self.ac_addclient.triggered.connect(self.addClient)
        self.ac_updateclient.triggered.connect(self.updateClient)
        self.ac_deleteclient.triggered.connect(self.deleteClient) 
        self.ac_refreshtable.triggered.connect(lambda x : self.refresh(self.tabwidget.tabText(self.tabwidget.currentIndex())))
        self.ac_aboutapp.triggered.connect(self.aboutApp)
        self.ac_developerinfo.triggered.connect(self.developerInfo)
        self.loadData(self.exp_Class)
        self.show()

    def Importer_UI(self):
        pass
#LOad Data from Tables Method.
    def loadData(self, usrClass):
        if usrClass == "Exporter":
            db_cur = self.db_conn.cursor()
            db_cur.execute(" SELECT * FROM clients ")
            clients_data  = db_cur.fetchall()
            db_cur.execute(" SELECT * FROM products ")
            products_data = db_cur.fetchall()
            db_cur.execute(" SELECT * FROM requests ")
            requests_data = db_cur.fetchall()
# Get Clients Table 
            self.table_1.setRowCount(0)
            for t1_index, t1_row in enumerate(clients_data):
                self.table_1.insertRow(t1_index)
                for t1_feature, t1_value in enumerate(t1_row):
                    self.table_1.setItem(t1_index, t1_feature, QTableWidgetItem(str(t1_value)))
# Get Products Table
            self.table_2.setRowCount(0)
            for t2_index, t2_row in enumerate(products_data):
                self.table_2.insertRow(t2_index)
                for t2_feature, t2_value in enumerate(t2_row):
                    self.table_2.setItme(t2_index, t2_feature, QTableWidgetItem(str(t2_value)))
# Get Requests Table
            self.table_3.setRowCount(0)
            for t3_index, t3_row in enumerate(requests_data):
                self.table_3.insertRow(t3_index)
                for t3_feature, t3_value in enumerate(t3_row):
                    self.table_3.setItem(t3_index, t3_feature, QTableWidgetItem(str(t3_value)))
            db_cur.close()
        elif usrClass == "Importer":
            pass

# Refresh Table method.
    def refresh(self, table):
        db_cur = self.db_conn.cursor()
        sql_query = """ SELECT * FROM {} """.format(table)
        db_cur.execute(sql_query)
        table_data = db_cur.fetchall()
        widget = self.table_1 if table == 'clients' else self.table_2 if table == 'products' else self.table_3
        widget.setRowCount(0)
        for t1_index, t1_row in enumerate(table_data):
                widget.insertRow(t1_index)
                for t1_feature, t1_value in enumerate(t1_row):
                    widget.setItem(t1_index, t1_feature, QTableWidgetItem(str(t1_value)))
        db_cur.close()

# Add Client method - connect with Add Client Action
    def addClient(self):
        add_dialog = Add_Client(self.db_conn)
        add_dialog.exec_()

# Update Client method - connect with Add Update Action    
    def updateClient(self):
        update_dialog = Update_Client(self.db_conn)
        update_dialog.exec_()

# Delete Client Method - connect with Delete Client Action
    def deleteClient(self):
        delete_dialog = Delete_Client(self.db_conn)
        delete_dialog.exec_()

# Add Product Method - connect with Add Product Action
    def addProduct(self):
        pass

# Update Product Method - connect with Update Product Action
    def aupdateProduct(self):
        pass

# Delete Product Method - connect with Delete Product Action
    def deleteProduct(self):
        pass

# About App method - connect with About App Action
    def aboutApp(self):
        about_app = About_App()
        about_app.exec_()

# Developer Info method - connect with Developer Info Action
    def developerInfo(self):
        developer_info = Developer_Info()
        developer_info.exec_()


# Exporter Operations
# Add Client Dialog - Add Client Action in toolbar.
class Add_Client(QDialog):
    def __init__(self, db_connect):
        super(Add_Client, self).__init__()
        self.db_con = db_connect
        self.Grid   = QGridLayout()
        self.lbl_1  = QLabel(self)
        self.lbl_2  = QLabel(self)
        self.lbl_3  = QLabel(self)
        self.lbl_4  = QLabel(self)
        self.lbl_5  = QLabel(self)
        self.lbl_6  = QLabel(self)
        self.edt_1  = QLineEdit(self)
        self.edt_2  = QLineEdit(self)
        self.edt_3  = QLineEdit(self)
        self.edt_4  = QLineEdit(self)
        self.edt_5  = QLineEdit(self)
        self.edt_6  = QLineEdit(self)
        self.btn_1  = QPushButton(self)
        self.title  = "Add Client"
        self.width  = 340
        self.height = 380
        self.Add_UI()

# Add Client Interface Method
    def Add_UI(self):
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setWindowTitle(self.title)
        self.setContentsMargins(20, 20, 20, 20)
        self.lbl_1.setText('First Name')
        self.lbl_2.setText('Last Name')
        self.lbl_3.setText('Email')
        self.lbl_4.setText('Username')
        self.lbl_5.setText('Password')
        self.lbl_6.setText('Number Phone')
        self.btn_1.setText('Add')
        self.Grid.addWidget(self.lbl_1, 0, 0)
        self.Grid.addWidget(self.lbl_2, 1, 0)
        self.Grid.addWidget(self.lbl_3, 2, 0)
        self.Grid.addWidget(self.lbl_4, 3, 0)
        self.Grid.addWidget(self.lbl_5, 4, 0)
        self.Grid.addWidget(self.lbl_6, 5, 0)
        self.Grid.addWidget(self.edt_1, 0, 1, 1, 2)
        self.Grid.addWidget(self.edt_2, 1, 1, 1, 2)
        self.Grid.addWidget(self.edt_3, 2, 1, 1, 2)
        self.Grid.addWidget(self.edt_4, 3, 1, 1, 2)
        self.Grid.addWidget(self.edt_5, 4, 1, 1, 2)
        self.Grid.addWidget(self.edt_6, 5, 1, 1, 2)
        self.Grid.addWidget(self.btn_1, 6, 0, 1, 3)
        self.setLayout(self.Grid)
        self.btn_1.clicked.connect(self.do_Add)

# Add Client Method
    def do_Add(self):
        first_name = self.edt_1.text()
        last_name  = self.edt_2.text()
        email      = self.edt_3.text()
        username   = self.edt_4.text()
        password   = self.edt_5.text()
        num_phone  = self.edt_6.text()
        db_cur    = self.db_con.cursor()
        add_query = """ INSERT INTO clients (Full_Name, Email, Username, Password, Number_Phone)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s')"""%(first_name + '  ' + last_name, email, username, password, num_phone)
        db_cur.execute(add_query)
        self.db_con.commit()
        db_cur.close()
        self.close()


# Update Client Dialog - Update Client Action in toolbar.
class Update_Client(QDialog):
    def __init__(self, db_connect):
        super(Update_Client, self).__init__()
        self.db_con = db_connect
        self.Grid   = QGridLayout()
        self.lbl_1  = QLabel(self)
        self.lbl_2  = QLabel(self)
        self.lbl_3  = QLabel(self)
        self.lbl_4  = QLabel(self)
        self.lbl_5  = QLabel(self)
        self.lbl_6  = QLabel(self)
        self.lbl_7  = QLabel(self)
        self.edt_1  = QLineEdit(self)
        self.edt_2  = QLineEdit(self)
        self.edt_3  = QLineEdit(self)
        self.edt_4  = QLineEdit(self)
        self.edt_5  = QLineEdit(self)
        self.edt_6  = QLineEdit(self)
        self.edt_7  = QLineEdit(self)
        self.btn_1  = QPushButton(self)
        self.btn_2  = QPushButton(self)
        self.title  = "Update Client"
        self.width  = 340
        self.height = 380
        self.Update_UI()

# Update Client Interface Method
    def Update_UI(self):
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setWindowTitle(self.title)
        self.setContentsMargins(20, 10, 20, 10)
        self.edt_1.setPlaceholderText('username')
        self.lbl_1.setText('Client')
        self.lbl_2.setText('First Name')
        self.lbl_3.setText('Last Name')
        self.lbl_4.setText('Email')
        self.lbl_5.setText('Username')
        self.lbl_6.setText('Password')
        self.lbl_7.setText('Number Phone')
        self.btn_1.setText('Get Client Data')
        self.btn_2.setText('Save')
        self.Grid.addWidget(self.lbl_1, 0, 0)
        self.Grid.addWidget(self.lbl_2, 2, 0)
        self.Grid.addWidget(self.lbl_3, 3, 0)
        self.Grid.addWidget(self.lbl_4, 4, 0)
        self.Grid.addWidget(self.lbl_5, 5, 0)
        self.Grid.addWidget(self.lbl_6, 6, 0)
        self.Grid.addWidget(self.lbl_7, 7, 0)
        self.Grid.addWidget(self.edt_1, 0, 1, 1, 2)
        self.Grid.addWidget(self.edt_2, 2, 1, 1, 2)
        self.Grid.addWidget(self.edt_3, 3, 1, 1, 2)
        self.Grid.addWidget(self.edt_4, 4, 1, 1, 2)
        self.Grid.addWidget(self.edt_5, 5, 1, 1, 2)
        self.Grid.addWidget(self.edt_6, 6, 1, 1, 2)
        self.Grid.addWidget(self.edt_7, 7, 1, 1, 2)
        self.Grid.addWidget(self.btn_1, 1, 0, 1, 3)
        self.Grid.addWidget(self.btn_2, 8, 0, 1, 3)
        self.setLayout(self.Grid)
        self.btn_1.clicked.connect(self.get_Client_Data)
        self.btn_2.clicked.connect(self.do_Update)

# Get Client Data Method from Table 
    def get_Client_Data(self):
        self.client_username = self.edt_1.text()
        self.db_cursor = self.db_con.cursor()
        sql_query      = """ SELECT Full_Name, Email, Username, Password, Number_Phone FROM clients WHERE Username='%s' """%self.client_username
        self.client    = self.db_cursor.execute(sql_query)
        if self.client != 0:
            self.client_data = self.db_cursor.fetchone()
            full_name  = self.client_data[0]
            first_name = full_name.split('  ')[0]
            last_name  = full_name.split('  ')[1]
            email      = self.client_data[1]
            username   = self.client_data[2]
            password   = self.client_data[3]
            num_phone  = self.client_data[4]
            self.edt_2.setText(first_name)
            self.edt_3.setText(last_name)
            self.edt_4.setText(email)
            self.edt_5.setText(username)
            self.edt_6.setText(password)
            self.edt_7.setText(num_phone)
        else:
            QMessageBox.warning(self, 'Client not Exist:)', 'Sorry, client isn\'t exist, please try another client')

# Update Client Data Method
    def do_Update(self):
        old_username  = self.client_username
        new_firstname = self.edt_2.text()
        new_lastname  = self.edt_3.text()
        new_fullname  = new_firstname + "  " + new_lastname
        new_email     = self.edt_4.text()
        new_username  = self.edt_5.text()
        new_password  = self.edt_6.text()
        new_numphone  = self.edt_7.text()
        sql_query     = """ UPDATE clients SET Full_Name = '%s', Email = '%s', Username = '%s', Password = '%s', 
                            Number_Phone = '%s' WHERE Username = '%s' """%(new_fullname, new_email, new_username,
                                                                           new_password, new_numphone, old_username)
        self.db_cursor.execute(sql_query)
        self.db_con.commit()
        self.db_cursor.close()
        self.close()
        

# Delete Client Dialog - Delete Client Action in tool bar.
class Delete_Client(QDialog):
    def __init__(self, db_connect):
        super(Delete_Client, self).__init__()
        self.db_con = db_connect
        self.Grid   = QGridLayout()
        self.lbl_1  = QLabel(self)
        self.edt_1  = QLineEdit(self)
        self.btn_1  = QPushButton(self)
        self.title  = "Delete Client"
        self.width  = 340
        self.height = 140
        self.Delete_UI()

# Delete Client Interface Method
    def Delete_UI(self):
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setWindowTitle(self.title)
        self.setContentsMargins(20, 0, 20, 0)
        self.lbl_1.setText('Client')
        self.edt_1.setPlaceholderText('Username')
        self.btn_1.setText('Delete')
        self.Grid.addWidget(self.lbl_1, 0, 0)
        self.Grid.addWidget(self.edt_1, 0, 1, 1, 2)
        self.Grid.addWidget(self.btn_1, 1, 0, 1, 3)
        self.setLayout(self.Grid)
        self.btn_1.clicked.connect(lambda x : self.do_Delete(self.edt_1.text()))

# Delete Client Method
    def do_Delete(self, client):
        username    = client
        sql_query   = """ DELETE FROM clients WHERE Username = '%s' """%username
        self.db_cur = self.db_con.cursor()
        del_clients = self.db_cur.execute(sql_query)
        if del_clients == 0:
            text_message = "Sorry, username '%s' not found in table "%username
            QMessageBox.warning(self, 'User Not Found', text_message)
        else:
            self.db_con.commit()
            self.db_cur.close()
            self.close()


# Add Product Dialog - Add Product Action in toolbar
class Add_Product(QDialog):
    pass


# Update Product Dialog - Update Product Action in toolbar
class Update_Product(QDialog):
    pass


# Delete Product Dialog - Delete Product Action in toolbar
class Delete_Product(QDialog):
    pass


# AboutApp Dialog - AboutApp Action in toolbar.
class About_App(QDialog):
    def __init__(self):
        super(About_App, self).__init__()
        self.Grid    = QGridLayout()
        self.lbl_1   = QLabel(self)
        self.lbl_2   = QLabel(self)
        self.lbl_3   = QLabel(self)
        self.lbl_4   = QLabel(self)
        self.lbl_5   = QLabel(self)
        self.lbl_6   = QLabel(self)
        self.lbl_7   = QLabel(self)
        self.lbl_8   = QLabel(self)
        self.lbl_9   = QLabel(self)
        self.img_1   = QPixmap('Resources/spyder_ide.png')
        self.img_2   = QPixmap('Resources/python.png')
        self.img_3   = QPixmap('Resources/Qt.png')
        self.img_4   = QPixmap('Resources/8icons.png')
        self.img_5   = QPixmap('Resources/xampp.png')
        self.img_6   = QPixmap('Resources/mysql.png')
        self.logo    = QPixmap('Resources/sm_logo.png')
        self.app_txt = """SalesManager Application has created for organize exporter jobs.\nCreated at 12 May 2020.\nDeveloped by : Tarek Ghajary """ 
        self.width   = 600
        self.height  = 420
        self.title   = "About Application"
        self.init_UI()

# AboutApp Interface Method
    def init_UI(self):
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setContentsMargins(0, 20, 0, 20)
        self.setWindowTitle(self.title)
        self.lbl_2.setText(self.app_txt)
        self.lbl_3.setText("Built by :")
        self.lbl_1.setPixmap(self.logo)
        self.lbl_4.setPixmap(self.img_1)
        self.lbl_5.setPixmap(self.img_2)
        self.lbl_6.setPixmap(self.img_3)
        self.lbl_7.setPixmap(self.img_4)
        self.lbl_8.setPixmap(self.img_5)
        self.lbl_9.setPixmap(self.img_6)
        self.Grid.addWidget(self.lbl_1, 0, 0, 1, 10)
        self.Grid.addWidget(self.lbl_2, 1, 2, 1, 6)
        self.Grid.addWidget(self.lbl_3, 2, 2)
        self.Grid.addWidget(self.lbl_4, 3, 2)
        self.Grid.addWidget(self.lbl_5, 3, 3)
        self.Grid.addWidget(self.lbl_6, 3, 4)
        self.Grid.addWidget(self.lbl_7, 3, 5)
        self.Grid.addWidget(self.lbl_8, 3, 6)
        self.Grid.addWidget(self.lbl_9, 3, 7)
        self.setLayout(self.Grid)


# DeveloperInfo Dialod - DeveloperInfo Action in toolbar
class Developer_Info(QDialog):
    def __init__(self):
        super(Developer_Info, self).__init__()
        self.Grid    = QGridLayout()
        self.lbl_bio = QLabel(self)
        self.lbl_1   = QLabel(self)
        self.lbl_2   = QLabel(self)
        self.lbl_3   = QLabel(self)
        self.lbl_4   = QLabel(self)
        self.lbl_5   = QLabel(self)
        self.lbl_6   = QLabel(self)
        self.lbl_7   = QLabel(self)
        self.lbl_8   = QLabel(self)
        self.lbl_9   = QLabel(self)
        self.lbl_10  = QLabel(self)
        self.lbl_11  = QLabel(self)
        self.lbl_12  = QLabel(self)
        self.lbl_13  = QLabel(self)
        self.lbl_14  = QLabel(self)
        self.lbl_15  = QLabel(self)
        self.lbl_16  = QLabel(self)
        self.lbl_17  = QLabel(self)
        self.lbl_18  = QLabel(self)
        self.img_1   = QPixmap('Resources/facebook.png')
        self.img_2   = QPixmap('Resources/twitter.png')
        self.img_3   = QPixmap('Resources/linkedin.png')
        self.img_4   = QPixmap('Resources/telegram.png')
        self.img_5   = QPixmap('Resources/github.png')
        self.img_6   = QPixmap('Resources/kaggle.png')
        self.img_7   = QPixmap('Resources/codepen.png')
        self.img_8   = QPixmap('Resources/youtube.png')
        self.img_9   = QPixmap('Resources/gmail.png')
        self.bio     = "Tarek Ghajary \nSyria, Tartous.\nStudent in Economic Faculty.\nTartous University - Syria."
        self.fb_link = "<a href='https://www.facebook.com/T94GH09' style='text-decoration:none;color:black;font-size:15px;'>Tarek GH</a>"
        self.tw_link = "<a href='https://twitter.com/tarekgh15' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.in_link = "<a href='https://www.linkedin.com/in/tarek-ghajary-95ab0b195/' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.tg_link = "<a href='https://t.me/TarekGhajary' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.gh_link = "<a href='https://www.github.com/CHESyrian' style='text-decoration:none;color:black;font-size:15px;'>CHESyrian</a>"
        self.kg_link = "<a href='https://www.kaggle.com/tarekghajary' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.cp_link = "<a href='https://codepen.io/TarekGhajary' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.yt_link = "<a href='https://www.youtube.com/channel/UCYE58lu16Kdartsc_UE0raQ' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.gm_link = "<a href='mailto:tarek940gh@gmail.com' style='text-decoration:none;color:black;font-size:15px;'>Tarek Ghajary</a>"
        self.links   = [self.lbl_10, self.lbl_11, self.lbl_12, self.lbl_13, self.lbl_14, self.lbl_15,
                        self.lbl_16, self.lbl_17, self.lbl_18]
        self.width   = 280
        self.height  = 620
        self.win_ico = "Resources/sm_logo_icon.ico"
        self.title   = "Developer Informations"
        self.init_UI()

# Developer Informations Interface
    def init_UI(self):
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setContentsMargins(50, 10, 50, 10)
        self.setWindowTitle(self.title)
        self.lbl_bio.setStyleSheet('font-size:13px;')
        self.lbl_bio.setText(self.bio)
        self.lbl_1.setPixmap(self.img_1)
        self.lbl_2.setPixmap(self.img_2)
        self.lbl_3.setPixmap(self.img_3)
        self.lbl_4.setPixmap(self.img_4)
        self.lbl_5.setPixmap(self.img_5)
        self.lbl_6.setPixmap(self.img_6)
        self.lbl_7.setPixmap(self.img_7)
        self.lbl_8.setPixmap(self.img_8)
        self.lbl_9.setPixmap(self.img_9)
        self.lbl_10.setText(self.fb_link)
        self.lbl_11.setText(self.tw_link)
        self.lbl_12.setText(self.in_link)
        self.lbl_13.setText(self.tg_link)
        self.lbl_14.setText(self.gh_link)
        self.lbl_15.setText(self.kg_link)
        self.lbl_16.setText(self.cp_link)
        self.lbl_17.setText(self.yt_link)
        self.lbl_18.setText(self.gm_link)
        self.Grid.addWidget(self.lbl_bio, 0, 0, 1, 2)
        self.Grid.addWidget(self.lbl_1, 1, 0)
        self.Grid.addWidget(self.lbl_2, 2, 0)
        self.Grid.addWidget(self.lbl_3, 3, 0)
        self.Grid.addWidget(self.lbl_4, 4, 0)
        self.Grid.addWidget(self.lbl_5, 5, 0)
        self.Grid.addWidget(self.lbl_6, 6, 0)
        self.Grid.addWidget(self.lbl_7, 7, 0)
        self.Grid.addWidget(self.lbl_8, 8, 0)
        self.Grid.addWidget(self.lbl_9, 9, 0)
        self.Grid.addWidget(self.lbl_10, 1, 1)
        self.Grid.addWidget(self.lbl_11, 2, 1)
        self.Grid.addWidget(self.lbl_12, 3, 1)
        self.Grid.addWidget(self.lbl_13, 4, 1)
        self.Grid.addWidget(self.lbl_14, 5, 1)
        self.Grid.addWidget(self.lbl_15, 6, 1)
        self.Grid.addWidget(self.lbl_16, 7, 1)
        self.Grid.addWidget(self.lbl_17, 8, 1)
        self.Grid.addWidget(self.lbl_18, 9, 1)
        self.setLayout(self.Grid)
        for link in self.links:
            link.setOpenExternalLinks(True)


# Login UI Dialog run after Main UI 
class Login_UI(QDialog):
    def __init__(self):
        super(Login_UI, self).__init__()
        self.usr_class   = QComboBox(self)
        self.log_usr_lbl = QLabel(self)
        self.log_pwd_lbl = QLabel(self)
        self.log_usr_edt = QLineEdit(self)
        self.log_pwd_edt = QLineEdit(self)
        self.logging_btn = QPushButton(self)
        self.Grid_2      = QGridLayout(self)
        self.init_UI()
#Login Interface Method
    def init_UI(self):
        self.setGeometry(320, 120, 720, 480)
        self.usr_class.addItem('Exporter')
        self.usr_class.addItem('Importer')
        self.logging_btn.setText('Log In')
        self.log_usr_lbl.setText('username')
        self.log_pwd_lbl.setText('password')
        self.log_usr_edt.setPlaceholderText('(username or email)')
        self.log_pwd_edt.setEchoMode(QLineEdit.Password)
        self.Grid_2.setContentsMargins(250, 150, 250, 150)
        self.Grid_2.addWidget(self.usr_class, 0, 0, 1, 2)
        self.Grid_2.addWidget(self.log_usr_lbl, 1, 0)
        self.Grid_2.addWidget(self.log_usr_edt, 1, 1)
        self.Grid_2.addWidget(self.log_pwd_lbl, 2, 0)
        self.Grid_2.addWidget(self.log_pwd_edt, 2, 1)
        self.Grid_2.addWidget(self.logging_btn, 3, 0, 1, 2)
        self.logging_btn.clicked.connect(self.SelectLoginClass)
        self.exec_()
# Select Login Class Method based on User Class
    def SelectLoginClass(self):
        self.usrClass = self.usr_class.itemText(self.usr_class.currentIndex())
        self.login_info = {'username': self.log_usr_edt.text(), 
                           'password': self.log_pwd_edt.text(),
                           'Class'   : self.usrClass,
                           'DBName'  : ''}
        if self.usrClass == "Importer":
            self.Login_Imp(self.login_info)
        elif self.usrClass == "Exporter":
            self.Login_Exp(self.login_info)
        else: print('Error')
        
# Login as Importer Method
    def Login_Imp(self, infos):
        pass

# Login as Exporter Method
    def Login_Exp(self, infos):
        username = infos['username']
        password = infos['password']
        db_connect  = SQL.connect('localhost', 'root', '', 'salesmanager_clients')
        db_cursor   = db_connect.cursor()
        sql_query_1 = """SELECT * FROM exporter_clients WHERE Username='%s'"""%username
        user_data   = db_cursor.execute(sql_query_1)
        if user_data != 0:
            user_auth     = db_cursor.fetchone()
            database_name = user_auth[6]
            if username == user_auth[2] and password == user_auth[3]:
                with open('Data/Auth_INFO.txt', 'w') as file:
                    text = {'username':username, 'password':password, 'Class':'Exporter', 'DBName':database_name}
                    file.write(str(text))
                    file.close()
                    self.login_info = text
                db_cursor.close()
                db_connect.close()
                self.accept()
        else:
            QMessageBox.warning(self, 'User Not Exist:)', 'User isn\'t exist, please enter your username' )

# Method return Client Informations
    def clientInfo(self):
        return self.login_info


# Cipher Algorithm.
class CHECipher():
    def __init__(self):
        self.plane_1 = "NOPQRSTUVWXYZABCDEFGHIJKLM"
        self.plane_2 = "abcdefghijklmnopqrstuvwxyz"
        self.plane_3 = " .:;!$@?&,"
        self.plane_4 = "0123456789"
        self.steps   = "9AVwWdue1DmplLc6NP5SXqQrRYzFgaUv8yZG2hM4siIkKoOxtTbBHCEfnjJ3"
        
# Encodec Method
    def Encodec(self, text='', step=0, step_plus=0):
        text_after_encodec = []
        cipher    = []
        for letter in text:
            if letter in self.plane_1:
                letter = self.plane_2[self.plane_1.index(letter)]
                text_after_encodec.append(letter)
            elif letter in self.plane_2:
                letter = self.plane_1[self.plane_2.index(letter)]
                text_after_encodec.append(letter)
            elif letter in self.plane_3:
                letter = self.plane_4[self.plane_3.index(letter)]
                text_after_encodec.append(letter)
            elif letter in self.plane_4:
                letter = self.plane_3[self.plane_4.index(letter)]
                text_after_encodec.append(letter)
            else:
                letter = letter
                text_after_encodec.append(letter)
        for i in text_after_encodec:
            for j in range(step):
                s = choice(self.steps)
                cipher.append(s)
            step += step_plus
            cipher.append(i)
        cipher_text = "".join(cipher)
        return cipher_text
        
# Decodec Method
    def Decodec(self, text='', step=0, step_plus=0):
        text_after_decodec = []
        while step in range(len(text)):
            letter = text[step]
            if letter in self.plane_2:
                letter = self.plane_1[self.plane_2.index(letter)]
                text_after_decodec.append(letter)
            elif letter in self.plane_1:
                letter = self.plane_2[self.plane_1.index(letter)]
                text_after_decodec.append(letter)
            elif letter in self.plane_3:
                letter = self.plane_4[self.plane_3.index(letter)]
                text_after_decodec.append(letter)
            elif letter in self.plane_4:
                letter = self.plane_3[self.plane_4.index(letter)]
                text_after_decodec.append(letter)
            else:
                letter = letter
                text_after_decodec.append(letter)
            text = text[step+1:]
            step += step_plus
        origin_text = "".join(text_after_decodec)
        return origin_text


# Cheking on Authentication Method
def is_authenticated():
    auth_file  = 'Auth_INFO.txt'
    list_files = os.listdir('Data/')
    if auth_file in list_files:
        with open('Data/Auth_INFO.txt', 'r') as file:
            INFO     = eval(file.read())
            username = INFO['username']
            password = INFO['password']
            Class    = INFO['Class']
            if Class == 'Exporter':
                db_conn    = SQL.connect('localhost', 'root', '', 'salesmanager_clients')
                db_curs    = db_conn.cursor()
                sql_query1 = """SELECT Username FROM exporter_clients WHERE Username='%s'"""%username
                check_username = db_curs.execute(sql_query1)
                if check_username != 0:
                    sql_query2 = """SELECT * FROM exporter_clients WHERE Username='%s'"""%username
                    db_curs.execute(sql_query2)
                    user_auth = db_curs.fetchone()
                    if username == user_auth[2] and password == user_auth[3]:
                        db_curs.close()
                        db_conn.close()
                        return (True, INFO)
    else:
        return False



if __name__ == "__main__":
    App = QApplication(argv)
    check = is_authenticated()
    if check:
        auth_info = check[1]
        main_ui = Main_UI(auth_info)
    else:
        login      = Login_UI()
        auth_info  = login.clientInfo()
        if login.exec_() == QDialog.Accepted:
            main_ui = Main_UI(auth_info)
    exit(App.exec_())