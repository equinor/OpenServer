from .openserver import OpenServer
import pandas as pd
import numpy as np


class ProsperFile(OpenServer):
    #def __init__(self, *args, **kwargs):
    #    super(ProsperFile, self).__init__(*args, **kwargs)
    #    unit_system = 'OilField'
    #    self.DoCmd(f'PROSPER.SETUNITSYS("{unit_system}")')
    #    print(f'Selected unit system: {unit_system}')

    def prepare_gradient_calc(self) -> None:
        """Prepare the prosper file for gradient calculation"""
        self.DoSet("PROSPER.SIN.EQP.Surf.Disable", 1)  # Disable surface equipment
        self.DoSet("PROSPER.ANL.GRD.Firstnode", 1)  # Set first node
        nodes = self.DoGet("PROSPER.ANL.NODES.NUMBER")
        self.DoSet("PROSPER.ANL.GRD.LastNode", nodes)
        self.DoSet(
            "PROSPER.ANL.CHK.Choke", 4
        )  # Set choke method to ELF for downhole restrictions
        self.DoSet(
            "PROSPER.ANL.GRD.Sens.SensDB.Clear", 0
        )  # Clear gradient sensitivities if present

    def get_fluid_type(self) -> str:
        fluid_types = {0: "oil", 1: "gas", 2: "condensate"}
        fluid_int = self.DoGet("PROSPER.SIN.SUM.Fluid")
        fluid = fluid_types[fluid_int]
        return fluid

    def get_al_type(self) -> str:
        al_types = {0: "none", 1: "gaslift", 2: "esp"}
        al_int = self.DoGet("PROSPER.SIN.SUM.LiftMethod")
        al = al_types[al_int]
        return al

    def calculate_gradient(
        self,
        whp: float,
        oil_rate: float = 0,
        gas_rate: float = 0,
        gas_lift_rate: float = 0,
        water_rate: float = 0,
    ) -> None:
        self.prepare_gradient_calc()

        liq_rate = oil_rate + water_rate
        wgr = water_rate / gas_rate if gas_rate else 0
        cgr = oil_rate / gas_rate if gas_rate else 0
        gor = gas_rate / oil_rate if oil_rate else 0
        wc = water_rate / liq_rate  # TODO: Check if *100

        fluid = self.get_fluid_type()
        al = self.get_al_type()
        self.DoSet("PROSPER.ANL.GRD.Pres", whp)

        if fluid == "oil":
            self.DoSet("PROSPER.ANL.GRD.WC", wc)
            self.DoSet("PROSPER.ANL.GRD.GOR", gor)
            self.DoSet("PROSPER.ANL.GRD.Rate", liq_rate)
        elif fluid == "gas":
            self.DoSet("PROSPER.ANL.GRD.WGR", wgr)
            self.DoSet("PROSPER.ANL.GRD.CGR", cgr)
            self.DoSet("PROSPER.ANL.GRD.Rate", gas_rate / 1000)
        elif fluid == "condensate":
            self.DoSet("PROSPER.ANL.GRD.WGR", wgr)
            self.DoSet("PROSPER.ANL.GRD.SGR", gor)
            self.DoSet("PROSPER.ANL.GRD.Rate", gas_rate / 1000)

        if al == "gaslift":
            self.DoSet("PROSPER.SIN.GLF.Entry", 1)  # Set to run with gas lift gas rate
            self.DoSet("PROSPER.SIN.GLF.GLRate", gas_lift_rate / 1000)

        self.DoCmd("PROSPER.ANL.GRD.CALC")

    def get_gradient_data(self) -> pd.DataFrame:
        holdup = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Holdup[$]")
        bottom_md = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].MSD[$]")
        bottom_tvd = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].TVD[$]")
        total_noslip_velocity = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].VlTotl[$]")
        diameter = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].DiaInt[$]")
        angle = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Angle[$]")
        v_sup_gas = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Vgnslp[$]")
        v_sup_liq = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Vlnslp[$]")
        rho_mix = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].RhoMix[$]")
        mu_gas = (
            self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].FmuGas[$]") * 0.001
        )  # Convert from mPa.s to kg/m-s
        mu_liq = (
            self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].FmuLiq[$]") * 0.001
        )  # Convert from mPa.s to kg/m-s
        v_slip_liq = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Vlslip[$]")
        v_slip_gas = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Vgslip[$]")
        rho_liq = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].RhoLiq[$]")
        rho_gas = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].RhoGas[$]")
        holdup = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Holdup[$]")
        pressure = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Pres[$]")
        temperature = self.DoGet("PROSPER.OUT.GRD.Results[0][0][0].Temp[$]")

        df = pd.DataFrame(
            {
                "bottom_md": bottom_md,
                "bottom_tvd": bottom_tvd,
                "holdup": holdup,
                "diameter": diameter,
                "angle": angle,
                "rho_liq": rho_liq,
                "mu_liq": mu_liq,
                "rho_mix": rho_mix,
                "mu_gas": mu_gas,
                "rho_gas": rho_gas,
                "presure": pressure,
                "temperature": temperature,
                "v_sup_liq": v_sup_liq,
                "v_sup_gas": v_sup_gas,
                "v_slip_liq": v_slip_liq,
                "v_slip_gas": v_slip_gas,
                "v_total_noslip": total_noslip_velocity,
            }
        )
        # Add mixture properties
        df["v_mix"] = v_sup_liq + v_sup_gas
        df["mu_mix"] = np.where(
            df["v_mix"] == 0,
            np.nan,
            (df["mu_liq"] * df["v_sup_liq"] + df["mu_gas"] * df["v_sup_gas"])
            / df["v_mix"],
        )

        df = df[
            (df["v_slip_liq"] + df["v_slip_gas"]) != 0
        ].copy()  # Remove rows where velocity is zero

        return df
