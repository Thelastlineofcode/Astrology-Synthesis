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
#include "house.h"

#ifdef SWISS_EPHEM
#include "swephexp.h"
#endif

using namespace SolonMath;

HouseClass::HouseClass()
{
    Asc = 0;
    MC = 0;
    IC = 0;
    RA_Asc = 0;
    RA_MC = 0;
    RA_IC = 0;
    EastPoint = 0;
    VertexPoint = 0;
    FortunaPoint = 0;
    memset( cusp, 0, sizeof(cusp) );
}


HouseClass::~HouseClass()
{
}


void
HouseClass::set_observer( ObserverClass *ob )
{
    observer = ob;
}


void
HouseClass::calculate_points()
{
    EastPoint = round_degree( arcustangent2(
                    cosinus( observer->LST ),
                    -sinus( observer->LST ) * cosinus( observer->oecl )
                    ) - observer->ayanamsa );
    VertexPoint = round_degree( EastPoint + 180 );
    FortunaPoint = 0;
}


#define PRIMITIVE_DISTANCE(alfa,beta) \
            ( (beta) < (alfa) ) ? ( 360+(beta) - (alfa) ) : ( (beta) - (alfa) )
    

#define PRIMITIVE1(alfa,beta) round_degree( (alfa)+(1.0*(PRIMITIVE_DISTANCE(alfa,beta))/3.0) )
#define PRIMITIVE2(alfa,beta) round_degree( (alfa)+(2.0*(PRIMITIVE_DISTANCE(alfa,beta))/3.0) )

// convect between equatorial and ecliptic longitude
#define RA_TO_ECL( _ra_ ) \
    round_degree( arcustangent2( sinus(_ra_), cosinus(_ra_)*cosinus(observer->oecl) ) )

#define ECL_TO_RA( _long_ ) \
    round_degree( arcustangent2( sinus(_long_), cosinus(_long_)*cosinus(observer->oecl) ) )

