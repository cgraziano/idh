#############################################################################
# Demo nmo stretch

from imports import *

from edu.mines.jtk.dsp.Conv import *
from warp import WaveletNmo,WarpedWavelet,ShapingFilter
from data import SUDataGrabber

#############################################################################

#pngDir = "./png"
pngDir = None

def main(args):
  #goCmpGatherWithKnownWavelet()
  #goEstimateWaveletForOneOffset()
  #goEstimateWaveletFromCmpGather()
  #goEstimateWaveletFromOzGather()
  #goEstimateWaveletFromVikingGrabenGather()
  goEstimateWaveletForOneOffsetVikingGraben()

def goEstimateWaveletFromVikingGrabenGather():
  """ Estimates wavelet from Viking Graben data """
  fileLoc = "C:/Users/Chris/Documents/CWP/Research/research/vikinggrabenCMP/cdp=1300.strip"
  st = Sampling(1500,0.004,0.0); nt,dt,ft = st.count,st.delta,st.first
  sx = Sampling(60,0.0125,3.275); nx,dx,fx = sx.count,sx.delta,sx.first
  vnmo = 2.0 
  hp = SUDataGrabber.grab2DFile(fileLoc, nx, nt)
  na,ka = 11,0 # sampling for inverse wavelet a
  nh,kh = 201,-50 # sampling for wavelet h
  wn = WaveletNmo(st,sx,vnmo)
  a = wn.getInverseA(na,ka,hp) # estimate inverse wavelet
  h = wn.getWaveletH(na,ka,a,nh,kh); # estimate wavelet
  g = wn.applyHNmoA(na,ka,a,nh,kh,h,hp)
  e = wn.applyNmo(hp)

  print "a ="; dump(a);
  tmin = st.first
  tmax = st.first+st.count*st.delta
  perc = 98.0
  plotGather(st,sx,hp,tmin=tmin,tmax=tmax,perc=perc,title="input gather")
  plotGather(st,sx,e,tmin=tmin,tmax=tmax,perc=perc,title="conventional NMO")
  plotGather(st,sx,g,tmin=tmin,tmax=tmax,perc=perc,title="improved NMO")
  

def goEstimateWaveletFromOzGather():
  """ Estimates wavelet from one of Oz Yilmaz's gathers """
  name = "oz30"
  if name is "oz16":
    st = Sampling(1325,0.004,0.004); nt,dt,ft = st.count,st.delta,st.first
    sx = Sampling(  48,0.025,0.233); nx,dx,fx = sx.count,sx.delta,sx.first
    vnmo = 1.90 # NMO velocity
  elif name is "oz30":
    st = Sampling(2175,0.004,0.00400); nt,dt,ft = st.count,st.delta,st.first
    sx = Sampling(  96,0.025,0.23075); nx,dx,fx = sx.count,sx.delta,sx.first
    vnmo = 1.60 # NMO velocity
  f = zerofloat(nt,nx)
  ais = ArrayInputStream("/data/seis/oz/"+name+".F")
  ais.readFloats(f)
  ais.close()
  f = tpow(3.0,st,f)
  na,ka = 11,0 # sampling for inverse wavelet a
  nh,kh = 201,-50 # sampling for wavelet h
  wn = WaveletNmo(st,sx,vnmo)
  a = wn.getInverseA(na,ka,f) # estimate inverse wavelet
  h = wn.getWaveletH(na,ka,a,nh,kh); # estimate wavelet
  g = wn.applyHNmoA(na,ka,a,nh,kh,h,f)
  e = wn.applyNmo(f)
  print "a ="; dump(a);
  tmin,tmax,perc = 2.5,3.0,98.0
  plotGather(st,sx,f,tmin=tmin,tmax=tmax,perc=perc,title="input gather")
  plotGather(st,sx,e,tmin=tmin,tmax=tmax,perc=perc,title="conventional NMO")
  plotGather(st,sx,g,tmin=tmin,tmax=tmax,perc=perc,title="improved NMO")
  #plotSequence(Sampling(na,st.delta,ka*st.delta),normalize(a),title="inverse")
  plotSequence(Sampling(nh,st.delta,kh*st.delta),normalize(h),
               title="estimated wavelet")

