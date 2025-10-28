/***************************************************************************
 *   SymSolon - a free astrology software                                  *
 *   Copyright (C) 2007 by Bela MIHALIK,,,                                 *
 *   bela.mihalik@gmail.com                                                *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/
#include "observer.h"
#include "solarsystem.h"

#ifdef SWISS_EPHEM
#include "swephexp.h"
#endif

using namespace SolonMath;


ObserverClass::ObserverClass()
{
    year  = 2000;
    month = 1;
    day   = 1;
    UT    = 0;
    observerLong = 0;
    observerLat  = 0;
    update();
    ayanamsa = 0;
}


ObserverClass::~ObserverClass()
{
}


void
ObserverClass::set_ayanamsa( double ayanamsaIn )
{
    ayanamsa = ayanamsaIn;
}


void
ObserverClass::set_location( double aLong, double aLat )
{
    observerLong = aLong;
    observerLat  = aLat;
    update();
}


void
ObserverClass::set_time( int aYear, int aMonth, int aDay, double aUT )
{    
    year  = aYear;
    month = aMonth;
    day   = aDay;
    UT    = aUT;
    update();
}


void
ObserverClass::shift_date( TimeStepType tstep, double value )
{
    switch ( tstep )
    {
        case TIMESTEP_YEAR:
            year += (int)value;
            break;
        
        case TIMESTEP_MONTH:
            month += (int)value;
            break;
        
        case TIMESTEP_WEEK:
            day += 7*(int)value;
            break;
        
        case TIMESTEP_DAY:
            day += (int)value;
            break;
        
        case TIMESTEP_HOUR:
            UT += value;
            break;
        
        case TIMESTEP_MINUTE:
            UT += value/60.0;
            break;
        
        case TIMESTEP_SECOND:
            UT += value/3600.0;
            break;
        
        default:
            break;
    }
    
    update(); // update function normalizes the date also
}


void
ObserverClass::calculate_days_from_2000()
{
    // calculate days elapsed from 2000.0.0.0
    d  = (int) ( (367*year) - (int)(7*(int)((year+(month+9)/12)))/4 + (int)(275*month)/9 + day - 730530 );
    d += UT / 24.0;
}


void
ObserverClass::calculate_julian_day()
{
    // we don't use swiss ephem julian day calculator here
    // because accept negative UT and days greater then 31.
    gregorian_to_julian( year, month, day, UT, JD );
}


void
ObserverClass::julian_day_to_date()
{
    double  _JD=0, _UT=0;
    int     _year=0, _month=0, _day=0, base=0;
    
    // this is a little hack!
    // i couldn't find a correct julian-day to gregorian-day converter
    // most of the codes are miss +/- 1 day before/after 1900.01.01
    // because of this i created an iterative algorithm that verify
    // the accuracy of conversion to/form julian/gregorian dates.
    
    base = 0;
    do {
        _JD = JD;
        julian_to_gregorian( base, _JD, _year, _month, _day, _UT );
        gregorian_to_julian( _year, _month, _day, _UT, _JD );
        base++;
    } while ( (_JD != JD) && (base < 4) );
    
    year = _year;
    month = _month;
    day = _day;
    UT = _UT;
}


void
ObserverClass::gregorian_to_julian(
		int _y, int _m, int _d, double _ut, double &jdOut )
{
    if (_m <= 2) { _m = _m + 12; _y = _y - 1; }
    jdOut = (int)(365.25*(_y+4716)) + (int)(30.6001*(_m+1)) + _d - 13 - 1524.5 + (double)_ut/24.0;
}


void
ObserverClass::julian_to_gregorian(
		double base, double jd,
		int &yearOut, int &monthOut, int &dayOut, double &utOut )
{
    /*
    int        y=0, m=0, d=0, j=0;
    double    _ut=0;
    
    // universal time:
    _ut = JD - ((int)JD);
    if (_ut < 0.5)
    {
        _ut += 0.5;
        j = 2;
    }
    else
    {
        _ut -= 0.5;
        j = 2;
    }
    UT = _ut * 24.0;
    
    // gregorian date:
    j += (int)(JD - _ut);
    
    j = j - 1721119 ;
    y = (4 * j - 1) / 146097;
    j = 4 * j - 1 - 146097 * y;
    d = j / 4;
    j = (4 * d + 3) / 1461;
    d = 4 * d + 3 - 1461 * j;
    d = (d + 4) / 4;
    m = (5 * d - 3) / 153;
    d = 5 * d - 3 - 153 * m;
    d = (d + 5) / 5;
    y = 100 * y + j;
    if (m < 10)
    {
        m = m + 3;
    }
    else
    {
        m = m - 9 ; y = y + 1;
    }
    
    year = y;
    month = m;
    day = d;
    */

    // 1st - calcluate universal time (UT)
    double _ut = jd - ((int)jd);
    if (_ut < 0.5)
    {
        _ut += 0.5;
    }
    else
    {
        _ut -= 0.5;
    }
    utOut = _ut * 24.0;
    
    // 2nd - calculate gregorian day (year, month, day)
    double jd0 = jd + 0.5 + base;
    
    double z = (int)jd0;
    double f = jd0 - z;
    
    double a = 0.0;
    double alp = 0.0;
    if ( z < 2299161 )
    {
        a = z;
    }
    else
    {
        alp = (int)((z - 1867216.25)/36524.25);
        a = z + 1.0 + alp - (int)(alp/4.0);
    }
    
    double b = a + 1524;
    double c = (int)((b - 122.1)/365.25);
    double d = (int)(365.25*c);
    double e = (int)((b - d)/30.6001);
    
    double _day = b - d - (int)(30.6001*e) + f;
    
    double _mon = 0;
    if (e < 13.5)
    {
        _mon = e - 1;
    }
    else
    {
        _mon = e - 13;
    }
    
    double _yr = 0;
    if (_mon > 2.5)
    {
        _yr = c - 4716;
    }
    else
    {
        _yr = c - 4715;
    }
    
    yearOut = (int)_yr;
    monthOut = (int)_mon;
    dayOut = (int)_day;
}


