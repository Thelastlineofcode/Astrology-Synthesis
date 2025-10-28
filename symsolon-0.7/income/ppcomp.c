/*
  The primary orbital elements are here denoted as: 

    N = longitude of the ascending node
    i = inclination to the ecliptic (plane of the Earth's orbit)
    w = argument of perihelion
    a = semi-major axis, or mean distance from Sun
    e = eccentricity (0=circle, 0-1=ellipse, 1=parabola)
    M = mean anomaly (0 at perihelion; increases uniformly with time)

  Related orbital elements are:

    w1 = N + w   = longitude of perihelion
    L  = M + w1  = mean longitude
    q  = a*(1-e) = perihelion distance
    Q  = a*(1+e) = aphelion distance
    P  = a ^ 1.5 = orbital period (years if a is in AU, astronomical units)
    T  = Epoch_of_M - (M(deg)/360_deg) / P  = time of perihelion
    v  = true anomaly (angle between position and perihelion)
    E  = eccentric anomaly

  One Astronomical Unit (AU) is the Earth's mean distance to the Sun,
  or 149.6 million km. When closest to the Sun, a planet is in perihelion,
  and when most distant from the Sun it's in aphelion. For the Moon, an
  artificial satellite, or any other body orbiting the Earth, one says
  perigee and apogee instead, for the points in orbit least and most
  distant from Earth.

  To describe the position in the orbit, we use three angles: Mean Anomaly,
  True Anomaly, and Eccentric Anomaly. They are all zero when the planet is
  in perihelion:

  Mean Anomaly (M): This angle increases uniformly over time, by 360 degrees
  per orbital period. It's zero at perihelion. It's easily computed from the
  orbital period and the time since last perihelion.

  True Anomaly (v): This is the actual angle between the planet and the
  perihelion, as seen from the central body (in this case the Sun).
  It increases non-uniformly with time, changing most rapidly at perihelion.

  Eccentric Anomaly (E): This is an auxiliary angle used in Kepler's Equation,
  when computing the True Anomaly from the Mean Anomaly and the orbital
  eccentricity. Note that for a circular orbit (eccentricity=0), these three
  angles are all equal to each other.

  Another quantity we will need is ecl, the obliquity of the ecliptic, i.e.
  the "tilt" of the Earth's axis of rotation (currently ca 23.4 degrees and
  slowly decreasing). First, compute the "d" of the moment of interest
  (section 3). Then, compute the obliquity of the ecliptic:

    ecl = 23.4393 - 3.563E-7 * d

*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


typedef enum { SUN=0, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO, PLANETS_MAX } PlanetType;

char *PlanetNames[] = { "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto" };
char *SignNames[] = { "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces" };

typedef struct PlanetStruct
{
	char	name[32];
	int		isSunCentered;
	// --- primary orbital elements ---
	double	N;	// longitude of the ascending node
	double	i;	// inclination to the ecliptic (plane of the Earth's orbit)
	double	w;	// argument of perihelion
	double	a;	// semi-major axis, or mean distance from Sun
	double	e;	// eccentricity (0=circle, 0-1=ellipse, 1=parabola)
	double	M;	// mean anomaly (0 at perihelion; increases uniformly with time)
	// --- releated orbital elements ---
	double	w1;	// = N + w   = longitude of perihelion
	double	L;	// = M + w1  = mean longitude
	double	q;	// = a*(1-e) = perihelion distance
	double	Q;	// = a*(1+e) = aphelion distance
	//double P;	// = a ^ 1.5 = orbital period (years if a is in AU, astronomical units)
	//double T;	// = Epoch_of_M - (M(deg)/360_deg) / P  = time of perihelion
	double	v;	// = true anomaly (angle between position and perihelion)
	double	E;	// = eccentric anomaly
	double	r;	// = rs = distance
	// --- polar coordinates ---
	double	longitude;
	double	latitude;
	double	distance;
	// --- geocentric cartesian coordinates ---
	double	x;
	double	y;
	double	z;
	// --- equatorial coordinates ---
	double	RA;
	double	Dec;
	double	er;
	// --- ecliptic coordinates ---
	double	Long;
	double	Lat;
} PlanetStruct;


typedef struct ObserverStruct
{
	// --- time of observation ---
	double	d;
	double	UT;
	// --- position of observation ---
	double	Long;
	double	Lat;
} ObserverStruct;



double
round_degree( double deg )
{
	deg = deg - ((int)(deg/360))*360;
	if ( deg < 0 ) deg += 360;
	return deg;
}


double
sinus( double deg )
{
	return sin( deg * M_PI / 180.0 );
}


double cosinus( double deg )
{
	return cos( deg * M_PI / 180.0 );
}


double
tangent( double deg )
{
	return tan( deg * M_PI / 180.0 );
}


double arcustangent( double val )
{
	return ((atan( val ) * 180.0) / M_PI);
}


double arcustangent2( double x, double y )
{
	return ((atan2( x, y ) * 180.0) / M_PI);
}


double arcussinus( double val )
{
	return ((asin( val ) * 180.0) / M_PI);
}


void
calculate_releated_orbital_elements( PlanetStruct *orbit, int iteration_error )
{
	double		E0=0, E1=0, i=0, xv=0, yv=0;
	
	// round to 360 degree
	orbit->N = round_degree( orbit->N );
	orbit->M = round_degree( orbit->M );
	orbit->w = round_degree( orbit->w );
	
	// calculate releated orbital elements
	orbit->w1 = orbit->N + orbit->w;
	orbit->L  = orbit->M + orbit->w1;
	orbit->q  = orbit->a * ( 1 - orbit->e );
	orbit->Q  = orbit->a * ( 1 + orbit->e );
	//orbit->P  = pow( orbit->a, 1.5 );
	//orbit->T  = Epoch_of_M - ( ( orbit->M / 360.0 ) / orbit->P );
	
	// compute the eccentric anomaly E from the mean anomaly M and from the eccentricity e
	orbit->E = orbit->M + orbit->e * ( 180 / M_PI ) * sinus( orbit->M ) * ( 1.0 + orbit->e * cosinus( orbit->M ) );
	
	if ( iteration_error > 0 )
	{
		E1 = orbit->E;
		i = 0;
		
		do
		{
			E0 = E1;
			E1 = E0 - ( E0 - orbit->e * ( 180.0 / M_PI ) * sinus( E0 ) - orbit->M ) / ( 1.0 - orbit->e * cosinus( E0 ) );
			i++;
		}
		while ( abs( E0 - E1 ) < iteration_error && i<1000 );
		
		// if formula won't converge
		if (i>=1000)
		{
			// near-parabolic orbit
			
			// parabolic orbit
			
		}
		
		orbit->E = E1;
	}
	
	// Then compute the planet's distance r and its true anomaly v from
	xv = orbit->a * ( cosinus( orbit->E ) - orbit->e );
	yv = orbit->a * ( sqrt( 1.0 - orbit->e * orbit->e ) * sinus( orbit->E ) );
	orbit->v = arcustangent2( yv, xv );
	orbit->r = sqrt( xv * xv + yv * yv );

	orbit->v = round_degree( orbit->v );
}


void
get_orbital_elements( PlanetType planet, double d, PlanetStruct *orbit, double ecl )
{
	if ( orbit == NULL ) return;
	memset( orbit, 0, sizeof(struct OrbitalElementsType) );
	
	switch(planet)
	{
	case SUN: // !!! Earth centered !!!
		
		strcpy(orbit->name, "Sun");
		orbit->isSunCentered = 1;
		
		// The orbital elements
		orbit->N = 0.0;
		orbit->i = 0.0;
		orbit->w = 282.9404 + 4.70935E-5 * d;
		orbit->a = 1.000000; //  (AU)
		orbit->e = 0.016709 - 1.151E-9 * d;
		orbit->M = 356.0470 + 0.9856002585 * d;
				
		calculate_releated_orbital_elements( orbit, 0 );
			
printf("d=%f, ws=%f, a=%f, e=%f, M=%f, E=%f\n", d, orbit->w, orbit->a, orbit->e, orbit->M, orbit->E);
			
		break;
	
	case MOON: // !!! Earth centered !!!
		
		strcpy(orbit->name, "Moon");
		orbit->isSunCentered = 0;
		
		orbit->N = 125.1228 - 0.0529538083 * d;
		orbit->i = 5.1454;
		orbit->w = 318.0634 + 0.1643573223 * d;
		orbit->a = 60.2666; // (Earth radii)
		orbit->e = 0.054900;
		orbit->M = 115.3654 + 13.0649929509 * d;
	
/*
N = longitude of the ascending node
i = inclination to the ecliptic (plane of the Earth's orbit)
w = argument of perihelion
a = semi-major axis, or mean distance from Sun
e = eccentricity (0=circle, 0-1=ellipse, 1=parabola)
M = mean anomaly (0 at perihelion; increases uniformly with time)
*/		
		
		calculate_releated_orbital_elements( orbit, 0.001 );
		
		break;
	
	case MERCURY:
		
		strcpy(orbit->name, "Mercury");
		orbit->isSunCentered = 1;
		
		orbit->N =  48.3313 + 3.24587E-5 * d;
		orbit->i = 7.0047 + 5.00E-8 * d;
		orbit->w =  29.1241 + 1.01444E-5 * d;
		orbit->a = 0.387098; // (AU)
		orbit->e = 0.205635 + 5.59E-10 * d;
		orbit->M = 168.6562 + 4.0923344368 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	
	case VENUS:
		
		strcpy(orbit->name, "Venus");
		orbit->isSunCentered = 1;
		
		orbit->N =  76.6799 + 2.46590E-5 * d;
		orbit->i = 3.3946 + 2.75E-8 * d;
		orbit->w =  54.8910 + 1.38374E-5 * d;
		orbit->a = 0.723330; //  (AU)
		orbit->e = 0.006773 - 1.302E-9 * d;
		orbit->M =  48.0052 + 1.6021302244 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	
	case MARS:
		
		strcpy(orbit->name, "Mars");
		orbit->isSunCentered = 1;
		
		orbit->N =  49.5574 + 2.11081E-5 * d;
		orbit->i = 1.8497 - 1.78E-8 * d;
		orbit->w = 286.5016 + 2.92961E-5 * d;
		orbit->a = 1.523688; // (AU)
		orbit->e = 0.093405 + 2.516E-9 * d;
		orbit->M =  18.6021 + 0.5240207766 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	
	case JUPITER:
		
		strcpy(orbit->name, "Jupiter");
		orbit->isSunCentered = 1;
		
		orbit->N = 100.4542 + 2.76854E-5 * d;
		orbit->i = 1.3030 - 1.557E-7 * d;
		orbit->w = 273.8777 + 1.64505E-5 * d;
		orbit->a = 5.20256; // (AU)
		orbit->e = 0.048498 + 4.469E-9 * d;
		orbit->M =  19.8950 + 0.0830853001 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	
	case SATURN:
		
		strcpy(orbit->name, "Saturn");
		orbit->isSunCentered = 1;
		
		orbit->N = 113.6634 + 2.38980E-5 * d;
		orbit->i = 2.4886 - 1.081E-7 * d;
		orbit->w = 339.3939 + 2.97661E-5 * d;
		orbit->a = 9.55475; // (AU)
		orbit->e = 0.055546 - 9.499E-9 * d;
		orbit->M = 316.9670 + 0.0334442282 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	
	case URANUS:
		
		strcpy(orbit->name, "Uranus");
		orbit->isSunCentered = 1;
		
		orbit->N =  74.0005 + 1.3978E-5 * d;
		orbit->i = 0.7733 + 1.9E-8 * d;
		orbit->w =  96.6612 + 3.0565E-5 * d;
		orbit->a = 19.18171 - 1.55E-8 * d; // (AU)
		orbit->e = 0.047318 + 7.45E-9 * d;
		orbit->M = 142.5905 + 0.011725806 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	
	case NEPTUNE:
		
		strcpy(orbit->name, "Neptune");
		orbit->isSunCentered = 1;
		
		orbit->N = 131.7806 + 3.0173E-5 * d;
		orbit->i = 1.7700 - 2.55E-7 * d;
		orbit->w = 272.8461 - 6.027E-6 * d;
		orbit->a = 30.05826 + 3.313E-8 * d; // (AU)
		orbit->e = 0.008606 + 2.15E-9 * d;
		orbit->M = 260.2471 + 0.005995147 * d;
		calculate_releated_orbital_elements( orbit, 0.001 );
		break;
	}
	
	
}


