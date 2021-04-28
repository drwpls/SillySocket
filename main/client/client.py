import sys
import threading
import logging
import screenshot
import registry

import client_gui
import client_connect

import shutdown


FEATURE_CODE = {
    'PING': '00',
    'ProcessRunning': '01',
    'AppRunning': '02',
    'Shutdown': '03',
    'Screenshot': '04',
    'Keystroke': '05',
    'RegistryEdit': '06',
}

client_connection = client_connect.Client_Connection()


def click_connectbutton(window):
    if (client_connection.connect_status == client_connection.Status_Code.DISCONNECT
            or client_connection.connect_status == client_connection.Status_Code.TIMEOUT):

        host_str = str(window.IPTextBox.text())
        port_str = window.PortTextBox.text()
        pos = 0
        if window.validator.validate(port_str, pos)[0] != window.validator.Acceptable:
            errmsg = window.showError('Invalid Address', 'Invalid Port')
            errmsg.exec_()
            return -1
        port_str = int(port_str)
        # Try to connect to server for the first time, after disconnect or timeout seasion
        # turn status to connecting
        client_connection.connect_status = client_connection.Status_Code.CONNECTING
        window.change_GUI_status(window.Status_Code.CONNECTING)
        # try to connect to host
        connection_thread = threading.Thread(target=client_connection.start_connect, args=(host_str, port_str))
        connection_thread.start()

        # start timer - update GUI and send sample data to server (PING)
        window.timer_update_GUI.start(500)

    elif (client_connection.connect_status == client_connection.Status_Code.CONNECTED):
        # Users choose to close connection
        client_connection.stop_connect()
        window.change_GUI_status(window.Status_Code.DISCONNECT)
        # stop the timer
        window.timer_update_GUI.stop()


def click_sendbutton(window):
    if client_connection.connect_status != client_connection.Status_Code.CONNECTED:
        # by default, showError will display NOCONNECTION error
        errmsg = window.showError()
        errmsg.exec_()
        return -1
    message = str(window.Input.text())
    client_connection.send_message(message)


def click_shutdownbutton(window):
    if client_connection.connect_status != client_connection.Status_Code.CONNECTED:
        errmsg = window.showError()
        errmsg.exec_()
        return -1

    # if connected, perform shutdown_dialog
    shutdown_dialog = shutdown.Shutdown_Dialog(client_connection.mainsock)
    dialog_result_code = shutdown_dialog.exec_()


def click_screenshotbutton(window):
    if client_connection.connect_status != client_connection.Status_Code.CONNECTED:
        # show error msg
        errmsg = window.showError()
        errmsg.exec_()
        return -1

    take_screenshot = screenshot.Screenshot_Dialog(client_connection.mainsock)
    subthread = threading.Thread(target=take_screenshot.exec_(), args=())
    subthread.start()


def click_registrybutton(window):
    if client_connection.connect_status != client_connection.Status_Code.CONNECTED:
        # show error msg
        errmsg = window.showError()
        errmsg.exec_()
        return -1

    reg_edit = registry.Registry_Dialog(client_connection.mainsock)
    subthread = threading.Thread(target=reg_edit.exec_(), args=())
    subthread.start()


def update_GUI(window):
    if (client_connection.connect_status == client_connection.Status_Code.CONNECTING):
        window.change_GUI_status(window.Status_Code.CONNECTING)
    elif (client_connection.connect_status == client_connection.Status_Code.TIMEOUT):
        window.change_GUI_status(window.Status_Code.TIMEOUT)
    elif (client_connection.connect_status == client_connection.Status_Code.DISCONNECT):
        # In case lost connection from server, we make notification to user
        if (client_connection.lost_connect == True):
            client_connection.lost_connect = False
            server_address = str(client_connection.mainsock.getpeername()[0]) + ':' + str(client_connection.mainsock.getpeername()[1])
            errmsg = window.showError('Lost connection', ' from server: ' + server_address)
            errmsg.exec_()
        window.change_GUI_status(window.Status_Code.DISCONNECT)
    elif (client_connection.connect_status == client_connection.Status_Code.CONNECTED):               # in-connecting
        window.change_GUI_status(window.Status_Code.CONNECTED)
        # sent '00' after every 500ms to check server's signal
        client_connection.send_message('00')


def on_quit():
    if client_connection.connect_status == client_connection.Status_Code.CONNECTING \
            or client_connection.connect_status == client_connection.Status_Code.CONNECTED:
        client_connection.stop_connect()
    app.exit()


def connect_GUI_feature(window):
    app.lastWindowClosed.connect(on_quit)
    window.timer_update_GUI.timeout.connect(lambda: update_GUI(window))
    window.add_click_behavior(window.ConnectButton, lambda: click_connectbutton(window))
    window.add_click_behavior(window.SendButton, lambda: click_sendbutton(window))
    window.add_click_behavior(window.ShutdownButton, lambda: click_shutdownbutton(window))
    window.add_click_behavior(window.ScreenshotButton, lambda: click_screenshotbutton(window))
    window.add_click_behavior(window.RegistryEditButton, lambda: click_registrybutton(window))


if __name__ == '__main__':
    app = client_gui.QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = client_gui.client_window()
    window.show()

    connect_GUI_feature(window)
    sys.exit(app.exec_())
