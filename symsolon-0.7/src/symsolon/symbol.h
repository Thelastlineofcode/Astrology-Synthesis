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
#ifndef SYMBOL_H
#define SYMBOL_H

#include "solon_global.h"
#include <QtSvg/QSvgRenderer>
#include <QFile>
#include <QtGui/QMessageBox>
#include <QTextStream>
#include <QtXml/QXmlSimpleReader>
#include <QtXml/QXmlInputSource>
#include <QtXml/QXmlErrorHandler>
#include <QtXml/QXmlContentHandler>
#include <QtXml/QDomNode>
#include <QtXml/QDomEntity>
#include <QtXml/QDomDocument>
#include <QtXml/QDomElement>


class SymbolClass : public QObject, QXmlDefaultHandler
{
    Q_OBJECT;
    
public:


typedef struct _PlanetInfoType
{
    int                     index;
    char                    name[64];        // the name of planet
    double                  orbit;
    int                     enabled;
    unsigned int            color;           // 0x00rrggbb
    char                    fileName[64];
} PlanetInfoType;


typedef struct _SignInfoType
{
    int                     index;
    char                    name[64];        // the name of sign
    char                    fileName[64];
} SignInfoType;


typedef struct _HouseInfoType
{
    int                     index;
    char                    name[64];        // the name of house
} HouseInfoType;


typedef struct _AspectInfoType
{
    int                     index;
    char                    name[64];               // name of aspect
    char                    abbreviation[64];       // abbreviation of aspect
    double                  angle;
    double                  orbit;
    double                  harmony;                // [0..1] 0=disharminic, 1=harmonic
    int                     planetEnergy;           // aspect brings this planet's energy
    unsigned int            color;                  // 0x00rrggbb
    int                     enabled;
    char                    fileName[65];
} AspectInfoType;


typedef struct _PointInfoType
{
    int                     index;
    char                    name[64];               // the name of point
    double                  orbit;
    int                     enabled;
    char                    fileName[64];
} PointInfoType;


typedef struct _CardDescriptionType
{
    QString                 summary;
    QString                 general;
    QString                 problem;
    QString                 way;
    QString                 outcome;
} CardDescriptionType;

typedef struct _SymbolonInfoType
{
    int                     index;
    int                     sign1, sign2;    // the sign combination of card
    char                    name[64];        // the name of card
    CardDescriptionType     description;
} SymbolonInfoType;


typedef struct _EffectInfoType
{
    int                     index;
    char                    inHouse[64];    // where does it take effect? (hol hat?)
    char                    inSign[64];        // how does it work? (hogyan hat?)
} EffectInfoType;

typedef struct _MonthInfoType
{
    int                     index;
    char                    name[64];
    int                     length;
    int                     extraLength;
} MonthInfoType;


public:

    static PlanetInfoType       PlanetInfoTable[];
    static PointInfoType        PointInfoTable[];
    static SignInfoType         SignInfoTable[];
    static HouseInfoType        HouseInfoTable[];
    static AspectInfoType       AspectInfoTable[];
    static SymbolonInfoType     SymbolonInfoTable[];
    static MonthInfoType        MonthInfoTable[];
    static EffectInfoType       EffectInfoTable[];
    
    PlanetInfoType              planetInfo[PLANET_MAX+1];
    PointInfoType               pointInfo[POINT_MAX+1];
    SignInfoType                signInfo[SIGN_MAX+1];
    HouseInfoType               houseInfo[12+1];
    AspectInfoType              aspectInfo[ASPECT_MAX+1];
    SymbolonInfoType            symbolonInfo[SYMBOLON_MAX+1];
    EffectInfoType              effectInfo[SIGN_MAX+1];
    
    QSvgRenderer                *Planets;
    QSvgRenderer                *Points;
    QSvgRenderer                *Signs;
    QImage                      *Symbolons;
    QSvgRenderer                *Aspects;
    
    SymbolClass( QObject *obj=(QObject*)0 );
    ~SymbolClass();
    
    void set_label_color( quint32 topColor );
    void paint_sign( QPainter &p, int sign, double x, double y, double w, double h );
    void paint_planet( QPainter &p, int planet, double x, double y, double w, double h );
    void paint_aspect( QPainter &p, int aspect, double x, double y, double w, double h );
    void paint_symbolon( QPainter &p, int symbolon, double x, double y, double w, double h,
                         QString topLabel = "",
                         AlignType align=ALIGN_CENTER, VAlignType valign=ALIGN_MIDDLE );
    void paint_symbolon( QPainter &p, int symbolon, double x, double y, double w, double h,
                         QString topLabel, QString topLabel2,
                         AlignType align=ALIGN_CENTER, VAlignType valign=ALIGN_MIDDLE );
    int two_sign_to_symbolon( int sign1, int sign2 );
    int get_planet_of_sign( int sign );
    int get_sign_of_planet( int planet );
    int planet_to_symbolon( int planet, std::vector<int> constellationVector=(std::vector<int>)0 );
    int planet_to_symbolon2( int planet );
    int get_sign_of_planet( int planet, std::vector<int> constellationVector=(std::vector<int>)0 );
    int get_forced_sign( int sign );
    int is_symbolon_planet( int planet );
    int is_symbolon_aspect( int aspect );
    QString get_name_of_symbolon( int sym );
    void load_symbolon_description( QString fileName );
    
    QString index_to_english_name( InfoType type, int index );
    int english_name_to_index( InfoType type, QString name );
    
// public QXmlErrorHandler:
    bool fatalError (const QXmlParseException & exception);

// public QXmlContentHandler:
    bool startElement ( const QString & namespaceURI,
                        const QString & localName,
                        const QString & qName, const QXmlAttributes & atts );
    bool endElement ( const QString & namespaceURI,
                      const QString & localName, const QString & qName );
    bool characters ( const QString & chars );

private:

    int             loadProgressCounter;
    QFont           deckBottomFont;
    QFont           deckTopFont;
    QFontMetrics    *deckBottomMetrics;
    QFontMetrics    *deckTopMetrics;
    QPen            deckTopPen;
    QPen            deckBottomPen;
    QString         xmlElementName;
    QString         xmlElementChars;
    int             xmlElementCardNum;

};

extern SymbolClass        *Symbol;

#endif