void
get_polar_coordinates( OrbitalElementsType *orbit, PolarCoordinateType *polar )
{
	double	xh=0, yh=0, zh=0;
	
	if ( orbit == NULL ) return;
	if ( polar == NULL ) return;
	memset( polar, 0, sizeof(struct PolarCoordinateType) );
	
	xh = orbit->r * ( cosinus( orbit->N ) * cosinus( orbit->v + orbit->w ) - sinus( orbit->N ) * sinus( orbit->v + orbit->w ) * cosinus( orbit->i ) );
	yh = orbit->r * ( sinus( orbit->N ) * cosinus( orbit->v + orbit->w ) + cosinus( orbit->N ) * sinus( orbit->v + orbit->w ) * cosinus( orbit->i ) );
	zh = orbit->r * ( sinus( orbit->v + orbit->w ) * sinus( orbit->i ) );
	
	polar->longitude = arcustangent2( yh, xh );
	polar->latitude  = arcustangent2( zh, sqrt( xh*xh + yh*yh ) );
	polar->distance  = sqrt( xh*xh + yh*yh + zh*zh );
	
	polar->longitude = round_degree( polar->longitude );
	polar->latitude  = round_degree( polar->latitude );
}


void
get_geocentric_coordinates( PolarCoordinateType *polar, GeocentricCoordinateType *geo, PolarCoordinateType *polarSun )
{
	double	xh=0, yh=0, zh=0, xs=0, ys=0;
	
	if ( polar == NULL ) return;
	if ( geo == NULL ) return;
	memset( geo, 0, sizeof(struct GeocentricCoordinateType) );
	
	xh = polar->distance * cosinus(polar->longitude) * cosinus(polar->latitude);
	yh = polar->distance * sinus(polar->longitude)   * cosinus(polar->latitude);
	zh = polar->distance                             * sinus(polar->latitude);
	
	if ( polarSun )
	{
		xs = polarSun->distance * cosinus( polarSun->longitude );
		ys = polarSun->distance * sinus( polarSun->longitude );
		geo->x = xh + xs;
		geo->y = yh + ys;
		geo->z = zh;
	}
	else // case of MOON or any geocentric planet position
	{
		geo->x = xh;
		geo->y = yh;
		geo->z = zh;
	}
}


