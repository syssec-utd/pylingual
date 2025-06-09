from thespian.actors import ActorSystem
import sys
if __name__ == '__main__':
    portnum = int(sys.argv[1])
    addrmv = sys.argv[2]
    assert addrmv in '+-'
    cap = sys.argv[3]
    asys = ActorSystem('multiprocTCPBase', {'Admin Port': portnum})
    asys.updateCapability(cap, True if addrmv == '+' else None)