def goEstimateWaveletFromCmpGather():
  """ Estimates wavelet from a CMP gather """
  st = Sampling(501,0.004,0.0); nt,dt,ft = st.count,st.delta,st.first
  sx = Sampling(201,0.010,0.0); nx,dx,fx = sx.count,sx.delta,sx.first
  nref,vnmo = 100,2.0 # number of reflectors and NMO velocity
  freq,decay = 30.0,0.1 # peak frequency and decay for wavelet
  p = makeCmpReflections(vnmo,nref,st,sx) # cmp gather without wavelet
  f = addArWavelet(freq,decay,st,sx,p) # cmp gather with wavelet
  plotGather(st,sx,f,"CMP gather")
  na,ka = 11,-5 # sampling for inverse wavelet a
  ak = zerofloat(na) # array for the known inverse wavelet a
  r,w = exp(-decay),2.0*PI*freq*st.delta # radius and frequency of poles
  a1,a2 = -2.0*r*cos(w),r*r # coefficients for inverse wavelet
  ak[0-ka] = 1.0
  ak[1-ka] = a1
  ak[2-ka] = a2
  wn = WaveletNmo(st,sx,vnmo)
  ae = wn.getInverseA(na,ka,f) # the estimated inverse wavelet
  nh,kh = 100,-20 # sampling for wavelet h
  for a in [ak,ae]:
    if a is ak:
      title = "known wavelet"
    else:
      title = "estimated wavelet"
    print title
    h = wn.getWaveletH(na,ka,a,nh,kh);
    plotSequence(Sampling(nh,st.delta,kh*st.delta),normalize(h),title=title)
    g = wn.applyHNmoA(na,ka,ak,nh,kh,h,f)
    plotGather(st,sx,g,"NMO with "+title)

def goEstimateWaveletForOneOffsetVikingGraben():
  """ Estimates wavelet from a non-zero-offset and zero-offset trace """
  fileLoc = "C:/Users/Chris/Documents/CWP/Research/research/vikinggrabenCMP/cdp=1300.strip"
  st = Sampling(1500,0.004,0.0); nt,dt,ft = st.count,st.delta,st.first
  sx = Sampling(60,0.049,.262); nx,dx,fx = sx.count,sx.delta,sx.first
  vnmo = 2.0 # NMO velocity
  freq,decay = 30.0,0.1 # peak frequency and decay for wavelet


  ixx,ixy = 59,0 # indices for non-zero-offset and zero-offset traces
  offset = sx.getValue(ixx) # the non-zero offset

  hp = SUDataGrabber.grab2DFile(fileLoc, nx, nt)
  axx = zerofloat(nt)
  shp = applyNmo(vnmo,st,sx,hp)

  x,y = hp[ixx],hp[ixy] # x is non-zero-offset trace; y is zero-offset trace
  na,ka = 11,-5 # number of samples and index of 1st sample for inverse
  ak = zerofloat(na) # array for the known inverse wavelet a
  r,w = exp(-decay),2.0*PI*freq*st.delta # radius and frequency of poles
  a1,a2 = -2.0*r*cos(w),r*r # coefficients for inverse wavelet
  ak[0-ka] = 1.0
  ak[1-ka] = a1
  ak[2-ka] = a2
  ww = WarpedWavelet(WarpedWavelet.Nmo(st,offset,vnmo))
  ae = ww.estimateInverse(na,ka,x,y) # the estimated wavelet inverse
  tmin = st.first
  tmax = st.first+st.count*st.delta
  perc = 98.0
  for a in [ak,ae]:
    print 'ak = '+ str(ak)
    print 'ae = '+ str(ae)
    if a is ak:
      title = "known wavelet"
    else:
      title = "estim. wavelet"
    print title
    ax = zerofloat(nt)
    ay = zerofloat(nt)
    conv(na,ka,a,nt,0,x,nt,0,ax)
    conv(na,ka,a,nt,0,y,nt,0,ay)
    sax = applyNmo1(offset,vnmo,st,ax)
    rms = sqrt(sum(pow(sub(ay,sax),2))/nt)
    print "a = ",; dump(a)
    print "rms error =",rms
    nh,kh = 100,-20 # number of samples, index of 1st sample for wavelet h
    h = ww.estimateWavelet(na,ka,a,nh,kh);
    wn = WaveletNmo(st,sx,vnmo)
    g = wn.applyHNmoA(na,ka,a,nh,kh,h,hp)
    plotSequence(Sampling(nh,st.delta,kh*st.delta),normalize(h),title=title)
    plotGather(st,sx,g,tmin=tmin,tmax=tmax,perc=perc,title=title+" improved nmo, "+str(ixy) + ","+ str(ixx))


   
  #hsax = zerofloat(nt)
  #conv(nh,kh,h,nt,0,sax,nt,0,hsax)
  #sx = applyNmo1(offset,vnmo,st,x)
  #plotSequence(st,x,3.0,"x")
  #plotSequence(st,sx,3.0,"sx")
  #plotSequence(st,hsax,3.0,"hsax")
  #plotSequence(st,y,3.0,"y")
  plotGather(st,sx,hp,tmin=tmin,tmax=tmax,perc=perc,title="input gather")
  plotGather(st,sx,shp,tmin=tmin,tmax=tmax,perc=perc,title="conventional nmo")
  #plotGather(st,sx,e,tmin=tmin,tmax=tmax,perc=perc,title="conventional NMO")
  #plotGather(st,sx,g,tmin=tmin,tmax=tmax,perc=perc,title="improved NMO")
