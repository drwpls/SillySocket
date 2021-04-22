import client_gui
import client_connect
import sys
import threading
import time

client_connection = client_connect.Client_Connection()

def click_connectbutton(window):
    if (client_connection.connect_status == 0):
        client_connection.connect_status = -1  # Connecting status
        host_str = str(window.IPTextBox.text())
        port_str = int(window.PortTextBox.text())   
        connection_thread = threading.Thread(target = client_connection.start_connect, args = (host_str, port_str), )
        connection_thread.start()
        window.timer_update_GUI.start(500)
    elif (client_connection.connect_status == 1):
        client_connection.stop_connect()
        window.ConnectButton.setText('Connect!')
        window.ConnectStatus.setText('DISCONNECT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")
        window.timer_update_GUI.stop()

def click_sentbutton(window):
    if not client_connection.connect_status:
        return -1
    message = str(window.Input.text()).encode('utf-8')
    client_connection.mainsock.sendall(message)

def UPDATE_GUI(window):
    ConnectingString = ['Connecting', 'Connecting.', 'Connecting..', 'Connecting...']
    if (client_connection.connect_status == -1):
        # do nothing
        text = window.ConnectButton.text()
        index = 3
        if (text != 'Connect!'):
            index = ConnectingString.index(text)
        #index = ConnectingString.index(text)
        index = (index + 1) % 4
        window.ConnectButton.setText(ConnectingString[index])
    elif (client_connection.connect_status == 0):
        window.ConnectButton.setText('Connect!')
        window.ConnectStatus.setText('DISCONNECT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")
    else:
        window.ConnectButton.setText('Disconnect!')
        window.ConnectStatus.setText('CONNECTED!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : green; }")



def connect_GUI_Feature(window):
    window.add_Click_Behavior(window.ConnectButton,lambda: click_connectbutton(window))
    window.add_Click_Behavior(window.SentButton, lambda: click_sentbutton(window))
    window.timer_update_GUI.timeout.connect(lambda: UPDATE_GUI(window))

if __name__ == '__main__':
    app = client_gui.QtWidgets.QApplication([])
    window = client_gui.client_window()
    window.show()
    host_str = window.IPTextBox.text()
    #print(host_str)
    connect_GUI_Feature(window)
    sys.exit(app.exec_())
