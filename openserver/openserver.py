import win32com.client
import numpy as np

class OpenServer:
    def __init__(self):
        self.status = "Disconnected"
        self.server = None

    def connect(self):
        """
        Method used to connect to the Petroleum Experts com object which also checks out the license
        """
        self.server = win32com.client.Dispatch("PX32.OpenServer.1")
        self.status = "Connected"
        return print("OpenServer is connected")

    def disconnect(self):
        """
        Method to check in the license
        """
        self.server = None
        self.status = "Disconnected"
        return print("OpenServer has been disconnected")

    def DoCmd(self, Cmd):
        """
        The DoCmd function is used to perform calculations and other functions such as file opening in an IPM tool.
        OpenServer command strings can be found in the OpenServer User Manual or in-menu of some IPM tools.

        Arguments:
            Cmd {string} -- OpenServer command string
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            Err = self.server.DoCommand(Cmd)
            if Err > 0:
                print(self.server.GetErrorDescription(Err))
        except:
            self.disconnect()

    def DoSet(self, Sv, Val):
        """
        The DoSet command is used to set the value of a data item.
        OpenServer access strings can be found directly from an IPM tool by Ctrl + Right-Click mouse on a field in an
        IPM tool, in the OpenServer User Manual or in-menu of some IPM tools.

        Arguments:
            Sv {string} -- OpenServer access string
            Val {} -- Value
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            Err = self.server.SetValue(Sv, Val)
            AppName = self.GetAppName(Sv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                print(self.server.GetErrorDescription(Err))
        except:
            self.disconnect()

    def DoGet(self, Gv):
        """
        The DoGet function is used to get the value of a data item or result.
        OpenServer access strings can be found directly from an IPM tool by Ctrl + Right-Click mouse on a field in an
        IPM tool, in the OpenServer User Manual or in-menu of some IPM tools.

        Arguments:
            Gv {string} -- OpenServer access string

        Returns:
            Value of a data item or result
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            value = self.server.GetValue(Gv)
            AppName = self.GetAppName(Gv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                print(self.server.GetLastErrorMessage(AppName))
            if value.isdigit():  # Checking if integer
                value = int(value)
            elif '[$]' in Gv and type(value) == str:
                value = np.fromstring(value, sep="|")
            else:
                try:
                    value = float(value)  # Checking if float
                except ValueError:
                    pass  # Fallback to string
            return value
        except:
            self.disconnect()

    def GetAppName(self, Strval):
        AppName = Strval.split('.')[0]
        if AppName not in ['PROSPER', 'MBAL', 'GAP', 'PVT', 'RESOLVE']:
            print('Unrecognised application name in tag string')
        return AppName

def is_documented_by(original):
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target
    return wrapper

@is_documented_by(OpenServer.DoCmd)
def DoCmd(Cmd):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoCmd(Cmd)

@is_documented_by(OpenServer.DoSet)
def DoSet(Sv, Val):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoSet(Sv, Val)

@is_documented_by(OpenServer.DoGet)
def DoGet(Gv):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoGet(Gv)

