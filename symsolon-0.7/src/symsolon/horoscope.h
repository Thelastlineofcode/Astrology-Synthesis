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
#ifndef HOROSCOPE_H
#define HOROSCOPE_H

#include "solon_global.h"
#include "solonmath.h"
#include "planet.h"
#include "solarsystem.h"
#include "observer.h"
#include "house.h"
#include "aspectmatrix.h"


class HoroscopeClass{

public:
    
    SolarSystemClass        solarSystem;
    ObserverClass           observer;
    HouseClass              houses;
    AspectMatrixClass       aspects;
    bool                    synastryFlag;
    
    HoroscopeClass();
    HoroscopeClass( int aYear, int aMonth, int aDay, double UT,
                    double aLong, double aLat, double ayanamsa = 0 );
    ~HoroscopeClass();
    
    void set_date( int aYear, int aMonth, int aDay, double UT );
    void set_location( double aLong, double aLat );
    void calculate_scope();    
    void dump( char *out );
    
    int get_sign_where_house_cusp( int h );
    int get_sign_where_planet( int planetIndex );
    int get_house_where_planet( int planetIndex );
    int get_house_at_degree( double degree );
    double get_time_at_degree( double degree );
    void shift_date( TimeStepType tstep, double value );
    void get_date( char *retStr );
    void set_ayanamsa( double ayanamsaIn );
    double get_degree_of_planet( int planetIndex );

private:

    void calculate_ascendant_position( PlanetClass &asc );

};

#endif
