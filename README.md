# OpenServer
Code for running Petroleum Experts OpenServer API commands in Python. More general information about this API protocol can be found on [Petroleum Experts'](https://www.petex.com/products/ipm-suite/openserver/) site.

Please have a look at the [CONTRIBUTING.MD file](https://github.com/equinor/OpenServer/blob/master/CONTRIBUTING.md) if you want to contribute.


## Python

### Getting started
Lorem Lipsum
pip install ...


### Example in Python

The following code will import the OpenServer module, start Prosper, open a Prosper file named C-2 on root drive and adding a comment into the comment section in Prosper.

```
import OpenServer

DoCmd('PROSPER.START()')
DoCmd('PROSPER.OPENFILE("C:\C-2.OUT")')
DoSet('PROSPER.SIN.SUM.Comments', 'Testing OpenServer from Python')
```

