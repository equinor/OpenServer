import pytest
import os.path
from openserver.openserver import *
from datetime import datetime

my_path = os.path.abspath(os.path.dirname(__file__))
prosperfile = os.path.join(my_path, "../resources/prosper_testfile.OUT")
now = str(datetime.now())

c = OpenServer()
c.connect()

def test_openserver_functions():
    c.DoCmd('PROSPER.START()')
    c.DoCmd('PROSPER.OPENFILE("{}")'.format(prosperfile))
    c.DoSet("PROSPER.SIN.SUM.Comments", now)
    assert c.DoGet("PROSPER.SIN.SUM.Comments") == now

def test_DoGet_docstring():
    assert DoGet.__doc__ == c.DoGet.__doc__

def test_DoSet_docstring():
    assert DoSet.__doc__ == c.DoSet.__doc__

def test_DoCmd_docstring():
    assert DoCmd.__doc__ == c.DoCmd.__doc__

c.DoCmd('PROSPER.SHUTDOWN')
c.disconnect()