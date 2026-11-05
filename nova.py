from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mysql.connector
import hashlib
import math
from cryptography.fernet import Fernet

mainframe_db=mysql.connector.connect( #database that stores all accounts created
    user='root',
    host='localhost',
    password='xxx',
    database="passwordmanager",
    port=3306,
    use_pure=True
)
mainframe_cursor=mainframe_db.cursor()


repo_db=mysql.connector.connect( #password repository for all accounts
    user='root',
    host='localhost',
    password='xxx',
    database="passwordrepo",
    port=3306,
    use_pure=True
)
repo_cursor=repo_db.cursor()

app=QApplication([])
win=QWidget()
sgn=QWidget()
lgn=QWidget()
hel=QWidget()
inf=QWidget()
inter=QWidget()
delall=QWidget()
delspec=QWidget()
upd=QWidget()
ins=QWidget()
retrspec=QWidget()
retrall=QWidget()
delacc=QWidget()

stack=QStackedWidget()
stack.addWidget(win) #win at pos 0
stack.addWidget(sgn) #sgn at pos 1
stack.addWidget(lgn) #lgn at pos 2
stack.addWidget(hel) #help at pos 3
stack.addWidget(inf) #info at pos 4
stack.addWidget(inter) #inter at pos 5
stack.addWidget(delall) #delall at pos 6
stack.addWidget(delspec) #delspec at pos 7
stack.addWidget(upd) #upd at pos 8
stack.addWidget(ins) #ins at pos 9
stack.addWidget(retrspec) #retrspec at pos 10
stack.addWidget(retrall) #retrall at pos 11
stack.addWidget(delacc) #delacc at pos 12

#global variables:
sessionname=""

app.setStyleSheet("""
    QWidget {
        background-color:#222;
        margin-top:10px;
    }
    #wlclbl {
        color:white;
        font-size: 40px;
        font-family:;
    }
    #winbut {
        background-color: white;
        border-radius: 5px;
        border-style:solid;
        border-width: 3px;
        height: 40px;
        width: 110px;
        font-size: 20px;
        border-color:#52d1ff;
    }
    #psmng {
        color:white;
        font-size:20px;
        font-family:consolas;
        margin-top: 30px;
    }
    #sep {
        color:#52d1ff;
        margin-bottom: 0px;
    }
    #sgn_name {
        height:60px;
        width:350px;
        border-style:solid;
        border-color:white;
        border-width:3px;
        border-radius:20px;
        color:#52d1ff;
        font-size:20px;
        padding:7px;
    }
    #sgn_but {
        background-color:white;
        border-style:solid;
        border-radius:5px;
        border-width: 3px;
        height: 40px;
        width: 110px;
        font-size: 20px;
        border-color:#52d1ff;
    }
    #sgn_but:hover {
        background-color:#52d1ff;
    }
    #sgn_but:pressed {
        background-color:#54ecc4;
    }
    #sgn_nameerr {
        color:red;
        font-size:15px;
        width: 1000px;
    }
    #helplbl {
        color: white;
        font-size:18px;
        margin-top: 35px;
        margin-left:20px;
        margin-right: 20px;
        width: 10px;
    }
    #infomessage {
        color: white;
        border-color: #52d1ff;
        border-style:solid;
        font-size:18px;
    }
    #infomessage QScrollBar:vertical {
        background-color:red;
    }
    #inter_but {
        background-color:white;
        border-style:solid;
        border-radius:5px;
        border-width: 3px;
        height: 40px;
        width: 220px;
        font-size: 20px;
        border-color:#52d1ff;
    }
    #inter_but:hover {
        background-color:#52d1ff;
    }
    #inter_but:pressed {
        background-color:#54ecc4;
    }
    #delallwarn {
        color: white;
        font-size:24px;
        margin-top: 35px;
        margin-left:20px;
        margin-right: 20px;
        width: 10px;
    }
    #delall_but {
        background-color:white;
        border-style:solid;
        border-radius:5px;
        border-width: 3px;
        height: 40px;
        width: 110px;
        font-size: 20px;
        border-color:red;
    }
    #delall_but:hover {
        background-color:#f79c9c;
    }
    #delall_but:pressed {
        background-color:#fc4444;
    }
    #ins_name {
        height:40px;
        width:350px;
        border-style:solid;
        border-color:white;
        border-width:3px;
        border-radius:20px;
        color:#52d1ff;
        font-size:20px;
        padding:7px;
    }
    #psmng_red {
        color:red;
        font-size:20px;
        font-family:consolas;
        margin-top: 30px;
    }
""")

