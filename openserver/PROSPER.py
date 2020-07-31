#dict of PROSPE on some features. Used to revert back from integer to string


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
#dLIFTTYPE[1]={}
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
