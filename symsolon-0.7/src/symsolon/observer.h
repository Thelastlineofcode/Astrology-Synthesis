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
#ifndef OBSERVER_H
#define OBSERVER_H

#include "solon_global.h"
#include "solonmath.h"
#include "planet.h"

#define JULIAN2000 2451543.5

class ObserverClass {

public:

    // --- time of observation ---
    int             year;
    int             month;
    int             day;
    double          UT;
    double          d;  // days elapsed from 2000.0.0.0
    double          JD; // Julian Day
    
    // --- position of observer on eath surface ---
    double          observerLong;    // (degrees)  East:+  West:-
    double          observerLat;    // (degrees)  North:+ South:-
    
    double          ayanamsa;   // used ayanamsa (in degrees)
    
    // ---
    double          oecl;        // obliquity of the ecliptic (approx. 23.4 degrees)
    double          GMST;        // Greenwich Mean Sidereal time
    double          GAST;        // Greenwich Apparent Sidereal time
    double          LST;        // local sidereal time (in degrees)
    PlanetClass     polarSun;    // contain polar coordinates of sun
    
    ObserverClass();
    ~ObserverClass();
    
    void set_location( double aLong, double aLat );
    void set_time( int aYear, int aMonth, int aDay, double aUT );
    void update();
    void calculate_coordinates( PlanetClass &p );
    void calculate_ecliptic_coordinates( PlanetClass &p );
    void calculate_topocentric_position( PlanetClass &p );
    void calculate_equatorial_coordinates( PlanetClass &p );
    void calculate_geocentric_coordinates( PlanetClass &p );
    void calculate_horizontal_coordinates( PlanetClass &p );
    void calculate_days_from_2000();
    void shift_date( TimeStepType tstep, double value );
    void calculate_julian_day();
    void julian_day_to_date();
    void set_ayanamsa( double ayanamsaIn );

private:

    void julian_to_gregorian( double base, double jd,
		int &yearOut, int &monthOut, int &dayOut, double &utOut );
    void gregorian_to_julian(
		int _y, int _m, int _d, double _ut, double &jdOut );
};

#endif
