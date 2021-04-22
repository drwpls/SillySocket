import server_gui
import server_connect
import sys
import threading

host = '0.0.0.0'    # all network interface
port = 65432
server_connection = server_connect.Server_Connection(host, port)

def click_listenbox(window):
   # global window
    if (server_connection.connect_status == 0):
        server_connection.connect_status = 1 # set to connected flag
        window.ListenBox.setText('Wait for Client\nClick to stop accept connect request.')
        
        threading._start_new_thread(server_connection.start_listen, ())
    else:
        server_connection.connect_status = 0 # set to disconnected flag
        server_connection.stop_listen()
        window.ListenBox.setText('Start accept connection.')
       
        

def connect_GUI_Feature(window):
    window.add_Click_Behavior(window.ListenBox,lambda: click_listenbox(window))

if __name__ == '__main__':
    # create application window
    app = server_gui.QtWidgets.QApplication([])
    window = server_gui.server_window()
    window.show()

    connect_GUI_Feature(window)
    sys.exit(app.exec_())