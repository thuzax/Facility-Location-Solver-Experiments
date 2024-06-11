/* 
================================================================================

FILE      Module Rnd.c

VERSION : 1.0
DATE    : 21 September 1998
LANGUAGE: C
AUTHOR  : Lionnel Maugis * Sofreavia / ATM 
          maugis@cenaath.cena.dgac.fr
          http://www.cenaath.cena.dgac.fr/~maugis 
          1, rue de Champagne - 91200 ATHIS-MONS
          Postal Address : Orly Sud 205 - 94542 ORLY AEROGARE CEDEX
SUBJECT : Portable Uniform Integer Random Number in [0-2^31] range
          Performs better than ansi-C rand() 
          D.E Knuth, 1994 - The Stanford GraphBase
================================================================================
*/

#define RANDOM()        (*rand_fptr >= 0 ? *rand_fptr-- : flipCycle ()) 
#define two_to_the_31   ((unsigned long)0x80000000) 
#define RREAL           ((double)RANDOM()/(double)two_to_the_31)
#define mod_diff(x,y)   (((x)-(y))&0x7fffffff) 

static long A[56]= {-1};
long *rand_fptr = A;

/* ---------------------------------------------------------------------------*/
long flipCycle()
{
  register long *ii,*jj;
  for (ii = &A[1], jj = &A[32]; jj <= &A[55]; ii++, jj++)
    *ii= mod_diff (*ii, *jj);

  for (jj = &A[1]; ii <= &A[55]; ii++, jj++)
    *ii= mod_diff (*ii, *jj);
  rand_fptr = &A[54];
  return A[55];
}

/* ---------------------------------------------------------------------------*/
void initRand (long seed)
{
  register long i;
  register long prev = seed, next = 1;
  seed = prev = mod_diff (prev,0);
  A[55] = prev;
  for (i = 21; i; i = (i+21)%55)
  {
    A[i] = next;
    next = mod_diff (prev, next);
    if (seed&1) seed = 0x40000000 + (seed >> 1);
    else seed >>= 1;
    next = mod_diff (next,seed);
    prev = A[i];
  }
	
  for (i = 0; i < 7; i++) flipCycle(); 
}
/* ---------------------------------------------------------------------------*/
long unifRand (long m)
{
  register unsigned long t = two_to_the_31 - (two_to_the_31%m);
  register long r;
  do {
    r = RANDOM();
  } while (t <= (unsigned long)r);
  return r%m;
}

/* ---------------------------------------------------------------------------*/
double URand ()
{
  double x;
  x = RREAL;
  return ( x );
}