void
get_equatorial_coordinates( GeocentricCoordinateType *geo, EquatorialCoordinateType *equ, double oecl )
{
	double	xe=0, ye=0, ze=0;
	
	if ( geo == NULL ) return;
	if ( equ == NULL ) return;
	memset( equ, 0, sizeof(struct EquatorialCoordinateType) );
	
	xe = geo->x;
	ye = geo->y * cosinus( oecl ) - geo->z * sinus( oecl );
	ze = geo->y * sinus( oecl ) + geo->z * cosinus( oecl );
	
	equ->RA  = arcustangent2( ye, xe );
	equ->Dec = arcustangent2( ze, sqrt( xe*xe + ye*ye ) );
	equ->r  = sqrt( xe*xe + ye*ye + ze*ze );
	
	equ->RA  = round_degree( equ->RA );
}


double
get_LST( TimeType *t, LocationCoordinateType *loc, PolarCoordinateType *polarSun )
{
	double		GMST0=0, LST=0;
	
	GMST0 = ( polarSun->longitude + 180.0 ) / 15; // Greenwich Mean Sidereal Time at 0h UT
	LST = GMST0 + t->UT + (loc->Long / 15); // Local Sidereal Time
	LST -= 24*(int)(LST/24);
	
	return LST;
}


void
get_topocentric_position( EquatorialCoordinateType *equ, PolarCoordinateType *polarSun, int isPlanet, LocationCoordinateType *loc, TimeType *t )
{
	double		par=0, rho=0, gclat=0, HA=0, g=0, LST=0;
	
	if (isPlanet)
	{
		par = ( 8.794 / 3600.0 ) / equ->r;
	}
	else // case of Moon (or any geocentric object)
	{
		par = arcussinus( 1.0 / equ->r );
	}
	
	gclat = loc->Lat - 0.1924 * sinus( 2 * loc->Lat );
	rho   = 0.99833 + 0.00167 * cosinus( 2 * loc->Lat );
	
	LST = get_LST( t, loc, polarSun ); // get Local Sidereal Time	
	HA = (15*LST) - equ->RA; // Moon's geocentric Hour Angle
	
	g = arcustangent( tangent(gclat) / cosinus(HA) );
	
	equ->RA  = equ->RA  - par * rho * cosinus(gclat) * sinus(HA) / cosinus(equ->Dec);
	equ->Dec = equ->Dec - par * rho * sinus(gclat) * sinus(g - equ->Dec) / sinus(g);
}


