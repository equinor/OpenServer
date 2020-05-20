# Python script to execute Petroleum Experts OpenServer commands.
# Written by Thorjan Knudsvik, January 2018

import win32com.client
Server = win32com.client.Dispatch("PX32.OpenServer.1")

def DoSet(Sv, Val):
    Err = Server.SetValue(Sv, Val)
    AppName = GetAppName(Sv)
    Err = Server.GetLastError(AppName)
    if Err > 0:
        print(Server.GetErrorDescription(Err))

def DoCmd(Cmd):
    Err = Server.DoCommand(Cmd)
    if Err > 0:
        print(Server.GetErrorDescription(Err))

def DoGet(Gv):
    DoGet = Server.GetValue(Gv)
    AppName = GetAppName(Gv)
    Err = Server.GetLastError(AppName)
    if Err > 0:
        print(Server.GetLastErrorMessage(AppName))
    return float(DoGet)

def GetAppName(Strval):
    AppName = Strval.split('.')[0]
    if AppName not in ['PROSPER', 'MBAL', 'GAP', 'PVT', 'RESOLVE']:
        print('Unrecognised application name in tag string')
    return AppName
