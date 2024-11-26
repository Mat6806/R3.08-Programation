import socket, threading, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,  QLabel, QLineEdit, QPushButton,  QVBoxLayout, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.client_socket = socket.socket()
        self.connected = False

      
    
      
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QVBoxLayout()
        widget.setLayout(grid)
        
        grid.addWidget(QLabel("Adresse IP :"))
        self.ip = QLineEdit("127.0.0.1")
        grid.addWidget(self.ip)
 
        grid.addWidget(QLabel("Port :"))
        self.port = QLineEdit("4200")
        grid.addWidget(self.port)

        self.Servconnect = QPushButton('connexion au serveur')
        self.Servconnect.clicked.connect(self.connexionserv)
        grid.addWidget(self.Servconnect)

        self.upload = QPushButton('upload')
        self.upload.clicked.connect(self.upload)
        self.upload.setEnabled(False)
        grid.addWidget(self.upload)


    def connexionserv(self):
        try:
            ip = self.ip.text()
            port = int(self.port.text())
            self.client_socket.connect((ip,port))
        except ConnectionRefusedError as error:
            print(f"Connexion refusée : {error}")
        except TimeoutError as error:
            print(f"Délai dépassé : {error}")

    
    def upload(self):
        if not self.connected:
            self.result_display.append("Erreur : Vous devez d'abord vous connecter au serveur.")
            return
        
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier à uploader", "", "Python Files (*.py);;All Files (*)", options=options)

    
    
    def close_connection(self):
        """
        Ferme la connexion au serveur.
        """
        if self.client_socket:
            self.client_socket.close()
            print("Connexion fermée.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