void
get_ecliptic_coordinates( EquatorialCoordinateType *equ, EclipticCoordinateType *ecc, double oecl )
{
	double	x=0, y=0;
	
	ecc->Lat = arcussinus( cosinus( oecl ) * sinus( equ->Dec ) - sinus( equ->RA ) * cosinus( equ->Dec ) * sinus( oecl ) );
	x = cosinus( equ->RA ) * cosinus( equ->Dec );
	y = sinus( oecl ) * sinus( equ->Dec ) + sinus( equ->RA ) * cosinus( equ->Dec ) * cosinus( oecl );
	
	ecc->Long = arcustangent2( y, x );
	ecc->Long = round_degree( ecc->Long );
}


#define calculate_basic_coordinates( PLANET ) \
{ \
	get_orbital_elements( PLANET, d, &orbit[ PLANET ], oecl ); \
	get_polar_coordinates( &orbit[ PLANET ], &polar[ PLANET ] ); \
}

#define calculate_final_coordinates( PLANET ) \
{ \
	get_geocentric_coordinates( &polar[ PLANET ], &geo[ PLANET ], &polar[SUN] ); \
	get_equatorial_coordinates( &geo[ PLANET ], &equ[ PLANET ], oecl ); \
	get_ecliptic_coordinates( &equ[ PLANET ], &ecc[ PLANET ], oecl ); \
}


