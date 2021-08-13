<p align="center">
<img src="https://raw.githubusercontent.com/equinor/openserver/master/resources/logo.png" title="OpenServer"/>
</p>

[![PyPI](https://img.shields.io/pypi/v/openserver)](https://pypi.org/project/openserver/)

# OpenServer
Code for running Petroleum Experts OpenServer API commands in Python. More general information about this API protocol can be found on [Petroleum Experts'](https://www.petex.com/products/ipm-suite/openserver/) site.

Please have a look at the [CONTRIBUTING.MD file](https://github.com/equinor/OpenServer/blob/master/CONTRIBUTING.md) if you want to contribute.


## Python

### Getting started
Install the required package:
```
pip install openserver
```

### Example in Python

There are two ways of using the functions, either by importing a class called OpenServer or by importing all modules. The first is the most "pythonic" way which can be used to disconnect from the license server. The latter is easier for those converting from visual basic style coding environment. 

The following code will import the OpenServer module, start Prosper, open a Prosper file named well_2 on C-drive and adding a comment into the comment section in Prosper.

#### by using the class ####

```
from openserver import OpenServer

c = OpenServer()
c.connect()

c.DoCmd('PROSPER.START()')
c.DoCmd('PROSPER.OPENFILE("C:\\well_2.OUT")')
c.DoSet('PROSPER.SIN.SUM.Comments', 'Testing OpenServer from Python')

c.disconnect()
```

or

```
from openserver import OpenServer

with OpenServer() as c:
    c.DoCmd('PROSPER.START()')
    c.DoCmd('PROSPER.OPENFILE("C:\\well_2.OUT")')
    c.DoSet('PROSPER.SIN.SUM.Comments', 'Testing OpenServer from Python')
```

#### by importing all modules ####

```
from openserver import *

DoCmd('PROSPER.START()')
DoCmd('PROSPER.OPENFILE("C:\\well_2.OUT")')
DoSet('PROSPER.SIN.SUM.Comments', 'Testing OpenServer from Python')
```

