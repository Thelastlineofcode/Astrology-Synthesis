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
 * original orbital calculation algorithm from
 *  Paul Schlyter, Stockholm, Sweden
 */
#include "solarsystem.h"

#ifdef SWISS_EPHEM
#include "swephexp.h"
#endif

using namespace SolonMath;


SolarSystemClass::SolarSystemClass()
{
    const int MAX_NUMBER_OF_PLANETS = 100;
    planetVector = new PlanetClass*[MAX_NUMBER_OF_PLANETS];
    
    memset(planetVector, 0, MAX_NUMBER_OF_PLANETS*sizeof(PlanetClass*) );
    numberOfPlanets = 0;
    
    Sun.init( PLANET_SUN );
    Moon.init( PLANET_MOON );
    Mercury.init( PLANET_MERCURY );
    Venus.init( PLANET_VENUS );
    Mars.init( PLANET_MARS );
    Jupiter.init( PLANET_JUPITER );
    Saturn.init( PLANET_SATURN );
    Uranus.init( PLANET_URANUS );
    Neptune.init( PLANET_NEPTUNE );
    Pluto.init( PLANET_PLUTO );
    NNode.init( PLANET_NORTH_NODE );
    SNode.init( PLANET_SOUTH_NODE );
    Ceres.init( PLANET_CERES );
    Eris.init( PLANET_ERIS );
    Chiron.init( PLANET_CHIRON );
    Pallas.init( PLANET_PALLAS );
    Juno.init( PLANET_JUNO );
    Vesta.init( PLANET_VESTA );
    Pholus.init( PLANET_PHOLUS );
    // theoretical planets
    Cupido.init( PLANET_CUPIDO );
    Hades.init( PLANET_HADES );
    Zeus.init( PLANET_ZEUS );
    Kronos.init( PLANET_KRONOS );
    Apollon.init( PLANET_APOLLON );
    Admetos.init( PLANET_ADMETOS );
    Vulkanus.init( PLANET_VULKANUS );
    Poseidon.init( PLANET_POSEIDON );
    Isis.init( PLANET_ISIS );
    Nibiru.init( PLANET_NIBIRU );
    Harrington.init( PLANET_HARRINGTON );
    Leverrier.init( PLANET_LEVERRIER );
    Adams.init( PLANET_ADAMS );
    Lowell.init( PLANET_LOWELL );
    Pickering.init( PLANET_PICKERING );
    Vulcan.init( PLANET_VULCAN );
    WhiteMoon.init( PLANET_WHITE_MOON );
    
    // fill up vector
    planetVector[ numberOfPlanets++ ]  = &Sun;
    planetVector[ numberOfPlanets++ ]  = &Moon;
    planetVector[ numberOfPlanets++ ]  = &Mercury;
    planetVector[ numberOfPlanets++ ]  = &Venus;
    planetVector[ numberOfPlanets++ ]  = &Mars;
    planetVector[ numberOfPlanets++ ]  = &Jupiter;
    planetVector[ numberOfPlanets++ ]  = &Saturn;
    planetVector[ numberOfPlanets++ ]  = &Uranus;
    planetVector[ numberOfPlanets++ ]  = &Neptune;
    planetVector[ numberOfPlanets++ ]  = &Pluto;
    planetVector[ numberOfPlanets++ ]  = &NNode;
    planetVector[ numberOfPlanets++ ]  = &SNode;
    planetVector[ numberOfPlanets++ ]  = &Ceres;
    planetVector[ numberOfPlanets++ ]  = &Eris;
    planetVector[ numberOfPlanets++ ]  = &Chiron;
    planetVector[ numberOfPlanets++ ]  = &Pallas;
    planetVector[ numberOfPlanets++ ]  = &Juno;
    planetVector[ numberOfPlanets++ ]  = &Vesta;
    planetVector[ numberOfPlanets++ ]  = &Pholus;
    // theoretical planets
    planetVector[ numberOfPlanets++ ]  = &Cupido;
    planetVector[ numberOfPlanets++ ]  = &Hades;
    planetVector[ numberOfPlanets++ ]  = &Zeus;
    planetVector[ numberOfPlanets++ ]  = &Kronos;
    planetVector[ numberOfPlanets++ ]  = &Apollon;
    planetVector[ numberOfPlanets++ ]  = &Admetos;
    planetVector[ numberOfPlanets++ ]  = &Vulkanus;
    planetVector[ numberOfPlanets++ ]  = &Poseidon;
    planetVector[ numberOfPlanets++ ]  = &Isis;
    planetVector[ numberOfPlanets++ ]  = &Nibiru;
    planetVector[ numberOfPlanets++ ]  = &Harrington;
    planetVector[ numberOfPlanets++ ]  = &Leverrier;
    planetVector[ numberOfPlanets++ ]  = &Adams;
    planetVector[ numberOfPlanets++ ]  = &Lowell;
    planetVector[ numberOfPlanets++ ]  = &Pickering;
    planetVector[ numberOfPlanets++ ]  = &Vulcan;
    planetVector[ numberOfPlanets++ ]  = &WhiteMoon;
    // END
    planetVector[ numberOfPlanets   ]  = NULL;
}


SolarSystemClass::~SolarSystemClass()
{
    delete planetVector;
}


void
SolarSystemClass::calculate_planet_positions( ObserverClass &ob )
{
    int        i=0;
    
    d = ob.d;
#ifdef SWISS_EPHEM
    calculate_swiss_ephem_positions();
#else
    calculate_raw_positions();
    calculate_perturbations();
#endif
    
    for (i=0; planetVector[i]; i++)
    {
        ob.calculate_coordinates( (PlanetClass&)*planetVector[i] );
    }
}


void
SolarSystemClass::open_swiss_ephem()
{
    swe_set_ephe_path( QString(SolonConfig->sharePath + "/swe").toUtf8().data() );
}


