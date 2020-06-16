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

def test_get_parts_array():
    assert np.array_equal(c.DoGet('PROSPER.SIN.EQP.Devn.Data[1:3].Md'), np.array([   100., 1000., 2000.]))

def test_set_array():
    day_of_year = datetime.now().timetuple().tm_yday
    array = np.array([0, 1, 2, day_of_year])
    c.DoSet('PROSPER.SIN.EQP.Gauge.Data[0:3].Depth', array)
    assert np.array_equal(c.DoGet('PROSPER.SIN.EQP.Gauge.Data[0:3].Depth'), array)

def test_set_list():
    values = ['top', datetime.now().strftime('%H:%M')]
    c.DoSet('PROSPER.SIN.EQP.Down.Data[0:1].Label', values)
    assert np.array_equal(c.DoGet('PROSPER.SIN.EQP.Down.Data[0:1].Label'), values)

def test_product_prefix():
    with pytest.raises(ValueError, match='The tag string product prefix was not recognised'):
        c.DoCmd('Excel.value')
    with pytest.raises(ValueError, match='The tag string product prefix was not recognised'):
        c.DoSet('Excel.value', 1)
    with pytest.raises(ValueError, match='The tag string product prefix was not recognised'):
        c.DoGet('Excel.value')

def test_variable_names():
    with pytest.raises(ValueError, match='Command not recognised'):
        c.DoCmd('PROSPER.value')
    with pytest.raises(ValueError, match='Variable name was not found'):
        c.DoSet('PROSPER.value', 1)
    with pytest.raises(ValueError, match='Variable name was not found'):
        c.DoGet('PROSPER.value')

def test_end():
    c.DoCmd('PROSPER.SHUTDOWN')
    c.disconnect()
    assert c.status == 'Disconnected'
