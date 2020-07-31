#dict of PROSPER on some features. Used to revert back from integer to string

#main dict in relation to variable name and sub dict:

mainDict={'PROSPER.SIN.SUM.FLUID':dFLUID,
'PROSPER.SIN.SUM.PVTMODEL':dPVTMODEL,
'PROSPER.SIN.SUM.EOSMODEL':dEOSMODEL,
'PROSPER.SIN.SUM.SEPARATOR':dSEPARATOR,
'PROSPER.SIN.SUM.EMULSION':dEMULSION,
'PROSPER.SIN.SUM.HYDRATE':dHYDRATE,
'PROSPER.SIN.SUM.FLOWTYPE':dFLOWTYPE,
'PROSPER.SIN.SUM.WELLTYPE':dWELLTYPE,
'PROSPER.SIN.SUM.LIFTMETHOD':dLIFTMETHOD,
'PROSPER.SIN.SUM.PREDICT':dPREDICT,
'PROSPER.SIN.SUM.TEMPMODEL':dTEMPMODEL,
'PROSPER.SIN.SUM.RANGE':dRANGE,
'PROSPER.SIN.SUM.OUTPUT':dOUTPUT,
'PROSPER.SIN.SUM.STEAM':dSTEAM,
'PROSPER.SIN.SUM.COMPLETION':dCOMPLETION,
'PROSPER.SIN.SUM.GRAVELPACK':dGRAVELPACK,
'PROSPER.SIN.SUM.GASCONING':dGASCONING,
'PROSPER.PVT.INPUT.PBCORR':dPB,
'PROSPER.PVT.INPUT.UOCORR':dVISCO,
'PROSPER.SIN.SUM.VisMod':dVISCOMOD,
'PROSPER.ANL.QLG.Dome':dDOMECORR, 
'PROSPER.ANL.QLG.InjPoint':dORIFICE,
'PROSPER.ANL.SYS.SolutionNode':dSOLNODE,
'PROSPER.ANL.SYS.RateType':dRATETYPE 
         }

#Sub dict with the relation between integer and description string:
dFLUID={0: 'Oil' ,1:'Gas' ,2:'Condensate'}
dPVTMODEL={0:'Black oil', 2:'EOS'}
dEOSMODEL={0:'Internal'}
dSEPARATOR={0:'Single stage',1:'Two stage'}
dEMULSION={0: 'Off', 1:'On'}
dHYDRATE={0: 'Off', 1:'On'}
dFLOWTYPE={0:'Tubing', 1:'Annular', 2:'Both'} 
dWELLTYPE={0:'Producer',1:'Injector',2:'Water injector'}
dLIFTMETHOD={ 0:'None',
          1:'Gas Lift (Continuous)',
          2:'Electric Submersible Pump',
          3:'Hydraulic Drive Downhole Pump',
          4:'Progressive Cavity Pump',
          5:'Coil Tubing Gas Lift',
          6:'Diluent Injection',
          7:'Jet Pump',
          8:'Multiphase Pump',
          9:'Sucker Rod Pump',
          10:'Gas Lift (Intermittent)'}

dPREDICT={0:'Pressure only' ,1:'Pressure and Temperature (Offshore)' ,2:'Pressure and Temperature (On land)'}
dTEMPMODEL={0:'Rough Approximation', 1: 'Enthaply Balance', 2: 'Improved Approximation'}
dRANGE={0:'Full system',1:'Pipeline only'}
dOUTPUT={0:'Output display off' ,1:'Output display on'}
dSTEAM={0: 'Off', 1:'On'}
dCOMPLETION={0: 'Cased hole', 1:'Open hole'}
dGRAVELPACK={0:'None',
   1:'Gravel pack',
   2:'Pre-packed screen',
   3:'Wire wrapped screen',
   4:'Slotted liner'}
dGASCONING={0: 'Flag off', 1:'Flag on'}

dCORR={ 'DunsandRosModified' :0
        ,'HagedornBrown':1
        ,'FancherBrown':2
        ,'MukerjeeBrill':4
        ,'BeggsandBrill':5
        ,'PetroleumExperts':8
        ,'Orkiszewski':9
        ,'PetroleumExperts2':10
        ,'DunsandRosOriginal':11
        ,'PetroleumExperts3':12
        ,'GREmodifiedbyPE':14
        ,'PetroleumExperts4':18
        ,'Hydro3P':19
        ,'PetroleumExperts5':20
        ,'PE6HeavyOil':21
        ,'Hydro2P':25
        ,'PE5Extended':27
        ,'OLGAS2P':28
        ,'OLGAS3P':29
        ,'OLGAS3PEXT':30
        ,'LedaFlow2P':31
        ,'LedaFlow3P':32
}

dPB={
    0:'Glaso'
    ,1:'Standing'
    ,2:'Lasater'
    ,3:'VazquezBeggs'
    ,4:'Petroskyetal'
    ,5:'AlMarhoun'
    ,6:'DeGhettoetalHeavyoil'   
}

dVISCO={
      0:'Bealetal'
    ,1:'Beggsetal'
    ,2:'Petroskyetal'
    ,3:'EgbogahetalHeavyOil'
    ,4:'BergmanSutton'
    ,5:'DeGhettoetalHeavyOil'
    ,6:'DeGhettoetalModified'
}

dVISCOMOD={0:'Newtonian'
          ,1:'Non Newtonian'}

dDOMECORR={0:'Dome pressure correction Off'
          ,1:'Dome pressure correction On'
          }

dORIFICE={0:'Orifice',
          1:'Venturi'}

dSOLNODE={3:'Wellhead',
         1:'Bottom node',
         2:'Top node'}

dRATETYPE={
         0:'Fluid rate',   
         1:'Oil rate',
         3:'HC mass flow rate',
         2:'Gas rate'
}