void
HouseClass::calculate_houses()
{
#ifdef SWISS_EPHEM
    int        i=0, hsys='P';
    double    hcusps[14], ascmc[11];
    
    // A/E - Equal (cusp1=Asc)
    // B - Alcabitius
    // C - Campanus
    // H - Azimuthal or Horizontal
    // K - Koch
    // M - Morinus
    // N - Alcabitus
    // O - Porphyry
    // P - Placidus
    // R - Regiomontanus
    // T - Polich/Page ("topocentric")
    // U - Krusinski
    // V - Vehlow equal (Asc. is middle of house 1)
    // X - Axial rotation / Meridian
    // -----
    // G - 36 Gauquelin sectors
    
    switch ( SolonConfig->houseSystem )
    {
        default:
        case HOUSESYSTEM_PLACIDUS: hsys = 'P'; break;
        case HOUSESYSTEM_KOCH: hsys = 'K'; break;
        case HOUSESYSTEM_CAMPANUS: hsys = 'C'; break;
        case HOUSESYSTEM_MERIDIAN: hsys = 'X'; break;
        case HOUSESYSTEM_REGIOMONTANUS: hsys = 'R'; break;
        case HOUSESYSTEM_PORPHYRY: hsys = 'O'; break;
        case HOUSESYSTEM_MORINUS: hsys = 'M'; break;
        case HOUSESYSTEM_TOPOCENTRIC: hsys = 'T'; break;
        case HOUSESYSTEM_VEDIC: hsys = 'P'; break;
        case HOUSESYSTEM_EQUAL: hsys = 'E'; break;
		case HOUSESYSTEM_ALCABITIUS: hsys = 'B'; break;
    }
    
    swe_houses_ex( observer->JD, 0, observer->observerLat, observer->observerLong,
                    hsys, hcusps, ascmc );
    
    Asc = ascmc[ SE_ASC ];
    MC = ascmc[ SE_MC ];
    RA_MC = ascmc[ SE_ARMC ];
    VertexPoint = ascmc[ SE_VERTEX ];
    RA_Asc = ascmc[ SE_EQUASC ];
    //ascmc[ SE_COASC1 ];
    //ascmc[ SE_COASC2 ];
    //ascmc[ SE_POLASC ];
    
    for (i=0; i<=12; i++)
    {
        cusp[i] = hcusps[i];
    }
    
    if ( SolonConfig->houseSystem == HOUSESYSTEM_VEDIC )
    {
        cusp[1]  = Asc - 15;
        cusp[2]  = round_degree( Asc + 15 );
        cusp[3]  = round_degree( Asc + 45 );
        cusp[10] = round_degree( Asc - 105 );
        cusp[11] = round_degree( Asc - 75 );
        cusp[12] = round_degree( Asc - 45 );
        // opposite side cusps
        cusp[4] = round_degree( cusp[10] + 180 );
        cusp[5] = round_degree( cusp[11] + 180 );
        cusp[6] = round_degree( cusp[12] + 180 );
        cusp[7]  = round_degree( cusp[1] + 180 );
        cusp[8]  = round_degree( cusp[2] + 180 );
        cusp[9]  = round_degree( cusp[3] + 180 );
    }
    
#else
    int        i=0;
    double    oecl=0, lat=0;
    double    x1=0, x2=0, x3=0, pol=0, alpha=0, beta=0;
    
    oecl  = observer->oecl;
    lat   = observer->observerLat;
    
    RA_MC = observer->LST;
    RA_IC = round_degree( RA_MC + 180 );
    
    Asc = round_degree( arcustangent2( 
            cosinus( RA_MC ),
            -sinus( RA_MC ) * cosinus( oecl ) -    tangent( lat ) * sinus( oecl )
            ) );
    
    RA_Asc  = ECL_TO_RA( Asc );
    
    MC      = RA_TO_ECL( RA_MC );
    IC      = round_degree( RA_IC );
    
    switch ( SolonConfig->houseSystem )
    {
        default:
        case HOUSESYSTEM_PLACIDUS:
            cusp[1]  = Asc;
            cusp[2]  = placidus_cusp(120.0, 1.5, 1);
            cusp[3]  = placidus_cusp(150.0, 3.0, 1);
            cusp[10] = MC;
            cusp[11] = placidus_cusp(30.0, 3.0, -1);
            cusp[12] = placidus_cusp(60.0, 1.5, -1);
            break;
        
        case HOUSESYSTEM_KOCH:
            x1 = arcussinus( sinus( RA_MC ) * tangent( lat ) * tangent( oecl ) );
            for (i=1; i <= 12; i++) {
                alpha = round_degree( 60.0 + i*30.0 );        
                if (alpha >= 180)
                {
                    pol = -1.0;
                    x2  = (alpha / 90.0) - 3.0;
                }
                else
                {
                    pol = 1.0;
                    x2  = (alpha / 90.0) - 1.0;
                }
                x3 = round_degree( RA_MC + alpha + (x1 * x2) );
                cusp[i] = arcustangent2( sinus(x3),
                        cosinus(x3) * cosinus( oecl ) -    pol * tangent( lat ) * sinus( oecl ) );
            }
            break;
        
        case HOUSESYSTEM_CAMPANUS:
            for (i=1; i<=12; i++)
            {
                alpha = 60.000001 + i * 30.0;
                beta  = arcustangent( tangent(alpha) * cosinus(lat) );
                if ( beta < 0.0 ) beta += 180;
                if ( sinus( alpha ) < 0.0 ) beta += 180;
                cusp[i] = arcustangent2( sinus( RA_MC + beta ),
                            cosinus(RA_MC + beta ) * cosinus( oecl ) -
                                sinus( beta ) * tangent( lat ) * sinus( oecl ) );
            }
            break;
        
        case HOUSESYSTEM_MERIDIAN:
            cusp[1]  = RA_TO_ECL( 90.0 );
            cusp[2]  = RA_TO_ECL( 120.0 );
            cusp[3]  = RA_TO_ECL( 150.0 );
            cusp[10] = RA_TO_ECL( 360.0 );
            cusp[11] = RA_TO_ECL( 30.0 );
            cusp[12] = RA_TO_ECL( 60.0 );
            break;
        
        case HOUSESYSTEM_REGIOMONTANUS:
            for (i=1; i<=12; i++)
            {
                alpha = round_degree( 60.0 + i * 30.0 );
                cusp[i] = arcustangent2( sinus( RA_MC + alpha ),
                            cosinus( RA_MC + alpha ) * cosinus( oecl ) -
                                sinus( alpha ) * tangent( lat ) * sinus( oecl ) );
            }
            break;
        
        case HOUSESYSTEM_PORPHYRY:
            cusp[1]  = Asc;
            cusp[2]  = PRIMITIVE1(Asc, IC);
            cusp[3]  = PRIMITIVE2(Asc, IC);
            cusp[10] = MC;
            cusp[11] = PRIMITIVE1(MC, Asc);
            cusp[12] = PRIMITIVE2(MC, Asc);
            break;
        
        case HOUSESYSTEM_MORINUS:
            for (i=1; i <= 12; i++)
            {
                alpha = round_degree( 60.0 + i * 30.0 );
                cusp[i] = arcustangent2( sinus(RA_MC + alpha) * cosinus( oecl ),
                            cosinus( RA_MC + alpha ) );
            }
            break;
        
        case HOUSESYSTEM_TOPOCENTRIC:
            cusp[1] = topocentric_cusp( 90.0, lat );
            cusp[2] = round_degree(topocentric_cusp( 120.0, arcustangent( tangent( lat ) / 1.5)  ) + 180);
            cusp[3] = round_degree(topocentric_cusp( 150.0, arcustangent( tangent( lat ) / 3.0) ) + 180);
            cusp[10] = MC;
            cusp[11] = topocentric_cusp( 30.0, arcustangent( tangent( lat ) / 3.0) );
            cusp[12] = topocentric_cusp( 60.0, arcustangent( tangent( lat ) / 1.5) );
            break;

        case HOUSESYSTEM_VEDIC:
            cusp[1]  = Asc - 15;
            cusp[2]  = round_degree( Asc + 15 );
            cusp[3]  = round_degree( Asc + 45 );
            cusp[10] = round_degree( Asc - 105 );
            cusp[11] = round_degree( Asc - 75 );
            cusp[12] = round_degree( Asc - 45 );
            break;
        
        case HOUSESYSTEM_EQUAL:
            cusp[1]  = Asc;
            cusp[2]  = round_degree( Asc + 30 );
            cusp[3]  = round_degree( Asc + 60 );
            cusp[10] = round_degree( Asc - 90 );
            cusp[11] = round_degree( Asc - 60 );
            cusp[12] = round_degree( Asc - 30 );
            break;
    }
    
    cusp[4] = round_degree( cusp[10] + 180 );
    cusp[5] = round_degree( cusp[11] + 180 );
    cusp[6] = round_degree( cusp[12] + 180 );
    cusp[7]  = round_degree( cusp[1] + 180 );
    cusp[8]  = round_degree( cusp[2] + 180 );
    cusp[9]  = round_degree( cusp[3] + 180 );
#endif
    
    if (observer->ayanamsa != 0)
    {
        Asc -= observer->ayanamsa;
        MC -= observer->ayanamsa;
        VertexPoint -= observer->ayanamsa;
        for (int i=0; i<=12; i++) cusp[i] -= observer->ayanamsa;
    }
}


