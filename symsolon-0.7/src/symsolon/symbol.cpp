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
#include "symbol.h"
#include "startup.h"

#include <QCoreApplication>
#include <QRect>


SymbolClass                        *Symbol = NULL;


SymbolClass::MonthInfoType SymbolClass::MonthInfoTable[] =
{
    { 0,    "",                         0,         0 },
    { 1,    QT_TR_NOOP("January"),      31,        31 },
    { 2,    QT_TR_NOOP("February"),     28,        29 },
    { 3,    QT_TR_NOOP("March"),        31,        31 },
    { 4,    QT_TR_NOOP("Apryl"),        30,        30 },
    { 5,    QT_TR_NOOP("May"),          31,        31 },
    { 6,    QT_TR_NOOP("Juni"),         30,        30 },
    { 7,    QT_TR_NOOP("July"),         31,        31 },
    { 8,    QT_TR_NOOP("August"),       31,        31 },
    { 9,    QT_TR_NOOP("September"),    30,        30 },
    { 10,   QT_TR_NOOP("October"),      31,        31 },
    { 11,   QT_TR_NOOP("November"),     30,        30 },
    { 12,   QT_TR_NOOP("December"),     31,        31 },
};

SymbolClass::PlanetInfoType  SymbolClass::PlanetInfoTable[]  =
{
    { PLANET_NONE,       "",                      0, false, 0,              ""    },
    { PLANET_SUN,        QT_TR_NOOP("Sun"),       7, true,  UINT_ORANGE,    "planet-sun.svg" },
    { PLANET_MOON,       QT_TR_NOOP("Moon"),      6, true,  UINT_WHITE,     "planet-moon.svg" },
    { PLANET_MERCURY,    QT_TR_NOOP("Mercury"),   5, true,  UINT_YELLOW,    "planet-mercury.svg"},
    { PLANET_VENUS,      QT_TR_NOOP("Venus"),     5, true,  UINT_MAGENTA,   "planet-venus.svg" },
    { PLANET_EARTH,      QT_TR_NOOP("Earth"),     5, false, UINT_BROWN,     "planet-earth.svg" },
    { PLANET_MARS,       QT_TR_NOOP("Mars"),      5, true,  UINT_RED,       "planet-mars.svg" },
    { PLANET_JUPITER,    QT_TR_NOOP("Jupiter"),   5, true,  UINT_BLUE,      "planet-jupiter.svg"},
    { PLANET_SATURN,     QT_TR_NOOP("Saturn"),    5, true,  UINT_CYAN,      "planet-saturn.svg" },
    { PLANET_URANUS,     QT_TR_NOOP("Uranus"),    5, true,  UINT_DARKCYAN,  "planet-uranus.svg" },
    { PLANET_NEPTUNE,    QT_TR_NOOP("Neptune"),   5, true,  UINT_DARKBLUE,  "planet-neptune.svg"},
    { PLANET_PLUTO,      QT_TR_NOOP("Pluto"),     5, true,  UINT_DARKRED,   "planet-pluto.svg" },
    { PLANET_NORTH_NODE, QT_TR_NOOP("Noth-Node"), 1, false, UINT_GRAY,      "planet-nnode.svg" },
    { PLANET_SOUTH_NODE, QT_TR_NOOP("South-Node"),1, false, UINT_GRAY,      "planet-snode.svg" },
    { PLANET_CHIRON,     QT_TR_NOOP("Chiron"),    1, false, UINT_GRAY,      "planet-chiron.svg" },
    { PLANET_CERES,      QT_TR_NOOP("Ceres"),     1, false, UINT_GRAY,      "planet-ceres.svg" },
    { PLANET_ERIS,       QT_TR_NOOP("Eris"),      1, false, UINT_GRAY,      "planet-eris.svg" },
    { PLANET_PALLAS,     QT_TR_NOOP("Pallas"),    1, false, UINT_GRAY,      "planet-pallas.svg" },
    { PLANET_JUNO,       QT_TR_NOOP("Juno"),      1, false, UINT_GRAY,      "planet-juno.svg" },
    { PLANET_VESTA,      QT_TR_NOOP("Vesta"),     1, false, UINT_GRAY,      "planet-vesta.svg" },
    { PLANET_PHOLUS,     QT_TR_NOOP("Pholus"),    1, false, UINT_GRAY,      "" },
    
    // uranian & hypotetic planets
    { PLANET_CUPIDO,     QT_TR_NOOP("Cupido"),    1, false, UINT_GRAY,      "" },
    { PLANET_HADES,      QT_TR_NOOP("Hades"),     1, false, UINT_GRAY,      "" },
    { PLANET_ZEUS,       QT_TR_NOOP("Zeus"),      1, false, UINT_GRAY,      "" },
    { PLANET_KRONOS,     QT_TR_NOOP("Kronos"),    1, false, UINT_GRAY,      "" },
    { PLANET_APOLLON,    QT_TR_NOOP("Apollon"),   1, false, UINT_GRAY,      "" },
    { PLANET_ADMETOS,    QT_TR_NOOP("Admetos"),   1, false, UINT_GRAY,      "" },
    { PLANET_VULKANUS,   QT_TR_NOOP("Vulkanus"),  1, false, UINT_GRAY,      "" },
    { PLANET_POSEIDON,   QT_TR_NOOP("Poseidon"),  1, false, UINT_GRAY,      "" },
    { PLANET_ISIS,       QT_TR_NOOP("Isis"),      1, false, UINT_GRAY,      "" },
    { PLANET_NIBIRU,     QT_TR_NOOP("Nibiru"),    1, false, UINT_GRAY,      "" },
    { PLANET_HARRINGTON, QT_TR_NOOP("Harrington"),1, false, UINT_GRAY,      "" },
    { PLANET_LEVERRIER,  QT_TR_NOOP("Leverrier"), 1, false, UINT_GRAY,      "" },
    { PLANET_ADAMS,      QT_TR_NOOP("Adams"),     1, false, UINT_GRAY,      "" },
    { PLANET_LOWELL,     QT_TR_NOOP("Lowell"),    1, false, UINT_GRAY,      "" },
    { PLANET_PICKERING,  QT_TR_NOOP("Pickering"), 1, false, UINT_GRAY,      "" },
    { PLANET_VULCAN,     QT_TR_NOOP("Vulcan"),    1, false, UINT_GRAY,      "" },
    { PLANET_WHITE_MOON, QT_TR_NOOP("White Moon"),1, false, UINT_GRAY,      "" },
    { PLANET_PROSERPINA, QT_TR_NOOP("Proserpina"),1, false, UINT_GRAY,      "" },
    { PLANET_WALDEMATH,  QT_TR_NOOP("Waldemath"), 1, false, UINT_GRAY,      "" },
    
    { PLANET_MAX,        "",                      0, false, 0,              "" }
};


