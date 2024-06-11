/*----------------------------------------------------------------------------*/
/* FILE     : gencflp.c                                                       */
/* VERSION  : 1.0                                                             */
/* DATE     : July 13, 2000                                                   */
/* LANGUAGE : C                                                               */
/* AUTHOR   : Andreas Klose                                                   */
/*            Institute for Operations Research                               */
/*            University of St. Gallen                                        */
/*            Bodanstrasse 6, CH-9000 St. Gallen                              */
/*            andreas.klose@unisg.ch                                          */
/*----------------------------------------------------------------------------*/
/* SUBJECT  : program to generate CFLP test problems                          */
/*----------------------------------------------------------------------------*/
/* USAGE    : gencflp <inputfile> <path>                                      */
/*            - inputfile is an ascii file providing information about        */
/*              the test problem instances which "gencflp" should generate.   */
/*              This file must provide the following infomation:              */
/*              (1) Seed, i.e an integer number specifying the seed number    */
/*                  for the random number generator (if Seed=0 a seed number  */
/*                  is generated automatically)                               */
/*              (2) for every problem class:                                  */
/*                    #customers  #depot sites  ratio  problem name           */
/*                  where ratio is the desired ratio of total capacity to     */
/*                  total demand.                                             */
/*            - path is an optional argument specifying the output path       */
/*----------------------------------------------------------------------------*/    
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "rnd.h"

/*----------------------------------------------------------------------------*/
int    m,n,num;     /* number of customers, depots, instances                 */
int    *f, *d, *s;  /* fixed depot costs, demands and capacities              */
int    *x, *y;      /* coordinates                                            */
int    totd,totc;   /* total demand and total capacity                        */
char   name[512];   /* problem name                                           */
char   fname[512];  /* name of file where to store problem instance           */
double r;           /* r = totc/totd                                          */
time_t tt;

/*----------------------------------------------------------------------------*/

void gencusts( void )
/* generate customers with demand 5 + u[0,30] */
{
  int i;

  totd = 0;
  for (i=0;i<m;i++){
    d[i] = unifRand(31)+5;
    x[i] = unifRand(1000);
    y[i] = unifRand(1000);
    totd += d[i];
  }
}

/*----------------------------------------------------------------------------*/

void gendepots( void )
/* generate depots with capacity s[j] = 10 + u[0,150] and fixed cost 
   f[j] = (u[0,10] + 100)*sqrt(s[j])+u[0,90] */
{
  int j;
  double ff;
  double corr;

  totc = 0;
  for (j=0;j<n;j++){
    s[j] = unifRand(151)+10;
    ff   = (unifRand(10) + 100.0)*sqrt((double)s[j]) + unifRand(90) + 0.5;
    f[j] = (int) ff;
    x[j+m] = unifRand(1000);
    y[j+m] = unifRand(1000);
    totc += s[j];
  }

  corr = ( (double)totd/(double)totc)*r;
  totc = 0;
  for (j=0;j<n;j++){
    ff = s[j]*corr+0.5;
    s[j] = (int)ff;
    totc += s[j];
  }
}

/*----------------------------------------------------------------------------*/

