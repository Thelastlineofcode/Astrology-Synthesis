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

#ifndef SOLON_GLOBAL_H
#define SOLON_GLOBAL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>
#include <math.h>

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>

#include <QObject>
#include <QtGui/QApplication>
#include <QtGui/QWidget>
#include <QtGui/QPainter>
#include <QDebug>

#define SWISS_EPHEM         on

#define SYMBOLON_MAX        79
#define HOUSE_MAX           13

typedef enum
{
    INFOTYPE_NONE=0,
    INFOTYPE_PLANET,
    INFOTYPE_SIGN,
    INFOTYPE_ASPECT,
    INFOTYPE_HOUSE,
    INFOTYPE_SYMBOLON,
    INFOTYPE_TRANSIT,
    INFOTYPE_PLANETASPECT,
    INFOTYPE_MAX
} InfoType;

typedef enum
{
    SIGN_NONE=0,
    SIGN_ARIES,
    SIGN_TAURUS,
    SIGN_GEMINI,
    SIGN_CANCER,
    SIGN_LEO,
    SIGN_VIRGO,
    SIGN_LIBRA,
    SIGN_SCORPION,
    SIGN_SAGITTARIUS,
    SIGN_CAPRICORN,
    SIGN_AQUARIUS,
    SIGN_PISCES,
    SIGN_MAX,
    SIGN_FORCE_TAURUS,
    SIGN_FORCE_GEMINI,
    SIGN_FORCE_VIRGO,
    SIGN_FORCE_LIBRA
} SignIndexType;


typedef enum
{
    PLANET_NONE=0,
    PLANET_SUN,
    PLANET_MOON,
    PLANET_MERCURY,
    PLANET_VENUS,
    PLANET_EARTH,
    PLANET_MARS,
    PLANET_JUPITER,
    PLANET_SATURN,
    PLANET_URANUS,
    PLANET_NEPTUNE,
    PLANET_PLUTO,
    PLANET_NORTH_NODE,
    PLANET_SOUTH_NODE,
    PLANET_CHIRON,
    PLANET_CERES,
    PLANET_ERIS,
    PLANET_PALLAS,
    PLANET_JUNO,
    PLANET_VESTA,
    PLANET_PHOLUS,
    // uranian & hypotetic planets
    PLANET_CUPIDO,
    PLANET_HADES,
    PLANET_ZEUS,
    PLANET_KRONOS,
    PLANET_APOLLON,
    PLANET_ADMETOS,
    PLANET_VULKANUS,
    PLANET_POSEIDON,
    PLANET_ISIS,
    PLANET_NIBIRU,
    PLANET_HARRINGTON,
    PLANET_LEVERRIER,
    PLANET_ADAMS,
    PLANET_LOWELL,
    PLANET_PICKERING,
    PLANET_VULCAN,
    PLANET_WHITE_MOON,
    PLANET_PROSERPINA,
    PLANET_WALDEMATH,
    PLANET_MAX
} PlanetIndexType;


typedef enum
{
    POINT_NONE=0,
    POINT_VERTEX,
    POINT_FORTUNA,
    POINT_EAST_POINT,
    POINT_MAX
} PointIndexType;


typedef enum
{
    ASPECT_NONE=0,
    ASPECT_CONJUCT,         // 0      ^ 7
    ASPECT_SEMIDECILE,      // 18     ^ 1
    ASPECT_SEMISEXTIL,      // 30     ^ 3
    ASPECT_UNDECIM,         // 32.73  ^ 1
    ASPECT_SEMIQUINTIL,     // 36     ^ 1
    ASPECT_NOVIL,           // 40     ^ 1
    ASPECT_SEMIQUADRAT,     // 45     ^ 3
    ASPECT_SEPTIL,          // 51.43  ^ 1
    ASPECT_SEXTIL,          // 60     ^ 6
    ASPECT_BIUNDECIM,       // 65.45  ^ 1
    ASPECT_QUINTIL,         // 72     ^ 2
    ASPECT_BINOVIL,         // 80     ^ 1
    ASPECT_QUADRAT,         // 90     ^ 7
    ASPECT_TRIUNDECIM,      // 98.18  ^ 1
    ASPECT_BISEPTILE,       // 102.86 ^ 1
    ASPECT_SQUINE,          // 105    ^ 1
    ASPECT_SESQUIQUINTILE,  // 108 ^ 1
    ASPECT_TRIGON,          // 120    ^ 7
    ASPECT_QUADRIUNDECIM,   // 130.9^ 1
    ASPECT_SESQUIQUADRAT,   // 135  ^ 3
    ASPECT_BIQUINTIL,       // 144    ^ 2
    ASPECT_QUINCUNX,        // 150    ^ 3
    ASPECT_TRISEPTIL,       // 154.29 ^ 1
    ASPECT_QUANTONOVIL,     // 160    ^ 1
    ASPECT_QUINQUEUNDECIM,  // 163.6 ^ 1
    ASPECT_QUINDECILE,      // 165    ^ 1
    ASPECT_OPPOSITE,        // 180    ^ 7
    ASPECT_MIRROR,          // -      ^ 1
    ASPECT_MAX
} AspectIndexType;


typedef enum
{
    HOUSESYSTEM_NONE=0,
    HOUSESYSTEM_PLACIDUS,
    HOUSESYSTEM_KOCH,
    HOUSESYSTEM_EQUAL,
    HOUSESYSTEM_CAMPANUS,
    HOUSESYSTEM_MERIDIAN,
    HOUSESYSTEM_REGIOMONTANUS,
    HOUSESYSTEM_PORPHYRY,
    HOUSESYSTEM_MORINUS,
    HOUSESYSTEM_VEDIC,
    HOUSESYSTEM_TOPOCENTRIC,
	HOUSESYSTEM_ALCABITIUS,
	HOUSESYSTEM_MAX
} HouseSystemEnum;


