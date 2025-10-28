/***************************************************************************
 *   SymSolon - a free astrology software                                  *
 *   Copyright (C) 2007 by Bela MIHALIK                                    *
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
#ifndef HOUSE_H
#define HOUSE_H

#include "solon_global.h"
#include "solonmath.h"
#include "solarsystem.h"
#include "observer.h"

class HouseClass{

public:
    
    double                cusp[12+1];
    ObserverClass        *observer;
    double                Asc, MC, IC, RA_Asc, RA_MC, RA_IC;
    double                EastPoint;
    double                VertexPoint;
    double                FortunaPoint;
    
    HouseClass();
    ~HouseClass();
    
    void set_observer( ObserverClass *ob );
    void calculate_houses();
    void calculate_points();

private:
    double placidus_cusp(double angle, double ff, int neg);
    double topocentric_cusp( double angle, double lat );

};

#endif
