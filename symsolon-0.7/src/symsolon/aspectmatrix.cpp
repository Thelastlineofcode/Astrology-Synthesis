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
#include "aspectmatrix.h"


AspectMatrixClass::AspectMatrixClass()
{
    memset( matrix, 0, sizeof(matrix) );
}


AspectMatrixClass::~AspectMatrixClass()
{
}


void
AspectMatrixClass::calculate( SolarSystemClass *solsys1, SolarSystemClass *solsys2 )
{
    int                i=0, j=0, k=0, n=0;
    PlanetClass        **pv1=NULL, **pv2=NULL;
    double            diff=0, orbit=0, orbitMirror=0, result=0;
    
    if (solsys1 == NULL) return;
    if (solsys2 == NULL)
    {
        pv1 = pv2 = solsys1->planetVector;
    }
    else // synastry or transit analysis
    {
        pv1 = solsys1->planetVector;
        pv2 = solsys2->planetVector;
    }
    
    n = solsys1->numberOfPlanets;
    
    memset( matrix, 0, sizeof(matrix) );
    memset( powerMatrix, 0, sizeof(powerMatrix) );
    
    for (i=0; i<n; i++)
    {
        for (j=0; j<n; j++)
        {
            if ( pv1==pv2 && i==j ) continue;
            if ( (pv1[i]->index == PLANET_SOUTH_NODE && pv2[j]->index == PLANET_NORTH_NODE) ||
                 (pv1[i]->index == PLANET_NORTH_NODE && pv2[j]->index == PLANET_SOUTH_NODE) )
            {
                continue;
            }
            if ( pv1[i]->Long >= pv2[j]->Long ) diff = pv1[i]->Long - pv2[j]->Long;
                                           else diff = (pv1[i]->Long+360) - pv2[j]->Long;
            if (diff > 180) diff = 360 - diff;
                        
            for (k=0; k<ASPECT_MAX; k++)
            {
                if (SolonConfig->aspectOrbitAsLimit)
                {
                    orbit =    (Symbol->planetInfo[ pv1[i]->index ].orbit/2) +
                            (Symbol->planetInfo[ pv2[j]->index ].orbit/2);
                    if (orbit > Symbol->aspectInfo[k].orbit)
                            orbit = Symbol->aspectInfo[k].orbit;
                }
                else
                {
                    orbit = (Symbol->aspectInfo[k].orbit) +
                        (Symbol->planetInfo[ pv1[i]->index ].orbit/2) +
                        (Symbol->planetInfo[ pv2[j]->index ].orbit/2);
                }
                
                if ( !Symbol->aspectInfo[k].enabled ) continue;
                if ( k == ASPECT_MIRROR )
                {
                    orbitMirror = orbit;
                    result = ABSOLUTE( pv1[i]->Long - (360-pv2[j]->Long) ) - orbitMirror;
                    if ( result <= 0 )
                    {
                        matrix[ pv1[i]->index ][ pv2[j]->index] = (AspectIndexType)k;
                        powerMatrix[ pv1[i]->index ][ pv2[j]->index] =
                                                (int)(-(100*result)/orbitMirror);
                    }
                }
                else
                {
                    result = ABSOLUTE( Symbol->aspectInfo[k].angle - diff );                    
                    if ( result <= orbit )
                    {
                        matrix[ pv1[i]->index ][ pv2[j]->index] = (AspectIndexType)k;
                        powerMatrix[ pv1[i]->index ][ pv2[j]->index] =
                                                    100-(int)((100*result)/orbit);
                    }
                }
            }
        }
    }
}

