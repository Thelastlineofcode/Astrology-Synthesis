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

#include "planet.h"

PlanetClass::PlanetClass()
{
    clear_orbital_elements();
}


PlanetClass::PlanetClass( int _index )
{
    clear_orbital_elements();
    init( _index );
}


PlanetClass::~PlanetClass()
{
}


void
PlanetClass::init( int _index )
{
    index  = (PlanetIndexType)_index;
    name   = Symbol->planetInfo[index].name;
}


void
PlanetClass::clear_orbital_elements()
{
    N = 0;
    i = 0;
    w = 0;
    a = 0;
    e = 0;
    M = 0;
    iteration_error = 0;
    w1 = 0;
    L = 0;
    q = 0;
    Q = 0;
    v = 0;
    E = 0;
    r = 0;
}

