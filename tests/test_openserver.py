import pytest
import os.path
from openserver.openserver import *
from datetime import datetime
import numpy as np

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

def test_get_integer():
    assert isinstance(c.DoGet("PROSPER.SIN.SUM.Fluid"), int)

def test_get_array():
    assert isinstance(c.DoGet('PROSPER.SIN.EQP.Devn.Data[$].Md'), np.ndarray)

def test_get_float():
    assert isinstance(c.DoGet("PROSPER.PVT.Input.Grvgas"), float)

def test_get_string():
    assert isinstance(c.DoGet("PROSPER.SIN.SUM.Company"), str)

def test_get_full_array():
    assert np.array_equal(c.DoGet('PROSPER.SIN.EQP.Devn.Data[$].Md'), np.array([   0.,  100., 1000., 2000.]))

#def test_get_parts_array():
#    assert np.array_equal(c.DoGet('PROSPER.SIN.EQP.Devn.Data[1:3].Md'), np.array([   100., 1000.]))

def test_appname():
    with pytest.raises(ValueError, match='The tag string product prefix was not recognised'):
        c.DoGet('Excel.value')

# Can not figure out how to run these last two
c.DoCmd('PROSPER.SHUTDOWN')
c.disconnect()