void
get_planet_coordinates( TimeType *t, EquatorialCoordinateType equ[], EclipticCoordinateType ecc[], LocationCoordinateType *loc )
{
	OrbitalElementsType			orbit[ PLANETS_MAX + 1 ];
	PolarCoordinateType			polar[ PLANETS_MAX + 1 ];
	GeocentricCoordinateType	geo[ PLANETS_MAX + 1 ];
	double						Ms=0, Mm=0, Nm=0, ws=0, wm=0, Ls=0, Lm=0, D=0, F=0, Mj=0, Msa=0, Mu=0, S=0, P=0, // perturbation params.
								epoch = 2000.0, // date of the given orbital elements
								oecl=0, // obliquity of the ecliptic (approx. 23.4 degrees)
								lon_corr=0, // preccesion correction
								xs=0, ys=0, xe=0, ye=0, ze=0, d=0;
	int							i=0;
	
	d = t->d; // time
	oecl = 23.4393 - 3.563E-7 * d;
	lon_corr = 3.82394E-5 * ( 365.2422 * ( epoch - 2000.0 ) - d );
	
	get_orbital_elements( SUN, d, &orbit[ SUN ], oecl ); \
	polar[SUN].longitude = orbit[SUN].v + orbit[SUN].w;
	polar[SUN].latitude  = 0;
	polar[SUN].distance  = orbit[SUN].r;
	
	calculate_basic_coordinates( MOON );
	calculate_basic_coordinates( MERCURY );
	calculate_basic_coordinates( VENUS );
	calculate_basic_coordinates( MARS );
	calculate_basic_coordinates( JUPITER );
	calculate_basic_coordinates( SATURN );
	calculate_basic_coordinates( URANUS );
	calculate_basic_coordinates( NEPTUNE );
	
	// --- calculate perturbations of the moon ---
	
	Ms = orbit[SUN].M;			// Mean Anomaly of the Sun
	Mm = orbit[MOON].M;		// Mean Anomaly of the Moon
	Nm = orbit[MOON].N;		// Longitude of the Moon's node
	ws = orbit[SUN].w;			// Argument of perihelion for the Sun
	wm = orbit[MOON].w;		// Argument of perihelion for the Moon
	Ls = Ms + ws;		// Mean Longitude of the Sun  (Ns=0)
	Lm = Mm + wm + Nm;	// Mean longitude of the Moon
	D = Lm - Ls;		// Mean elongation of the Moon
	F = Lm - Nm;		// Argument of latitude for the Moon
	
	polar[MOON].longitude +=
				- 1.274 * sinus(Mm - 2*D)          // (the Evection)
				+ 0.658 * sinus(2*D)               // (the Variation)
				- 0.186 * sinus(Ms)                // (the Yearly Equation)
				- 0.059 * sinus(2*Mm - 2*D)
				- 0.057 * sinus(Mm - 2*D + Ms)
				+ 0.053 * sinus(Mm + 2*D)
				+ 0.046 * sinus(2*D - Ms)
				+ 0.041 * sinus(Mm - Ms)
				- 0.035 * sinus(D)                 // (the Parallactic Equation)
				- 0.031 * sinus(Mm + Ms)
				- 0.015 * sinus(2*F - 2*D)
				+ 0.011 * sinus(Mm - 4*D);
	
	polar[MOON].latitude +=
				- 0.173 * sinus(F - 2*D)
				- 0.055 * sinus(Mm - F - 2*D)
				- 0.046 * sinus(Mm + F - 2*D)
				+ 0.033 * sinus(F + 2*D)
				+ 0.017 * sinus(2*Mm + F);
	
	// distance calculated in unit of radius of the earth
	polar[MOON].distance +=
				- 0.58 * cosinus(Mm - 2*D)
				- 0.46 * cosinus(2*D);
	
	// --- calculate perturbations for jupiter, saturn and uranus ---
	
	Mj  = orbit[JUPITER].M;		// Mean anomaly of Jupiter
	Msa = orbit[SATURN].M;		// Mean anomaly of Saturn
	Mu  = orbit[URANUS].M;		// Mean anomaly of Uranus (needed for Uranus only)
	
	polar[JUPITER].longitude +=
				-0.332 * sinus(2*Mj - 5*Msa - 67.6)
				-0.056 * sinus(2*Mj - 2*Msa + 21)
				+0.042 * sinus(3*Mj - 5*Msa + 21)
				-0.036 * sinus(Mj - 2*Msa)
				+0.022 * cosinus(Mj - Msa)
				+0.023 * sinus(2*Mj - 3*Msa + 52)
				-0.016 * sinus(Mj - 5*Ms - 69);
	
	polar[SATURN].longitude +=
				+0.812 * sinus(2*Mj - 5*Msa - 67.6)
				-0.229 * cosinus(2*Mj - 4*Msa - 2)
				+0.119 * sinus(Mj - 2*Msa - 3)
				+0.046 * sinus(2*Mj - 6*Msa - 69)
				+0.014 * sinus(Mj - 3*Msa + 32);
	
	polar[SATURN].latitude +=
				-0.020 * cosinus(2*Mj - 4*Msa - 2)
				+0.018 * sinus(2*Mj - 6*Msa - 49);
	
	polar[URANUS].longitude +=
				+0.040 * sinus(Msa - 2*Mu + 6)
				+0.035 * sinus(Msa - 3*Mu + 33)
				-0.015 * sinus(Mj - Mu + 20);
	
	// --- orbital elements and perturbations of pluto (valid from 1900 to 2100) ---
	
	S  =   50.03  +  0.033459652 * d;
	P  =  238.95  +  0.003968789 * d;
	
	polar[PLUTO].longitude = 238.9508  +  0.00400703 * d
				- 19.799 * sinus(P)     + 19.848 * cosinus(P)
				+ 0.897 * sinus(2*P)    - 4.956 * cosinus(2*P)
				+ 0.610 * sinus(3*P)    + 1.211 * cosinus(3*P)
				- 0.341 * sinus(4*P)    - 0.190 * cosinus(4*P)
				+ 0.128 * sinus(5*P)    - 0.034 * cosinus(5*P)
				- 0.038 * sinus(6*P)    + 0.031 * cosinus(6*P)
				+ 0.020 * sinus(S-P)    - 0.010 * cosinus(S-P);
	
	polar[PLUTO].latitude = -3.9082
				- 5.453 * sinus(P)     - 14.975 * cosinus(P)
				+ 3.527 * sinus(2*P)    + 1.673 * cosinus(2*P)
				- 1.051 * sinus(3*P)    + 0.328 * cosinus(3*P)
				+ 0.179 * sinus(4*P)    - 0.292 * cosinus(4*P)
				+ 0.019 * sinus(5*P)    + 0.100 * cosinus(5*P)
				- 0.031 * sinus(6*P)    - 0.026 * cosinus(6*P)
									+ 0.011 * cosinus(S-P);

	polar[PLUTO].distance =  40.72
				+ 6.68 * sinus(P)       + 6.90 * cosinus(P)
				- 1.18 * sinus(2*P)     - 0.03 * cosinus(2*P)
				+ 0.15 * sinus(3*P)     - 0.14 * cosinus(3*P);
	
	// ----- correcting longitude coordinates according to presession -----
	/*
	for (i=SUN; i<PLANETS_MAX; i++)
	{
		if (i==MOON) continue;
		polar[SUN].longitude += lon_corr;
	}
	*/
	
	// ----- NOW WE CALCULATE THE GEOCENTRIC AND EQUATORIAL COORDINATES -----
	// ----- [[[ SUN ]]] -----
	
	// Convert lonsun, r to ecliptic rectangular geocentric coordinates xs,ys:
	xs = polar[SUN].distance * cosinus( polar[SUN].longitude );
	ys = polar[SUN].distance * sinus( polar[SUN].longitude );
	
	// To convert this to equatorial, rectangular, geocentric coordinates, compute
	xe = xs;
	ye = ys * cosinus( oecl );
	ze = ys * sinus( oecl );
	
	// Finally, compute the Sun's Right Ascension (RA) and Declination (Dec):
	equ[SUN].RA  = arcustangent2( ye, xe );
	equ[SUN].Dec = arcustangent2( ze, sqrt( xe*xe + ye*ye ) );
	equ[SUN].r   = sqrt( xe*xe + ye*ye + ze*ze );
	get_ecliptic_coordinates( &equ[ SUN ], &ecc[ SUN ], oecl );
	
	// ----- [[[ MOON ]]] -----
	
	get_geocentric_coordinates( &polar[MOON], &geo[MOON], NULL );
	get_equatorial_coordinates( &geo[MOON], &equ[MOON], oecl );
	get_topocentric_position( &equ[MOON], &polar[SUN], 0, loc, t );
	get_ecliptic_coordinates( &equ[ MOON ], &ecc[ MOON ], oecl );
	
	// ----- Other planets -----
	
	calculate_final_coordinates( MERCURY );
	calculate_final_coordinates( VENUS );
	calculate_final_coordinates( MARS );
	calculate_final_coordinates( JUPITER );
	calculate_final_coordinates( SATURN );
	calculate_final_coordinates( URANUS );
	calculate_final_coordinates( NEPTUNE );
	calculate_final_coordinates( PLUTO );
}


