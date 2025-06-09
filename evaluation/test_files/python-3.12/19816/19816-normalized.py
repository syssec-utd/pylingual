def prebuild_model(metamodel):
    """
    Transform textual OAL actions in a ooaofooa *metamodel* to instances in the
    subsystems Value and Body. Instances of the following classes are supported:
    
    - S_SYNC
    - S_BRG
    - O_TFR
    - O_DBATTR
    - SM_ACT
    - SPR_RO
    - SPR_RS
    - SPR_PO
    - SPR_PS
    """
    for kind in ['S_SYNC', 'S_BRG', 'O_TFR', 'O_DBATTR', 'SM_ACT', 'SPR_RO', 'SPR_RS', 'SPR_PO', 'SPR_PS']:
        for inst in metamodel.select_many(kind):
            if inst.Suc_Pars:
                prebuild_action(inst)