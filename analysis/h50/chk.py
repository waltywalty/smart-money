import sys
ts=[int(l.split()[0]) for l in sys.stdin if l.strip() and l.split()[0].isdigit()]
print('n=',len(ts),'first',ts[0],'last',ts[-1])
exp=list(range(ts[0],ts[-1]+1,3600))
print('expected',len(exp))
miss=[t for t in exp if t not in set(ts)]
print('missing',miss)
d=set()
prev=None
for t in ts:
    if prev is not None and t-prev!=3600: d.add((prev,t))
    prev=t
print('irregular steps',d)
