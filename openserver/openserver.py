from __future__ import annotations

import numpy as np
from typing import Any

import io
import os
import zipfile

import requests

try:
    import pythoncom
    import win32com.client
except ImportError:  # pragma: no cover - exercised only when pywin32 is unavailable
    pythoncom = None
    win32com = None


def _format_os_value(value):
    if isinstance(value, np.ndarray):
        return np.array2string(value, separator='|')[1:-1]
    if isinstance(value, list):
        return '|'.join([str(x) for x in value])
    return value


def _parse_os_value(value, tag):
    if value.isdigit():
        return int(value)
    if '|' in value:
        if any(x in tag for x in (',', '[$]', '@', ':')):
            str_array = np.array(value[0:-1].split('|'))
            try:
                num_array = str_array.astype(float)
            except ValueError:
                num_array = np.array([])
            if num_array.size == str_array.size:
                return num_array
            return str_array
    else:
        try:
            return float(value)
        except ValueError:
            pass
    return value

class OpenServer:
    def __init__(self):
        self.status = "Disconnected"
        self.server: Any = None

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
        if win32com is None or pythoncom is None:
            raise ConnectionError("pywin32 is required to use the local COM OpenServer client") from None
        try:
            self.server = win32com.client.Dispatch(com)
            self.status = "Connected"
            print("OpenServer is connected")
        except pythoncom.com_error:
            raise ConnectionError("Unable to establish a connection") from None

    def disconnect(self):
        """
        Method to check in the license
        """
        self.server = None
        self.status = "Disconnected"
        print("OpenServer has been disconnected")

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

    def DoSet(self, Sv, Val: Any = ''):
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
            Val = _format_os_value(Val)
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
            return _parse_os_value(value, Gv)
        except ValueError as exc:
            print(exc)
            self.disconnect()
            raise

    def GetAppName(self, Strval):
        return Strval.split('.')[0]


