<p align="center">
<img src="https://raw.githubusercontent.com/equinor/openserver/master/resources/logo.png" title="OpenServer"/>
</p>

[![PyPI](https://img.shields.io/pypi/v/openserver)](https://pypi.org/project/openserver/)
[![SCM Compliance](https://scm-compliance-api.radix.equinor.com/repos/equinor/openserver/badge)](https://scm-compliance-api.radix.equinor.com/repos/equinor/openserver/badge)
[![Runs on Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

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

## Remote OpenServer (PxOnlineServer)

In addition to the local COM client, the package ships a `PxOnlineServer` client
that talks to a Petroleum Experts [PxOnlineServer](https://www.petex.com/products/ipm-suite/openserver/)
instance over its REST API. It runs the *same* `DoCmd`/`DoSet`/`DoGet` commands as
the local client, but against a model hosted on the server - no local IPM install
is required.

`requests` is used for the HTTP calls and is installed automatically.

### Connecting to a session

A remote model lives in a *master session* on the server. On connect, the master
session is copied into a temporary *user session* that your commands run against;
the user session is removed again on disconnect.

```python
from openserver import PxOnlineServer

with PxOnlineServer(
    base_url="http://my-pxserver:8056",
    master_session="my_master_session",  # a master session containing a PROSPER module
    module_name="IPM-OS",                # the server-side OpenServer module name
) as c:
    print(c.DoGet("PROSPER.SIN.SUM.Comments"))
    c.DoSet("PROSPER.SIN.SUM.Comments", "Testing remote OpenServer from Python")
```

To attach to an existing user session instead of creating one, pass `guid` and
`session` instead of `master_session`.

### Loading a model from the Model Catalogue

The Model Catalogue is the server's versioned file store. `open_catalogue_file`
is the remote analogue of `PROSPER.OPENFILE`: it loads a catalogue model into the
session so the familiar `DoCmd`/`DoSet`/`DoGet` calls operate on it. There is no
`PROSPER.START()` remotely - the module is already running in the session.

```python
from openserver import PxOnlineServer

with PxOnlineServer(base_url="http://my-pxserver:8056",
                    master_session="my_master_session",
                    module_name="IPM-OS") as c:
    # Remote equivalent of PROSPER.OPENFILE - give the catalogue host + file path
    c.open_catalogue_file(
        "Root/Region/Field/Company/ProsperModel/Well.Out",
        host_alias="MyCatalogueHost",
    )

    # ...then it's the same as the local COM client
    c.DoSet("PROSPER.SIN.SUM.Comments", "Testing remote OpenServer from Python")
    print(c.DoGet("PROSPER.SIN.SUM.Comments"))
```

`open_catalogue_file` returns the catalogue guid, so you can pass it back in as
`catalogue_guid=...` to open further files without re-initialising the catalogue.

The file is uploaded under the existing main file's name, so the session's
reported `MainFile` label is unchanged - but its contents (and everything
`DoGet`/`DoSet`/`DoCmd` see) are the catalogue file you loaded.

See [examples/px_online_server_basic.py](examples/px_online_server_basic.py) for a
complete, runnable walkthrough.

### Limitations

`PxOnlineServer` currently targets a PxOnlineServer instance that requires no
authentication - it sends no credentials. 