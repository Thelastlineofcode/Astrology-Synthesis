#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

FILE *f1=NULL, *f2=NULL;
int size1=0, size2=0, pos1=0, pos2=0;
char *buf1=NULL, *buf2=NULL, city1[256]="", city2[256]="", line2[1024]="";
int i=0, j=0, k=0, l=0, start=0, found=0, counter=1, allcount=0, curcount=0,
    len1=0, len2=0;
unsigned char *indexa=NULL;


count_all_cities()
{
  for (pos2=0; pos2<size2 && !found; pos2++)
  {
    if ( buf2[pos2] == '\n' || buf2[pos2] == 0 ) allcount++;
  }
  indexa = malloc( allcount+10 ); 
  memset( indexa, 0, allcount+10 );
}


find_in_cities2()
{
  fprintf(stderr, "[%i] searching for %s...", counter++, city1);
  len1 = strlen( city1 );
  for (k=len1-1; k>=0; k--)
  {
    if (city1[k]==' ' || city1[k]=='^' || city1[k]==0)
      city1[k] = 0;
    else break;
  }
  len1 = strlen(city1);
  
  for (pos2=j=k=found=curcount=0; pos2<size2; pos2++)
  {
    if ( buf2[pos2] == '\n' || buf2[pos2] == 0 )
    {
      curcount++;
      line2[j++] = 0;
      j=0;
      if ( indexa[curcount] ) continue;
      for (start=k=l=0; k<strlen(line2); k++)
      {
	if ( start==1 && line2[k]==',' )
	{
	  city2[l++] = 0;
	  l=0;
	  len2 = strlen( city2 );
	  if ( len1==len2 && strcmp(city1, city2)==0 )
	  {
	    found++;
	    indexa[curcount] = 1;
	    printf( "%s\n", line2 );
	  }
	  continue;
	}
        if ( line2[k]==',' )
	{
	  start=1;
	  continue;
	}
	if (start) city2[l++] = line2[k];
      }
      continue;
    }
    line2[j++] = buf2[pos2];
  }
  fprintf(stderr, "%i new\n", found);
}


int
main( int argc, char *argv[] )
{

  f1 = fopen( "150", "r" );
  f2 = fopen( "cities.txt", "r" );
  
  fseek( f1, 0, SEEK_END );
  fseek( f2, 0, SEEK_END );
  size1 = ftell( f1 );
  size2 = ftell( f2 );
  fseek( f1, 0, SEEK_SET );
  fseek( f2, 0, SEEK_SET );

  buf1 = malloc( size1+1 );
  buf2 = malloc( size2+1 );

  fread( buf1, 1, size1, f1 );
  fread( buf2, 1, size2, f2 );
 
  count_all_cities();
  fprintf(stderr, "allcount=%i\n", allcount);

  for (i=j=k=l=pos1=pos2=0; pos1<size1; pos1++)
  {
    if ( buf1[pos1] == '\n' || buf1[pos1] == 0 )
    {
      city1[i++] = 0;
      i=0;
      if ( strlen(city1) <= 0 ) continue;
      find_in_cities2();
      continue;
    }
    city1[i++] = buf1[pos1];
  }
  
  free(buf1);
  free(buf2);

  return 0;
}