stack.setFixedSize(500, 500)
icon=QIcon("NOVA.png")
stack.setWindowIcon(icon)

#controller functions:
def win_signin(): #transfers from win to signin
    stack.setCurrentIndex(1)
    stack.setWindowTitle("Sign Up")

def win_login(): #transfers from win to login
    stack.setCurrentIndex(2)
    stack.setWindowTitle("Log In")

def win_help(): #transfers from win to help
    stack.setCurrentIndex(3)
    stack.setWindowTitle("Help")

def win_info(): #transfers from win to info
    stack.setCurrentIndex(4)
    stack.setWindowTitle("Information")

def sgn_win(): #transfers from sgn to win, and clears input fields and error messages
    sgnname.clear()
    sgnpassword.clear()
    sgnnameerr.setText("")
    sgnpassworderr.setText("")
    stack.setCurrentIndex(0)
    stack.setWindowTitle("Password Manager")

def hel_win():
    stack.setCurrentIndex(0)
    stack.setWindowTitle("Password Manager")

def info_win():
    stack.setCurrentIndex(0)
    stack.setWindowTitle("Password Manager")

def sgn_createacc(): #verifies if details entered pass all restrictions and only then transfers from sgn to inter
    sgnnameerr.setText("")
    sgnpassworderr.setText("")
    global sessionname
    
    tname=sgnname.text()
    password=sgnpassword.text()
    tpassword=hashlib.sha256(password.encode()).hexdigest()
    validcreds=True
    
    mainframe_cursor.execute("SELECT * FROM Accounts;") #checks if the details entered have a copy in the database
    result=mainframe_cursor.fetchall()
    for i in result:
        if tname==i[0]:
            validcreds=False
            sgnnameerr.setText("Account with the same name already exists.")
        if tpassword==i[1]:
            validcreds=False
            sgnpassworderr.setText("Please use another password.")

    for i in tname: #checks if the name entered consists of alphabets and whitespaces only
        if i.isalpha()==False:
            if i!=" ":
                validcreds=False
                sgnnameerr.setText("Name must only consist of alphabets and whitespaces.")
        
    if len(password)<10: #checks if length of password is atleast 10
        validcreds=False
        sgnpassworderr.setText("Password must be atleast 10 characters long.")

    if len(tname)<3:
        validcreds=False
        sgnnameerr.setText("Name must be atleast 3 characters long.")

    if validcreds:
        enckey=Fernet.generate_key()
        values=(tname,tpassword,enckey)
        query="INSERT INTO Accounts VALUES (%s, %s, %s);"
        mainframe_cursor.execute(query, values)
        mainframe_db.commit()
        stack.setCurrentIndex(5)
        stack.setWindowTitle("Main Interface")
        sessionname=tname

        query2=f"CREATE TABLE `{sessionname}` (name VARCHAR(800), label VARCHAR(800), password VARCHAR(800));"
        repo_cursor.execute(query2)
        repo_db.commit()
        
        interwlc.setText("Welcome, "+sessionname)
        interwlc.adjustSize()
        interwlc.move((500-interwlc.width())//2,160)

def lgn_win():
    lgnname.clear()
    lgnpassword.clear()
    lgnnameerr.setText("")
    lgnpassworderr.setText("")
    stack.setCurrentIndex(0)
    stack.setWindowTitle("Password Manager")

def lgn_verifyacc():
    lgnpassworderr.setText("")
    lgnnameerr.setText("")
    tname=lgnname.text()
    global sessionname
    password=lgnpassword.text()
    tpassword=hashlib.sha256(password.encode()).hexdigest()
    ufound=False
    pmatch=False
    query="SELECT * FROM Accounts;"
    mainframe_cursor.execute(query)
    result=mainframe_cursor.fetchall()
    for i in result:
        retruser=i[0]
        retrpass=i[1]
        if tname==retruser:
            ufound=True
            if tpassword==retrpass:
                pmatch=True
    if ufound==False:
        lgnnameerr.setText("Account not found.")
    else:
        if pmatch:
            stack.setCurrentIndex(5)
            stack.setWindowTitle("Interface")
            sessionname=tname
            interwlc.setText("Welcome, "+sessionname)
            interwlc.adjustSize()
            interwlc.move((500-interwlc.width())//2,160)
            
        else:
            lgnpassworderr.setText("Password does not match.")

def inter_delall():
    stack.setCurrentIndex(6)
    stack.setWindowTitle("Delete All")

def inter_delspec():
    stack.setCurrentIndex(7)
    stack.setWindowTitle("Delete Specific")

def inter_upd():
    stack.setCurrentIndex(8)
    stack.setWindowTitle("Update via Label")

def inter_ins():
    stack.setCurrentIndex(9)
    stack.setWindowTitle("Add New")

def inter_retrspec():
    stack.setCurrentIndex(10)
    stack.setWindowTitle("Retrieve via Label")

def inter_retrall():
    stack.setCurrentIndex(11)
    stack.setWindowTitle("Retrieve All")
    global sessionname
    query3="SELECT * FROM accounts WHERE name=%s;"
    mainframe_cursor.execute(query3,(sessionname,))
    hjt=mainframe_cursor.fetchall()
    key=hjt[0][2]
    query=f"SELECT * FROM `{sessionname}`;"
    mnstr=""
    repo_cursor.execute(query)
    rtq=repo_cursor.fetchall()
    if rtq:
        for i in range(0,len(rtq)):
            for j in range(0, 3):
                if j==0 and i==0:
                    tstr=mnstr
                    newstr=f"Username: {rtq[i][j]}"
                    mnstr=f"{tstr}{newstr}"
                elif j==0:
                    tstr=mnstr
                    newstr=f"\n\nUsername: {rtq[i][j]}"
                    mnstr=f"{tstr}{newstr}"
                elif j==1:
                    tstr=mnstr
                    newstr=f"\nLabel: {rtq[i][j]}"
                    mnstr=f"{tstr}{newstr}"
                elif j==2:
                    cipher=Fernet(key)
                    tdec=cipher.decrypt(rtq[i][j])
                    dec=tdec.decode()
                    tstr=mnstr
                    newstr=f"\nPassword: {dec}"
                    mnstr=f"{tstr}{newstr}"
            ttstr=mnstr
            tnewstr=f"\n"
            mnstr=f"{ttstr}{tnewstr}"
        retrallmess.setText(f"{mnstr}")
    else:
        retrallmess.setText("No data found.")

def inter_delacc():
    stack.setCurrentIndex(12)
    stack.setWindowTitle("Delete Account")

def delall_inter():
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")
    
def ins_inter():
    inslabel.clear()
    insusername.clear()
    inspassword.clear()
    inserr.setText("                                                                                    ")
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")

def retrall_inter():
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")
    
def retrspec_inter():
    retrspecoplabel.setObjectName("psmng")
    retrspecoplabel.style().unpolish(retrspecoplabel)
    retrspecoplabel.style().polish(retrspecoplabel)
    retrspecoplabel.update()
    retrspecoplabel.setText("")
    retrspecoplabel.move(170,220)
    retrspecnamelbl.setText(f"")
    retrspecpasslbl.setText(f"")
    retrspeclbllbl.setText(f"")
    retrspeclabel.clear()
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")

def delallproceed():
    global sessionname
    query2=f"TRUNCATE TABLE `{sessionname}`;"
    repo_cursor.execute(query2)
    repo_db.commit()
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")

def delspec_inter():
    delspecerr.setText("")
    delspeclabel.clear()
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")

def delspecproceed():
    global sessionname
    rtext=delspeclabel.text()
    value=rtext
    query=f"SELECT * FROM `{sessionname}` WHERE label=%s;"
    repo_cursor.execute(query,(value,))
    tres=repo_cursor.fetchall()
    if tres:
        query2=f"DELETE FROM `{sessionname}` WHERE label=%s;"
        repo_cursor.execute(query2,(value,))
        repo_db.commit()
        stack.setCurrentIndex(5)
        stack.setWindowTitle("Interface")
    else:
        delspecerr.setText("Label not found.")

def insert():
    username=insusername.text()
    label=inslabel.text()
    password=inspassword.text()
    global sessionname
    value=label
    queryfsd=f"SELECT * FROM `{sessionname}` WHERE label=%s;"
    repo_cursor.execute(queryfsd,(value,))
    fg=repo_cursor.fetchall()
    if fg:
        inserr.setText("Label already exists. Try another label.")
    else:
        query3="SELECT * FROM accounts WHERE name=%s;"
        mainframe_cursor.execute(query3,(sessionname,))
        hjt=mainframe_cursor.fetchall()
        key=hjt[0][2]
        cipher=Fernet(key)
        enc=cipher.encrypt(password.encode())
        query2=f"INSERT INTO `{sessionname}` VALUES(%s, %s, %s);"
        vlg=(username, label, enc)
        repo_cursor.execute(query2, vlg)
        repo_db.commit()
        inslabel.clear()
        insusername.clear()
        inspassword.clear()
        inserr.setText("")
        stack.setCurrentIndex(5)
        stack.setWindowTitle("Interface")
    
def retrievespecific():
    retrspecoplabel.setObjectName("psmng")
    retrspecoplabel.style().unpolish(retrspecoplabel)
    retrspecoplabel.style().polish(retrspecoplabel)
    retrspecoplabel.update()
    retrspecoplabel.move(170,220)
    retrspecnamelbl.setText(f"")
    retrspecpasslbl.setText(f"")
    retrspeclbllbl.setText(f"")
    global sessionname
    query3="SELECT * FROM accounts WHERE name=%s"
    mainframe_cursor.execute(query3,(sessionname,))
    hjt=mainframe_cursor.fetchall()
    key=hjt[0][2]
    vl=retrspeclabel.text()
    query4=f"SELECT * FROM `{sessionname}` WHERE label=%s"
    repo_cursor.execute(query4, (vl,))
    fgo=repo_cursor.fetchall()
    if fgo:
        rname=fgo[0][0]
        rlabel=fgo[0][1]
        rpass=fgo[0][2]
        cipher=Fernet(key)
        tdec=cipher.decrypt(rpass)
        dec=tdec.decode()
        retrspecoplabel.setText("RETRIEVED DATA")
        retrspecnamelbl.setText(f"Username: {rname}")
        retrspecpasslbl.setText(f"Password: {dec}")
        retrspeclbllbl.setText(f"Label: {rlabel}")
    else:
        retrspecoplabel.setObjectName("psmng_red")
        retrspecoplabel.style().unpolish(retrspecoplabel)
        retrspecoplabel.style().polish(retrspecoplabel)
        retrspecoplabel.update()
        retrspecoplabel.move(130,220)
        retrspecoplabel.setText("Label does not exist.")

def delacc_inter():
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")

def deleteaccount():
    global sessionname
    query=f"DROP TABLE `{sessionname}`;"
    repo_cursor.execute(query)
    repo_db.commit()

    print("repo all ok")

    query2="DELETE FROM accounts WHERE name=%s;"
    vrl=sessionname
    mainframe_cursor.execute(query2, (vrl,))
    mainframe_db.commit()

    print("main all ok")

    sessionname=""
    stack.setCurrentIndex(0)
    stack.setWindowTitle("Nova Password Manager")

def upd_inter():
    upderr.setText("")
    updusername.clear()
    updlabel.clear()
    updpassword.clear()
    stack.setCurrentIndex(5)
    stack.setWindowTitle("Interface")

def updatespecific():
    klabel=updlabel.text()
    global sessionname
    query=f"SELECT * FROM `{sessionname}` WHERE label=%s;"
    repo_cursor.execute(query, (klabel,))

    print("label check ok")
    
    gty=repo_cursor.fetchall()
    if gty:
        kusername=updusername.text()
        kpassword=updpassword.text()
        query3="SELECT * FROM accounts WHERE name=%s;"
        mainframe_cursor.execute(query3,(sessionname,))

        print("key fetch ok")
        
        hjt=mainframe_cursor.fetchall()
        key=hjt[0][2]
        cipher=Fernet(key)
        enc=cipher.encrypt(kpassword.encode())
        query2=f"UPDATE `{sessionname}` SET name=%s, password=%s WHERE label=%s;"
        v2=(kusername, enc, klabel)
        print(v2)
        repo_cursor.execute(query2, v2)
        repo_db.commit()
        print("query charge ok")
    else:
        upderr.setText("Label not found.")
    

# win widgets:
lbl=QLabel("",win)
logo=QPixmap("NOVA.png")
logo=logo.scaled(150, 150)
lbl.setPixmap(logo) #win logo

psmng=QLabel("P A S S W O R D   M A N A G E R", win)
psmng.setObjectName("psmng")

sep=QLabel("__________________________________________________________",win)
sep.setObjectName("sep")

wlclbl=QLabel("Welcome, user", win)
wlclbl.setObjectName("wlclbl")

signin=QPushButton("Sign-up",win)
login=QPushButton("Log-in",win)
info=QPushButton("Info",win)
helpp=QPushButton("Help",win)
signin.setObjectName("winbut")
login.setObjectName("winbut")
info.setObjectName("winbut")
helpp.setObjectName("winbut")
signin.clicked.connect(win_signin)
login.clicked.connect(win_login)
info.clicked.connect(win_info)
helpp.clicked.connect(win_help) #buttons, and their connections


inst=QPixmap("INSTALOGO.png")
inst=inst.scaled(30,30)
insta=QLabel("",win)
insta.setPixmap(inst)

fac=QPixmap("FACEBOOKLOGO.png")
facebook=QLabel("",win)
fac=fac.scaled(30,30)
facebook.setPixmap(fac)

git=QPixmap("GITHUBLOGO.png")
git=git.scaled(30,30)
github=QLabel("",win)
github.setPixmap(git)

you=QPixmap("YOUTUBELOGO.png")
you=you.scaled(40,30)
youtube=QLabel("",win)
youtube.setPixmap(you)

#win placements:
lbl.move(180, 1)
psmng.move(80, 150)
sep.move(50, 200)
wlclbl.move(115, 230)
signin.move(135, 300)
info.move(265, 300)
login.move(135, 360)
helpp.move(265, 360)
insta.move(10, 440)
facebook.move(50, 440)
github.move(90, 440)
youtube.move(130, 440)




#sgn widgets:
sgnlogo=QLabel(sgn)
actlogo=QPixmap("NOVA.png")
actlogo=actlogo.scaled(80,80)
sgnlogo.setPixmap(actlogo)

sgndsp=QLabel("S I G N   U P",sgn)
sgndsp.setObjectName("psmng")

sgnsep=QLabel("__________________________________________________________",sgn)
sgnsep.setObjectName("sep")

sgnname=QLineEdit(sgn)
sgnname.setPlaceholderText("                       N A M E")
sgnname.setObjectName("sgn_name")

sgnnameerr=QLabel("                                                                                          ",sgn)
sgnnameerr.setObjectName("sgn_nameerr")

sgnpassword=QLineEdit(sgn)
sgnpassword.setPlaceholderText("                P A S S W O R D")
sgnpassword.setObjectName("sgn_name")

sgnpassworderr=QLabel("                                                                                    ",sgn)
sgnpassworderr.setObjectName("sgn_nameerr")

sgnback=QPushButton("Back",sgn)
sgnback.setObjectName("sgn_but")
sgnback.clicked.connect(sgn_win)

sgnproc=QPushButton("Proceed",sgn)
sgnproc.setObjectName("sgn_but")
sgnproc.clicked.connect(sgn_createacc)

#sgn placements:
sgnlogo.move(200,1)
sgndsp.move(170, 70)
sgnsep.move(45, 120)
sgnname.move(70,165)
sgnnameerr.move(85, 250)
sgnpassword.move(70,285)
sgnpassworderr.move(85, 370)
sgnback.move(45,410)
sgnproc.move(340,410)


#lgn widgets:
lgnlogo=QLabel(lgn)
actlogo2=QPixmap("NOVA.png")
actlogo2=actlogo2.scaled(80,80)
lgnlogo.setPixmap(actlogo2)

lgndsp=QLabel(" L O G   I N",lgn)
lgndsp.setObjectName("psmng")

lgnsep=QLabel("__________________________________________________________",lgn)
lgnsep.setObjectName("sep")

lgnname=QLineEdit(lgn)
lgnname.setPlaceholderText("                       N A M E")
lgnname.setObjectName("sgn_name")

lgnnameerr=QLabel("                                                                                          ",lgn)
lgnnameerr.setObjectName("sgn_nameerr")

lgnpassword=QLineEdit(lgn)
lgnpassword.setPlaceholderText("                P A S S W O R D")
lgnpassword.setObjectName("sgn_name")

lgnpassworderr=QLabel("                                                                                    ",lgn)
lgnpassworderr.setObjectName("sgn_nameerr")

lgnback=QPushButton("Back",lgn)
lgnback.setObjectName("sgn_but")
lgnback.clicked.connect(lgn_win)

lgnproc=QPushButton("Proceed",lgn)
lgnproc.setObjectName("sgn_but")
lgnproc.clicked.connect(lgn_verifyacc)

#lgn placements:
lgnlogo.move(200,1)
lgndsp.move(170, 70)
lgnsep.move(45, 120)
lgnname.move(70,165)
lgnnameerr.move(85, 250)
lgnpassword.move(70,285)
lgnpassworderr.move(85, 370)
lgnback.move(45,410)
lgnproc.move(340,410)


#inter widgets:
interlogo=QLabel(inter)
interpix=QPixmap("NOVA.png")
interpix=interpix.scaled(150, 150)
interlogo.setPixmap(interpix)

interwlc=QLabel("Welcome, "+sessionname,inter)
interwlc.setAlignment(Qt.AlignCenter)
interwlc.setObjectName("wlclbl")

interdelall=QPushButton("Delete All",inter)
interdelall.setObjectName("inter_but")
interdelall.clicked.connect(inter_delall)

interdelspec=QPushButton("Delete Specific", inter)
interdelspec.setObjectName("inter_but")
interdelspec.clicked.connect(inter_delspec)

interupd=QPushButton("Update Specific",inter)
interupd.setObjectName("inter_but")
interupd.clicked.connect(inter_upd)

interins=QPushButton("Insert New",inter)
interins.setObjectName("inter_but")
interins.clicked.connect(inter_ins)

interretrspec=QPushButton("Retrieve Specific",inter)
interretrspec.setObjectName("inter_but")
interretrspec.clicked.connect(inter_retrspec)

interretrall=QPushButton("Retrieve All",inter)
interretrall.setObjectName("inter_but")
interretrall.clicked.connect(inter_retrall)

interdelacc=QPushButton("Delete Account", inter)
interdelacc.setObjectName("inter_but")
interdelacc.clicked.connect(inter_delacc)

#inter placements:
interlogo.move(180,1)
interwlc.adjustSize()
interwlc.move((500-interwlc.width())//2,180)
interdelall.move(20,240)
interdelspec.move(255,240)
interupd.move(20,295)
interins.move(255,295)
interretrspec.move(20, 350)
interretrall.move(255,350)
interdelacc.move(130, 405)

#help widgets:
hellogo=QLabel(hel)
folklogo2=QPixmap("NOVA.png")
folklogo2=folklogo2.scaled(80,80)
hellogo.setPixmap(folklogo2)

helpfolklbl=QLabel("H E L P", hel)
helpfolklbl.setObjectName("psmng")

helpsep=QLabel("__________________________________________________________",hel)
helpsep.setObjectName("sep")

helplbl=QLabel("This application allows you to securely store, retrieve, update, and delete your passwords for various services in one place. Begin by creating an account or logging in with your existing credentials. After logging in, you'll be able to manage your saved passwords through the main interface. All available features can be accessed through the menu, allowing you to organize and maintain your password repository with ease.",hel)
helplbl.setWordWrap(True)
helplbl.setObjectName("helplbl")
helplbl.setFixedSize(500,300)
helplbl.setAlignment(Qt.AlignHCenter)

helpbutton=QPushButton("Back",hel)
helpbutton.setObjectName("sgn_but")
helpbutton.clicked.connect(hel_win)

#help placements:
hellogo.move(200,1)
helpfolklbl.move(200, 70)
helpsep.move(45, 120)
helplbl.move(1,130)
helpbutton.move(197,410)

#info widgets:
infologo=QLabel(inf)
sonlogo=QPixmap("NOVA.png")
sonlogo=sonlogo.scaled(80,80)
infologo.setPixmap(sonlogo)

infolable=QLabel("I N F O", inf)
infolable.setObjectName("psmng")

infosep=QLabel("__________________________________________________________",inf)
infosep.setObjectName("sep")
infomess=QTextEdit(inf)
infomess.setPlainText("Developer: Neil Shibu Cheruvathoor\n\nApplication: Offline Password Manager\n\nArchitecture: Client-Side Desktop Application\n\nProgramming Language: Python 3.14\n\nGUI Framework: PyQt5\n\nDatabase: MySQL 9.7\n\nDatabase Connector: mysql-connector-python 9.7.0\n\nAuthentication: SHA-256 Password Hashing\n\nEncryption: Fernet Symmetric Encryption\n\nDatabase Operations: CRUD (Create, Read, Update, Delete)\n\nCore Features: User Registration, Login, Password Storage, Password Retrieval, Password Updating, Password Deletion\n\nDevelopment Focus: Cybersecurity, Database Management, GUI Development, Encryption, Authentication, and Python-MySQL Integration\n\nProject Type: Offline Desktop Application\n\nPurpose: Secure local storage and management of user credentials.")
infomess.setReadOnly(True)
infomess.setObjectName("infomessage")
infomess.resize(400,200)

infobutton=QPushButton("Back",inf)
infobutton.setObjectName("sgn_but")
infobutton.clicked.connect(info_win)

#info placements
infologo.move(200,1)
infolable.move(200,70)
infosep.move(45,120)
infomess.move(54,165)
infobutton.move(197,410)

#dellall widgets:
delalllogo=QLabel(delall)
rlogo=QPixmap("NOVA.png")
rlogo=rlogo.scaled(70,70)
delalllogo.setPixmap(rlogo)

delallsep=QLabel("__________________________________________________________", delall)
delallsep.setObjectName("sep")

delallwarn=QLabel("Are you sure you'd like to erase your data? This is permanent and cannot be undone.",delall)
delallwarn.setObjectName("delallwarn")
delallwarn.setWordWrap(True)
delallwarn.setAlignment(Qt.AlignHCenter)

delallback=QPushButton("Back",delall)
delallback.setObjectName("sgn_but")
delallback.clicked.connect(delall_inter)

delallproc=QPushButton("Proceed", delall)
delallproc.setObjectName("delall_but")
delallproc.clicked.connect(delallproceed)

#dellall placements:
delalllogo.move(220, 1)
delallsep.move(45, 80)
delallwarn.move(25, 90)
delallback.move(30, 410)
delallproc.move(360,410)

#delsepc widgets:
delspeclogo=QLabel(delspec)
flogo=QPixmap("NOVA.png")
flogo=flogo.scaled(70,70)
delspeclogo.setPixmap(flogo)

delspecsep=QLabel("__________________________________________________________", delspec)
delspecsep.setObjectName("sep")

delspecwarn=QLabel("Enter the service label who's credentials you'd like removed. This cannot be undone.",delspec)
delspecwarn.setObjectName("delallwarn")
delspecwarn.setWordWrap(True)
delspecwarn.setAlignment(Qt.AlignHCenter)

delspeclabel=QLineEdit(delspec)
delspeclabel.setPlaceholderText("                       L A B E L")
delspeclabel.setObjectName("sgn_name")

delspecback=QPushButton("Back",delspec)
delspecback.setObjectName("sgn_but")
delspecback.clicked.connect(delspec_inter)

delspecproc=QPushButton("Proceed", delspec)
delspecproc.setObjectName("delall_but")
delspecproc.clicked.connect(delspecproceed)

delspecerr=QLabel("                                                                                    ",delspec)
delspecerr.setObjectName("sgn_nameerr")



#delspec placements:
delspeclogo.move(220, 1)
delspecsep.move(45, 80)
delspeclabel.move(70, 260)
delspecwarn.move(35, 100)
delspecback.move(30, 410)
delspecproc.move(360, 410)
delspecerr.move(85, 345)

#ins widgets:
inslogo=QLabel(ins)
inslogo.setPixmap(flogo)

inssep=QLabel("__________________________________________________________",ins)
inssep.setObjectName("sep")

inslabel=QLineEdit("",ins)
inslabel.setPlaceholderText("                       L A B E L")
inslabel.setObjectName("ins_name")

insusername=QLineEdit("",ins)
insusername.setPlaceholderText("                U S E R N A M E")
insusername.setObjectName("ins_name")

inspassword=QLineEdit("", ins)
inspassword.setPlaceholderText("                P A S S W O R D")
inspassword.setObjectName("ins_name")

insback=QPushButton("Back",ins)
insback.setObjectName("sgn_but")
insback.clicked.connect(ins_inter)

insinsert=QPushButton("Add", ins)
insinsert.setObjectName("sgn_but")
insinsert.clicked.connect(insert)

inserr=QLabel("                                                                                    ",ins)
inserr.setObjectName("sgn_nameerr")

#ins placements:
inslogo.move(220,1)
inssep.move(45, 80)
inslabel.move(70, 150)
insusername.move(70, 220)
inspassword.move(70, 290)
insback.move(30, 410)
insinsert.move(360, 410)
inserr.move(110,357)

#retrspec widgets:
retrspeclogo=QLabel(retrspec)
retrspeclogo.setPixmap(flogo)

retrspecsep=QLabel("__________________________________________________________",retrspec)
retrspecsep.setObjectName("sep")

retrspeclabel=QLineEdit("",retrspec)
retrspeclabel.setPlaceholderText("                       L A B E L")
retrspeclabel.setObjectName("sgn_name")

retrspecoplabel=QLabel("                       ",retrspec)
retrspecoplabel.setObjectName("psmng")

retrspecnamelbl=QLabel("                                                                                 ",retrspec)
retrspecnamelbl.setObjectName("psmng")

retrspecpasslbl=QLabel("                                                             ",retrspec)
retrspecpasslbl.setObjectName("psmng")

retrspeclbllbl=QLabel("                                                                   ",retrspec)
retrspeclbllbl.setObjectName("psmng")

retrspecback=QPushButton("Back",retrspec)
retrspecback.setObjectName("sgn_but")
retrspecback.clicked.connect(retrspec_inter)

retrspecretr=QPushButton("Retrieve",retrspec)
retrspecretr.setObjectName("sgn_but")
retrspecretr.clicked.connect(retrievespecific)


#retrspec placements:
retrspeclogo.move(220, 1)
retrspecsep.move(45,80)
retrspeclabel.move(70, 130)
retrspecoplabel.move(170,220)
retrspecnamelbl.move(80, 250)
retrspecpasslbl.move(80, 275)
retrspeclbllbl.move(80, 300)
retrspecback.move(30, 410)
retrspecretr.move(360, 410)

#retrall widgets:
retralllogo=QLabel(retrall)
retralllogo.setPixmap(flogo)

retrallsep=QLabel("__________________________________________________________",retrall)
retrallsep.setObjectName("sep")

retrallmess=QTextEdit(retrall)
retrallmess.setReadOnly(True)
retrallmess.setObjectName("infomessage")
retrallmess.resize(400,200)

retrallback=QPushButton("Back",retrall)
retrallback.setObjectName("sgn_but")
retrallback.clicked.connect(retrall_inter)


#retrall placements:
retralllogo.move(220, 1)
retrallsep.move(45,80)
retrallmess.move(54,165)
retrallback.move(197,410)

#delacc wdigets:
delacclogo=QLabel(delacc)
delacclogo.setPixmap(flogo)

delaccsep=QLabel("__________________________________________________________",delacc)
delaccsep.setObjectName("sep")

delaccwarn=QLabel("You are about to DELETE YOUR ACCOUNT. This cannot be undone. Proceed?",delacc)
delaccwarn.setObjectName("delallwarn")
delaccwarn.setWordWrap(True)
delaccwarn.setAlignment(Qt.AlignHCenter)

delaccback=QPushButton("Back",delacc)
delaccback.setObjectName("sgn_but")
delaccback.clicked.connect(delacc_inter)

delaccproc=QPushButton("Proceed",delacc)
delaccproc.setObjectName("delall_but")
delaccproc.clicked.connect(deleteaccount)

#delacc placements:
delacclogo.move(220, 1)
delaccsep.move(45, 80)
delaccwarn.move(45, 100)
delaccback.move(30, 410)
delaccproc.move(360, 410)

#upd widgets:
updlogo=QLabel(upd)
updlogo.setPixmap(flogo)

updsep=QLabel("__________________________________________________________",upd)
updsep.setObjectName("sep")

updlabel=QLineEdit("",upd)
updlabel.setPlaceholderText("                       L A B E L")
updlabel.setObjectName("ins_name")

updusername=QLineEdit("",upd)
updusername.setPlaceholderText("            N E W  U S E R N A M E")
updusername.setObjectName("ins_name")

updpassword=QLineEdit("", upd)
updpassword.setPlaceholderText("            N E W  P A S S W O R D")
updpassword.setObjectName("ins_name")

updback=QPushButton("Back",upd)
updback.setObjectName("sgn_but")
updback.clicked.connect(upd_inter)

updproc=QPushButton("Proceed",upd)
updproc.setObjectName("sgn_but")
updproc.clicked.connect(updatespecific)

upderr=QLabel("                          ",upd)
upderr.setObjectName("sgn_nameerr")


#upd placements:
updlogo.move(220, 1)
updsep.move(45, 80)
updlabel.move(70, 150)
updusername.move(70, 220)
updpassword.move(70, 290)
updback.move(30, 410)
updproc.move(360, 410)
upderr.move(110,357)


stack.setCurrentIndex(0)
stack.setWindowTitle("Password Manager")
stack.show()
app.exec()