double
HouseClass::placidus_cusp(double angle, double ff, int neg)
{
    int        i=0;
    double    lo=0, r1=0, xs=0;
    double    RA_MC = observer->LST;
    double    oecl  = observer->oecl;
    double    lat   = observer->observerLat;
    
    r1 = RA_MC + angle;
    
    for (i = 1; i <= 10; i++)
    {
        xs = neg * sinus(r1) * tangent(oecl) * tangent(lat == 0.0 ? 0.0001 : lat);
        xs = arcuscosinus(xs);
        if (xs < 0.0) xs += 180;
        if (neg >= 0)
        {
            r1 = RA_MC + 180 - (xs/ff);
        }
        else
        {
            r1 = RA_MC + (xs/ff);
        }
    }
    
    //LO = arcustangent2( tangent(R1) , cosinus(oecl) );
    lo = arcustangent( tangent(r1) / cosinus(oecl) );
    if (lo < 0.0) lo += 180;
    if (sinus(r1) < 0.0) lo += 180;
    return lo;
}


double
HouseClass::topocentric_cusp( double angle, double lat )
{
    double    alpha=0, beta=0, gamma=0;
    double    RA_MC = observer->LST;
    double    oecl  = observer->oecl;
    
    alpha = round_degree( RA_MC + angle );
    beta  = arcustangent( tangent(lat) / cosinus(alpha) );
    gamma = arcustangent( cosinus(beta) * tangent(alpha) / cosinus( beta + oecl ) );
    if (gamma < 0.0) gamma += 180;
    if (sinus(gamma) < 0.0) gamma += 180;
    return gamma;
}

