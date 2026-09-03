"""Basic remote OpenServer usage via PxOnlineServer.

Runs the same DoCmd/DoSet/DoGet calls as the local COM client, but against a
Petroleum Experts PxOnlineServer instance. No local IPM install is required.

The base_url, master_session and module_name below are examples - replace them
with values for your own server. `master_session` is referenced by name and is
copied into a temporary user session on connect; that user session is removed
again on disconnect.
"""

from openserver import PxOnlineServer

BASE_URL: str = "http://my-pxserver:8056"
MASTER_SESSION: str = "my-master-session"   # a master session that contains a PROSPER OpenServer module
MODULE_NAME: str = "IPM-OS"      # the server-side OpenServer module name

MC_FILE_PATH: str = r'Root/Europe/Norway/prosper-testfile.OUT'  # Case-sensitive
MC_HOST_ALIAS: str = "my-mc-alias"

# --- Generic OpenServer usage against a Model Catalogue file ---
with PxOnlineServer(base_url=BASE_URL, master_session=MASTER_SESSION, module_name=MODULE_NAME) as c:
    # Open a model from the Model Catalogue
    # Perform a simple VLP/IPR calculation
    # Return the liquid rate result
    c.open_catalogue_file(MC_FILE_PATH, host_alias=MC_HOST_ALIAS)
    print(f"Opened {MC_FILE_PATH}")

    unit_system = "Norwegian S.I."
    c.DoCmd(f"PROSPER.SETUNITSYS(\"{unit_system}\")")

    whp: float = 30  # bara
    wc: float = 40  # percent water cut
    gor_tot: float = 79  # gas-oil ratio total
    c.DoSet("PROSPER.ANL.SYS.Pres", whp)  # Set top node pressure
    c.DoSet("PROSPER.ANL.SYS.WC", wc)  # Set water cut
    c.DoSet("PROSPER.ANL.SYS.GOR", gor_tot)  # Set GOR total

    c.DoCmd("PROSPER.ANL.SYS.CALC")  # Calculate VLP/IPR

    qliq = c.DoGet("PROSPER.OUT.SYS.SOL[0].QLIQ")  # Get liquid flow rate
    print(f"Liquid flow rate: {qliq}")


with PxOnlineServer(base_url=BASE_URL, master_session=MASTER_SESSION, module_name=MODULE_NAME) as d:
    catalogue_guid: str = d.open_catalogue_file(MC_FILE_PATH, host_alias=MC_HOST_ALIAS)

    # --- Download a copy of a Model Catalogue file to disk ---
    file_bytes = d.mc_download_file(catalogue_guid, MC_FILE_PATH)
    local_name = MC_FILE_PATH.rsplit("/", 1)[-1]
    with open(local_name, "wb") as f:
        f.write(file_bytes)
    print(f"Downloaded {len(file_bytes)} bytes to {local_name}")