class PxOnlineServer:
    """Remote OpenServer client for a Petroleum Experts PxOnlineServer instance.
    Targets a PxOnlineServer that operates without authentication. 
    """

    def __init__(self, base_url: str, master_session: str | None = None, module_name: str | None = None,
                 guid: str | None = None, session: str | None = None,
                 remove_user_session_on_disconnect: bool | None = None, timeout: float = 30,
                 http_session: Any = None) -> None:
        if not module_name:
            raise ValueError("module_name is required")
        if not master_session and not (guid and session):
            raise ValueError("Either master_session or both guid and session must be provided")

        self.base_url = base_url.rstrip('/')
        self.master_session = master_session
        self.module_name = module_name
        self.guid = guid
        self.session = session or master_session
        self.timeout = timeout
        self.http_session = http_session or requests.Session()
        self.status = "Disconnected"
        self._created_user_session = guid is None
        if remove_user_session_on_disconnect is None:
            remove_user_session_on_disconnect = self._created_user_session
        self.remove_user_session_on_disconnect = remove_user_session_on_disconnect

    def __enter__(self) -> "PxOnlineServer":
        self.connect()
        return self

    def __exit__(self, *args) -> None:
        self.disconnect()

    def connect(self) -> None:
        try:
            if not self.guid:
                self.guid = self._create_user_session()
        except requests.RequestException as exc:
            raise ConnectionError("Unable to establish a connection") from exc
        self._os_connect()
        print("PxOnlineServer is connected")

    def _os_connect(self) -> None:
        try:
            response = self._post(
                "/pxapi/Sessions/OSConnect",
                params={"guid": self.guid, "session": self.session, "moduleToConnect": self.module_name},
            )
        except requests.HTTPError as exc:
            modules = [m.get("Label") for m in self.get_session_data().get("GenericOpenServerCache", [])]
            if self.module_name not in modules:
                raise ConnectionError(
                    f"Unknown module {self.module_name!r}. Available modules: {modules}"
                ) from exc
            raise ConnectionError("Unable to establish a connection") from exc
        except requests.RequestException as exc:
            raise ConnectionError("Unable to establish a connection") from exc
        self._raise_for_error_response(response, connection_error=True)
        self.status = "Connected"

    def disconnect(self) -> None:
        if self.guid and self.status == "Connected":
            self._os_disconnect()
        if self.guid and self._created_user_session and self.remove_user_session_on_disconnect:
            response = self._post(
                "/pxapi/Sessions/RemoveUserSession",
                params={"guid": self.guid, "sessionToDelete": self.session},
            )
            self._raise_for_error_response(response)
        print("PxOnlineServer has been disconnected")

    def _os_disconnect(self) -> None:
        try:
            response = self._post(
                "/pxapi/Sessions/OSDisconnect",
                params={"guid": self.guid, "session": self.session, "moduleToDisconnect": self.module_name},
            )
            self._raise_for_error_response(response)
        finally:
            self.status = "Disconnected"

    def reconnect(self) -> None:
        """Disconnect and reconnect the OpenServer module, keeping the user session.

        Reloads the session's main file - use after uploading a replacement model file.
        """
        if self.status == "Connected":
            self._os_disconnect()
        self._os_connect()

    def DoCmd(self, Cmd: str) -> None:
        if not self.status == "Connected":
            self.connect()
        response = self._post(
            "/pxapi/Sessions/OSCmd",
            params={"guid": self.guid, "session": self.session, "moduleName": self.module_name, "cmd": Cmd},
        )
        data = self._json(response)
        self._raise_for_os_response(data)

    def DoSet(self, Sv: str, Val: Any = '') -> None:
        if not self.status == "Connected":
            self.connect()
        response = self._post(
            "/pxapi/Sessions/OSSet",
            params={
                "guid": self.guid,
                "session": self.session,
                "moduleName": self.module_name,
                "varToSet": Sv,
                "valToSet": _format_os_value(Val),
            },
        )
        data = self._json(response)
        self._raise_for_os_response(data)

    def DoGet(self, Gv: str) -> Any:
        if not self.status == "Connected":
            self.connect()
        response = self._post(
            "/pxapi/Sessions/OSGet",
            params={"guid": self.guid, "session": self.session, "moduleName": self.module_name, "varToGet": Gv},
        )
        data = self._json(response)
        self._raise_for_os_response(data)
        return _parse_os_value(data.get("Return", ""), Gv)

    def get_session_data(self) -> dict[str, Any]:
        """Return the session definition, incl. loaded OpenServer modules and their MainFile."""
        if not self.guid:
            self.connect()
        response = self._get(
            "/pxapi/Sessions/GetSessionData",
            params={"guid": self.guid, "sessionName": self.session},
        )
        return self._json(response)

    def get_master_sessions(self) -> Any:
        """Return the list of master sessions available on the server."""
        response = self._get("/pxapi/Sessions/Get", params={"guid": "*"})
        return self._json(response)

    def mc_get_api_hosts(self) -> Any:
        """Return the Model Catalogue host aliases this API can connect to."""
        response = self._get("/pxapi/MC/GetApiHosts")
        return self._json(response)

    def mc_init(self, host_alias: str, user_domain: str | None = None, user_name: str | None = None) -> Any:
        """Initialise the Model Catalogue API for a host alias; returns the catalogue guid.

        user_domain/user_name default to the current Windows AD user (USERDOMAIN/USERNAME).
        """
        hosts = self.mc_get_api_hosts()
        if isinstance(hosts, list) and host_alias not in hosts:
            raise ValueError(f"Unknown Model Catalogue host {host_alias!r}. Available hosts: {hosts}")
        if user_domain is None:
            user_domain = os.environ.get("USERDOMAIN", "")
        if user_name is None:
            user_name = os.environ.get("USERNAME", "")
        response = self._post(
            "/pxapi/MC/InitApi",
            params={"hostAlias": host_alias, "userDomain": user_domain, "userName": user_name},
        )
        return self._json(response)

    def mc_get_folders(self, catalogue_guid: str) -> Any:
        """Return the folders in the Model Catalogue (uses the catalogue guid from mc_init)."""
        response = self._post("/pxapi/MC/GetFolders", params={"guid": catalogue_guid})
        return self._json(response)

    def mc_get_files_by_folder_id(self, catalogue_guid: str, folder_ids: str) -> Any:
        """Return the files in the given catalogue folder id(s), in the form 'a,b,c'."""
        response = self._post(
            "/pxapi/MC/GetFilesByFolderId",
            params={"guid": catalogue_guid, "folderIdsString": folder_ids},
        )
        return self._json(response)

    def mc_get_folder_id_by_path(self, catalogue_guid: str, folder_path: str) -> Any:
        """Resolve a catalogue folder path (e.g. 'Root/Europe/Norway') to its folder id."""
        names = [p for p in folder_path.replace("\\", "/").split("/") if p]
        folders = self.mc_get_folders(catalogue_guid)
        parent_id = None
        folder_id = None
        for name in names:
            match = next(
                (f for f in folders
                 if f.get("Name") == name and f.get("ParentFolderId") == parent_id),
                None,
            )
            if match is None:
                raise ValueError(f"Folder {name!r} not found in path {folder_path!r}")
            folder_id = match["Id"]
            parent_id = folder_id
        return folder_id

    def mc_get_file_id_by_path(self, catalogue_guid: str, file_path: str) -> Any:
        """Resolve a catalogue file path (folder path + '/' + file name) to its file id."""
        folder_path, _, file_name = file_path.replace("\\", "/").rpartition("/")
        folder_id = self.mc_get_folder_id_by_path(catalogue_guid, folder_path)
        files = self.mc_get_files_by_folder_id(catalogue_guid, str(folder_id))
        match = next((f for f in files if f.get("FileName") == file_name), None)
        if match is None:
            raise ValueError(f"File {file_name!r} not found in folder {folder_path!r}")
        return match["Id"]

    def mc_get_a_copy_of_files(self, catalogue_guid: str, file_ids: str, recursive: bool = False,
                              date: str = "") -> requests.Response:
        """Get a copy of catalogue file(s) as a zipped directory; returns the raw HTTP response."""
        return self._post(
            "/pxapi/MC/GetACopyOfFiles",
            params={
                "guid": catalogue_guid,
                "fileIds": file_ids,
                "recursive": str(recursive).lower(),
                "date": date,
            },
        )

    def mc_download_file(self, catalogue_guid: str, file_path: str) -> bytes:
        """Download a single catalogue file by its path; returns the file's bytes.

        `file_path` is the full catalogue path incl. the file name, e.g.
        'Root/Europe/Norway/North Sea/Yggdrasil/ByteAll/ProsperModel/SK1.Out'.
        """
        file_name = file_path.replace("\\", "/").rpartition("/")[2]
        file_id = self.mc_get_file_id_by_path(catalogue_guid, file_path)
        response = self.mc_get_a_copy_of_files(catalogue_guid, str(file_id))
        with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
            return archive.read(file_name)

    def upload_file_to_user_session(self, file_bytes: bytes, file_name: str, file_type: str = "model") -> Any:
        """Upload a file (e.g. a model) into the current user session."""
        if not self.guid:
            self.connect()
        response = self.http_session.post(
            self.base_url + "/pxapi/Sessions/UploadFileToUserSession",
            params={"uid": self.guid, "session": self.session, "fileName": file_name, "type": file_type},
            files={"File": (file_name, file_bytes)},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return self._json(response)

    def open_catalogue_file(self, file_path: str, host_alias: str | None = None,
                            catalogue_guid: str | None = None) -> Any:
        """Load a Model Catalogue file into the session as the active model.

        The remote analogue of ``PROSPER.OPENFILE``: downloads the file, uploads it
        in place of the session's current main file, and reconnects the module.
        Provide either ``host_alias`` (to initialise the catalogue) or an existing
        ``catalogue_guid``; the catalogue guid is returned so it can be reused.
        """
        if catalogue_guid is None:
            if host_alias is None:
                raise ValueError("Provide either host_alias or catalogue_guid")
            catalogue_guid = str(self.mc_init(host_alias))
        file_bytes = self.mc_download_file(catalogue_guid, file_path)
        main_file = self.get_session_data().get("GenericOpenServerCache", [{}])[0].get("MainFile", "")
        self.upload_file_to_user_session(file_bytes, main_file)
        self.reconnect()
        return catalogue_guid

    def _create_user_session(self) -> str:
        try:
            response = self._post(
                "/pxapi/Sessions/CreateUserSession",
                params={"sessionToCopy": self.master_session},
            )
            uid = self._json(response)
        except requests.HTTPError:
            uid = None
        if isinstance(uid, dict):
            uid = uid.get("UserID") or uid.get("uid") or uid.get("guid")
        if not uid:
            masters = self.get_master_sessions()
            if isinstance(masters, list) and self.master_session not in masters:
                raise ConnectionError(
                    f"Unknown master session {self.master_session!r}. "
                    f"Available master sessions: {masters}"
                )
            raise ConnectionError("Unable to create a user session")
        return uid

    def _post(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        response = self.http_session.post(self.base_url + path, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response

    def _get(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        response = self.http_session.get(self.base_url + path, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response

    def _json(self, response: requests.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return response.text

    def _raise_for_error_response(self, response: requests.Response, connection_error: bool = False) -> None:
        data = self._json(response)
        if isinstance(data, str):
            if data and data != "0":
                if connection_error:
                    raise ConnectionError(data)
                raise ValueError(data)
        elif isinstance(data, int) and data != 0:
            if connection_error:
                raise ConnectionError(str(data))
            raise ValueError(str(data))

    def _raise_for_os_response(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise ValueError(str(data))
        error = data.get("ErrorStr")
        error_code = data.get("ErrorCode")
        if error or error_code not in (None, "", "0", 0):
            raise ValueError(error or str(error_code))

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

