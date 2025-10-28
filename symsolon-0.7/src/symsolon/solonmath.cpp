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

#include "solonmath.h"

namespace SolonMath {


char*
format_deg( double deg, char *str )
{
    int        d=0, m=0, s=0, polarity=0;
    
    if (deg<0)
    {
        polarity=-1;
        deg = -deg;
    }
    
    d = (int)(deg);
    m = (int)(60.0*(deg - d));
    s = (int)((deg - (d + m/60.0)) * 3600.0);
    
    sprintf( str, "%s%i:%02i:%02i", (polarity<0)?"-":" ", d, m, s );
    return str;
}


char*
format_hour( double deg, char *str )
{    
    double    hourpos = 24.0 * deg / 360.0;
    int        h=0, m=0, s=0, polarity=0;
    
    if (hourpos<0)
    {
        polarity=-1;
        hourpos = -hourpos;
    }
    
    h = (int)(hourpos);
    m = (int)(60.0*(hourpos - h));
    s = (int)((hourpos - (h + m/60.0)) * 3600.0);
    
    sprintf( str, "%s%i:%02i:%02i", (polarity<0)?"-":" ", h, m, s );
    return str;
}


char*
format_astro( double deg, char *str )
{
    const char    *signNames[] = { "Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis" };
    int           d=0, dd=0, m=0, sign=0;
    
    deg = round_degree( deg );
    
    sign = (int)(deg/30);
    d    = (int)deg;
    dd    = (int)(d - sign*30);
    m    = (int)(60.0*(deg - d));
    
    sprintf( str, "%i%s%02i", dd, signNames[sign], m );
    return str;
}


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


double
cosinus( double deg )
{
    return cos( deg * M_PI / 180.0 );
}


double
arcuscosinus( double val )
{
    return ((acos( val ) * 180.0) / M_PI);
}


double
tangent( double deg )
{
    return tan( deg * M_PI / 180.0 );
}


double
arcustangent( double val )
{
    return ((atan( val ) * 180.0) / M_PI);
}


double
arcustangent2( double x, double y )
{
    return ((atan2( x, y ) * 180.0) / M_PI);
}


double
arcussinus( double val )
{
    return ((asin( val ) * 180.0) / M_PI);
}

};
