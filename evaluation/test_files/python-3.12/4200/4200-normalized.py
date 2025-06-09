def _define(self):
    """
        gate ch a,b {
        h b;
        sdg b;
        cx a,b;
        h b;
        t b;
        cx a,b;
        t b;
        h b;
        s b;
        x b;
        s a;}
        """
    definition = []
    q = QuantumRegister(2, 'q')
    rule = [(HGate(), [q[1]], []), (SdgGate(), [q[1]], []), (CnotGate(), [q[0], q[1]], []), (HGate(), [q[1]], []), (TGate(), [q[1]], []), (CnotGate(), [q[0], q[1]], []), (TGate(), [q[1]], []), (HGate(), [q[1]], []), (SGate(), [q[1]], []), (XGate(), [q[1]], []), (SGate(), [q[0]], [])]
    for inst in rule:
        definition.append(inst)
    self.definition = definition