void writeprob( void )
/* write problem to file */
{
  FILE   *out;
  double cost,dx,dy;
  int    *pdx, *pdy, *pcx, *pcy;
  int    i,j;

  time(&tt);
  out = fopen(fname,"wt");
  pcx = x, pcy = y;
  pdx = x+m, pdy = y+m;
  if ( n == m ) {
    pdx = x, pdy = y;
    pcx = x+n, pcy = y+n;
  }
  if ( out ){
    fprintf(out,"[CFLP-PROBLEMFILE]\n");
    fprintf(out,"%s %s","generated at: ",ctime(&tt));
    fprintf(out,"%s %-d %s %-d %s %-.2f\n","#customers:",m,"; #depot sites:",n, "; ratio:",r);
    fprintf(out,"\n[DEPOTS]\n");
    fprintf(out,"capacity fixcost varcost xcoord ycoord name\n");
    for (j=0;j<n;j++){
      fprintf(out,"%-d %-d %-s %-d %-d %-s%-d\n",s[j],f[j],"0",pdx[j],pdy[j],"Depot",j);
    }
    fprintf(out,"\n[CUSTOMERS]\n");
    fprintf(out,"demand xcoord ycoord name\n");
    for (i=0;i<m;i++){
      fprintf(out,"%-d %-d %-d %-s%-d\n",d[i],pcx[i],pcy[i],"Customer",i);
    }
    fprintf(out,"\n[COSTMATRIX]\n");
    fprintf(out,"c= d_eucli(a,b) * 0.01\n");
    fprintf(out,"[MATRIX]\n");
    fprintf(out,"%-s %-d %-d\n","Dim",n,m);
    for (j=0;j<n;j++){
      for (i=0;i<m;i++){
        dx = abs(x[i]-x[m+j]);
        dy = abs(y[i]-y[m+j]);
        cost = sqrt(dx*dx + dy*dy)*0.01*d[i];
        fprintf(out,"%-.4f ",cost);
      }
      fprintf(out,"\n");
    }
  }
  fclose(out);
}

/*----------------------------------------------------------------------------*/

int main(int argc, char **argv)
{
 char *Ext = ".cfl";
 char *nc;
 char path[256];
 char *slash = "/";
 int  count;
 int  goon;
 int  len;
 long seed;
 float ratio;
 FILE *file;

 
 printf("\n%s\n","=========================================================");
 printf("%s\n","       CFLP TEST PROBLEM GENERATOR           ");
 printf("%s\n","========================================================="); 
 printf("%s\n"," USAGE: input_file [path]");
 printf("%s\n","        input_file = input file");
 printf("%s\n","        path       = output directory (optional)");
 printf("%s\n","========================================================="); 
 printf("%s\n"," Structure of input file:");
 printf("%s\n"," (1) seed = seed for initializing random number generator");
 printf("%s\n","            (seed is selected automatically if seed<=0)");
 printf("%s\n"," (2) for every problem class:");
 printf("%s\n","       #customers  #depot sites  ratio  problem name");
 printf("%s\n","========================================================="); 
  
 strcpy(path,"");
 nc = (char *) calloc(10, sizeof(char));
 file = fopen(argv[1],"r");
 goon = (int)(file != NULL);
 if (goon){
   if (argc > 2){
     strcpy(path,argv[2]);
     len = strlen(path)-1;
     if ( path[len] != *slash ) strcat(path,slash);
   }
   goon = fscanf(file,"%d\n",&seed);
   if ( seed <= 0 ) {
     time(&tt);
     seed = (long)tt;
   }
   if (goon) initRand(seed);
 }
 while (goon > 0){
   goon = fscanf(file,"%d%d%f%d%s\n",&m,&n,&ratio,&num,name);
   r = (double)ratio;
   if (goon > 0){
     f = (int *) calloc(n, sizeof(int) );
     d = (int *) calloc(m, sizeof(int) );
     s = (int *) calloc(n, sizeof(int) );
     x = (int *) calloc(n+m, sizeof(int) );
     y = (int *) calloc(n+m, sizeof(int) );
     for (count=1;count<=num;count++){
       strcpy(fname,path);
       strcat(fname,name);
       gcvt((double)count,1,nc);
       strcat(fname,nc);
       strcat(fname,Ext);
       gencusts();
       gendepots();
       writeprob();
       printf("%s%d %s %s\n","Problem instance no.",count,"written to",fname);
     }
     free(f);
     free(d);
     free(s);
     free(x);
     free(y);
   }
 }  
 if ( file != NULL )  
   fclose(file);
 printf("%s%d\n","Terminated. Used seed number = ",seed); 

 return( 0 );
}

