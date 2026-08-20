"""earthquake.usgs.gov returns 403 to the research UA from the very first request, while
an impossible path on the same host returns 404 - so the pair separates and it is a
block, not a rate limit and not exhaustion.

The remaining question is what the block is conditioned on, because the answer changes
what B3 should do: a UA-conditioned block means the host has chosen to exclude
identified automated clients, and those markets are simply unreachable by a compliant
client.  An IP-conditioned block would mean the vantage is suspect and every other
measurement from it needs re-checking.

This is a DIAGNOSTIC.  No browser user-agent is impersonated, and whatever it returns
does not license spoofing one.
"""
import subprocess,json
U='https://earthquake.usgs.gov/earthquakes/browse/'
IMP='https://earthquake.usgs.gov/__impossible_control_20260820__'
OTHER='https://earthquake.usgs.gov/fdsnws/event/1/version'
UAS=[('research','smart-money-research/1.0 (+B2 source-layer study; contact rogerlgk@gmail.com)'),
     ('curl-default',None),('empty','')]
def hit(u,ua):
    c=['curl','-sS','-o','/dev/null','-H','Expect:','--max-time','20','-w','%{http_code}']
    if ua is not None: c+=['-A',ua]
    c+=[u]
    r=subprocess.run(c,capture_output=True,text=True)
    return r.stdout.strip() or '-1'
print('%-14s %-10s %-10s %-10s'%('user-agent','target','impossible','fdsnws api'))
for lab,ua in UAS:
    print('%-14s %-10s %-10s %-10s'%(lab,hit(U,ua),hit(IMP,ua),hit(OTHER,ua)))
print()
print('control on a DIFFERENT usgs host with the research UA:')
for u in ['https://www.usgs.gov/','https://earthquake.usgs.gov/earthquakes/map/']:
    print('   %-52s %s'%(u,hit(u,UAS[0][1])))
