import numpy as np
import pytest

from openserver.openserver import PxOnlineServer


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code
        self.text = str(payload)

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.text)


class FakeHttpSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, params=None, timeout=None):
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        return FakeResponse(self.responses.pop(0))


def test_connect_creates_user_session_and_connects_to_module():
    http_session = FakeHttpSession(["user-guid", 0])

    server = PxOnlineServer(
        "http://pxserver:8056",
        master_session="upload",
        module_name="IPM-OS",
        http_session=http_session,
    )

    server.connect()

    assert server.guid == "user-guid"
    assert server.session == "upload"
    assert server.status == "Connected"
    assert http_session.calls[0]["url"] == "http://pxserver:8056/pxapi/Sessions/CreateUserSession"
    assert http_session.calls[0]["params"] == {"sessionToCopy": "upload"}
    assert http_session.calls[1]["url"] == "http://pxserver:8056/pxapi/Sessions/OSConnect"
    assert http_session.calls[1]["params"] == {
        "guid": "user-guid",
        "session": "upload",
        "moduleToConnect": "IPM-OS",
    }


def test_disconnect_removes_owned_user_session():
    http_session = FakeHttpSession([0, 0])
    server = PxOnlineServer(
        "http://pxserver:8056",
        master_session="upload",
        module_name="IPM-OS",
        guid="user-guid",
        http_session=http_session,
        remove_user_session_on_disconnect=True,
    )
    server.status = "Connected"
    server._created_user_session = True

    server.disconnect()

    assert server.status == "Disconnected"
    assert http_session.calls[0]["url"] == "http://pxserver:8056/pxapi/Sessions/OSDisconnect"
    assert http_session.calls[1]["url"] == "http://pxserver:8056/pxapi/Sessions/RemoveUserSession"


def test_disconnect_does_not_remove_attached_user_session_by_default():
    http_session = FakeHttpSession([0])
    server = PxOnlineServer(
        "http://pxserver:8056",
        guid="existing-guid",
        session="existing-session",
        module_name="IPM-OS",
        http_session=http_session,
    )
    server.status = "Connected"

    server.disconnect()

    assert len(http_session.calls) == 1
    assert http_session.calls[0]["url"] == "http://pxserver:8056/pxapi/Sessions/OSDisconnect"


def test_do_set_serializes_numpy_array():
    http_session = FakeHttpSession([{"Return": "", "ErrorStr": "", "ErrorCode": "0"}])
    server = PxOnlineServer(
        "http://pxserver:8056",
        guid="existing-guid",
        session="existing-session",
        module_name="IPM-OS",
        http_session=http_session,
    )
    server.status = "Connected"

    server.DoSet("PROSPER.SIN.EQP.Gauge.Data[0:2].Depth", np.array([0, 1, 2]))

    assert http_session.calls[0]["params"]["valToSet"] == "0|1|2"


def test_do_get_parses_remote_array_response():
    http_session = FakeHttpSession([{"Return": "0|100|200|", "ErrorStr": "", "ErrorCode": "0"}])
    server = PxOnlineServer(
        "http://pxserver:8056",
        guid="existing-guid",
        session="existing-session",
        module_name="IPM-OS",
        http_session=http_session,
    )
    server.status = "Connected"

    assert np.array_equal(server.DoGet("PROSPER.SIN.EQP.Devn.Data[$].Md"), np.array([0., 100., 200.]))


def test_do_command_raises_value_error_for_openserver_error():
    http_session = FakeHttpSession([{"Return": "", "ErrorStr": "Variable name was not found", "ErrorCode": "1"}])
    server = PxOnlineServer(
        "http://pxserver:8056",
        guid="existing-guid",
        session="existing-session",
        module_name="IPM-OS",
        http_session=http_session,
    )
    server.status = "Connected"

    with pytest.raises(ValueError, match="Variable name was not found"):
        server.DoCmd("PROSPER.value")