void
ObserverClass::update()
{
    // normalize date (means we recalculate the date to
    // eliminate negative hours, days greater than 31, etc. etc. )
    // we use julian day converter for normalization process
    calculate_julian_day();
    julian_day_to_date();
    // calculate days elapsed from 2000.0.0
    calculate_days_from_2000();
    // calculate julian day again (just for safe - not needed really)
    calculate_julian_day();
    
    // ---- get coordinates of the sun ----
    SolarSystemClass::calculate_sun_position( d, polarSun );
    
    // --- obliquity of the ecliptic ---
    oecl = 23.4393 - 3.563E-7 * d;
    
    // ---- Local Sidereal Time ----
    double JD0 = (int)JD;
    if (JD-JD0 >= 0.5) { JD0 += 0.5; } else { JD0 -= 0.5; } // JD of previous midnight
    double H = 24 * (JD - JD0); // hours elapsed since JD0
    double D = JD - 2451545.0; // days elapsed since 2000.Jan.1 12h
    double D0 = JD0 - 2451545.0; // days elapsed since 2000.0.0
    double T = D / 36525; // number of centuries since the year 2000
    // GMST = Greenwich mean sidereal time
    GMST = 6.697374558 + 0.06570982441908 * D0  + 1.00273790935 * H + 0.000026 * T * T; 
    // GMST = 18.697374558 + 24.06570982441908 * D; // this is the simple method
    
    GMST -= 24*(int)(GMST/24);
    GMST = round_degree( GMST*15 );
    
    double L = 280.47 + 0.98565 * D; // Mean Longitude of the Sun
    double omega = 125.04 - 0.052954 * D; // Longitude of the ascending node of the Moon
    double delta_fi = (-0.000319 * sinus (omega) - 0.000024 * sinus( 2*L )) * 15; // nutation in longitude
    double eqeq = delta_fi * cosinus( oecl ); // equation of the equinoxes
    GAST = GMST + eqeq; // Greenwich apparent sidereal time
    
    LST = round_degree( GAST + observerLong );
}


void
ObserverClass::calculate_coordinates( PlanetClass &p )
{
    calculate_geocentric_coordinates( p );
    calculate_equatorial_coordinates( p );
    if (SolonConfig->topocentricCalculationUsed) calculate_topocentric_position( p );
    calculate_ecliptic_coordinates( p );
}