SymbolClass::PointInfoType  SymbolClass::PointInfoTable[]  =
{
    { POINT_NONE,        "",                          0, false,  "" },
    { POINT_VERTEX,      QT_TR_NOOP("Vertex"),        1, false,  "point-vertex.svg"    },
    { POINT_FORTUNA,     QT_TR_NOOP("Fortuna"),       1, false,  "point-fortuna.svg"},
    { POINT_EAST_POINT,  QT_TR_NOOP("East-Point"),    1, false,  "point-eastpoint.svg"},
    { POINT_MAX,         "",                          0, false,  ""    }
};


SymbolClass::SignInfoType  SymbolClass::SignInfoTable[]  =
{
    { SIGN_NONE,         "",                         ""                        },
    { SIGN_ARIES,        QT_TR_NOOP("Aries"),        "sign-01-aries.svg"       },
    { SIGN_TAURUS,       QT_TR_NOOP("Taurus"),       "sign-02-taurus.svg"      },
    { SIGN_GEMINI,       QT_TR_NOOP("Gemini"),       "sign-03-gemini.svg"      },
    { SIGN_CANCER,       QT_TR_NOOP("Cancer"),       "sign-04-cancer.svg"      },
    { SIGN_LEO,          QT_TR_NOOP("Leo"),          "sign-05-leo.svg"         },
    { SIGN_VIRGO,        QT_TR_NOOP("Virgo"),        "sign-06-virgo.svg"       },
    { SIGN_LIBRA,        QT_TR_NOOP("Libra"),        "sign-07-libra.svg"       },
    { SIGN_SCORPION,     QT_TR_NOOP("Scorpion"),     "sign-08-scorpion.svg"    },
    { SIGN_SAGITTARIUS,  QT_TR_NOOP("Sagittarius"),  "sign-09-sagittarius.svg" },
    { SIGN_CAPRICORN,    QT_TR_NOOP("Capricorn"),    "sign-10-capricorn.svg"   },
    { SIGN_AQUARIUS,     QT_TR_NOOP("Aquarius"),     "sign-11-aquarius.svg"    },
    { SIGN_PISCES,       QT_TR_NOOP("Pisces"),       "sign-12-pisces.svg"      },
    { SIGN_MAX,          "",                         ""                        }
};


SymbolClass::HouseInfoType  SymbolClass::HouseInfoTable[] =
{
    { 0,    "" },
    { 1,    QT_TR_NOOP("initiative") },
    { 2,    QT_TR_NOOP("wealth") },
    { 3,    QT_TR_NOOP("communication") },
    { 4,    QT_TR_NOOP("home") },
    { 5,    QT_TR_NOOP("creativiry") },
    { 6,    QT_TR_NOOP("duties") },
    { 7,    QT_TR_NOOP("partner") },
    { 8,    QT_TR_NOOP("attachment") },
    { 9,    QT_TR_NOOP("persuasion") },
    { 10,   QT_TR_NOOP("society") },
    { 11,   QT_TR_NOOP("friendship") },
    { 12,   QT_TR_NOOP("retreat") },
    { 13,   "" }
};

SymbolClass::EffectInfoType  SymbolClass::EffectInfoTable[] =
{
    { 0,    "",                                 "" },
    { 1,    QT_TR_NOOP("area of initiative"),   QT_TR_NOOP("as warrior") },
    { 2,    QT_TR_NOOP("wealth"),               QT_TR_NOOP("as lover") },
    { 3,    QT_TR_NOOP("communication"),        QT_TR_NOOP("as mediator") },
    { 4,    QT_TR_NOOP("at home"),              QT_TR_NOOP("as mother") },
    { 5,    QT_TR_NOOP("area of creativiry"),   QT_TR_NOOP("as king") },
    { 6,    QT_TR_NOOP("area of duties"),       QT_TR_NOOP("as servant") },
    { 7,    QT_TR_NOOP("in partnership"),       QT_TR_NOOP("as partner") },
    { 8,    QT_TR_NOOP("area of attachment"),   QT_TR_NOOP("as seducer") },
    { 9,    QT_TR_NOOP("area of ideology"),     QT_TR_NOOP("as ideology") },
    { 10,   QT_TR_NOOP("in society"),           QT_TR_NOOP("as master") },
    { 11,   QT_TR_NOOP("in friendship"),        QT_TR_NOOP("as jester") },
    { 12,   QT_TR_NOOP("in retreat"),           QT_TR_NOOP("as angel") },
    { 13,   "",                                 "" }
};

