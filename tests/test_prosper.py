import pytest
import os.path
from openserver.prosper import ProsperFile
from datetime import datetime
import numpy as np

my_path = os.path.abspath(os.path.dirname(__file__))
prosperfile = os.path.join(my_path, "../resources/prosper_testfile.OUT")
gapfile = os.path.join(my_path, "../resources/gap_testfile.gap")
now = str(datetime.now())

c = ProsperFile()

c.connect()


def test_start():
    c.DoCmd("PROSPER.START()")
    c.DoCmd(f'PROSPER.OPENFILE("{prosperfile}")')
    assert c.status == "Connected"


def test_prepare_gradient_calc():
    c.prepare_gradient_calc()
    assert c.DoGet("PROSPER.SIN.EQP.Surf.Disable") == 1
    assert c.DoGet("PROSPER.ANL.GRD.Firstnode") == 1
    nodes = c.DoGet("PROSPER.ANL.NODES.NUMBER")
    assert c.DoGet("PROSPER.ANL.GRD.LastNode") == nodes
    assert c.DoGet("PROSPER.ANL.CHK.Choke") == 4  # Elf method


def test_get_fluid():
    assert c.get_fluid_type() == "oil"


def test_end():
    c.DoCmd("PROSPER.SHUTDOWN")
    c.disconnect()
    assert c.status == "Disconnected"
