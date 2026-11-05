This is a local password manager I created as my field project. There are a few things to know if you'd like to use this application.

1.) you must have MySQL installed manually on your device. You will also need a Python Runtime Environment installed. And finally, the application requires the following libraries to be installed beforehand:
          > mysql.connector
          > hashlib
          > math
          > PyQt5
          > cryptography.fernet
2.) for this application to work, MySQL must have two databases created. For convenience, you can just run the following commands on your MySQL CLI.
```
          > CREATE DATABASE passwordmanager;
          > USE passwordmanager;
          > CREATE TABLE accounts(name VARCHAR(300), password VARCHAR(300), `key` VARCHAR(300));
          > CREATE DATABASE passwordrepo;
```
3.) Please remember to replace the placeholder passwords ("xxx") in the source file (nova.py) with your actual MySQL root password. The MySQL connection modules are written near the start of the file, so you should not have trouble finding it.
3.) I currently do not have any intentions to update this repository, as I prefer working on other projects.

Concepts that I have demonstrated using this project:
1.) Multi-user authentication
2.) Hashing using SHA256
3.) Encryption and decryption using keys
4.) Strong understanding of RDBMS concepts
