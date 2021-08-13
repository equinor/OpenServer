import win32com.client
import numpy as np
import pythoncom

class OpenServer:
    def __init__(self):
        self.status = "Disconnected"
        self.server = None

    def __enter__(self): 
        """
        Custom function for managing connections with the server and preventing licence blockage using a "with" statement.
        In case of any error, the script will automatically disconnect from the server and then raising an exception.
        See context manager for more information.
        
        Example:
        with OpenServer() as c:
            c.DoSet(Sv='target', Val='value')
            ...do other things...
        """
        self.connect()
        return self

    def __exit__(self, *args):
        """
        Refer to __enter__ docstring.
        """
        self.disconnect()

    def connect(self, com='PX32.OpenServer.1'):
        """
        Method used to connect to the Petroleum Experts com object which also checks out the license
        com {string} -- Petroleum Experts COM object
        """
        try:
            self.server = win32com.client.Dispatch(com)
            self.status = "Connected"
            return print("OpenServer is connected")
        except pythoncom.com_error:
            raise ConnectionError("Unable to establish a connection") from None

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
                self.error = self.server.GetErrorDescription(Err)
                raise ValueError(self.error)
        except ValueError as exc:
            print(exc)
            self.disconnect()
            raise

    def DoSet(self, Sv, Val=''):
        """
        The DoSet command is used to set the value of a data item.
        OpenServer access strings can be found directly from an IPM tool by Ctrl + Right-Click mouse on a field in an
        IPM tool, in the OpenServer User Manual or in-menu of some IPM tools.

        Arguments:
            Sv {string} -- OpenServer access string
            Val {} -- Value, list or a one-dimensional numpy array
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            if isinstance(Val, np.ndarray):  # Checks if input is numpy array
                Val = np.array2string(Val, separator='|')[1:-1]
            if isinstance(Val, list):  # Checks if input is list
                Val = '|'.join([str(x) for x in Val])
            Err = self.server.SetValue(Sv, Val)
            AppName = self.GetAppName(Sv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                self.error = self.server.GetErrorDescription(Err)
                raise ValueError(self.error)
        except ValueError as exc:
            print(exc)
            self.disconnect()
            raise

    def DoGet(self, Gv):
        """
        The DoGet function is used to get the value of a data item or result.
        OpenServer access strings can be found directly from an IPM tool by Ctrl + Right-Click mouse on a field in an
        IPM tool, in the OpenServer User Manual or in-menu of some IPM tools.

        Arguments:
            Gv {string} -- OpenServer access string
            Example
            {'PROSPER.OUT.GRD.Results[0][0][0].TVD[0]'}
            {'PROSPER.OUT.GRD.Results[0,1][0][0].TVD[0,1,2]'}
            {'PROSPER.OUT.GRD.Results[0][0][0].TVD[$]'}

        Returns:
            Value of a data item or result.
            Note: If an array is requested in Gv, a numpy array is returned.
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            value = self.server.GetValue(Gv)
            AppName = self.GetAppName(Gv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                self.error = self.server.GetLastErrorMessage(AppName)
                raise ValueError(self.error)
            if value.isdigit():  # Checking if integer
                value = int(value)
            elif '|' in value:  # Checking if | in string is returned
                if any(x in Gv for x in (',', '[$]', '@', ':')):
                    num_array = np.fromstring(value[0:-1], sep="|", dtype=float)
                    str_array = np.array(value[0:-1].split('|'))
                    if num_array.size == str_array.size:  
                        value = num_array  # Return numeric array
                    else:
                        value = str_array  # Return an array of strings
            else:
                try:
                    value = float(value)  # Checking if float
                except ValueError:
                    pass  # Fallback to string
            return value
        except ValueError as exc:
            print(exc)
            self.disconnect()
            raise

    def GetAppName(self, Strval):
        return Strval.split('.')[0]

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