SymbolClass::AspectInfoType SymbolClass::AspectInfoTable[] = 
{
    { ASPECT_NONE,        "",               "",      0,        0,    0,
      PLANET_NONE,        0,                false,    "" },
    
    { ASPECT_CONJUCT,     "CONJUCT",        "Con",   0,        7,    0.5,
      PLANET_SUN,         UINT_ORANGE,      true,     "aspect-conjuct.svg" },
    
    { ASPECT_SEMIDECILE,  "SEMIDECILE",     "SD",    18,       1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-semidecil.svg" },
    
    { ASPECT_SEMISEXTIL,  "SEMISEXTIL",     "SSx",   30,       3,    0.66,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-semisextil.svg" },
    
    { ASPECT_UNDECIM,     "UNDECIM",        "Und",   360.0/11, 1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-undecim.svg" },
    
    { ASPECT_SEMIQUINTIL, "SEMIQUINTIL",    "SQn",   36,       1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-semiquintil.svg" },
    
    { ASPECT_NOVIL,       "NOVIL",          "Nov",   40,       1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,     false,  "aspect-novil.svg" },
    
    { ASPECT_SEMIQUADRAT, "SEMIQUADRAT",    "SSq",   45,       3,    0.25,
      PLANET_MARS,        UINT_BROWN,       true,    "aspect-sesquiquadrat.svg" },
    
    { ASPECT_SEPTIL,      "SEPTIL",         "Sep",   360.0/7,  1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,    "aspect-septil.svg" },
    
    { ASPECT_SEXTIL,      "SEXTIL",         "SXt",   60,       6,    0.75,
      PLANET_VENUS,       UINT_BLUE,        true,    "aspect-sextil.svg" },
    
    { ASPECT_BIUNDECIM,   "BIUNDECIM",      "bun",   720.0/11, 1,    0,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-biundecim.svg" },
    
    { ASPECT_QUINTIL,     "QUINTIL",        "QNt",   72,       2,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-quintil.svg" },
    
    { ASPECT_BINOVIL,     "BINOVIL",        "BNv",   80,       1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-binovil.svg" },
    
    { ASPECT_QUADRAT,     "QUADRAT",        "SQr",   90,       7,    0,
      PLANET_SATURN,      UINT_RED,         true,    "aspect-quadrat.svg" },
    
    { ASPECT_TRIUNDECIM,  "TRIUNDECIM",     "tun",   180.0/11, 1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-triundecim.svg" },
    
    { ASPECT_BISEPTILE,   "BISEPTIL",       "Bsp",   720.0/7,  1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-biseptil.svg" },
    
    { ASPECT_SQUINE,      "SQUINE",         "sqn",   105,      1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-squine.svg" },
    
    { ASPECT_SESQUIQUINTILE,"SESQUIQUINTILE","sqi",  108,      1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-sesquiquintil.svg" },
    
    { ASPECT_TRIGON,      "TRIGON",         "Tri",   120,      7,    1,
      PLANET_JUPITER,     UINT_GREEN,       true,    "aspect-trigon.svg" },
    
    { ASPECT_QUADRIUNDECIM,"QUADRIUNDECIM", "qun",   130.90908, 1,   0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-quadriundecim.svg" },
    
    { ASPECT_SESQUIQUADRAT,"SESQUIQUADRAT", "Ses",   135,      3,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-semiquadrat.svg" },
    
    { ASPECT_BIQUINTIL,   "BIQUINTIL",      "BQt",   144,        2,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-biquintil.svg" },
    
    { ASPECT_QUINCUNX,    "QUINCUNX",       "Inc",   150,        3,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-quincunx.svg" },
    
    { ASPECT_TRISEPTIL,   "TRISEPTIL",      "TSp",   154.285714,    1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-triseptil.svg" },
    
    { ASPECT_QUANTONOVIL, "QUANTONOVIL",    "QNv",   160,        1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-quantonovil.svg" },
    
    { ASPECT_QUINQUEUNDECIM,"QUINQUEUNDECIM","qqu",  163.63636,  1,     0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-quinqueundecim.svg" },
    
    { ASPECT_QUINDECILE,  "QUINDECILE",     "qd",    165,        1,    0.5,
      PLANET_NONE,        UINT_DARKGRAY,    false,   "aspect-quindecile.svg" },
    
    { ASPECT_OPPOSITE,    "OPPOSITE",       "Opp",   180,        7,    0.5,
      PLANET_MOON,        UINT_WHITE,       true,    "aspect-opposite.svg" },
    
    { ASPECT_MIRROR,      "MIRROR",         "Mir",   720,        1,    0,
      PLANET_PLUTO,        UINT_COLOR_MIX( UINT_RED, UINT_DARKGRAY ), true,
      "aspect-mirrorpoint.svg" },
    
    { ASPECT_MAX,         "",               "",      0,          0,    0,
      PLANET_NONE,        0,                false,   "" }
};


SymbolClass::CardDescriptionType nullDes = { "", "", "", "", "" };

SymbolClass::SymbolonInfoType SymbolClass::SymbolonInfoTable[] = 
{
    { 0,    SIGN_NONE,         SIGN_NONE,         "",                              nullDes },
    
    // --- signs ---
    { 1,    SIGN_ARIES,        SIGN_ARIES,        QT_TR_NOOP("WARRIOR"),           nullDes },
    { 2,    SIGN_TAURUS,       SIGN_TAURUS,       QT_TR_NOOP("LOVER"),             nullDes },
    { 3,    SIGN_GEMINI,       SIGN_GEMINI,       QT_TR_NOOP("MEDIATOR"),          nullDes },
    { 4,    SIGN_CANCER,       SIGN_CANCER,       QT_TR_NOOP("MOTHER"),            nullDes },
    { 5,    SIGN_LEO,          SIGN_LEO,          QT_TR_NOOP("EGO"),               nullDes },
    { 6,    SIGN_VIRGO,        SIGN_VIRGO,        QT_TR_NOOP("SERVITOR"),          nullDes },
    { 7,    SIGN_LIBRA,        SIGN_LIBRA,        QT_TR_NOOP("PARTNER"),           nullDes },
    { 8,    SIGN_SCORPION,     SIGN_SCORPION,     QT_TR_NOOP("SEDUCER"),           nullDes },
    { 9,    SIGN_SAGITTARIUS,  SIGN_SAGITTARIUS,  QT_TR_NOOP("PREACHER"),          nullDes },
    { 10,   SIGN_CAPRICORN,    SIGN_CAPRICORN,    QT_TR_NOOP("MASTER"),            nullDes },
    { 11,   SIGN_AQUARIUS,     SIGN_AQUARIUS,     QT_TR_NOOP("JESTER"),            nullDes },
    { 12,   SIGN_PISCES,       SIGN_PISCES,       QT_TR_NOOP("ANGEL"),             nullDes },
    
    // --- CANCER ---
    { 13,   SIGN_CANCER,       SIGN_ARIES,        QT_TR_NOOP("DEFIANCE"),          nullDes },
    { 14,   SIGN_CANCER,       SIGN_TAURUS,       QT_TR_NOOP("TWO FACES OF EVE"),  nullDes },
    { 15,   SIGN_CANCER,       SIGN_GEMINI,       QT_TR_NOOP("ARTICULATION"),      nullDes },
    { 16,   SIGN_CANCER,       SIGN_LEO,          QT_TR_NOOP("INCOMPATIBILITY"),   nullDes },
    { 17,   SIGN_CANCER,       SIGN_VIRGO,        QT_TR_NOOP("CARING"),            nullDes },
    { 18,   SIGN_CANCER,       SIGN_LIBRA,        QT_TR_NOOP("FAMILY"),            nullDes },
    { 19,   SIGN_CANCER,       SIGN_SCORPION,     QT_TR_NOOP("ABORTION"),          nullDes },
    { 20,   SIGN_CANCER,       SIGN_SAGITTARIUS,  QT_TR_NOOP("MNEMOSYNE"),         nullDes },
    { 21,   SIGN_CANCER,       SIGN_CAPRICORN,    QT_TR_NOOP("ICE QUEEN"),         nullDes },
    { 22,   SIGN_CANCER,       SIGN_AQUARIUS,     QT_TR_NOOP("DELIVERANCE"),       nullDes },
    { 23,   SIGN_CANCER,       SIGN_PISCES,       QT_TR_NOOP("BEAUTY-SLUMBER"),    nullDes },
    
    // --- LEO ---
    { 24,   SIGN_LEO,          SIGN_ARIES,        QT_TR_NOOP("BATTLE"),            nullDes },
    { 25,   SIGN_LEO,          SIGN_TAURUS,       QT_TR_NOOP("QUEEN"),             nullDes },
    { 26,   SIGN_LEO,          SIGN_GEMINI,       QT_TR_NOOP("ACTOR"),             nullDes },
    { 27,   SIGN_LEO,          SIGN_VIRGO,        QT_TR_NOOP("AILING KING"),       nullDes },
    { 28,   SIGN_LEO,          SIGN_LIBRA,        QT_TR_NOOP("WEDDING"),           nullDes },
    { 29,   SIGN_LEO,          SIGN_SCORPION,     QT_TR_NOOP("MAGICIAN"),          nullDes },
    { 30,   SIGN_LEO,          SIGN_SAGITTARIUS,  QT_TR_NOOP("FORTUNA"),           nullDes },
    { 31,   SIGN_LEO,          SIGN_CAPRICORN,    QT_TR_NOOP("BURDEN"),            nullDes },
    { 32,   SIGN_LEO,          SIGN_AQUARIUS,     QT_TR_NOOP("FALL"),              nullDes },
    { 33,   SIGN_LEO,          SIGN_PISCES,       QT_TR_NOOP("RETREAT"),           nullDes },
    
    // --- ARIES ---
    { 34,   SIGN_ARIES,        SIGN_TAURUS,       QT_TR_NOOP("EROS"),              nullDes },
    { 35,   SIGN_ARIES,        SIGN_GEMINI,       QT_TR_NOOP("STOCKS"),            nullDes },
    { 36,   SIGN_ARIES,        SIGN_VIRGO,        QT_TR_NOOP("GUILT"),             nullDes },
    { 37,   SIGN_ARIES,        SIGN_LIBRA,        QT_TR_NOOP("DISAGREEMENT"),      nullDes },
    { 38,   SIGN_ARIES,        SIGN_SCORPION,     QT_TR_NOOP("VAMPIRE"),           nullDes },
    { 39,   SIGN_ARIES,        SIGN_SAGITTARIUS,  QT_TR_NOOP("CRUSADER"),          nullDes },
    { 40,   SIGN_ARIES,        SIGN_CAPRICORN,    QT_TR_NOOP("PREVENTION"),        nullDes },
    { 41,   SIGN_ARIES,        SIGN_AQUARIUS,     QT_TR_NOOP("TROUBLEMAKER"),      nullDes },
    { 42,   SIGN_ARIES,        SIGN_PISCES,       QT_TR_NOOP("ABSOLUTE FOOL"),     nullDes },
    
    // --- TAURUS ---
    { 43,   SIGN_TAURUS,       SIGN_GEMINI,       QT_TR_NOOP("GOLDEN GIRL"),       nullDes },
    { 44,   SIGN_TAURUS,       SIGN_VIRGO,        QT_TR_NOOP("CLINGING"),          nullDes },
    { 45,   SIGN_TAURUS,       SIGN_LIBRA,        QT_TR_NOOP("GILDED CAGE"),       nullDes },
    { 46,   SIGN_TAURUS,       SIGN_SCORPION,     QT_TR_NOOP("MARIONETTE"),        nullDes },
    { 47,   SIGN_TAURUS,       SIGN_SAGITTARIUS,  QT_TR_NOOP("MATTER & SPIRIT"),   nullDes },
    { 48,   SIGN_TAURUS,       SIGN_CAPRICORN,    QT_TR_NOOP("RESPONSIBILITY.."),  nullDes },
    { 49,   SIGN_TAURUS,       SIGN_AQUARIUS,     QT_TR_NOOP("FAREWELL"),          nullDes },
    { 50,   SIGN_TAURUS,       SIGN_PISCES,       QT_TR_NOOP("GARDEN OF SPIRITS"), nullDes },
    
    // --- GEMINI ---
    { 51,   SIGN_GEMINI,       SIGN_VIRGO,        QT_TR_NOOP("STRATEGIST"),        nullDes },
    { 52,   SIGN_GEMINI,       SIGN_LIBRA,        QT_TR_NOOP("VANITY FAIR"),       nullDes },
    { 53,   SIGN_GEMINI,       SIGN_SCORPION,     QT_TR_NOOP("PIED PIPER"),        nullDes },
    { 54,   SIGN_GEMINI,       SIGN_SAGITTARIUS,  QT_TR_NOOP("MASTER & DISCIPLE"), nullDes },
    { 55,   SIGN_GEMINI,       SIGN_CAPRICORN,    QT_TR_NOOP("AFFLICTION"),        nullDes },
    { 56,   SIGN_GEMINI,       SIGN_AQUARIUS,     QT_TR_NOOP("DREAMING JOHNNY"),   nullDes },
    { 57,   SIGN_GEMINI,       SIGN_PISCES,       QT_TR_NOOP("SILENCE"),           nullDes },
    
    // --- VIRGO ---
    { 58,   SIGN_VIRGO,        SIGN_LIBRA,        QT_TR_NOOP("EVERYDAY LIFE"),     nullDes },
    { 59,   SIGN_VIRGO,        SIGN_SCORPION,     QT_TR_NOOP("CASTIGATION"),       nullDes },
    { 60,   SIGN_VIRGO,        SIGN_SAGITTARIUS,  QT_TR_NOOP("INQUISITION"),       nullDes },
    { 61,   SIGN_VIRGO,        SIGN_CAPRICORN,    QT_TR_NOOP("FEAR"),              nullDes },
    { 62,   SIGN_VIRGO,        SIGN_AQUARIUS,     QT_TR_NOOP("FURIES"),            nullDes },
    { 63,   SIGN_VIRGO,        SIGN_PISCES,       QT_TR_NOOP("DECEPTION"),         nullDes },
    
    // --- LIBRA ---
    { 64,   SIGN_LIBRA,        SIGN_SCORPION,     QT_TR_NOOP("DISASTER"),          nullDes },
    { 65,   SIGN_LIBRA,        SIGN_SAGITTARIUS,  QT_TR_NOOP("SYMBOLON"),          nullDes },
    { 66,   SIGN_LIBRA,        SIGN_CAPRICORN,    QT_TR_NOOP("SADNESS"),           nullDes },
    { 67,   SIGN_LIBRA,        SIGN_AQUARIUS,     QT_TR_NOOP("SEPARATION"),        nullDes },
    { 68,   SIGN_LIBRA,        SIGN_PISCES,       QT_TR_NOOP("KING'S TWO CHILDREN"),nullDes },
    
    // --- SCORPION ---
    { 69,   SIGN_SCORPION,     SIGN_SAGITTARIUS,  QT_TR_NOOP("BLACK MASS"),        nullDes },
    { 70,   SIGN_SCORPION,     SIGN_CAPRICORN,    QT_TR_NOOP("DEPRESSION"),        nullDes },
    { 71,   SIGN_SCORPION,     SIGN_AQUARIUS,     QT_TR_NOOP("PHOENIX"),           nullDes },
    { 72,   SIGN_SCORPION,     SIGN_PISCES,       QT_TR_NOOP("FALSE HALO"),        nullDes },
    
    // --- SAGITTARIUS ---
    { 73,   SIGN_SAGITTARIUS,  SIGN_CAPRICORN,    QT_TR_NOOP("CONFESSION"),        nullDes },
    { 74,   SIGN_SAGITTARIUS,  SIGN_AQUARIUS,     QT_TR_NOOP("QUANTUM LEAP"),      nullDes },
    { 75,   SIGN_SAGITTARIUS,  SIGN_PISCES,       QT_TR_NOOP("PYTHIA"),            nullDes },
    
    // --- CAPRICORN ---
    { 76,   SIGN_CAPRICORN,    SIGN_AQUARIUS,     QT_TR_NOOP("CAPTIVITY"),         nullDes },
    { 77,   SIGN_CAPRICORN,    SIGN_PISCES,       QT_TR_NOOP("MOIRA"),             nullDes },
    
    // --- AQUARIUS ---
    { 78,   SIGN_AQUARIUS,     SIGN_PISCES,       QT_TR_NOOP("GRAIL"),             nullDes }
};


/***************************************************************************************
  Symbol object constructor
 ***************************************************************************************/
SymbolClass::SymbolClass(QObject *obj) : QObject(obj)
{
    int            i=0, j=0;
    QString        symbolonFileNumStr;
    
    // planetInfo
    for (i=0; i<PLANET_MAX; i++)
        for (j=0; PlanetInfoTable[j].index<PLANET_MAX; j++)
            if ( PlanetInfoTable[j].index == i )
            {
                planetInfo[i] = PlanetInfoTable[j];
                strcpy( planetInfo[i].name, tr(PlanetInfoTable[j].name).toUtf8().constData() );
                break;
            }
    
    // signInfo
    for (i=0; i<SIGN_MAX; i++)
        for (j=0; SignInfoTable[j].index<SIGN_MAX; j++)
            if ( SignInfoTable[j].index == i )
            {
                signInfo[i] = SignInfoTable[j];
                strcpy( signInfo[i].name, tr(SignInfoTable[j].name).toUtf8().constData() );
                break;
            }
    
    // houseInfo
    for (i=0; i<=12; i++)
        for (j=0; HouseInfoTable[j].index<13; j++)
            if ( HouseInfoTable[j].index == i )
            {
                houseInfo[i] = HouseInfoTable[j];
                strcpy( houseInfo[i].name, tr(HouseInfoTable[j].name).toUtf8().constData() );
                break;
            }
    
    // effectInfo
    for (i=0; i<=12; i++)
        for (j=0; EffectInfoTable[j].index<13; j++)
            if ( EffectInfoTable[j].index == i )
            {
                effectInfo[i] = EffectInfoTable[j];
                strcpy( effectInfo[i].inHouse,
                        tr(EffectInfoTable[j].inHouse).toUtf8().constData() );
                strcpy( effectInfo[i].inSign,
                        tr(EffectInfoTable[j].inSign).toUtf8().constData() );
                break;
            }
    
    // aspectInfo
    for (i=0; i<ASPECT_MAX; i++)
        for (j=0; AspectInfoTable[j].index<ASPECT_MAX; j++)
            if ( AspectInfoTable[j].index == i )
            {
                aspectInfo[i] = AspectInfoTable[j];
                break;
            }

    // symbolonInfo
    for (i=0; i<SYMBOLON_MAX; i++)
        for (j=0; SymbolonInfoTable[j].index<SYMBOLON_MAX; j++)
            if ( SymbolonInfoTable[j].index == i )
            {
                symbolonInfo[i] = SymbolonInfoTable[j];
                strcpy( symbolonInfo[i].name, tr(SymbolonInfoTable[j].name).toUtf8().constData() );
                break;
            }
    
    // pointInfo
    for (i=0; i<POINT_MAX; i++)
        for (j=0; PointInfoTable[j].index<POINT_MAX; j++)
            if ( PointInfoTable[j].index == i )
            {
                pointInfo[i] = PointInfoTable[j];
                strcpy( pointInfo[i].name, tr(PointInfoTable[j].name).toUtf8().constData() );
                break;
            }
    
    loadProgressCounter = 0;
    Startup->ui->progressBar->setRange( 0, PLANET_MAX + SIGN_MAX + ASPECT_MAX +
                                            POINT_MAX + SYMBOLON_MAX + 1 );
    Startup->ui->progressBar->setValue( loadProgressCounter );
    QCoreApplication::processEvents();
    
    Planets   = new QSvgRenderer[ PLANET_MAX + 1 ];
    Points    = new QSvgRenderer[ POINT_MAX + 1 ];
    Signs     = new QSvgRenderer[ SIGN_MAX + 1 ];
    Aspects   = new QSvgRenderer[ ASPECT_MAX + 1 ];
    Symbolons = new QImage[ SYMBOLON_MAX + 1 ];
    
    for (i=PLANET_SUN; i<PLANET_MAX; i++)
    {
        QString name = planetInfo[i].fileName;
        if (name.size() <= 0) name = "planet-default.svg";
        Planets[ i ].load( SolonConfig->sharePath + "/planets/" + name  );
        Startup->ui->progressBar->setValue( loadProgressCounter++ );
        QCoreApplication::processEvents();
    }
    
    for (i=SIGN_ARIES; i<SIGN_MAX; i++)
    {
        Signs[ i ].load( SolonConfig->sharePath + "/signs/" + signInfo[i].fileName );
        Startup->ui->progressBar->setValue( loadProgressCounter++ );
        QCoreApplication::processEvents();
    }
    
    for (i=ASPECT_CONJUCT; i<ASPECT_MAX; i++)
    {
        Aspects[ i ].load( SolonConfig->sharePath + "/aspects/" + aspectInfo[i].fileName );
        Startup->ui->progressBar->setValue( loadProgressCounter++ );
        QCoreApplication::processEvents();
    }
    
    for (i=1; i<SYMBOLON_MAX; i++)
    {
        symbolonFileNumStr.sprintf("%02i", i);
        Symbolons[ i ].load( SolonConfig->sharePath + "/symbolons/symbolon-" + symbolonFileNumStr  );
        Startup->ui->progressBar->setValue( loadProgressCounter++ );
        QCoreApplication::processEvents();
    }
    
    for (i=1; i<POINT_MAX; i++)
    {
        Points[ i ].load( SolonConfig->sharePath + "/points/" + pointInfo[i].fileName );
        Startup->ui->progressBar->setValue( loadProgressCounter++ );
        QCoreApplication::processEvents();
    }
    
    // load symbolon description from file
    load_symbolon_description( SolonConfig->sharePath + "/descriptions/symbolon_text_" +
                                SolonConfig->language + ".xml" );
    
//#define _SAVE_WORKFILE 1
#ifdef _SAVE_WORKFILE
    QFile wof( "./symworkfile.txt" );
    wof.open( QIODevice::WriteOnly | QIODevice::Text );
    QTextStream wos( &wof );
    for ( int i=1; i<=78; i++ )
    {
        wos << "@" << i << "\n";
        wos << symbolonInfo[i].name;
        wos << symbolonInfo[i].description.summary.remove('\n') + "\n\n";
        wos << "@@z)\n";
        wos << symbolonInfo[i].description.general.remove('\n') + "\n\n";
        wos << "@@a)\n";
        wos << symbolonInfo[i].description.problem.remove('\n') + "\n\n";
        wos << "@@b)\n";
        wos << symbolonInfo[i].description.way.remove('\n') + "\n\n";
        wos << "@@c)\n";
        wos << symbolonInfo[i].description.outcome.remove('\n') + "\n\n";
    }
    wof.close();
#endif
    
    // set font sttings
    deckBottomFont.setStyleHint( QFont::SansSerif );
    deckBottomFont.setBold( true );
    deckBottomPen.setColor( Qt::darkCyan );
    deckBottomMetrics = NULL;
    
    deckTopFont.setStyleHint( QFont::SansSerif );
    deckTopFont.setBold( true );
    deckTopPen.setColor( QColor(SolonConfig->foregroundColor) );
    deckTopMetrics = NULL;
}


SymbolClass::~SymbolClass()
{
    delete[] Planets;
    delete[] Signs;
    delete[] Symbolons;
    //delete planetInfo;
    //delete signInfo;
    //delete symbolonInfo;
}


/***************************************************************************************
  painting functions
 ***************************************************************************************/

void
SymbolClass::set_label_color( quint32 topColor )
{
    deckTopPen.setColor( QColor(topColor) );
}


void
SymbolClass::paint_sign( QPainter &p, int sign, double x, double y, double w, double h )
{
    QRect vp = p.viewport();
    QMatrix mat = p.worldMatrix();
    x = x * mat.m11() + mat.dx() - mat.dx() / 16;
    y = y * mat.m22() + mat.dy() - mat.dy() / 16;
    p.setViewport( (int)x, (int)y, (int)w, (int)h );
    Signs[sign].render( &p );
    p.setViewport( vp );
}


void
SymbolClass::paint_planet( QPainter &p, int planet, double x, double y, double w, double h )
{
    QRect vp = p.viewport();
    QMatrix mat = p.worldMatrix();
    x = x * mat.m11() + mat.dx() - mat.dx() / 16;
    y = y * mat.m22() + mat.dy() - mat.dy() / 16;
    p.setViewport( (int)x, (int)y, (int)w, (int)h );
    Planets[planet].render( &p );
    p.setViewport( vp );   
}


void
SymbolClass::paint_aspect( QPainter &p, int aspect, double x, double y, double w, double h )
{
    QRect vp = p.viewport();
    QMatrix mat = p.worldMatrix();
    x = x * mat.m11() + mat.dx() - mat.dx() / 16;
    y = y * mat.m22() + mat.dy() - mat.dy() / 16;
    p.setViewport( (int)x, (int)y, (int)w, (int)h );
    Aspects[aspect].render( &p );
    p.setViewport( vp );
}


void
SymbolClass::paint_symbolon( QPainter &p, int symbolon, double x, double y, double w, double h,
                                QString topLabel, AlignType align, VAlignType valign )
{
    paint_symbolon( p, symbolon, x, y, w, h, topLabel, "", align, valign );
}


void
SymbolClass::paint_symbolon( QPainter &p, int symbolon, double x, double y, double w, double h,
                                QString topLabel, QString topLabel2,
                                AlignType align, VAlignType valign )
{
    int        iw = Symbolons[symbolon].width();
    int        ih = Symbolons[symbolon].height();
    double     ratio = 1;
    int        w2=(int)w, h2=(int)h, x2=(int)x, y2=(int)y, h3=(int)h;
    QString    name = get_name_of_symbolon( symbolon );
    
    if ( !SolonConfig->cardTopTextEnabled )
    {
        topLabel  = "";
        topLabel2 = "";
    }
    
    if ( (double)iw/w > (double)ih/h )
    { // the height is bigger then the width
        ratio = (double)iw/w;
        w2 = (int)( iw / ratio );
        h2 = (int)( ih / ratio );
        x2 = (int)x;
        y2 = (int)(y + (h - h2) / 2);
    }
    else
    { // the width is bigger than the height
        ratio = (double)ih/h;
        w2 = (int)( iw / ratio );
        h2 = (int)( ih / ratio );
        x2 = (int)(x + (w - w2) / 2);
        y2 = (int)y;
    }
    
    switch (align)
    {
        default: break;
        case ALIGN_LEFT: x2 = (int)x; break; 
        case ALIGN_RIGHT: x2 = (int)((x+w)-w2); break;
    }
    
    switch (valign)
    {
        default: break;
        case ALIGN_TOP: y2 = (int)y; break; 
        case ALIGN_BOTTOM: y2 = (int)((y+h)-h2); break;
    }
    
    // fonts and fontmetricses
    int fw2 = w2 / 10;
    if (fw2 < 1) fw2 = 1;
    deckTopFont.setPixelSize( fw2 );
    deckBottomFont.setPixelSize( fw2 );
    if (deckTopMetrics) delete deckTopMetrics;
    if (deckBottomMetrics) delete deckBottomMetrics;
    deckTopMetrics = new QFontMetrics( deckTopFont );
    deckBottomMetrics = new QFontMetrics( deckBottomFont );
    
    // cut space for top and bottom labels
    h3 = h2;
    if (topLabel.size() > 0) h3 -= deckTopMetrics->height();
    if (topLabel2.size() > 0) h3 -= deckTopMetrics->height();
    if (SolonConfig->cardBottomTextEnabled) h3 -= deckBottomMetrics->height();
    ratio = (double)h3 / h2;
    
    if (topLabel.size() > 0) y2 += (int)(h2 * (1-ratio)/2); // shift down the card
    if (topLabel2.size() > 0) y2 += (int)(h2 * (1-ratio)/2); // shift down the card
    // scale card smaller
    w2 = (int)(w2 * ratio);
    h2 = (int)(h2 * ratio);
    
    // draw the symbolon card image
    QRect    target(x2, y2, w2, h2);
    QRect    source(0, 0, -1, -1);
    p.drawImage( target, Symbolons[symbolon], source, Qt::AutoColor );
    
    // put top label(s)
    if (SolonConfig->cardTopTextEnabled)
    {
        p.setPen( deckTopPen );
        p.setFont( deckTopFont );
        if (topLabel.size() > 0)
        {
            p.drawText( x2+(w2/2)-deckTopMetrics->width(topLabel)/2,
                        y2 - (topLabel2.size()>0 ? (deckTopMetrics->height()) : 0),
                        topLabel );
        }
        if (topLabel2.size() > 0)
        {
            p.drawText( x2+(w2/2)-deckTopMetrics->width(topLabel2)/2,
                        y2,
                        topLabel2 );
        }
    }
    
    // put bottom label
    if (SolonConfig->cardBottomTextEnabled)
    {
        p.setFont( deckBottomFont );
        p.setPen( deckBottomPen );
        p.drawText( x2+(w2/2)-deckBottomMetrics->width(name)/2,
                    y2+h2+deckBottomMetrics->height()/2+1,
                    name );
    }
}


/***************************************************************************************
  informative & data manipulation functions
 ***************************************************************************************/
QString
SymbolClass::get_name_of_symbolon( int sym )
{
    if (sym <= 0 || sym >= SYMBOLON_MAX) return "";
    return QString::fromUtf8( symbolonInfo[sym].name );
}


int
SymbolClass::two_sign_to_symbolon( int sign1, int sign2 )
{
    if (( sign1==0 && sign2==0) || sign1>=SYMBOLON_MAX || sign2>=SYMBOLON_MAX ) return 0;
    if ( sign1==0 ) return sign2;
    if ( sign2==0 ) return sign1;
    
    int i=0;
    
    for (i=1; i<SYMBOLON_MAX; i++)
    {
        if ( sign1==symbolonInfo[i].sign1 && sign2==symbolonInfo[i].sign2 ||
             sign1==symbolonInfo[i].sign2 && sign2==symbolonInfo[i].sign1 )
        {
            return i;
        }
    }
    
    return 0;
}


int
SymbolClass::planet_to_symbolon( int planet, std::vector<int> constellationVector )
{
    return two_sign_to_symbolon( get_sign_of_planet( planet, constellationVector ), 0 );
}


int
SymbolClass::planet_to_symbolon2( int planet )
{
    if ( planet == PLANET_MERCURY )
    {
        return two_sign_to_symbolon( SIGN_VIRGO, 0 );
    }
    else if ( planet == PLANET_VENUS )
    {
        return two_sign_to_symbolon( SIGN_LIBRA, 0 );
    }
    else
    {
        return planet_to_symbolon( planet );
    }
}


int
SymbolClass::get_planet_of_sign( int sign )
{    
    switch ( sign )
    {
        default: return PLANET_NONE;
        case SIGN_ARIES: return PLANET_MARS;
        case SIGN_TAURUS: return PLANET_VENUS;
        case SIGN_GEMINI: return PLANET_MERCURY;
        case SIGN_CANCER: return PLANET_MOON;
        case SIGN_LEO: return PLANET_SUN;
        case SIGN_VIRGO: return PLANET_MERCURY;
        case SIGN_LIBRA: return PLANET_VENUS;
        case SIGN_SCORPION: return PLANET_PLUTO;
        case SIGN_SAGITTARIUS: return PLANET_JUPITER;
        case SIGN_CAPRICORN: return PLANET_SATURN;
        case SIGN_AQUARIUS: return PLANET_URANUS;
        case SIGN_PISCES: return PLANET_NEPTUNE;
    }
}


int
SymbolClass::get_forced_sign( int sign )
{
    switch ( sign )
    {
        default: return sign;
        case SIGN_TAURUS: return SIGN_FORCE_TAURUS;
        case SIGN_GEMINI: return SIGN_FORCE_GEMINI;
        case SIGN_VIRGO: return SIGN_FORCE_VIRGO;
        case SIGN_LIBRA: return SIGN_FORCE_LIBRA;
    }
}


int
SymbolClass::get_sign_of_planet( int planet, std::vector<int> constellationVector )
{
    int        i=0, i1=0, i2=0;
    
    switch ( planet )
    {
        default: return SIGN_NONE;
        case PLANET_MOON: return SIGN_CANCER;
        case PLANET_SUN: return SIGN_LEO;
        case PLANET_MERCURY:
        {
                for ( i=i1=i2=0; i<(int)constellationVector.size(); i++ )
                {
                    switch ( constellationVector.at(i) )
                    {
                        case SIGN_FORCE_GEMINI: return SIGN_GEMINI;
                        case SIGN_FORCE_VIRGO: return SIGN_VIRGO;
                        case SIGN_GEMINI: i1++; break;
                        case SIGN_VIRGO: i2++; break;
                    }
                }
                if (i1 > i2) return SIGN_GEMINI;
                else if (i1 < i2) return SIGN_VIRGO;
                else return SIGN_GEMINI;
        }
        case PLANET_VENUS:
        {
                for ( i=i1=i2=0; i<(int)constellationVector.size(); i++ )
                {
                    switch ( constellationVector.at(i) )
                    {
                        case SIGN_FORCE_TAURUS: return SIGN_TAURUS;
                        case SIGN_FORCE_LIBRA: return SIGN_LIBRA;
                        case SIGN_TAURUS: i1++; break;
                        case SIGN_LIBRA: i2++; break;
                    }
                }
                if (i1 > i2) return SIGN_TAURUS;
                else if (i1 < i2) return SIGN_LIBRA;
                else return SIGN_TAURUS;
        }
        case PLANET_MARS: return SIGN_ARIES;
        case PLANET_JUPITER: return SIGN_SAGITTARIUS;
        case PLANET_SATURN: return SIGN_CAPRICORN;
        case PLANET_URANUS: return SIGN_AQUARIUS;
        case PLANET_NEPTUNE: return SIGN_PISCES;
        case PLANET_PLUTO: return SIGN_SCORPION;
    }
}


// returns true if aspect used in symolon system
int
SymbolClass::is_symbolon_aspect( int aspect )
{
    if ( aspect == ASPECT_SEXTIL ||
         aspect == ASPECT_TRIGON ||
         aspect == ASPECT_SEMIQUADRAT ||
         aspect == ASPECT_QUADRAT ||
         aspect == ASPECT_MIRROR ||
         aspect == ASPECT_OPPOSITE ||
         aspect == ASPECT_CONJUCT )
    {
        return true;
    }
    else
    {
        return false;
    }
}


// returns true if planet used in symolon system
int
SymbolClass::is_symbolon_planet( int planet )
{
    if ( planet == PLANET_MOON ||
         planet == PLANET_SUN ||
         planet == PLANET_MERCURY ||
         planet == PLANET_VENUS ||
         planet == PLANET_MARS ||
         planet == PLANET_JUPITER ||
         planet == PLANET_SATURN ||
         planet == PLANET_URANUS ||
         planet == PLANET_NEPTUNE ||
         planet == PLANET_PLUTO )
    {
        return true;
    }
    else
    {
        return false;
    }
}

QString
SymbolClass::index_to_english_name( InfoType type, int index )
{
    int        i=0;
    
    switch (type)
    {
        default:
        case INFOTYPE_NONE:
            break;
        
        case INFOTYPE_PLANET:
            for (i=0; i<PLANET_MAX; i++)
                if ( PlanetInfoTable[i].index == index )
                    return PlanetInfoTable[i].name;
            break;
        
        case INFOTYPE_SIGN:
            for (i=0; i<SIGN_MAX; i++)
                if ( SignInfoTable[i].index == index )
                    return SignInfoTable[i].name;
            break;
        
        case INFOTYPE_ASPECT:
            for (i=0; i<ASPECT_MAX; i++)
                if ( AspectInfoTable[i].index == index )
                    return AspectInfoTable[i].name;
            break;
        
        case INFOTYPE_HOUSE:
            for (i=0; i<HOUSE_MAX; i++)
                if ( HouseInfoTable[i].index == index )
                    return HouseInfoTable[i].name;
            break;
        
        case INFOTYPE_SYMBOLON:
            for (i=0; i<SYMBOLON_MAX; i++)
                if ( SymbolonInfoTable[i].index == index )
                    return SymbolonInfoTable[i].name;
            break;
    }
    
    return "";
}


int
SymbolClass::english_name_to_index( InfoType type, QString name )
{
    int        i=0;
    
    switch (type)
    {
        default:
        case INFOTYPE_NONE:
            break;
        
        case INFOTYPE_PLANET:
            for (i=0; i<PLANET_MAX; i++)
                if ( name == PlanetInfoTable[i].name )
                    return PlanetInfoTable[i].index;
            break;
        
        case INFOTYPE_SIGN:
            for (i=0; i<SIGN_MAX; i++)
                if ( name == SignInfoTable[i].name )
                    return SignInfoTable[i].index;
            break;
        
        case INFOTYPE_ASPECT:
            for (i=0; i<ASPECT_MAX; i++)
                if ( name == AspectInfoTable[i].name )
                    return AspectInfoTable[i].index;
            break;
        
        case INFOTYPE_HOUSE:
            for (i=0; i<HOUSE_MAX; i++)
                if ( name == HouseInfoTable[i].name )
                    return HouseInfoTable[i].index;
            break;
        
        case INFOTYPE_SYMBOLON:
            for (i=0; i<SYMBOLON_MAX; i++)
                if ( name == SymbolonInfoTable[i].name )
                    return SymbolonInfoTable[i].index;
            break;
    }
    
    return 0;
}


/***************************************************************************************
  card description loader functions 
 ***************************************************************************************/

bool
SymbolClass::fatalError (const QXmlParseException & exception)
{
    QString qstr("");
     
    qstr = QString("") + "Fatal error on line" + exception.lineNumber() +
            ", column" + exception.columnNumber() + ":" +
            exception.message();
    
    QMessageBox::critical(NULL, "SymSolon", qstr);
    
    return false;
}


bool
SymbolClass::startElement ( const QString &/*namespaceURI*/,
            const QString &/*localName*/, const QString &qName,
            const QXmlAttributes &/*atts*/ )
{
    xmlElementName  = qName;
    xmlElementChars = "";
    return true;
}


bool
SymbolClass::endElement ( const QString &/*namespaceURI*/,
            const QString &/*localName*/, const QString & /*qName*/ )
{
    if ( xmlElementName == "card" )
    {
        xmlElementCardNum = 0;
    }
    else if ( xmlElementName == "number" )
    {
        xmlElementCardNum = xmlElementChars.toInt();
    }
    
    if (xmlElementCardNum>0 && xmlElementCardNum<SYMBOLON_MAX)
    {
        if ( xmlElementName == "summary" )
        {
            symbolonInfo[xmlElementCardNum].description.summary = xmlElementChars;
        }
        else if ( xmlElementName == "general" )
        {
            symbolonInfo[xmlElementCardNum].description.general = xmlElementChars;
        }
        else if ( xmlElementName == "problem" )
        {
            symbolonInfo[xmlElementCardNum].description.problem = xmlElementChars;
        }
        else if ( xmlElementName == "way" )
        {
            symbolonInfo[xmlElementCardNum].description.way = xmlElementChars;
        }
        else if ( xmlElementName == "outcome" )
        {
            symbolonInfo[xmlElementCardNum].description.outcome = xmlElementChars;
        }
    }
    
    // clear element buffer
    xmlElementName = "";
    xmlElementChars = "";
    
    return true;
}


bool
SymbolClass::characters ( const QString & chars )
{
    xmlElementChars += chars;
    return true;
}


void
SymbolClass::load_symbolon_description( QString fileName )
{
    QFile        f( fileName );
    
    if ( !f.open( QFile::ReadOnly| QFile::Text ) )
    {
        QMessageBox::warning(NULL, tr("SymSolon"),
            tr("Couldn't open description file for symbolon cards.") + "(" + fileName + ")" );
        return;
    }
    
    QXmlInputSource source( &f );
    QXmlSimpleReader reader;
    
    //Handler *handler = new Handler();
    reader.setContentHandler(this);
    reader.setErrorHandler(this);
    
    bool ok = reader.parse( &source, false );
    
    if (!ok)
    {
        QMessageBox::critical(NULL, "SymSolon", tr("XML parse error in description file") +
                              "(" + fileName + ")" );
        return;
    }
    
    Startup->ui->progressBar->setValue( loadProgressCounter++ );
    QCoreApplication::processEvents();
}