def goEstimateWaveletForOneOffset():
  """ Estimates wavelet from a non-zero-offset and zero-offset trace """
  st = Sampling(501,0.004,0.0); nt,dt,ft = st.count,st.delta,st.first
  sx = Sampling(201,0.010,0.0); nx,dx,fx = sx.count,sx.delta,sx.first
  nref,vnmo = 100,2.0 # number of reflectors and NMO velocity
  freq,decay = 30.0,0.1 # peak frequency and decay for wavelet
  p = makeCmpReflections(vnmo,nref,st,sx) # cmp gather without wavelet
  hp = addArWavelet(freq,decay,st,sx,p) # cmp gather with wavelet
  ixx,ixy = 1,0 # indices for non-zero-offset and zero-offset traces
  offset = sx.getValue(ixx) # the non-zero offset
  x,y = hp[ixx],hp[ixy] # x is non-zero-offset trace; y is zero-offset trace
  na,ka = 11,-5 # number of samples and index of 1st sample for inverse
  ak = zerofloat(na) # array for the known inverse wavelet a
  r,w = exp(-decay),2.0*PI*freq*st.delta # radius and frequency of poles
  a1,a2 = -2.0*r*cos(w),r*r # coefficients for inverse wavelet
  ak[0-ka] = 1.0
  ak[1-ka] = a1
  ak[2-ka] = a2
  ww = WarpedWavelet(WarpedWavelet.Nmo(st,offset,vnmo))
  ae = ww.estimateInverse(na,ka,x,y) # the estimated wavelet inverse
  for a in [ak,ae]:
    if a is ak:
      title = "known wavelet"
    else:
      title = "estimated wavelet"
    print title
    ax = zerofloat(nt)
    ay = zerofloat(nt)
    conv(na,ka,a,nt,0,x,nt,0,ax)
    conv(na,ka,a,nt,0,y,nt,0,ay)
    sax = applyNmo1(offset,vnmo,st,ax)
    rms = sqrt(sum(pow(sub(ay,sax),2))/nt)
    print "a = ",; dump(a)
    print "rms error =",rms
    nh,kh = 100,-20 # number of samples, index of 1st sample for wavelet h
    h = ww.estimateWavelet(na,ka,a,nh,kh);
    plotSequence(Sampling(nh,st.delta,kh*st.delta),normalize(h),title=title)
  return
  hsax = zerofloat(nt)
  conv(nh,kh,h,nt,0,sax,nt,0,hsax)
  sx = applyNmo1(offset,vnmo,st,x)
  plotSequence(st,x,3.0,"x")
  plotSequence(st,sx,3.0,"sx")
  plotSequence(st,hsax,3.0,"hsax")
  plotSequence(st,y,3.0,"y")

def goCmpGatherWithKnownWavelet():
  n = 501
  st = Sampling(501,0.004,0.0)
  sx = Sampling(201,0.010,0.0)
  nref,vnmo = 100,2.0
  freq,decay = 30.0,0.1
  p = makeCmpReflections(vnmo,nref,st,sx)
  hp = addArWavelet(freq,decay,st,sx,p)
  shp = applyNmo(vnmo,st,sx,hp)
  sp = applyNmo(vnmo,st,sx,p)
  hsp = addArWavelet(freq,decay,st,sx,sp)
  #plotGather(st,sx,p)
  plotGather(st,sx,hp,"CMP gather")
  plotGather(st,sx,shp,"NMO with wavelet distortion")
  plotGather(st,sx,hsp,"Reduced wavelet distortion")

