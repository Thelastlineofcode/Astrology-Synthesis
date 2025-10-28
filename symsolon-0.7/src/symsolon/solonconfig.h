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
#ifndef SOLONCONFIG_H
#define SOLONCONFIG_H

#include "solon_global.h"

#include <QFile>
#include <QtGui/QCloseEvent>
#include <QTextStream>
#include <QtGui/QFileDialog>
#include <QtGui/QMessageBox>
#include <QtXml/QXmlSimpleReader>
#include <QtXml/QXmlInputSource>
#include <QtXml/QXmlErrorHandler>
#include <QtXml/QXmlContentHandler>
#include <QtXml/QDomNode>
#include <QtXml/QDomEntity>
#include <QtXml/QDomDocument>
#include <QtXml/QDomElement>


class SolonConfigClass : public QObject, QXmlDefaultHandler
{
    Q_OBJECT

/* ayanamsa - the shif between thesigns and the constellation of stars */
typedef struct _AyanamsaInfoType
{
    int             index;
    const char      name[32];
    double          year;
    double          degreeShift;
} AyanamsaInfoType;

typedef struct _HouseSystemInfoType
{
    int             index;
    const char      name[32];
} HouseSystemInfoType;

typedef struct _LanguageInfoStruct
{
    const char      *name;
    const char      *id;
} LanguageInfoStruct;

typedef struct _TimeZoneInfoStruct
{
    const char      shortName[64];
    const char      name[64];
    const char      *dummy1;
    const char      *dummy2;
    const int       second;
} TimeZoneInfoStruct;

typedef struct _TimeZoneListInfoStruct
{
    int             seconds;
    const char      *text;
} TimeZoneListInfoStruct;


public:
    QString             progPath;
    QString             prefixPath;
    QString             sharePath;
    QString             clientDataPath;
    QString             programFileName;
    QString             configFileName;
    
    // settings
    QString             language;
    int                 houseSystem;
    int                 ayanamsaType;
    bool                topocentricCalculationUsed;
    bool                toolTipsEnabled;
    bool                detailedToolTipsEnabled;
    bool                cardTopTextEnabled;
    bool                cardBottomTextEnabled;
    bool                firstTimeStart;
    bool                aspectOrbitAsLimit;
    bool                transitPlanets[TRANSITMODE_MAX][PLANET_MAX];
    quint32             backgroundColor;
    quint32             foregroundColor;
    quint32             printingColor;
    QString             printingHeaderText;
    
    // tables
    static AyanamsaInfoType AyanamsaInfoTable[];
    static HouseSystemInfoType HouseSystemInfoTable[];
    static TimeZoneInfoStruct TimeZoneInfoTable[];
    static TimeZoneListInfoStruct TimeZoneListInfoTable[];
    
    LanguageInfoStruct *LanguageInfoTable;
    
    SolonConfigClass( int argc, char ** argv );
    ~SolonConfigClass();
    
// public QXmlErrorHandler:
    bool fatalError (const QXmlParseException & exception);

// public QXmlContentHandler:
    bool startElement ( const QString & namespaceURI,
            const QString & localName, const QString & qName,
            const QXmlAttributes & atts );
    bool endElement ( const QString & namespaceURI,
            const QString & localName, const QString & qName );
    bool characters ( const QString & chars );

public slots:
    
    virtual void open();
    virtual int save();

private:

    QString             xmlElementName;
    QString             xmlElementChars;
    QXmlAttributes      xmlAttributes;
    
    void appendXmlTag( QDomDocument &doc, QDomElement &root, QString name, QString value );
    void find_base_folders();
    void load_language_table();

};

extern SolonConfigClass        *SolonConfig;

void set_translation();


#endif
