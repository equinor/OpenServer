import win32com.client


class OpenServer:
    def __init__(self):
        self.status = "Disconnected"
        self.server = None

    def connect(self):
        self.server = win32com.client.Dispatch("PX32.OpenServer.1")
        self.status = "Connected"
        return print("OpenServer is connected")

    def disconnect(self):
        self.server = None
        self.status = "Disconnected"
        return print("OpenServer has been disconnected")

    def DoCmd(self, Cmd):
        if not self.status == 'Connected':
            self.connect()
        try:
            Err = self.server.DoCommand(Cmd)
            if Err > 0:
                print(self.server.GetErrorDescription(Err))
        except:
            self.disconnect()

    def DoSet(self, Sv, Val):
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
        if not self.status == 'Connected':
            self.connect()
        try:
            DoGet = self.server.GetValue(Gv)
            AppName = self.GetAppName(Gv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                print(self.server.GetLastErrorMessage(AppName))
            return DoGet
        except:
            self.disconnect()

    def GetAppName(self, Strval):
        AppName = Strval.split('.')[0]
        if AppName not in ['PROSPER', 'MBAL', 'GAP', 'PVT', 'RESOLVE']:
            print('Unrecognised application name in tag string')
        return AppName


def DoCmd(Cmd):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoCmd(Cmd)


def DoSet(Sv, Val):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoSet(Sv, Val)


def DoGet(Gv):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoGet(Gv)