def tpow(power,st,f):
  """Applies t^power gain."""
  nt,dt,ft = st.count,st.delta,st.first
  nx = len(f)
  tp = pow(rampfloat(ft,dt,nt),power) # sampled times raised to power
  g = zerofloat(nt,nx)
  for ix in range(nx):
    mul(tp,f[ix],g[ix])
  return g

def normalize(h):
  return div(h,max(h))

def estimateInverseWavelet(na,ka,offset,vnmo,st,x,y):
  nmo = WarpedWavelet.Nmo(st,offset,vnmo)
  ww = WarpedWavelet(nmo)
  a = ww.estimateInverse(na,ka,x,y)
  return a

def applyNmo1(offset,vnmo,st,p):
  q = zerofloat(st.count)
  nmo = WarpedWavelet.Nmo(st,offset,vnmo)
  nmo.apply(p,q)
  return q

def plotGather(st,sx,p,tmin=None,tmax=None,perc=None,title=None):
  sp = SimplePlot(SimplePlot.Origin.UPPER_LEFT)
  if title:
    sp.setTitle(title)
  sp.setHLabel("Offset (km)")
  sp.setVLabel("Time (s)")
  sp.setSize(400,750)
  if tmin and tmax:
    sp.setVLimits(tmin,tmax)
  pv = sp.addPixels(st,sx,p)
  if perc:
    pv.setPercentiles(100-perc,perc)

def plotSequence(s,x,xmax=None,title=None):
  sp = SimplePlot.asPoints(s,x)
  if xmax:
    sp.setVLimits(-xmax,xmax)
  if title:
    sp.setTitle(title)

def applyNmo(vel,st,sx,p):
  nt,nx = st.count,sx.count
  dt,dx = st.delta,sx.delta
  ft,fx = st.first,sx.first
  t0 = add(0.01*dt,rampfloat(ft,dt,nt))
  q = copy(p)
  si = SincInterp.fromErrorAndFrequency(0.01,0.4)
  for jx in range(nx):
    xj = sx.getValue(jx)
    cj = (xj*xj)/(vel*vel)
    ti = sqrt(add(mul(t0,t0),cj))
    si.interpolate(nt,dt,ft,p[jx],nt,ti,q[jx])
    q[jx] = mul(q[jx],div(t0,ti))
  return q

def makeCmpReflections(vel,nref,st,sx):
  nt,nx = st.count,sx.count
  dt,dx = st.delta,sx.delta
  ft,fx = st.first,sx.first
  p = zerofloat(nt,nx)
  ts = add(ft,mul((nt-1)*dt,randfloat(nref)))
  rs = sub(mul(2.0,randfloat(nref)),1.0)
  si = SincInterp.fromErrorAndFrequency(0.01,0.45)
  for jx in range(nx):
    xj = sx.getValue(jx)
    cj = (xj*xj)/(vel*vel)
    for jr in range(nref):
      tj = ts[jr]
      rj = rs[jr]
      tj = sqrt(tj*tj+cj)
      si.accumulate(tj,rj,nt,dt,ft,p[jx])
  return p

def addArWavelet(fpeak,decay,st,sx,p):
  r = exp(-decay)
  w = 2.0*PI*fpeak*st.delta
  a1,a2 = -2.0*r*cos(w),r*r
  #print "a1 =",a1," a2 =",a2
  poles = [Cdouble.polar(r,w),Cdouble.polar(r,-w)]
  zeros = []
  gain = 1.0
  x = copy(p)
  rcf = RecursiveCascadeFilter(poles,zeros,gain)
  rcf.apply1Forward(p,x)
  return x

def makeRandomEvents(n,seed=0):
  if seed!=0:
    r = Random(seed)
  else:
    r = Random()
  return pow(mul(2.0,sub(randfloat(r,n),0.5)),9.0)

#############################################################################
# Do everything on Swing thread.

class RunMain(Runnable):
  def run(self):
    main(sys.argv)
SwingUtilities.invokeLater(RunMain())
