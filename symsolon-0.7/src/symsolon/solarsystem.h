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
#ifndef SOLARSYSTEM_H
#define SOLARSYSTEM_H

#include "solon_global.h"
#include "solonmath.h"
#include "planet.h"
#include "observer.h"

class SolarSystemClass{

public:

    PlanetClass        Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto,
                    NNode, SNode, Chiron, Ceres, Eris, Pallas, Juno, Vesta,
                    Pholus, Cupido, Hades, Zeus, Kronos, Apollon, Admetos,
                    Vulkanus, Poseidon, Isis, Nibiru, Harrington, Leverrier, Adams, Lowell,
                    Pickering, Vulcan, WhiteMoon, Proserpina, Waldemath;
    
    PlanetClass        **planetVector; // filled up in constructor
    int                numberOfPlanets;
    double            d; // calculated time from 2000AC (in days)
    
    SolarSystemClass();
    ~SolarSystemClass();
    void calculate_planet_positions( ObserverClass &ob );
    static void calculate_sun_position( double dayTime, PlanetClass &sun );
    static void open_swiss_ephem();
    static void close_swiss_ephem();
    
private:

    void calculate_raw_positions();
    int calculate_raw_position_of_planet( PlanetIndexType pIndex );
    void calculate_swiss_ephem_positions();
    void calculate_swiss_epem_position_of_planet( PlanetIndexType pIndex );
    static void calculate_polar_coordinates( PlanetClass &p );
    static void calculate_releated_orbital_elements( PlanetClass &p );
    void zero_orbit( PlanetClass &planet );
    void calculate_perturbations();
    void calculate_moon_perturbations();
    void calculate_jupiter_and_saturn_perturbations();
    void calculate_uranus_perturbations();
};

#endif
