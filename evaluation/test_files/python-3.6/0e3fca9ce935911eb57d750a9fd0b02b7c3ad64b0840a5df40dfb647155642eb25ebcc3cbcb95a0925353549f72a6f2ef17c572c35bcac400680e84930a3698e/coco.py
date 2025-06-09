"""*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file coco.py                                        *
  * Example for the use of the Python language          *
  * (Complete Coco Problem.                             *
  *  Specify phase by PHASE parameter.                  *
  *  Data input in the model, not via data files.)      *
  *                                                     *
  * (c) 2018 Fair Isaac Corporation                     *
  *******************************************************"""
from __future__ import print_function
import xpress as xp
PHASE = 5
'* Phase = 3: Multi-period parameterised model; mines always open\n   * Phase = 4: Mines may open/closed freely; when closed save 20000 per month\n   * Phase = 5: Once closed always closed; larger saving\n'
NT = 4
RP = [0, 1]
RF = [0, 1]
RR = [0, 1]
RT = [i for i in range(NT)]
CPSTOCK = 2.0
CRSTOCK = 1.0
MXRSTOCK = 300
Post = [i for i in range(0, NT + 1)]
make = xp.vars(RP, RF, RT, name='make')
sell = xp.vars(RP, RF, RT, name='sell')
buy = xp.vars(RR, RF, RT, name='buy')
pstock = xp.vars(RP, RF, Post, name='pst')
rstock = xp.vars(RR, RF, Post, name='rst')
openm = xp.vars(RF, RT, name='openm', vartype=xp.binary)
REV = [[400, 380, 405, 350], [410, 397, 412, 397]]
CMAKE = [[150, 153], [75, 68]]
CBUY = [[100, 98, 97, 100], [200, 195, 198, 200]]
COPEN = [50000, 63000]
REQ = [[1.0, 0.5], [1.3, 0.4]]
MXSELL = [[650, 600, 500, 400], [600, 500, 300, 250]]
MXMAKE = [400, 500]
PSTOCK0 = [[50, 100], [50, 50]]
RSTOCK0 = [[100, 150], [50, 100]]
prob = xp.problem()
prob.addVariable(make, buy, sell, pstock, rstock, openm)
MaxProfit = xp.Sum((REV[p][t] * sell[p, f, t] for p in RP for f in RF for t in RT)) - xp.Sum((CMAKE[p][f] * make[p, f, t] for p in RP for f in RF for t in RT)) - xp.Sum((CBUY[r][t] * buy[r, f, t] for r in RR for f in RF for t in RT)) - xp.Sum((CPSTOCK * pstock[p, f, t] for p in RP for f in RF for t in range(1, NT + 1))) - xp.Sum((CRSTOCK * rstock[r, f, t] for r in RR for f in RF for t in range(1, NT + 1)))
if PHASE == 4:
    MaxProfit -= xp.Sum(((COPEN[f] - 20000) * openm[f, t] for f in RF for t in RT))
elif PHASE == 5:
    MaxProfit -= xp.Sum((COPEN[f] * openm[f, t] for f in RF for t in RT))
prob.setObjective(MaxProfit, sense=xp.maximize)
prob.addConstraint((pstock[p, f, t + 1] == pstock[p, f, t] + make[p, f, t] - sell[p, f, t] for p in RP for f in RF for t in RT))
prob.addConstraint((rstock[r, f, t + 1] == rstock[r, f, t] + buy[r, f, t] - xp.Sum((REQ[p][r] * make[p, f, t] for p in RP)) for r in RR for f in RF for t in RT))
prob.addConstraint((xp.Sum((make[p, f, t] for p in RP)) <= MXMAKE[f] * openm[f, t] for f in RF for t in RT))
prob.addConstraint((xp.Sum((sell[p, f, t] for f in RF)) <= MXSELL[p][t] for p in RP for t in RT))
prob.addConstraint((xp.Sum((rstock[r, f, t] for r in RR)) <= MXRSTOCK for f in RF for t in range(NT)))
if PHASE == 5:
    prob.addConstraint((openm[f, t + 1] <= openm[f, t] for f in RF for t in range(NT - 1)))
prob.addConstraint((pstock[p, f, 1] == PSTOCK0[p][f] for p in RP for f in RF))
prob.addConstraint((rstock[r, f, 1] == RSTOCK0[r][f] for r in RR for f in RF))
if PHASE < 4:
    prob.addConstraint((openm[f, t] == 1 for f in RF for t in RT))
prob.optimize()
print('Solution:\n Objective: ', prob.getObjVal())
hline = 60 * '-'
print('Total profit: ', prob.getObjVal())
print(hline)
print(8 * ' ', 'Period', end='')
for t in range(NT + 1):
    print('{:8}'.format(t), end='')
print('\n', hline)
print('Finished products\n', '=================')
for f in RF:
    print(' Factory', f)
    for p in RP:
        print(3 * ' ', 'P', p, ':  Prod', 12 * ' ', end='', sep='')
        for t in RT:
            print('{:8.2f}'.format(prob.getSolution(make[p, f, t])), end='')
        print('')
        print(8 * ' ', 'Sell', 12 * ' ', end='', sep='')
        for t in RT:
            print('{:8.2f}'.format(prob.getSolution(sell[p, f, t])), end='')
        print('')
        print(7 * ' ', '(Stock)', end='')
        for t in range(NT + 1):
            print('  (', '{:4.1f}'.format(prob.getSolution(pstock[p, f, t])), ')', end='', sep='')
        print('')
print(hline)
print('Raw material\n', '============')
for f in RF:
    print(' Factory', f)
    for r in RR:
        print(3 * ' ', 'R', r, ':  Buy', 12 * ' ', end='', sep='')
        for t in RT:
            print('{:8.2f}'.format(prob.getSolution(buy[r, f, t])), end='')
        print('')
        print(8 * ' ', 'Use', 12 * ' ', end='', sep='')
        for t in RT:
            print('{:8.2f}'.format(sum((REQ[p][r] * prob.getSolution(make[p, f, t]) for p in RP))), end='')
        print('')
        print(7 * ' ', '(Stock)', end='')
        for t in range(NT + 1):
            print(' (', '{:4.1f}'.format(prob.getSolution(rstock[r, f, t])), ')', end='', sep='')
        print('')
print(hline)