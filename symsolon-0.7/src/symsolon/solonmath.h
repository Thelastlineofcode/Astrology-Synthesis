/***************************************************************************
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

#ifndef SOLON_MATH_H
#define SOLON_MATH_H

#include "solon_global.h"

namespace SolonMath {

char* format_deg( double deg, char *str );
char* format_hour( double deg, char *str );
char* format_astro( double deg, char *str );
double round_degree( double deg );
double sinus( double deg );
double cosinus( double deg );
double arcuscosinus( double val );
double tangent( double deg );
double arcustangent( double val );
double arcustangent2( double x, double y );
double arcussinus( double val );

};

#define ROUND_DEG(x)  SolonMath::round_degree(x)

#define ANGLE_DISTANCE(alpha,beta) \
            ( (beta) < (alpha) ) ? ( 360+(beta) - (alpha) ) : ( (beta) - (alpha) )

#define ANGLE_SIGNED_DISTANCE(alpha,beta) \
            ( (beta)-(alpha) > -180 ? (beta)-(alpha) : (360+(beta))-(alpha) )

#ifndef SQUARE
#define SQUARE(x) ((x)*(x))
#endif

#endif
