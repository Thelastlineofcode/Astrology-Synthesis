#include "stdio.h"	/* for stdout, stderr, perror */
#include "string.h"	/* for strcpy */
#include "sys/types.h"	/* for time_t */
#include "time.h"	/* for struct tm */
#include "stdlib.h"	/* for exit, malloc, atoi */
#include "float.h"	/* for FLT_MAX and DBL_MAX */
#include "ctype.h"	/* for isalpha et al. */
#include "math.h"

#ifndef TM_YEAR_BASE
#define TM_YEAR_BASE	1900
#endif /* !defined TM_YEAR_BASE */

#ifndef SQUARE
#define SQUARE(x) ((x)*(x))
#endif

#define ZONEFINDER_TEST 1


char	TZDir[256] = "./zoneinfo";

// hu,budapest,Budapest,05,47.5,19.0833333


void
print_tm( struct tm *tmp )
{
	printf("%04d-%02d-%02d %02d:%02d %s\n",
		TM_YEAR_BASE+tmp->tm_year, 1+tmp->tm_mon, tmp->tm_mday,
		tmp->tm_hour, tmp->tm_min, (tmp->tm_isdst ? "DST" : "NODST")
		);
}


void
get_zone_and_dst( char *country, double longitude, double latitude,
	int year, int month, int day, double localTime,
	double *zoneShift, int *dst )
{
	typedef enum	{ SECTION_NONE, SECTION_COUNTRY, SECTION_AFTER_COUNTRY,
			SECTION_LONGITUDE, SECTION_LATITUDE, SECTION_AFTER_LATITUDE,
			SECTION_ZONE, SECTION_CLOSED } seactionEnum;
	int		pos=0, l=0, section=SECTION_NONE, size=0;
	char		countryBuf[65]="", longBuf[65]="", latBuf[65]="", zoneBuf[65]="",
			bestZone[256]="", *tzEnv = "", sbuf[256], sbuf2[256]="",
			*buffer = NULL, co[4]="";
	FILE		*f = NULL;
	time_t		tLocal=0, tGMT=0;
	struct tm	tmLocal, tmGMT, tms;
	double		longZone=0, latZone=0, distance=0, closestDistance=1000000;
	
	if (country == NULL) return;
	if (zoneShift == NULL) return;
	if (dst == NULL) return;
	
	*zoneShift = 0;
	*dst = 0;
	
	// set "TZDIR" environment variable
	sprintf( sbuf, "TZDIR=%s", TZDir );
	putenv( sbuf );
	
	// get default value of "TZ" environment variable
	tzEnv = getenv( "TZ" );
	
	// convert country code to upper case characters
	co[0] = toupper( country[0] );
	co[1] = toupper( country[1] );
	co[2] = '\0';
	
	// open "zone.tab" and read content
	sprintf( sbuf, "%s/zone.tab", TZDir );
	f = fopen( sbuf, "r" );
	if (f == NULL) return;
	fseek( f, 0, SEEK_END );
	size = ftell( f );
	fseek( f, 0, SEEK_SET );
	buffer = malloc( size+2 );
	if (buffer == NULL)
	{
		fclose(f);
		return;
	}
	fread( buffer, size, 1, f );
	buffer[size] = '\0';
	fclose( f );
	
	// search the closest city to the given location+latitude in the given country
	section = SECTION_NONE;
	for (pos=l=0; pos<=size; pos++)
	{
		if ( buffer[pos]=='\n' || buffer[pos]=='\r' || buffer[pos]=='\0' )
		{
			if (section == SECTION_CLOSED)
			{
				countryBuf[0] = toupper( countryBuf[0] );
				countryBuf[1] = toupper( countryBuf[1] );
				if ( strcmp( countryBuf, co ) == 0 )
				{
					// convert longitude and latitude to double numbers
					// longitude
					sbuf2[0]  = longBuf[0];
					sbuf2[1]  = longBuf[1];
					sbuf2[2]  = longBuf[2];
					sbuf2[3]  = '\0';
					longZone  = atof( sbuf2 );
					sbuf2[0]  = longBuf[3];
					sbuf2[1]  = longBuf[4];
					sbuf2[2]  = '\0';\
					if (longZone >= 0) longZone += atof( sbuf2 ) / 60.0;
					else longZone -= atof( sbuf2 ) / 60.0;
					// latuitude
					sbuf2[0]  = latBuf[0];
					sbuf2[1]  = latBuf[1];
					sbuf2[2]  = latBuf[2];
					sbuf2[3]  = latBuf[3];
					sbuf2[4]  = '\0';
					latZone   = atof( sbuf2 );
					sbuf2[0]  = latBuf[4];
					sbuf2[1]  = latBuf[5];
					sbuf2[2]  = '\0';
					if (latZone >= 0) latZone += atof( sbuf2 ) / 60.0;
					else latZone -= atof( sbuf2 ) / 60.0;
					// calculate city distance
					distance = sqrt( SQUARE(longitude-longZone)+SQUARE(latitude-latZone) );
					if (distance < closestDistance)
					{
						closestDistance = distance;
						strcpy(bestZone, zoneBuf);
#ifdef ZONEFINDER_TEST
						printf("<DEBUG> CLOSEST: ");
#endif
					}
#ifdef ZONEFINDER_TEST
				printf("<DEBUG> %s:%0.2f:%0.2f:%s\n", countryBuf, longZone, latZone, zoneBuf);
#endif
				}
			}

			if ( buffer[pos+1] != '#' ) section = SECTION_COUNTRY;
			else section = SECTION_NONE;

			countryBuf[0] = '\0';
			longBuf[0]    = '\0';
			latBuf[0]     = '\0';
			zoneBuf[0]    = '\0';

			continue;
		}

		switch (section)
		{
			default:
				break;

			case SECTION_COUNTRY:
				countryBuf[l++] = buffer[pos];
				if (buffer[pos+1]==' ' || buffer[pos+1]=='\t')
				{
					countryBuf[l] = '\0';
					l = 0;
					section = SECTION_AFTER_COUNTRY;
				}
				break;

			case SECTION_AFTER_COUNTRY:
				if (buffer[pos+1]!=' ' && buffer[pos+1]!='\t')
					section = SECTION_LONGITUDE;
				break;

			case SECTION_LONGITUDE:
				longBuf[l++] = buffer[pos];
				if (buffer[pos+1]=='+' || buffer[pos+1]=='-')
				{
					longBuf[l] = '\0';
					l = 0;
					section = SECTION_LATITUDE;
				}
				break;

			case SECTION_LATITUDE:
				latBuf[l++] = buffer[pos];
				if (buffer[pos+1]==' ' || buffer[pos+1]=='\t')
				{
					latBuf[l] = '\0';
					l = 0;
					section = SECTION_AFTER_LATITUDE;
				}
				break;

			case SECTION_AFTER_LATITUDE:
				if (buffer[pos+1]!=' ' && buffer[pos+1]!='\t')
					section = SECTION_ZONE;
				break;

			case SECTION_ZONE:
				zoneBuf[l++] = buffer[pos];
				if (buffer[pos+1]==' ' || buffer[pos+1]=='\t' ||
				    buffer[pos+1]=='\n' || buffer[pos+1]=='\r')
				{
					zoneBuf[l] = '\0';
					l = 0;
					section = SECTION_CLOSED;
				}
				break;

		}
	}

#ifdef ZONEFINDER_TEST
	printf( "<DEBUG> bestZone=%s\n", bestZone );
#endif

	// set zone for TZ system
	sprintf( sbuf, "TZ=%s", bestZone );
	putenv( sbuf );
	
	// get TZ time for bestZone
	memset( &tms, 0, sizeof(tms) );
	tms.tm_year = year - TM_YEAR_BASE;
	tms.tm_mon  = month - 1;
	tms.tm_mday = day;
	tms.tm_hour = 24 * (int)(localTime/24);
	tms.tm_min  = (int)(60 * ((double)localTime - tms.tm_hour));
	tms.tm_sec  = (int)(3600 * ((double)localTime - tms.tm_hour - (double)tms.tm_min/60.0));
	tms.tm_isdst = 0;
	tLocal = mktime( &tms );
	localtime_r( &tLocal, &tmLocal );
	if ( tmLocal.tm_isdst )
	{
		tms.tm_isdst = 1;
		tLocal = mktime( &tms );
		localtime_r( &tLocal, &tmLocal );
	}
	
	*dst = tmLocal.tm_isdst;
	
	gmtime_r( &tLocal, &tmGMT );

print_tm( &tmLocal );
print_tm( &tmGMT );

	tGMT = mktime( &tmGMT );
	*zoneShift = (double)difftime( tLocal, tGMT );
	
	// set "TZ" environment variable back to original value
	sprintf( sbuf, "TZ=%s", ((tzEnv==NULL) ? "" : tzEnv) );
	putenv( sbuf );
	
	if (buffer) free(buffer);
}


int
main( int argc, char *argv[] )
{
	double		zoneShift=0;
	int		dst=0;
	
	get_zone_and_dst( "in", 22, 88, 1995, 8, 22, 12.5, &zoneShift, &dst );
	
	printf( "DST=%s, ZoneShift=%i\n", (dst?"yes":"no"), (int)zoneShift );

	return 0;
}


