package dspCG;

/**
 * Computes the correlation function between two functions
 *
 * @author Chris Graziano
 */
public class Correlator {
  /**
   * Constructs a correlator to create the correlation function
   * @param float[] f input signal, sliding signal
   * @param float[] g input signal, stationary signal 
   * @return float[] of the correlation function
   */
  public Correlator(float[] f, float[] g) {
    //make sure f is the smaller sequence
    if (f.length>=g.length) {
      nf = g.length;
      ng = f.length;
      this.f = g;
      this.g = f;
    }
    else {
      nf = f.length;
      ng = g.length;
      this.f = f;
      this.g = g;
    }

    nlag = ng+nf-1;
    cor = new float[nlag];//the correlation function

  }
  public float[] correlate() {
    for (int lag=0; lag<nf; ++lag) {
      for (int l=0; ((l<=lag) && (l<nf)); ++l){
        cor[lag] += f[nf-1-l]*g[l]; 
      }
    } 
    for (int lag=nf; lag<ng; ++lag) {
      for (int l=0; l<nf; ++l){
        cor[lag] += f[nf-1-l]*g[lag-l]; 
      }
    } 
    for (int lag=ng; lag<nlag; ++lag) {
      for (int l=0, k=1; l<nlag-lag; ++l, ++k) {
        cor[lag] += f[l]*g[ng-k]; 
      }
    } 
    return cor;

  }
  private int nlag,nf,ng;
  private float[] cor,f,g;


}

