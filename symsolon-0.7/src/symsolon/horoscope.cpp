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
#include "horoscope.h"

using namespace SolonMath;


HoroscopeClass::HoroscopeClass()
{
    set_date( 2000, 0, 0, 0.0 );
    set_location( 0, 0 );
    calculate_scope();
}


HoroscopeClass::HoroscopeClass( int aYear, int aMonth, int aDay, double aUT,
                                double aLong, double aLat, double ayanamsa )
{
    set_ayanamsa( ayanamsa );
    set_date( aYear, aMonth, aDay, aUT );
    set_location( aLong, aLat );
    calculate_scope();
}


HoroscopeClass::~HoroscopeClass()
{
}


void
HoroscopeClass::set_date( int aYear, int aMonth, int aDay, double aUT )
{
    observer.set_time( aYear, aMonth, aDay, aUT );
}


void
HoroscopeClass::get_date( char *retStr )
{
    if (retStr == NULL) return;
    
    int hours   = (int)observer.UT;
    int minutes = (int)(60*(observer.UT - hours));
    int seconds = (int)(3600*(observer.UT - hours - (minutes/60.0)));
    
    sprintf( retStr, "%04i.%02i.%02i %02i:%02i:%02i",
        observer.year, observer.month, observer.day,
        hours, minutes, seconds );
}


void
HoroscopeClass::shift_date( TimeStepType tstep, double value )
{
    observer.shift_date( tstep, value );
    calculate_scope();
}


void
HoroscopeClass::set_location( double aLong, double aLat )
{
    observer.set_location( aLong, aLat );
}


void
HoroscopeClass::set_ayanamsa( double ayanamsaIn )
{
    observer.set_ayanamsa( ayanamsaIn );
}


void
HoroscopeClass::calculate_scope()
{
    solarSystem.calculate_planet_positions( observer );    
    houses.set_observer( &observer );
    houses.calculate_houses();
    houses.calculate_points();
    aspects.calculate( &solarSystem );
}


int
HoroscopeClass::get_house_where_planet( int planetIndex )
{
    int           i=0;
    
    for (i=0; i<solarSystem.numberOfPlanets; i++)
        if ( solarSystem.planetVector[i]->index == planetIndex ) break;
    
    if (i == solarSystem.numberOfPlanets) return 0;
    
    return get_house_at_degree( solarSystem.planetVector[i]->Long );
}


int
HoroscopeClass::get_sign_where_planet( int planetIndex )
{
    int           i=0;
    double        l=0;
    
    for (i=0; i<solarSystem.numberOfPlanets; i++)
        if ( solarSystem.planetVector[i]->index == planetIndex )
        {
            l = solarSystem.planetVector[i]->Long;
            return (int)(l/30) + 1;
        }
    
    return 0;
}


double
HoroscopeClass::get_degree_of_planet( int planetIndex )
{
    PlanetClass     *planet = NULL;
    
    for (int i=0; i<solarSystem.numberOfPlanets; i++)
        if (solarSystem.planetVector[i]->index == planetIndex)
        {
            planet = solarSystem.planetVector[i];
            break;
        }
    
    if (planet == NULL) return 0;
    else return planet->Long;
}


int
HoroscopeClass::get_house_at_degree( double degree )
{
    int           h=0;
    double        t0=0, t1=0;
    
    degree = ROUND_DEG( degree );
    for (h=1; h<=12; h++)
    {
        if (h<12)
        {
            t0 = houses.cusp[h];
            t1 = houses.cusp[h+1];
        }
        else
        {
            t0 = houses.cusp[12];
            t1 = houses.cusp[1];
        }
        if ( t1 < t0 ) { if ( degree>=t0 || degree<t1 ) return h; }
        if ( degree>=t0 && degree<t1 ) return h;
    }
    
    return 0;
}


double
HoroscopeClass::get_time_at_degree( double degree )
{
    int         h0=0, h1=0;
    double      dh=0, d=0;
    
    degree = ROUND_DEG( degree );
    h0 = get_house_at_degree( degree );
    if ( h0 <= 0 ) return 0;
    if ( h0 == 12 ) h1 = 1; else h1 = h0 + 1;
    dh = ANGLE_DISTANCE(houses.cusp[h0], houses.cusp[h1]);
    d = dh - (ANGLE_DISTANCE(houses.cusp[h0], degree));
    return ((12-h0)*7.0) + (7.0*d/dh);
}


int
HoroscopeClass::get_sign_where_house_cusp( int h )
{
    if (h<=0 || h>12) return 0;
    return (int)(houses.cusp[h]/30) + 1;
}


void
HoroscopeClass::dump( char *out )
{
    char                        sbuf[5][32], sbuf2[4096];
    int                            i=0, j=0, a=0;
    PlanetClass                    **pv = solarSystem.planetVector;
    
    strcpy(out, "");
    
    strcat(out, "-------------------------------------------------------------------------\n");
    sprintf(sbuf2, "%-10s %-12s %-12s %-12s %-12s\n", "Planet", "RA", "Dec", "Long", "Lat");
    strcat(out, sbuf2);
    strcat(out, "--------------------------------------------------------------------------\n");
    for (i=0; i<solarSystem.numberOfPlanets; i++)
    {
        sprintf( sbuf2, "%-10s %-12s %-12s %-12s %-12s %-12s\n",
                    pv[i]->name,
                    format_hour( pv[i]->RA, sbuf[0] ),
                    format_deg( pv[i]->Dec, sbuf[1] ),
                    format_deg( pv[i]->Long, sbuf[2] ),
                    format_deg( pv[i]->Lat, sbuf[3] ),
                    format_astro( pv[i]->Long, sbuf[4] )
                    );
        strcat(out, sbuf2);
    }
    strcat(out, "--------------------------------------------------------------------------\n");
    strcat(out, "Houses\n");
    strcat(out, "--------------------------------------------------------------------------\n");
    for (i=1; i<=12; i++)
    {
        sprintf( sbuf2, "%-4i %-15s %-15s\n",
                    i,
                    format_deg( houses.cusp[i], sbuf[0] ),
                    format_astro( houses.cusp[i], sbuf[1] )
                    );
        strcat(out, sbuf2);
    }
    strcat(out, "-------------------------------------------------------------------------\n");
    strcat(out, "Aspects\n");
    strcat(out, "--------------------------------------------------------------------------\n");
    for (i=0; i<solarSystem.numberOfPlanets; i++)
    {
        sprintf( sbuf2, "%-10s: ", pv[i]->name );
        for (j=0; j<solarSystem.numberOfPlanets; j++)
        {
            if ( (a=aspects.matrix[ pv[i]->index ][ pv[j]->index] ) != ASPECT_NONE )
            {
                strcat( sbuf2, Symbol->aspectInfo[a].name );
                strcat( sbuf2, "-" );
                strcat( sbuf2, pv[j]->name );
                strcat( sbuf2, " " );
            }
        }
        strcat( sbuf2, "\n" );
        strcat(out, sbuf2);
    }
    strcat(out, "-------------------------------------------------------------------------\n");
}

