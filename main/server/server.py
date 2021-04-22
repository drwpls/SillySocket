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
        window.ListenBox.setText('Wait for clients.\nClick to Stop Listening')
        connection_thread = threading.Thread(target = server_connection.start_listen)
        connection_thread.start()
        window.timer_update_GUI.start(500)
    else:
        server_connection.stop_listen()
        window.ListenBox.setText('Start Listening.')
        window.timer_update_GUI.stop()
       
def UPDATE_GUI(window):
    if server_connection.connect_status > 1:
        window.ListenBox.setText('Connected to ' + \
            str(server_connection.connect_status - 1)+  ' client(s)\n'+ 
            'Click to Stop Listening')
    elif server_connection.connect_status == 1:
        window.ListenBox.setText('Wait for clients.\nClick to Stop Listening')

def onQuit():
    if server_connection.connect_status:
        server_connection.stop_listen() # stop the thread
    app.exit()
def connect_GUI_Feature(window, app):
    app.lastWindowClosed.connect(onQuit)
    window.add_Click_Behavior(window.ListenBox,lambda: click_listenbox(window))
    window.timer_update_GUI.timeout.connect(lambda: UPDATE_GUI(window))

if __name__ == '__main__':
    # create application window
    app = server_gui.QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = server_gui.server_window()
    window.show()
    connect_GUI_Feature(window, app)
    sys.exit(app.exec_())