void
SolarSystemClass::close_swiss_ephem()
{
    swe_close();
}


void
SolarSystemClass::calculate_swiss_ephem_positions()
{
#ifdef SWISS_EPHEM
    calculate_swiss_epem_position_of_planet( PLANET_SUN );
    calculate_swiss_epem_position_of_planet( PLANET_MOON );
    calculate_swiss_epem_position_of_planet( PLANET_MERCURY );
    calculate_swiss_epem_position_of_planet( PLANET_VENUS );
    calculate_swiss_epem_position_of_planet( PLANET_MARS );
    calculate_swiss_epem_position_of_planet( PLANET_JUPITER );
    calculate_swiss_epem_position_of_planet( PLANET_SATURN );
    calculate_swiss_epem_position_of_planet( PLANET_URANUS );
    calculate_swiss_epem_position_of_planet( PLANET_NEPTUNE );
    calculate_swiss_epem_position_of_planet( PLANET_PLUTO );
    calculate_swiss_epem_position_of_planet( PLANET_CHIRON );
    calculate_swiss_epem_position_of_planet( PLANET_CERES );
    calculate_swiss_epem_position_of_planet( PLANET_ERIS );
    calculate_swiss_epem_position_of_planet( PLANET_PALLAS );
    calculate_swiss_epem_position_of_planet( PLANET_JUNO );
    calculate_swiss_epem_position_of_planet( PLANET_VESTA );
    calculate_swiss_epem_position_of_planet( PLANET_NORTH_NODE );
    calculate_swiss_epem_position_of_planet( PLANET_SOUTH_NODE );
    calculate_swiss_epem_position_of_planet( PLANET_PHOLUS );
    // uranian & hypotetic planets
    calculate_swiss_epem_position_of_planet( PLANET_CUPIDO );
    calculate_swiss_epem_position_of_planet( PLANET_HADES );
    calculate_swiss_epem_position_of_planet( PLANET_ZEUS );
    calculate_swiss_epem_position_of_planet( PLANET_KRONOS );
    calculate_swiss_epem_position_of_planet( PLANET_APOLLON );
    calculate_swiss_epem_position_of_planet( PLANET_ADMETOS );
    calculate_swiss_epem_position_of_planet( PLANET_VULKANUS );
    calculate_swiss_epem_position_of_planet( PLANET_POSEIDON );
    calculate_swiss_epem_position_of_planet( PLANET_ISIS );
    calculate_swiss_epem_position_of_planet( PLANET_NIBIRU );
    calculate_swiss_epem_position_of_planet( PLANET_HARRINGTON );
    calculate_swiss_epem_position_of_planet( PLANET_LEVERRIER );
    calculate_swiss_epem_position_of_planet( PLANET_ADAMS );
    calculate_swiss_epem_position_of_planet( PLANET_LOWELL );
    calculate_swiss_epem_position_of_planet( PLANET_PICKERING );
    calculate_swiss_epem_position_of_planet( PLANET_VULCAN );
    calculate_swiss_epem_position_of_planet( PLANET_WHITE_MOON );
    calculate_swiss_epem_position_of_planet( PLANET_PROSERPINA );
    calculate_swiss_epem_position_of_planet( PLANET_WALDEMATH );
#endif
}