void
ObserverClass::calculate_ecliptic_coordinates( PlanetClass &p )
{
    double    x=0, y=0;
    
    x = cosinus( p.RA ) * cosinus( p.Dec );
    y = sinus( oecl ) * sinus( p.Dec ) + sinus( p.RA ) * cosinus( p.Dec ) * cosinus( oecl );
    
    p.Lat = arcussinus( cosinus( oecl ) * sinus( p.Dec ) - sinus( p.RA ) * cosinus( p.Dec ) * sinus( oecl ) );
    
    p.Long = round_degree( arcustangent2( y, x ) - ayanamsa );
}


void
ObserverClass::calculate_topocentric_position( PlanetClass &p )
{
    double        par=0, rho=0, gclat=0, HA=0, g=0;
    
    if (p.er == 0) return;
    
    if (p.centerType == PlanetClass::SOLAR_CENTERED ||
        p.centerType == PlanetClass::THIS_IS_SUN)
    {
        par = ( 8.794 / 3600.0 ) / p.er;
    }
    else // case of Moon (or any geocentric object)
    {
        par = arcussinus( 1.0 / p.er );
    }
    
    gclat = observerLat - 0.1924 * sinus( 2 * observerLat );
    rho   = 0.99833 + 0.00167 * cosinus( 2 * observerLat );
    HA = LST - p.RA; // planets's geocentric Hour Angle (LST is given in degree)
    
    if (cosinus(HA) != 0)
    {
        g = arcustangent( tangent(gclat) / cosinus(HA) );
    }
    else
    {
        if (tangent(gclat) == 0) g = 0;
        if (tangent(gclat) > 0)  g = 90;
        if (tangent(gclat) > 0)  g = -90;
    }
    
    if (cosinus(p.Dec) != 0)
    {
        // correcting RA if Declination is not 90deg, otherwise leave RA as it is
        p.RA  -= par * rho * cosinus(gclat) * sinus(HA) / cosinus(p.Dec);
    }
    
    if (sinus(g) != 0)
    {
        // correcting Declination if g is not zero
        p.Dec -= par * rho * sinus(gclat) * sinus(g - p.Dec) / sinus(g);
    }
}


void
ObserverClass::calculate_horizontal_coordinates( PlanetClass& )
{
/*
    double    x=0, y=0, r=0, sina=0, d=0, ra=0;
    
    d  = p.Dec;
    ra = p.RA;
    
    //d = 0;
    //ra = 0;    
    
    sina = sinus(observerLat) * sinus(d) + cosinus(observerLat) * cosinus(d) * cosinus(ra);
    x = cosinus(observerLat) * sinus(d) - sinus(observerLat) * cosinus(d) * cosinus(ra);
    y = -cosinus(p.Dec) * sinus(p.RA);
    r = sqrt( x*x + y*y );
    
    p.Azimuth = arcustangent2( y, x );
    p.Azimuth = round_degree( p.Azimuth );
    x = r;
    y = sina;
    p.Altitude = arcustangent2( y, x );
*/
}


void
ObserverClass::calculate_equatorial_coordinates( PlanetClass &p )
{
    double    xe=0, ye=0, ze=0;
    
    xe = p.x;
    ye = p.y * cosinus( oecl ) - p.z * sinus( oecl );
    ze = p.y * sinus( oecl ) + p.z * cosinus( oecl );
    
    p.RA  = arcustangent2( ye, xe );
    p.Dec = arcustangent2( ze, sqrt( xe*xe + ye*ye ) );
    p.er  = sqrt( xe*xe + ye*ye + ze*ze );
    
    p.RA  = round_degree( p.RA );
}


void
ObserverClass::calculate_geocentric_coordinates( PlanetClass &p  )
{
    double    xh=0, yh=0, zh=0, xs=0, ys=0;
    
    xh = p.distance * cosinus(p.longitude) * cosinus(p.latitude);
    yh = p.distance * sinus(p.longitude)   * cosinus(p.latitude);
    zh = p.distance                        * sinus(p.latitude);
    
    if ( p.centerType == PlanetClass::SOLAR_CENTERED )
    {
        xs = polarSun.distance * cosinus( polarSun.longitude );
        ys = polarSun.distance * sinus( polarSun.longitude );
        p.x = xh + xs;
        p.y = yh + ys;
        p.z = zh;
    }
    else // case of MOON or any geocentric planet position
    {
        p.x = xh;
        p.y = yh;
        p.z = zh;
    }
}

