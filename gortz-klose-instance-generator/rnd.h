/* 
================================================================================

FILE      Include file Rnd.h

VERSION : 1.0
DATE    : 21 September 1998
LANGUAGE: c 
AUTHOR  : Lionnel Maugis * Sofreavia / ATM 
          maugis@cenaath.cena.dgac.fr
          http://www.cenaath.cena.dgac.fr/~maugis 
          1, rue de Champagne - 91200 ATHIS-MONS
          Postal Address : Orly Sud 205 - 94542 ORLY AEROGARE CEDEX
SUBJECT : Interface to Rnd.c (random number generator)
================================================================================
*/

#ifdef __cplusplus
extern "C" {
#endif

void initRand (long seed);
/* initialize random number generator using seed "seed" */

long unifRand (long m);
/* return uniform integer random number in [0,m) */

double URand ();
/* return uniform real random number in [0,1) */

#ifdef __cplusplus
}
#endif