char*
deg_format( char *str, double deg )
{	
	sprintf( str, "%i:%02i", (int)deg, (int)(60.0*(deg - (int)deg)) );
	return str;
}


char*
RA_format( char *str, double deg )
{	
	double	hourpos = 24.0 * deg / 360.0;
	int		h=0, m=0, s=0;
	
	h = (int)(hourpos);
	m = (int)(60.0*(hourpos - h));
	s = (int)((hourpos - (h + m/60.0)) * 3600.0);
	
	sprintf( str, "%i:%02i:%02ih", h, m, s );
	return str;
}


int
main( int argc, char *argv[] )
{
	int							y = 1976, m = 4, D = 24;
	double						UT=22.083-1, d=0;
	char						sbuf[256]="", eccStr[16]="", raStr[16]="", decStr[16]="";
	int							sign=0, i=0;
	EquatorialCoordinateType	equ[ PLANETS_MAX + 1 ];
	EclipticCoordinateType		ecc[ PLANETS_MAX + 1 ];
	LocationCoordinateType		loc;
	TimeType					t;
	
	memset( ecc, 0, sizeof(ecc) );
	
	// calculate time
	t.UT = UT;
	t.d  = (int) ( (367*y) - (int)(7*(int)((y+(m+9)/12)))/4 + (int)(275*m)/9 + D - 730530 );
	t.d += t.UT/24.0;
	
	// location
	loc.Long = +19.5;
	loc.Lat  = +47.29;
	
	get_planet_coordinates( &t, equ, ecc, &loc );
	
	printf("------------------------------------------------------------------------------------------\n");
	printf("%-15s %-15s %-15s %-15s %-15s\n", "Planet", "RA", "Dec", "Long", "Lat");
	printf("------------------------------------------------------------------------------------------\n");
	for (i=SUN; i<PLANETS_MAX; i++)
	{
		sign = (int)(ecc[i].Long/30);
		deg_format( eccStr, ecc[i].Long-(sign*30) );
		RA_format( raStr, equ[i].RA );
		deg_format( decStr, equ[i].Dec );
		sprintf( sbuf, "%s %s", SignNames[sign], eccStr );
		printf( "%-15s %-15s %-15s %-15f %-15f %-15s\n",
					PlanetNames[(int)i],
					raStr,
					decStr,
					ecc[i].Long,
					ecc[i].Lat,
					sbuf );
	}	
	printf("------------------------------------------------------------------------------------------\n");
	
	//get_LST();
	
}