void
SolarSystemClass::calculate_swiss_epem_position_of_planet( PlanetIndexType pIndex )
{
#ifdef SWISS_EPHEM
    bool    calculated = false;
    double    jd = JULIAN2000 + d;
    char    errStr[256]="", name[256]="";
    double    xx[6];
    
    switch (pIndex)
    {
        case PLANET_SUN:
            calculate_sun_position( d, Sun );
            calculated = true;
            break;
        
        case PLANET_MOON:
            Moon.centerType = PlanetClass::EARTH_CENTERED;
            Moon.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_MOON].name );
            if ( swe_calc_ut( jd, SE_MOON, SEFLG_TRUEPOS, xx, errStr ) >= 0 )
            {
                Moon.longitude = xx[0];
                Moon.latitude  = xx[1];
                Moon.distance  = xx[2] * (11740.5145095519*2);
                calculated = true;
            }
            break;
        
        case PLANET_MERCURY:
            Mercury.centerType = PlanetClass::SOLAR_CENTERED;
            Mercury.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_MERCURY].name );
            if ( swe_calc_ut( jd, SE_MERCURY, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Mercury.longitude = xx[0];
                Mercury.latitude  = xx[1];
                Mercury.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_VENUS:
            Venus.centerType = PlanetClass::SOLAR_CENTERED;
            Venus.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_VENUS].name );
            if ( swe_calc_ut( jd, SE_VENUS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Venus.longitude = xx[0];
                Venus.latitude  = xx[1];
                Venus.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_MARS:
            Mars.centerType = PlanetClass::SOLAR_CENTERED;
            Mars.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_MARS].name );
            if ( swe_calc_ut( jd, SE_MARS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Mars.longitude = xx[0];
                Mars.latitude  = xx[1];
                Mars.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_JUPITER:
            Jupiter.centerType = PlanetClass::SOLAR_CENTERED;
            Jupiter.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_JUPITER].name );
            if ( swe_calc_ut( jd, SE_JUPITER, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Jupiter.longitude = xx[0];
                Jupiter.latitude  = xx[1];
                Jupiter.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_SATURN:
            Saturn.centerType = PlanetClass::SOLAR_CENTERED;
            Saturn.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_SATURN].name );
            if ( swe_calc_ut( jd, SE_SATURN, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Saturn.longitude = xx[0];
                Saturn.latitude  = xx[1];
                Saturn.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_URANUS:
            Uranus.centerType = PlanetClass::SOLAR_CENTERED;
            Uranus.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_URANUS].name );
            if ( swe_calc_ut( jd, SE_URANUS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Uranus.longitude = xx[0];
                Uranus.latitude  = xx[1];
                Uranus.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_NEPTUNE:
            Neptune.centerType = PlanetClass::SOLAR_CENTERED;
            Neptune.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_NEPTUNE].name );
            if ( swe_calc_ut( jd, SE_NEPTUNE, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Neptune.longitude = xx[0];
                Neptune.latitude  = xx[1];
                Neptune.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_PLUTO:
            Pluto.centerType = PlanetClass::SOLAR_CENTERED;
            Pluto.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_PLUTO].name );
            if ( swe_calc_ut( jd, SE_PLUTO, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Pluto.longitude = xx[0];
                Pluto.latitude  = xx[1];
                Pluto.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_CERES:
            Ceres.centerType = PlanetClass::SOLAR_CENTERED;
            Ceres.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_CERES].name );
            if ( swe_calc_ut( jd, SE_CERES, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Ceres.longitude = xx[0];
                Ceres.latitude  = xx[1];
                Ceres.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_ERIS:
            Eris.centerType = PlanetClass::SOLAR_CENTERED;
            Eris.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_ERIS].name );
            strcat(name, "-Eris");
            if ( swe_calc_ut( jd, SE_AST_OFFSET+136199, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Eris.longitude = xx[0];
                Eris.latitude  = xx[1];
                Eris.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_CHIRON:
            Chiron.centerType = PlanetClass::SOLAR_CENTERED;
            Chiron.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_CHIRON].name );
            if ( swe_calc_ut( jd, SE_CHIRON, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Chiron.longitude = xx[0];
                Chiron.latitude  = xx[1];
                Chiron.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_PALLAS:
            Pallas.centerType = PlanetClass::SOLAR_CENTERED;
            Pallas.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_PALLAS].name );
            if ( swe_calc_ut( jd, SE_PALLAS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Pallas.longitude = xx[0];
                Pallas.latitude  = xx[1];
                Pallas.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_JUNO:
            Juno.centerType = PlanetClass::SOLAR_CENTERED;
            Juno.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_JUNO].name );
            if ( swe_calc_ut( jd, SE_JUNO, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Juno.longitude = xx[0];
                Juno.latitude  = xx[1];
                Juno.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_VESTA:
            Vesta.centerType = PlanetClass::SOLAR_CENTERED;
            Vesta.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_VESTA].name );
            if ( swe_calc_ut( jd, SE_VESTA, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Vesta.longitude = xx[0];
                Vesta.latitude  = xx[1];
                Vesta.distance  = xx[2];
                calculated = true;
            }
            break;
            
        case PLANET_NORTH_NODE:
            NNode.centerType = PlanetClass::EARTH_CENTERED;
            NNode.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_NORTH_NODE].name );
            if ( swe_calc_ut( jd, SE_TRUE_NODE, SEFLG_TRUEPOS, xx, errStr ) >= 0 )
            {
                NNode.longitude = xx[0];
                NNode.latitude  = xx[1];
                NNode.distance  = xx[2] * (11740.5145095519*2);
                calculated = true;
            }
            break;
        
        case PLANET_SOUTH_NODE:
            SNode.centerType = PlanetClass::EARTH_CENTERED;
            SNode.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_SOUTH_NODE].name );
            strcat(name, "-South");
            if ( swe_calc_ut( jd, SE_TRUE_NODE, SEFLG_TRUEPOS, xx, errStr ) >= 0 )
            {
                SNode.longitude = round_degree(xx[0] + 180);
                SNode.latitude  = xx[1];
                SNode.distance  = xx[2] * (11740.5145095519*2);
                calculated = true;
            }
            break;
        
        case PLANET_PHOLUS:
            Pholus.centerType = PlanetClass::SOLAR_CENTERED;
            Pholus.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_PHOLUS].name );
            if ( swe_calc_ut( jd, SE_PHOLUS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Pholus.longitude = xx[0];
                Pholus.latitude  = xx[1];
                Pholus.distance  = xx[2];
                calculated = true;
            }
            break;
            
        // ----- uranian & hypotetic planets -----
        case PLANET_CUPIDO:
            Cupido.centerType = PlanetClass::SOLAR_CENTERED;
            Cupido.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_CUPIDO].name );
            if ( swe_calc_ut( jd, SE_CUPIDO, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Cupido.longitude = xx[0];
                Cupido.latitude  = xx[1];
                Cupido.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_HADES:
            Hades.centerType = PlanetClass::SOLAR_CENTERED;
            Hades.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_HADES].name );
            if ( swe_calc_ut( jd, SE_HADES, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Hades.longitude = xx[0];
                Hades.latitude  = xx[1];
                Hades.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_ZEUS:
            Zeus.centerType = PlanetClass::SOLAR_CENTERED;
            Zeus.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_ZEUS].name );
            if ( swe_calc_ut( jd, SE_ZEUS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Zeus.longitude = xx[0];
                Zeus.latitude  = xx[1];
                Zeus.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_KRONOS:
            Kronos.centerType = PlanetClass::SOLAR_CENTERED;
            Kronos.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_KRONOS].name );
            if ( swe_calc_ut( jd, SE_KRONOS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Kronos.longitude = xx[0];
                Kronos.latitude  = xx[1];
                Kronos.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_APOLLON:
            Apollon.centerType = PlanetClass::SOLAR_CENTERED;
            Apollon.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_APOLLON].name );
            if ( swe_calc_ut( jd, SE_APOLLON, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Apollon.longitude = xx[0];
                Apollon.latitude  = xx[1];
                Apollon.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_ADMETOS:
            Admetos.centerType = PlanetClass::SOLAR_CENTERED;
            Admetos.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_ADMETOS].name );
            if ( swe_calc_ut( jd, SE_ADMETOS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Admetos.longitude = xx[0];
                Admetos.latitude  = xx[1];
                Admetos.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_VULKANUS:
            Vulkanus.centerType = PlanetClass::SOLAR_CENTERED;
            Vulkanus.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_VULKANUS].name );
            if ( swe_calc_ut( jd, SE_VULKANUS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Vulkanus.longitude = xx[0];
                Vulkanus.latitude  = xx[1];
                Vulkanus.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_POSEIDON:
            Poseidon.centerType = PlanetClass::SOLAR_CENTERED;
            Poseidon.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_POSEIDON].name );
            if ( swe_calc_ut( jd, SE_POSEIDON, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Poseidon.longitude = xx[0];
                Poseidon.latitude  = xx[1];
                Poseidon.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_ISIS:
            Isis.centerType = PlanetClass::SOLAR_CENTERED;
            Isis.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_ISIS].name );
            if ( swe_calc_ut( jd, SE_ISIS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Isis.longitude = xx[0];
                Isis.latitude  = xx[1];
                Isis.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_NIBIRU:
            Nibiru.centerType = PlanetClass::SOLAR_CENTERED;
            Nibiru.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_NIBIRU].name );
            if ( swe_calc_ut( jd, SE_NIBIRU, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Nibiru.longitude = xx[0];
                Nibiru.latitude  = xx[1];
                Nibiru.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_HARRINGTON:
            Harrington.centerType = PlanetClass::SOLAR_CENTERED;
            Harrington.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_HARRINGTON].name );
            if ( swe_calc_ut( jd, SE_HARRINGTON, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Harrington.longitude = xx[0];
                Harrington.latitude  = xx[1];
                Harrington.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_LEVERRIER:
            Leverrier.centerType = PlanetClass::SOLAR_CENTERED;
            Leverrier.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_LEVERRIER].name );
            if ( swe_calc_ut( jd, SE_NEPTUNE_LEVERRIER, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Leverrier.longitude = xx[0];
                Leverrier.latitude  = xx[1];
                Leverrier.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_ADAMS:
            Adams.centerType = PlanetClass::SOLAR_CENTERED;
            Adams.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_ADAMS].name );
            if ( swe_calc_ut( jd, SE_NEPTUNE_ADAMS, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Adams.longitude = xx[0];
                Adams.latitude  = xx[1];
                Adams.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_LOWELL:
            Lowell.centerType = PlanetClass::SOLAR_CENTERED;
            Lowell.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_LOWELL].name );
            if ( swe_calc_ut( jd, SE_PLUTO_LOWELL, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Lowell.longitude = xx[0];
                Lowell.latitude  = xx[1];
                Lowell.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_PICKERING:
            Pickering.centerType = PlanetClass::SOLAR_CENTERED;
            Pickering.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_PICKERING].name );
            if ( swe_calc_ut( jd, SE_PLUTO_PICKERING, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Pickering.longitude = xx[0];
                Pickering.latitude  = xx[1];
                Pickering.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_VULCAN:
            Vulcan.centerType = PlanetClass::SOLAR_CENTERED;
            Vulcan.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_VULCAN].name );
            if ( swe_calc_ut( jd, SE_VULCAN, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Vulcan.longitude = xx[0];
                Vulcan.latitude  = xx[1];
                Vulcan.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_WHITE_MOON:
            WhiteMoon.centerType = PlanetClass::SOLAR_CENTERED;
            WhiteMoon.hypotetic  = false;
            strcpy( name, Symbol->planetInfo[PLANET_WHITE_MOON].name );
            if ( swe_calc_ut( jd, SE_WHITE_MOON, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                WhiteMoon.longitude = xx[0];
                WhiteMoon.latitude  = xx[1];
                WhiteMoon.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_PROSERPINA:
            Proserpina.centerType = PlanetClass::SOLAR_CENTERED;
            Proserpina.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_PROSERPINA].name );
            if ( swe_calc_ut( jd, SE_PROSERPINA, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Proserpina.longitude = xx[0];
                Proserpina.latitude  = xx[1];
                Proserpina.distance  = xx[2];
                calculated = true;
            }
            break;
        
        case PLANET_WALDEMATH:
            Waldemath.centerType = PlanetClass::SOLAR_CENTERED;
            Waldemath.hypotetic  = true;
            strcpy( name, Symbol->planetInfo[PLANET_WALDEMATH].name );
            if ( swe_calc_ut( jd, SE_WALDEMATH, SEFLG_HELCTR, xx, errStr ) >= 0 )
            {
                Waldemath.longitude = xx[0];
                Waldemath.latitude  = xx[1];
                Waldemath.distance  = xx[2];
                calculated = true;
            }
            break;
        
        default:
            break;
    }
    
    if ( !calculated )
    {
        qDebug(errStr);
        qDebug("Couldn't calculate position of %s (index=%i) at julian day: %f", name, pIndex, jd );
        qDebug("Using analytical method (algorithm from Paul Schlyter)!");
        if ( !calculate_raw_position_of_planet( pIndex ) )
        {
            qDebug("'%s' calculation failed!", name );
        }
        else
        {
            // apply some perturbation rule is needed
            switch (pIndex)
            {
                case PLANET_MOON: calculate_moon_perturbations(); break;
                case PLANET_SATURN: calculate_jupiter_and_saturn_perturbations(); break;
                case PLANET_URANUS: calculate_uranus_perturbations(); break;
                default: break;
            }
        }
    }

#endif
}


void
SolarSystemClass::calculate_raw_positions()
{
    calculate_raw_position_of_planet( PLANET_SUN );
    calculate_raw_position_of_planet( PLANET_MOON );
    calculate_raw_position_of_planet( PLANET_MERCURY );
    calculate_raw_position_of_planet( PLANET_VENUS );
    calculate_raw_position_of_planet( PLANET_MARS );
    calculate_raw_position_of_planet( PLANET_JUPITER );
    calculate_raw_position_of_planet( PLANET_SATURN );
    calculate_raw_position_of_planet( PLANET_URANUS );
    calculate_raw_position_of_planet( PLANET_NEPTUNE );
    calculate_raw_position_of_planet( PLANET_PLUTO );
    calculate_raw_position_of_planet( PLANET_CHIRON );
    calculate_raw_position_of_planet( PLANET_CERES );
    calculate_raw_position_of_planet( PLANET_ERIS );
    calculate_raw_position_of_planet( PLANET_PALLAS );
    calculate_raw_position_of_planet( PLANET_JUNO );
    calculate_raw_position_of_planet( PLANET_VESTA );
    calculate_raw_position_of_planet( PLANET_NORTH_NODE );
    calculate_raw_position_of_planet( PLANET_SOUTH_NODE );
    //PLANET_PHOLUS
    //PLANET_VERTEX
    //PLANET_FORTUNA
    //PLANET_EAST_POINT
}


int
SolarSystemClass::calculate_raw_position_of_planet( PlanetIndexType pIndex )
{
    bool    calculated = false;
    double    P=0, S=0;
    
    switch (pIndex)
    {
        case PLANET_SUN:
            // --- SUN ---
            calculate_sun_position( d, Sun );
            calculated = true;
            break;
            
        case PLANET_MOON:    
            // --- MOON --- !!! Earth centered !!!
            Moon.N = 125.1228 - 0.0529538083 * d;
            Moon.i = 5.1454;
            Moon.w = 318.0634 + 0.1643573223 * d;
            Moon.a = 60.2666; // (Earth radii)
            Moon.e = 0.054900;
            Moon.M = 115.3654 + 13.0649929509 * d;
            Moon.centerType = PlanetClass::EARTH_CENTERED;
            Moon.iteration_error = 0.001;
            calculate_releated_orbital_elements( Moon );
            calculate_polar_coordinates( Moon );
            calculated = true;
            break;
            
        case PLANET_MERCURY:
            // --- MERCURY ---
            Mercury.N =  48.3313 + 3.24587E-5 * d;
            Mercury.i = 7.0047 + 5.00E-8 * d;
            Mercury.w =  29.1241 + 1.01444E-5 * d;
            Mercury.a = 0.387098; // (AU)
            Mercury.e = 0.205635 + 5.59E-10 * d;
            Mercury.M = 168.6562 + 4.0923344368 * d;
            Mercury.centerType = PlanetClass::SOLAR_CENTERED;
            Mercury.iteration_error = 0.001;
            calculate_releated_orbital_elements( Mercury );
            calculate_polar_coordinates( Mercury );
            calculated = true;
            break;
            
        case PLANET_VENUS:
            // --- VENUS ---
            Venus.N =  76.6799 + 2.46590E-5 * d;
            Venus.i = 3.3946 + 2.75E-8 * d;
            Venus.w =  54.8910 + 1.38374E-5 * d;
            Venus.a = 0.723330; //  (AU)
            Venus.e = 0.006773 - 1.302E-9 * d;
            Venus.M =  48.0052 + 1.6021302244 * d;
            Venus.centerType = PlanetClass::SOLAR_CENTERED;
            Venus.iteration_error = 0.001;
            calculate_releated_orbital_elements( Venus );
            calculate_polar_coordinates( Venus );
            calculated = true;
            break;
            
        case PLANET_MARS:
            // --- MARS ---
            Mars.N =  49.5574 + 2.11081E-5 * d;
            Mars.i = 1.8497 - 1.78E-8 * d;
            Mars.w = 286.5016 + 2.92961E-5 * d;
            Mars.a = 1.523688; // (AU)
            Mars.e = 0.093405 + 2.516E-9 * d;
            Mars.M =  18.6021 + 0.5240207766 * d;
            Mars.centerType = PlanetClass::SOLAR_CENTERED;
            Mars.iteration_error = 0.001;
            calculate_releated_orbital_elements( Mars );
            calculate_polar_coordinates( Mars );
            calculated = true;
            break;
            
        case PLANET_JUPITER:
            // --- JUPITER ---
            Jupiter.N = 100.4542 + 2.76854E-5 * d;
            Jupiter.i = 1.3030 - 1.557E-7 * d;
            Jupiter.w = 273.8777 + 1.64505E-5 * d;
            Jupiter.a = 5.20256; // (AU)
            Jupiter.e = 0.048498 + 4.469E-9 * d;
            Jupiter.M =  19.8950 + 0.0830853001 * d;
            Jupiter.centerType = PlanetClass::SOLAR_CENTERED;
            Jupiter.iteration_error = 0.001;
            calculate_releated_orbital_elements( Jupiter );
            calculate_polar_coordinates( Jupiter );
            calculated = true;
            break;
            
        case PLANET_SATURN:
            // --- SATURN ---
            Saturn.N = 113.6634 + 2.38980E-5 * d;
            Saturn.i = 2.4886 - 1.081E-7 * d;
            Saturn.w = 339.3939 + 2.97661E-5 * d;
            Saturn.a = 9.55475; // (AU)
            Saturn.e = 0.055546 - 9.499E-9 * d;
            Saturn.M = 316.9670 + 0.0334442282 * d;
            Saturn.centerType = PlanetClass::SOLAR_CENTERED;
            Saturn.iteration_error = 0.001;
            calculate_releated_orbital_elements( Saturn );
            calculate_polar_coordinates( Saturn );
            calculated = true;
            break;
            
        case PLANET_URANUS:
            // --- URANUS ---
            Uranus.N =  74.0005 + 1.3978E-5 * d;
            Uranus.i = 0.7733 + 1.9E-8 * d;
            Uranus.w =  96.6612 + 3.0565E-5 * d;
            Uranus.a = 19.18171 - 1.55E-8 * d; // (AU)
            Uranus.e = 0.047318 + 7.45E-9 * d;
            Uranus.M = 142.5905 + 0.011725806 * d;
            Uranus.centerType = PlanetClass::SOLAR_CENTERED;
            Uranus.iteration_error = 0.001;
            calculate_releated_orbital_elements( Uranus );
            calculate_polar_coordinates( Uranus );
            calculated = true;
            break;
            
        case PLANET_NEPTUNE:
            // --- NEPTUNE ---
            Neptune.N = 131.7806 + 3.0173E-5 * d;
            Neptune.i = 1.7700 - 2.55E-7 * d;
            Neptune.w = 272.8461 - 6.027E-6 * d;
            Neptune.a = 30.05826 + 3.313E-8 * d; // (AU)
            Neptune.e = 0.008606 + 2.15E-9 * d;
            Neptune.M = 260.2471 + 0.005995147 * d;
            Neptune.centerType = PlanetClass::SOLAR_CENTERED;
            Neptune.iteration_error = 0.001;
            calculate_releated_orbital_elements( Neptune );
            calculate_polar_coordinates( Neptune );
            calculated = true;
            break;
            
        case PLANET_PLUTO:
            // --- PLUTO ---
            // orbital elements just typed as informations
            // not used for calculation !!!
            Pluto.N = 110.30347 + 3.82394E-5 * d;
            Pluto.i = 17.14175;
            Pluto.w = 224.06676;
            Pluto.a = 39.48168677; // (AU)
            Pluto.e = 0.24880766;
            Pluto.M = 238.92881 + 0.003973966*d;
            Pluto.centerType = PlanetClass::SOLAR_CENTERED;
            Pluto.iteration_error = 0.001;
            
            // --- plar coordinated with perturbations of pluto (valid from 1900 to 2100) ---
            S  =   50.03  +  0.033459652 * d;
            P  =  238.95  +  0.003968789 * d;
            // -
            Pluto.longitude = 238.9508  +  0.00400703 * d
                        - 19.799 * sinus(P)     + 19.848 * cosinus(P)
                        + 0.897 * sinus(2*P)    - 4.956 * cosinus(2*P)
                        + 0.610 * sinus(3*P)    + 1.211 * cosinus(3*P)
                        - 0.341 * sinus(4*P)    - 0.190 * cosinus(4*P)
                        + 0.128 * sinus(5*P)    - 0.034 * cosinus(5*P)
                        - 0.038 * sinus(6*P)    + 0.031 * cosinus(6*P)
                        + 0.020 * sinus(S-P)    - 0.010 * cosinus(S-P);
            
            Pluto.latitude = -3.9082
                        - 5.453 * sinus(P)     - 14.975 * cosinus(P)
                        + 3.527 * sinus(2*P)    + 1.673 * cosinus(2*P)
                        - 1.051 * sinus(3*P)    + 0.328 * cosinus(3*P)
                        + 0.179 * sinus(4*P)    - 0.292 * cosinus(4*P)
                        + 0.019 * sinus(5*P)    + 0.100 * cosinus(5*P)
                        - 0.031 * sinus(6*P)    - 0.026 * cosinus(6*P)
                        + 0.011 * cosinus(S-P);
        
            Pluto.distance =  40.72
                        + 6.68 * sinus(P)       + 6.90 * cosinus(P)
                        - 1.18 * sinus(2*P)     - 0.03 * cosinus(2*P)
                        + 0.15 * sinus(3*P)     - 0.14 * cosinus(3*P);
            calculated = true;
            break;
            
        case PLANET_CERES:
            // --- CERES ---
            Ceres.N = 80.4069591479241 + 3.82394E-5 * d;
            Ceres.i = 10.5867116079954;
            Ceres.w = 73.15073411326651;
            Ceres.a = 2.76595642396794; // (AU)
            Ceres.e = 0.0797601732738271;
            Ceres.M = (215.800962246862-569.28) + 0.2142575197691738*d;
            Ceres.centerType = PlanetClass::SOLAR_CENTERED;
            Ceres.iteration_error = 0.001;
            calculate_releated_orbital_elements( Ceres );
            calculate_polar_coordinates( Ceres );
            calculated = true;
            break;
            
        case PLANET_ERIS:
            // --- ERIS ---
            Eris.N = 35.88444731431473 + 3.82394E-5 * d;
            Eris.i = 44.1594807936589;
            Eris.w = 151.5586008885899;
            Eris.a = 67.7315530579866; // (AU)
            Eris.e = 0.439987020586636;
            Eris.M = (197.9647736017444-4.6980) + 0.001768143557755414*d;
            Eris.centerType = PlanetClass::SOLAR_CENTERED;
            Eris.iteration_error = 0.001;
            calculate_releated_orbital_elements( Eris );
            calculate_polar_coordinates( Eris );
            calculated = true;
            break;
            
        case PLANET_CHIRON:
            // --- CHIRON ---
            Chiron.N = 209.39343 + 3.82394E-5 * d;
            Chiron.i = 6.92811;
            Chiron.w = 339.48791;
            Chiron.a = 13.7260805; // (AU)
            Chiron.e = 0.3840730;
            Chiron.M = (353.67214+33.762) + 0.01938136*d;
            Chiron.centerType = PlanetClass::SOLAR_CENTERED;
            Chiron.iteration_error = 0.001;
            calculate_releated_orbital_elements( Chiron );
            calculate_polar_coordinates( Chiron );
            calculated = true;
            break;
            
        case PLANET_PALLAS:
            // --- PALLAS ---
            Pallas.N = 173.13579 + 3.82394E-5 * d;
            Pallas.i = 34.84182;
            Pallas.w = 310.34481;
            Pallas.a = 2.7716684; // (AU)
            Pallas.e = 0.2307589;
            Pallas.M = (199.72616-567.52) + 0.21359553*d;
            Pallas.centerType = PlanetClass::SOLAR_CENTERED;
            Pallas.iteration_error = 0.001;
            calculate_releated_orbital_elements( Pallas );
            calculate_polar_coordinates( Pallas );
            calculated = true;
            break;
            
        case PLANET_JUNO:
            // --- JUNO ---
            Juno.N = 170.1200140677265 + 3.82394E-5 * d;
            Juno.i = 12.9703715756103;
            Juno.w = 247.8419926437428;
            Juno.a = 2.66788415832988; // (AU)
            Juno.e = 0.258023236359691;
            Juno.M = (121.2242163545212-600.96) + 0.2261796988771801*d;
            Juno.centerType = PlanetClass::SOLAR_CENTERED;
            Juno.iteration_error = 0.001;
            calculate_releated_orbital_elements( Juno );
            calculate_polar_coordinates( Juno );
            calculated = true;
            break;
            
        case PLANET_VESTA:
            // --- VESTA ---
            Vesta.N = 103.92607 + 3.82394E-5 * d;
            Vesta.i = 7.13351;
            Vesta.w = 150.30933;
            Vesta.a = 2.3613051; // (AU)
            Vesta.e = 0.0890882;
            Vesta.M = (232.80490-613.07) + 0.27162887*d;
            Vesta.centerType = PlanetClass::SOLAR_CENTERED;
            Vesta.iteration_error = 0.001;
            calculate_releated_orbital_elements( Vesta );
            calculate_polar_coordinates( Vesta );
            calculated = true;
            break;
            
        case PLANET_NORTH_NODE:
            // --- NORTH_NODE ---
            NNode.centerType = PlanetClass::EARTH_CENTERED;
            NNode.distance  = 60.2666; // !!! aproximatly
            NNode.longitude = SolonMath::round_degree( 125.1228 - 0.0529538083 * d );
            NNode.latitude  = 0;
            calculated = true;
            break;
            
        case PLANET_SOUTH_NODE:
            // --- SOUTH_NODE ---
            SNode.centerType = PlanetClass::EARTH_CENTERED;
            SNode.distance  = 60.2666; // !!! aproximatly
            SNode.longitude = SolonMath::round_degree( 125.1228 - 0.0529538083 * d + 180 );
            SNode.latitude  = 0;
            calculated = true;
            break;
            
        default:
            break;
    }
    
    return calculated;
}


/* caclulating sun position in separated static function
 * because we call it from outside
 * (the position of the sun is releated to earth, means
 *  we calculate the earth position to get sun position)
 */
void
SolarSystemClass::calculate_sun_position( double dayTime, PlanetClass &sun )
{
    bool    calculated = false;
    
#ifdef SWISS_EPHEM
    double    jd = JULIAN2000 + dayTime;
    char    errStr[256] = "";
    double    xx[6];
    
    sun.init( PLANET_SUN );
    sun.centerType = PlanetClass::THIS_IS_SUN;
    sun.hypotetic  = false;
    if (swe_calc_ut( jd, SE_EARTH, SEFLG_HELCTR, xx, errStr ) >= 0)
    {
        sun.longitude = round_degree( xx[0] + 180 );
        sun.latitude  = 0;
        sun.distance  = xx[2];
        calculated    = true;
    }
    else
    {
        qDebug( "Couldn't calculate position of Sun at julian day:%f", jd );
        qDebug( errStr );
    }
#endif
    
    if (!calculated)
    {
        sun.init( PLANET_SUN );
        sun.N = 0.0;
        sun.i = 0.0;
        sun.w = 282.9404 + 4.70935E-5 * dayTime;
        sun.a = 1.000000; //  (AU)
        sun.e = 0.016709 - 1.151E-9 * dayTime;
        sun.M = 356.0470 + 0.9856002585 * dayTime;
        sun.centerType = PlanetClass::THIS_IS_SUN;
        sun.iteration_error = 0;
        calculate_releated_orbital_elements( sun );
        // calculate polar coordinates
        sun.longitude = round_degree( sun.v + sun.w );
        sun.latitude  = 0;
        sun.distance  = sun.r;
    }
}


void
SolarSystemClass::calculate_perturbations()
{
    calculate_moon_perturbations();
    calculate_jupiter_and_saturn_perturbations();
    calculate_uranus_perturbations();
}


void
SolarSystemClass::calculate_moon_perturbations()
{
    double        Ms=0, Mm=0, Nm=0, ws=0, wm=0,
                Ls=0, Lm=0, D=0, F=0;
    
    // --- calculate perturbations of the moon ---
    
    Ms = Sun.M;            // Mean Anomaly of the Sun
    Mm = Moon.M;        // Mean Anomaly of the Moon
    Nm = Moon.N;        // Longitude of the Moon's node
    ws = Sun.w;            // Argument of perihelion for the Sun
    wm = Moon.w;        // Argument of perihelion for the Moon
    Ls = Ms + ws;        // Mean Longitude of the Sun  (Ns=0)
    Lm = Mm + wm + Nm;    // Mean longitude of the Moon
    D = Lm - Ls;        // Mean elongation of the Moon
    F = Lm - Nm;        // Argument of latitude for the Moon
    
    Moon.longitude +=
                - 1.274 * sinus(Mm - 2*D)          // (the Evection)
                + 0.658 * sinus(2*D)               // (the Variation)
                - 0.186 * sinus(Ms)                // (the Yearly Equation)
                - 0.059 * sinus(2*Mm - 2*D)
                - 0.057 * sinus(Mm - 2*D + Ms)
                + 0.053 * sinus(Mm + 2*D)
                + 0.046 * sinus(2*D - Ms)
                + 0.041 * sinus(Mm - Ms)
                - 0.035 * sinus(D)                 // (the Parallactic Equation)
                - 0.031 * sinus(Mm + Ms)
                - 0.015 * sinus(2*F - 2*D)
                + 0.011 * sinus(Mm - 4*D);
    
    Moon.latitude +=
                - 0.173 * sinus(F - 2*D)
                - 0.055 * sinus(Mm - F - 2*D)
                - 0.046 * sinus(Mm + F - 2*D)
                + 0.033 * sinus(F + 2*D)
                + 0.017 * sinus(2*Mm + F);
    
    // distance calculated in unit of radius of the earth
    Moon.distance +=
                - 0.58 * cosinus(Mm - 2*D)
                - 0.46 * cosinus(2*D);
}


void
SolarSystemClass::calculate_jupiter_and_saturn_perturbations()
{
    double        Ms=0, Mj=0, Msa=0, Mu=0;
    
    // --- calculate perturbations for jupiter, saturn and uranus ---
    
    Ms = Sun.M;            // Mean Anomaly of the Sun
    Mj  = Jupiter.M;    // Mean anomaly of Jupiter
    Msa = Saturn.M;        // Mean anomaly of Saturn
    Mu  = Uranus.M;        // Mean anomaly of Uranus (needed for Uranus only)
    
    Jupiter.longitude +=
                -0.332 * sinus(2*Mj - 5*Msa - 67.6)
                -0.056 * sinus(2*Mj - 2*Msa + 21)
                +0.042 * sinus(3*Mj - 5*Msa + 21)
                -0.036 * sinus(Mj - 2*Msa)
                +0.022 * cosinus(Mj - Msa)
                +0.023 * sinus(2*Mj - 3*Msa + 52)
                -0.016 * sinus(Mj - 5*Ms - 69);
    
    Saturn.longitude +=
                +0.812 * sinus(2*Mj - 5*Msa - 67.6)
                -0.229 * cosinus(2*Mj - 4*Msa - 2)
                +0.119 * sinus(Mj - 2*Msa - 3)
                +0.046 * sinus(2*Mj - 6*Msa - 69)
                +0.014 * sinus(Mj - 3*Msa + 32);
    
    Saturn.latitude +=
                -0.020 * cosinus(2*Mj - 4*Msa - 2)
                +0.018 * sinus(2*Mj - 6*Msa - 49);
}


void
SolarSystemClass::calculate_uranus_perturbations()
{
    double        Mj=0, Msa=0, Mu=0;
    
    // --- calculate perturbations for jupiter, saturn and uranus ---
    
    Mj  = Jupiter.M;    // Mean anomaly of Jupiter
    Msa = Saturn.M;        // Mean anomaly of Saturn
    Mu  = Uranus.M;        // Mean anomaly of Uranus (needed for Uranus only)
    
    Uranus.longitude +=
                +0.040 * sinus(Msa - 2*Mu + 6)
                +0.035 * sinus(Msa - 3*Mu + 33)
                -0.015 * sinus(Mj - Mu + 20);
}


void
SolarSystemClass::calculate_polar_coordinates( PlanetClass &p )
{
    double    xh=0, yh=0, zh=0;
    
    xh = p.r * ( cosinus( p.N ) * cosinus( p.v + p.w ) - sinus( p.N ) * sinus( p.v + p.w ) * cosinus( p.i ) );
    yh = p.r * ( sinus( p.N ) * cosinus( p.v + p.w ) + cosinus( p.N ) * sinus( p.v + p.w ) * cosinus( p.i ) );
    zh = p.r * ( sinus( p.v + p.w ) * sinus( p.i ) );
    
    p.longitude = arcustangent2( yh, xh );
    p.latitude  = arcustangent2( zh, sqrt( xh*xh + yh*yh ) );
    p.distance  = sqrt( xh*xh + yh*yh + zh*zh );
    
    p.longitude = round_degree( p.longitude );
    p.latitude  = round_degree( p.latitude );
}


void
SolarSystemClass::calculate_releated_orbital_elements( PlanetClass &p )
{
    double        E0=0, E1=0, i=0, xv=0, yv=0;
    
    // round to 360 degree
    p.N = round_degree( p.N );
    p.M = round_degree( p.M );
    p.w = round_degree( p.w );
    
    // calculate releated orbital elements
    p.w1 = p.N + p.w;
    p.L  = p.M + p.w1;
    p.q  = p.a * ( 1 - p.e );
    p.Q  = p.a * ( 1 + p.e );
    //p.P  = pow( p.a, 1.5 );
    //p.T  = Epoch_of_M - ( ( p.M / 360.0 ) / p.P );
    
    // compute the eccentric anomaly E from the mean anomaly M and from the eccentricity e
    p.E = p.M + p.e * ( 180 / M_PI ) * sinus( p.M ) * ( 1.0 + p.e * cosinus( p.M ) );
    
    if ( p.iteration_error > 0 )
    {
        E1 = p.E;
        i = 0;
        
        do
        {
            E0 = E1;
            E1 = E0 - ( E0 - p.e * ( 180.0 / M_PI ) * sinus( E0 ) - p.M ) / ( 1.0 - p.e * cosinus( E0 ) );
            i++;
        }
        while ( (fabs( E0 - E1 ) < p.iteration_error) && (i < 1000) );
        
        // if formula won't converge
        if (i>=1000)
        {
            // near-parabolic orbit
            
            // parabolic orbit
            
        }
        
        p.E = E1;
    }
    
    // Then compute the planet's distance r and its true anomaly v from
    xv = p.a * ( cosinus( p.E ) - p.e );
    yv = p.a * ( sqrt( 1.0 - p.e * p.e ) * sinus( p.E ) );
    p.v = arcustangent2( yv, xv );
    p.r = sqrt( xv * xv + yv * yv );

    p.v = round_degree( p.v );
}