typedef enum
{
    AYANAMSA_NONE=0,
    AYANAMSA_FAGAN_BRADLEY,
    AYANAMSA_LAHIRI,
    AYANAMSA_DELUCE,
    AYANAMSA_RAMAN,
    AYANAMSA_JONES,
    AYANAMSA_JOHNRDO,
    AYANAMSA_CAYCE,
    AYANAMSA_JUNG,
    AYANAMSA_RUDHYAR,
    AYANAMSA_DOBYNS,
    AYANAMSA_ELY,
    AYANAMSA_USHA_SHASHI,
    AYANAMSA_MAX
} AyanamsaEnum;


typedef enum {
    SCOPE_NONE=0,
    // classic
    SCOPE_CIRCLE,
    SCOPE_RECTANGLE,
    SCOPE_BOX,
    SCOPE_SYNASTRY,
    SCOPE_TRANSITS,
    SCOPE_LIFECYRCLE,
    // symbolon
    SCOPE_SYMBOLON_ASCSUN,
    SCOPE_SYMBOLON_DIALECTIC,
    SCOPE_SYMBOLON_ASC_INFLUENCE,
    SCOPE_SYMBOLON_SUN_INFLUENCE,
    SCOPE_SYMBOLON_MC_INFLUENCE,
    SCOPE_SYMBOLON_HOUSE_MANDAL,
    SCOPE_SYMBOLON_PLANET_HOUSE_MANDAL,
    SCOPE_SYMBOLON_PLANET_SIGN_MANDAL,
    SCOPE_SYMBOLON_PLANET_ANALYSIS,
    SCOPE_SYMBOLON_PLANET_ASPECTS,
    SCOPE_SYMBOLON_EXPLORE,
    // dataScope
    SCOPE_BASIC_DATA,
    SCOPE_ASPECTMATRIX,
    SCOPE_QUALITY_MATRICES,
    SCOPE_PLANET_INFO,
    SCOPE_TRANSIT_INFO,
    SCOPE_LIFECYRCLE_INFO,
    SCOPE_SYNASTRY_INFO,
    SCOPE_SYNASTRY_VENUSMARS_INFO,
    SCOPE_SYNASTRY_SUNASC_INFO,
    SCOPE_SYNASTRY_PLUTO_INFO,
    SCOPE_MAX
} ScopeStyleType;


typedef enum {
    DATASTYLE_NONE=0,
    DATASTYLE_BASIC,
    DATASTYLE_ASPECTMATRIX,
    DATASTYLE_MAX
} DataStyleType;


typedef enum {
    ALIGN_NONE=0,
    ALIGN_LEFT,
    ALIGN_RIGHT,
    ALIGN_CENTER,
    ALIGN_JUSIFY
} AlignType;

typedef enum {
    TIMESTEP_NONE=0,
    TIMESTEP_YEAR,
    TIMESTEP_MONTH,
    TIMESTEP_WEEK,
    TIMESTEP_DAY,
    TIMESTEP_HOUR,
    TIMESTEP_MINUTE,
    TIMESTEP_SECOND,
    TIMESTEP_MAX
} TimeStepType;

typedef enum {
    VALIGN_NONE=0,
    ALIGN_TOP,
    ALIGN_BOTTOM,
    ALIGN_MIDDLE
} VAlignType;

typedef enum {
    TRANSITMODE_NONE=0,
    TRANSITMODE_MONTH,
    TRANSITMODE_YEAR,
    TRANSITMODE_12YEAR,
    TRANSITMODE_100YEAR,
    TRANSITMODE_MAX
} TransitModeType;

typedef enum {
    PLANETBELT_DOUBLEENDED=0,
    PLANETBELT_SINGLEENDED,
    PLANETBELT_LIFECYRCLE
} PlnaetBeltType;


#define UINT_RED            0xff0000
#define UINT_YELLOW         0xffff00
#define UINT_ORANGE         0xffb000
#define UINT_GREEN          0x00ff00
#define UINT_CYAN           0x00ffff
#define UINT_BLUE           0x0000ff
#define UINT_MAGENTA        0xff00ff
#define UINT_WHITE          0xffffff
#define UINT_BLACK          0x000000
#define UINT_BROWN          0xb04000
#define UINT_GRAY           0xa0a0a0
#define UINT_DARKBLUE       0x0000a0
#define UINT_DARKRED        0x800000
#define UINT_DARKCYAN       0x008080
#define UINT_DARKGRAY       0x303030

#define UINT_GET_RED( color )           (((color)&0xff0000) >> 16)
#define UINT_GET_GREEN( color )         (((color)&0x00ff00) >> 8)
#define UINT_GET_BLUE( color )          (((color)&0x0000ff))
#define UINT_COLOR_MIX( c1, c2 ) \
            ( \
            (((UINT_GET_RED(c1) + UINT_GET_RED(c2)) / 2) << 16) | \
            (((UINT_GET_GREEN(c1) + UINT_GET_GREEN(c2)) / 2) << 8) | \
            ((UINT_GET_BLUE(c1) + UINT_GET_BLUE(c2)) / 2) \
            )


#include "symbol.h"
#include "solonconfig.h"

// macros for debugging
#define DDD { qDebug("<DEBUG>%s:%i", __FILE__, __LINE__); }

#define DIM_OF(x) ( sizeof((x)) / sizeof((x)[0]) )

#define ABSOLUTE(x) ( (x)<0 ? (-(x)) : (x) )

#endif
