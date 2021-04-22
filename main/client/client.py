import client_gui
import client_connect
import sys
import threading

client_connection = client_connect.Client_Connection()

def click_connectbutton(window):
    if (client_connection.connect_status == 0):
        window.ConnectButton.setText('Connecting...')

        
        
        try:
            host_str = str(window.IPTextBox.text())
            port_str = int(window.PortTextBox.text())     
            client_connection.connect_status = 1 
            threading._start_new_thread(client_connection.start_connect, (host_str, port_str))
            if client_connection.exc_info:
                raise client_connection.exc_info[1].with_traceback(client_connection.exc_info[2])
        except:
            print('Time out')
            client_connection.connect_status = 0
        else:
            window.ConnectStatus.setText('CONNECTED!')
            window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : green; }")
        finally:
            status = 'Disconnect!' if client_connection.connect_status == 1 else 'Connect!'
            window.ConnectButton.setText(status)
    else:
        # already set in stop_connect method
        #client_connection.connect_status = 0 # set to disconnected flag
        client_connection.stop_connect()
        window.ConnectButton.setText('Connect!')
        window.ConnectStatus.setText('DISCONNECT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

def click_sentbutton(window):
    if not client_connection.connect_status:
        return -1
    message = str(window.Input.text()).encode('utf-8')
    client_connection.mainsock.sendall(message)

def connect_GUI_Feature(window):
    window.add_Click_Behavior(window.ConnectButton,lambda: click_connectbutton(window))
    window.add_Click_Behavior(window.SentButton, lambda: click_sentbutton(window))

if __name__ == '__main__':
    app = client_gui.QtWidgets.QApplication([])
    window = client_gui.client_window()
    window.show()
    host_str = window.IPTextBox.text()
    #print(host_str)
    connect_GUI_Feature(window)
    sys.exit(app.exec_())
