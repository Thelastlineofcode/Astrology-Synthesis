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
#ifndef PLANET_H
#define PLANET_H

#include "solon_global.h"

class PlanetClass{

public:
    
    typedef enum { SOLAR_CENTERED, EARTH_CENTERED, THIS_IS_SUN, NOT_REAL_PLANET } CenterTypeEnum;
    
    char            *name; // name of planet
    PlanetIndexType    index; // unique identifier of planet (reference number)
    bool            hypotetic; // true if planet is hypotetic/theoretic one
    // --- primary orbital elements ---
    double            N;    // longitude of the ascending node
    double            i;    // inclination to the ecliptic (plane of the Earth's orbit)
    double            w;    // argument of perihelion
    double            a;    // semi-major axis, or mean distance from Sun
    double            e;    // eccentricity (0=circle, 0-1=ellipse, 1=parabola)
    double            M;    // mean anomaly (0 at perihelion; increases uniformly with time)
    // --- releated orbital elements ---
    double            w1;    // = N + w   = longitude of perihelion
    double            L;    // = M + w1  = mean longitude
    double            q;    // = a*(1-e) = perihelion distance
    double            Q;    // = a*(1+e) = aphelion distance
    //double        P;    // = a ^ 1.5 = orbital period (years if a is in AU, astronomical units)
    //double        T;    // = Epoch_of_M - (M(deg)/360_deg) / P  = time of perihelion
    double            v;    // = true anomaly (angle between position and perihelion)
    double            E;    // = eccentric anomaly
    double            r;    // = rs = distance
    // --- polar coordinates ---
    double            longitude;    // (degrees)
    double            latitude;    // (degrees)
    double            distance;
    // --- geocentric cartesian coordinates ---
    double            x;
    double            y;
    double            z;
    // --- equatorial coordinates ---
    double            RA;        // (degrees)
    double            Dec;    // (degrees)
    double            er;
    // --- horizontal coordinates ---
    double            Azimuth;
    double            Altitude;
    // --- ecliptic coordinates ---
    double            Long;    // (degrees)
    double            Lat;    // (degrees)
    
    CenterTypeEnum    centerType;
    double            iteration_error;    // iteration error in calculate_releated_orbital_elements() function
    
    PlanetClass();
    PlanetClass( int _index );
    ~PlanetClass();
    
    void clear_orbital_elements();
    void init( int _index );

};

#endif
