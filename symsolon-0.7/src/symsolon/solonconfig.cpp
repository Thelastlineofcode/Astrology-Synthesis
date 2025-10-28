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

#include "solonconfig.h"
#include <QFileInfo>
#include <QDir>
#include <QApplication>
#include <QFile>
#include <QTextStream>

#include "languageselector.h"


SolonConfigClass                        *SolonConfig = NULL;

/* !!! WARNING !!! Table order should follow the order of enumeration lint in solon_global.h */
SolonConfigClass::AyanamsaInfoType SolonConfigClass::AyanamsaInfoTable[] =
{
    { AYANAMSA_NONE,            "None",               0,          0 },
    { AYANAMSA_FAGAN_BRADLEY,   "Fagan/Bradley",    263,    22.9578 },
    { AYANAMSA_LAHIRI,          "Lahiri",           327,    21.9642 },
    { AYANAMSA_DELUCE,          "DeLuce",            10,    26.3905 },
    { AYANAMSA_RAMAN,           "Raman",            430,    20.3905 },
    { AYANAMSA_JONES,           "Jones",           -135,    28.4152 },
    { AYANAMSA_JOHNRDO,         "Johndro",         -363,    31.5988 },
    { AYANAMSA_CAYCE,           "Cayce",            -50,    27.2283 },
    { AYANAMSA_JUNG,            "Jung",              16,    26.3068 },
    { AYANAMSA_RUDHYAR,         "Rudhyar",          -95,    27.8567 },
    { AYANAMSA_DOBYNS,          "Dobyns",           172,    24.1285 },
    { AYANAMSA_ELY,             "Ely",            -13.6,      26.72 },
    { AYANAMSA_USHA_SHASHI,     "Usha-Shashi",      600,   19.70917 },
    { AYANAMSA_MAX,             "",                   0,          0 }
};


/* !!! WARNING !!! Table order should follow the order of enumeration lint in solon_global.h */
SolonConfigClass::HouseSystemInfoType SolonConfigClass::HouseSystemInfoTable[] =
{
    { HOUSESYSTEM_NONE,            "" },
    { HOUSESYSTEM_PLACIDUS,        "Placidus" },
    { HOUSESYSTEM_KOCH,            "Koch" },
    { HOUSESYSTEM_EQUAL,           "Equal" },
    { HOUSESYSTEM_CAMPANUS,        "Campanus" },
    { HOUSESYSTEM_MERIDIAN,        "Meridian" },
    { HOUSESYSTEM_REGIOMONTANUS,   "Regiomontanus" },
    { HOUSESYSTEM_PORPHYRY,        "Porphyry" },
    { HOUSESYSTEM_MORINUS,         "Morinus" },
    { HOUSESYSTEM_VEDIC,           "Vedic" },
    { HOUSESYSTEM_TOPOCENTRIC,     "Topocentric" },
#ifdef SWISS_EPHEM
	{ HOUSESYSTEM_ALCABITIUS,      "Alcabitius" },
#endif
    { HOUSESYSTEM_MAX,             "" }
};


SolonConfigClass::TimeZoneListInfoStruct SolonConfigClass::TimeZoneListInfoTable[] =
{
    {-39600, "International Date Line West, Midway Island, Samoa" },
    {-36000, "Hawaii" },
    {-32400, "Alaska" },
    {-28800, "Pacific Time (US & Canada), Tijuana" },
    {-25200, "Mountain Time (US & Canada), Chihuahua, Mazatlan, Arizona" },
    {-21600, "Central Time (US & Canada), Saskatchewan, Guadalajara, "
             "Mexico City, Monterrey, Central America" },
    {-18000, "Eastern Time (US & Canada), Indiana (East), Bogota, Lima, Quito" },
    {-14400, "Atlantic Time (Canada), Caracas, La Paz, Santiago" },
    {-12600, "Newfoundland" },
    {-10800, "Brasilia, Buenos Aires, Georgetown, Greenland" },
    { -7200, "Mid-Atlantic" },
    { -3600, "Azores, Cape Verde Is." },
    {     0, "Dublin, Edinburgh, Lisbon, London, Casablanca, Monrovia" },
    {  3600, "Belgrade, Bratislava, Budapest, Ljubljana, Prague, Sarajevo, "
             "Skopje, Warsaw, Zagreb, Brussels, Copenhagen, Madrid, Paris, "
             "Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna, West Central Africa" },
    {  7200, "Bucharest, Cairo, Helsinki, Kyev, Riga, Sofia, Tallinn, "
             "Vilnius, Athens, Istanbul, Minsk, Jerusalem, Harare, Pretoria" },
    { 10800, "Moscow, St. Petersburg, Volgograd, Kuwait, Riyadh, Nairobi, Baghdad" },
    { 12600, "Tehran" },
    { 14400, "Abu Dhabi, Muscat, Baku, Tbilisi, Yerevan" },
    { 16200, "Kabul" },
    { 18000, "Ekaterinburg, Islamabad, Karachi, Tashkent" },
    { 19800, "Chennai, Kolkata, Mumbai, New Delhi" },
    { 20700, "Kathmandu" },
    { 21600, "Astana, Dhaka, Sri Jayawardenepura, Almaty, Novosibirsk" },
    { 23400, "Rangoon" },
    { 25200, "Bangkok, Hanoi, Jakarta, Krasnoyarsk" },
    { 28800, "Beijing, Chongqing, Hong Kong, Urumqi, Kuala Lumpur, Singapore, "
             "Taipei, Perth, Irkutsk, Ulaan Bataar" },
    { 32400, "Seoul, Osaka, Sapporo, Tokyo, Yakutsk" },
    { 34200, "Darwin, Adelaide" },
    { 36000, "Canberra, Melbourne, Sydney, Brisbane, Hobart, Vladivostok, "
             "Guam, Port Moresby" },
    { 39600, "Magadan, Solomon Is., New Caledonia" },
    { 43200, "Fiji, Kamchatka, Marshall Is., Auckland, Wellington" },
    { 46800, "Nuku'alofa" },
    { 1000000, "" }
};


SolonConfigClass::SolonConfigClass( int /*argc*/, char  ** /*argv*/ )
{
    programFileName = QApplication::applicationFilePath();
    QFileInfo programFileInfo( programFileName );
    
    progPath   = programFileInfo.absolutePath();
    prefixPath = progPath.section("/", 0, -2);
    sharePath  = prefixPath + "/share/symsolon";
    
    find_base_folders();
    
    // default language
    load_language_table();
    language = "en";
    char *lang = getenv("LANG");
    if ( lang != NULL )
    {
        char *lang2 = strdup(lang);
        lang2[2] = '\0';
        for ( int i=0; LanguageInfoTable[i].name; i++ )
        {
        	if ( strcasecmp( LanguageInfoTable[i].id, lang2 ) == 0 )
        		language = LanguageInfoTable[i].id;
        }
        free(lang2);
    }
    
    // default settings
    cardTopTextEnabled = true;
    cardBottomTextEnabled = true;
    toolTipsEnabled = true;
    topocentricCalculationUsed = false;
    houseSystem = HOUSESYSTEM_PLACIDUS;
    ayanamsaType = AYANAMSA_NONE;
    aspectOrbitAsLimit = false;
    backgroundColor = 0;
    foregroundColor = 0xffffff;
    printingColor = 0;
    
    // transits
    memset( transitPlanets, 0, sizeof(transitPlanets) );
    // tnasit planets in a month
    transitPlanets[TRANSITMODE_MONTH][PLANET_MOON] = true;
    transitPlanets[TRANSITMODE_MONTH][PLANET_SUN] = true;
    transitPlanets[TRANSITMODE_MONTH][PLANET_MERCURY] = true;
    transitPlanets[TRANSITMODE_MONTH][PLANET_VENUS] = true;
    transitPlanets[TRANSITMODE_MONTH][PLANET_MARS] = true;
    // tnasit planets in a year
    transitPlanets[TRANSITMODE_YEAR][PLANET_SUN] = true;
    transitPlanets[TRANSITMODE_YEAR][PLANET_MERCURY] = true;
    transitPlanets[TRANSITMODE_YEAR][PLANET_VENUS] = true;
    transitPlanets[TRANSITMODE_YEAR][PLANET_MARS] = true;
    // tnasit planets in 12 year
    transitPlanets[TRANSITMODE_12YEAR][PLANET_MARS] = true;
    transitPlanets[TRANSITMODE_12YEAR][PLANET_JUPITER] = true;
    transitPlanets[TRANSITMODE_12YEAR][PLANET_SATURN] = true;
    transitPlanets[TRANSITMODE_12YEAR][PLANET_URANUS] = true;
    transitPlanets[TRANSITMODE_12YEAR][PLANET_NEPTUNE] = true;
    transitPlanets[TRANSITMODE_12YEAR][PLANET_PLUTO] = true;
    // tnasit planets in 100 year
    transitPlanets[TRANSITMODE_100YEAR][PLANET_JUPITER] = true;
    transitPlanets[TRANSITMODE_100YEAR][PLANET_SATURN] = true;
    transitPlanets[TRANSITMODE_100YEAR][PLANET_URANUS] = true;
    transitPlanets[TRANSITMODE_100YEAR][PLANET_NEPTUNE] = true;
    transitPlanets[TRANSITMODE_100YEAR][PLANET_PLUTO] = true;
    
    firstTimeStart = false;
    open();
}


SolonConfigClass::~SolonConfigClass()
{
}


void
SolonConfigClass::find_base_folders()
{
    QString homeConfigPath = "";
    
    // get home directory
    QString homeDir = getenv("HOME");
    
    if (homeDir.length()>0)
    {
        // it seems we are on UNIX -- try to open $HOME/.symsolon
        QDir dir( homeDir );
        if (dir.exists("symsolon") || dir.mkdir("symsolon"))
        {
            QDir sdir( dir.path() + "/symsolon" );
            if ( sdir.exists("clients") )
            {
                homeConfigPath = sdir.path();
            }
            if ( sdir.mkdir("clients") )
            {
                // copy the content of default client folder to this folder
                QString origClientDirPath = sharePath + "/clients";
                QString newClientDirPath = sdir.path() + "/clients";
                QDir origDir( origClientDirPath );
                QStringList list = origDir.entryList();
                for (int i=0; i<list.size(); i++)
                {
                    QFile::copy( origClientDirPath + "/" + list.at(i),
                                 newClientDirPath + "/" + list.at(i) );
                }
                homeConfigPath = sdir.path();
            }
        }
    }
    
    if (homeConfigPath.length() > 0)
    {
        configFileName = homeConfigPath + "/symsolon-config.xml";
        clientDataPath = homeConfigPath + "/clients";
    }
    else
    {
        // it seems we are on a Windows machine
        configFileName = prefixPath + "/etc/symsolon-config.xml";
        clientDataPath = sharePath + "/clients";
    }
}


void
SolonConfigClass::load_language_table()
{
    QFile f(sharePath + "/translations/languages.lst"  );
    
    if ( !f.open( QFile::ReadOnly| QFile::Text ) )
    {
        LanguageInfoTable = new LanguageInfoStruct[4];
        LanguageInfoTable[0].name = "English";
        LanguageInfoTable[0].id   = "en";
        LanguageInfoTable[1].name = "Deutsch";
        LanguageInfoTable[1].id   = "de";
        LanguageInfoTable[2].name = "Magyar";
        LanguageInfoTable[2].id   = "hu";
        LanguageInfoTable[3].name = NULL;
        LanguageInfoTable[3].id   = NULL;
        return;
    }
    
    QTextStream     s( &f );
    QString         line;
    QStringList     idList;
    QStringList     langList;
    
    while ( !s.atEnd() )
    {
        line = s.readLine().trimmed();
        if ( line.isEmpty() || line[0]==';' || line[0]=='#' ) continue;
        idList << line.section( ':', 0, 0, QString::SectionSkipEmpty ).trimmed();
        langList << line.section( ':', 1, 1, QString::SectionSkipEmpty ).trimmed();
    }
    
    LanguageInfoTable = new LanguageInfoStruct[ idList.size()+1 ];
    for ( int i=0; i<idList.size(); i++ )
    {
        LanguageInfoTable[ i ].id = strdup( idList.at(i).toLocal8Bit().constData() );
        LanguageInfoTable[ i ].name = strdup( langList.at(i).toLocal8Bit().constData() );
    }
    LanguageInfoTable[ idList.size() ].id = NULL;
    LanguageInfoTable[ idList.size() ].name = NULL;
    
    f.close();
}


bool
SolonConfigClass::fatalError (const QXmlParseException & exception)
{
    QString qstr("");
     
    qstr = QString("Configuration ERROR:") + "Fatal error on line" + exception.lineNumber() +
            ", column" + exception.columnNumber() + ":" +
            exception.message();
    
    QMessageBox::critical(NULL, "SymSolon", qstr);
    
    return false;
}


bool
SolonConfigClass::startElement ( const QString &/*namespaceURI*/,
            const QString &/*localName*/, const QString &qName,
            const QXmlAttributes &atts )
{
    xmlElementName  = qName;
    xmlElementChars = "";
    xmlAttributes = atts;
    return true;
}


bool
SolonConfigClass::endElement ( const QString &/*namespaceURI*/,
            const QString &/*localName*/, const QString & /*qName*/ )
{
    int         i=0, j=0;
    bool        ok=false;
    
    if ( xmlElementName == "language" )
    {
        for (i=0; LanguageInfoTable[i].name!=NULL; i++)
            if ( xmlElementChars == LanguageInfoTable[i].id )
            {
                language = xmlElementChars;
            }
    }
    else if ( xmlElementName == "houseSystem" )
    {
        for (i=0; HouseSystemInfoTable[i].index<HOUSESYSTEM_MAX; i++)
            if (HouseSystemInfoTable[i].name == xmlElementChars)
            {
                houseSystem = HouseSystemInfoTable[i].index;
            }
    }
    else if ( xmlElementName == "ayanamsaType" )
    {
        for (i=0; AyanamsaInfoTable[i].index<AYANAMSA_MAX; i++)
            if (AyanamsaInfoTable[i].name == xmlElementChars)
            {
                ayanamsaType = AyanamsaInfoTable[i].index;
            }
    }
    else if ( xmlElementName == "topocentricCalculationUsed" )
    {
        if (xmlElementChars == "true") topocentricCalculationUsed = true;
        else topocentricCalculationUsed = false;
    }
    else if ( xmlElementName == "toolTipsEnabled" )
    {
        if (xmlElementChars == "true") toolTipsEnabled = true;
        else toolTipsEnabled = false;
    }
    else if ( xmlElementName == "detailedToolTipsEnabled" )
    {
        if (xmlElementChars == "true") detailedToolTipsEnabled = true;
        else detailedToolTipsEnabled = false;
    }
    else if ( xmlElementName == "cardTopTextEnabled" )
    {
        if (xmlElementChars == "true") cardTopTextEnabled = true;
        else cardTopTextEnabled = false;
    }
    else if ( xmlElementName == "cardBottomTextEnabled" )
    {
        if (xmlElementChars == "true") cardBottomTextEnabled = true;
        else cardBottomTextEnabled = false;
    }
    else if ( xmlElementName == "clientDataPath" )
    {
        clientDataPath = xmlElementChars;
    }
    else if ( xmlElementName == "aspectOrbitAsLimit" )
    {
        if (xmlElementChars == "true") aspectOrbitAsLimit = true;
        else aspectOrbitAsLimit = false;
    }
    else if ( xmlElementName == "printingHeaderText" )
    {
        printingHeaderText = xmlElementChars;
    }
    else if ( xmlElementName == "backgroundColor" )
    {
        backgroundColor = xmlElementChars.toInt( NULL, 16 );
    }
    else if ( xmlElementName == "foregroundColor" )
    {
        foregroundColor = xmlElementChars.toInt( NULL, 16 );
    }
    else if ( xmlElementName == "printingColor" )
    {
        printingColor = xmlElementChars.toInt( NULL, 16 );
    }
    
    if (Symbol)
    {
        if ( xmlElementName == "planet" )
        {
            i = Symbol->english_name_to_index( INFOTYPE_PLANET, xmlAttributes.value("indexname"));
            strcpy( Symbol->planetInfo[i].name, xmlAttributes.value("name").toUtf8().constData() );
            Symbol->planetInfo[i].orbit = xmlAttributes.value("orbit").toDouble();
            Symbol->planetInfo[i].enabled = (xmlAttributes.value("enabled")=="true");
        }
        else if ( xmlElementName == "sign" )
        {
            i = Symbol->english_name_to_index( INFOTYPE_SIGN, xmlAttributes.value("indexname"));
            strcpy( Symbol->signInfo[i].name, xmlAttributes.value("name").toUtf8().constData() );
        }
        else if ( xmlElementName == "house" )
        {
            i = Symbol->english_name_to_index( INFOTYPE_HOUSE, xmlAttributes.value("indexname"));
            strcpy( Symbol->houseInfo[i].name, xmlAttributes.value("name").toUtf8().constData() );
        }
        else if ( xmlElementName == "aspect" )
        {
            i = Symbol->english_name_to_index( INFOTYPE_ASPECT, xmlAttributes.value("indexname"));
            strcpy( Symbol->aspectInfo[i].name, xmlAttributes.value("name").toUtf8().constData() );
            strcpy( Symbol->aspectInfo[i].abbreviation,
                        xmlAttributes.value("abbreviation").toUtf8().constData() );
            Symbol->aspectInfo[i].angle = xmlAttributes.value("angle").toDouble();
            Symbol->aspectInfo[i].orbit = xmlAttributes.value("orbit").toDouble();
            Symbol->aspectInfo[i].harmony = xmlAttributes.value("harmony").toDouble();
            Symbol->aspectInfo[i].planetEnergy =
                Symbol->english_name_to_index( INFOTYPE_PLANET, xmlAttributes.value("planetenergy") );
            Symbol->aspectInfo[i].color = xmlAttributes.value("color").toInt(&ok, 16);
            Symbol->aspectInfo[i].enabled = (xmlAttributes.value("enabled")=="true");
        }
        else if ( xmlElementName == "transitInMonthPlanets" ||
                  xmlElementName == "transitInYearPlanets" ||
                  xmlElementName == "transitIn12YearPlanets" ||
                  xmlElementName == "transitIn100YearPlanets" )
        {
            int transitMode = TRANSITMODE_NONE;
            if (xmlElementName == "transitInMonthPlanets") transitMode = TRANSITMODE_MONTH;
            if (xmlElementName == "transitInYearPlanets") transitMode = TRANSITMODE_YEAR;
            if (xmlElementName == "transitIn12YearPlanets") transitMode = TRANSITMODE_12YEAR;
            if (xmlElementName == "transitIn100YearPlanets") transitMode = TRANSITMODE_100YEAR;
            QStringList strl = xmlElementChars.split( ",", QString::SkipEmptyParts );
            for (i=0; i<strl.size(); i++) strl.replace( i, strl.at(i).trimmed() );
            for (i=0; i<PLANET_MAX; i++) transitPlanets[transitMode][i] = false;
            for (i=0; i<strl.size(); i++)
                for (j=0; j<PLANET_MAX; j++)
                    if ( strl.at(i) ==  Symbol->index_to_english_name( INFOTYPE_PLANET, j ) )
                        transitPlanets[transitMode][j] = true;
        }
        else if ( xmlElementName == "symbolon" )
        {
            i = Symbol->english_name_to_index( INFOTYPE_SYMBOLON, xmlAttributes.value("indexname"));
            strcpy( Symbol->symbolonInfo[i].name, xmlAttributes.value("name").toUtf8().constData() );
        }
    }
    
    // clear element buffer
    xmlElementName = "";
    xmlElementChars = "";
    
    return true;
}


bool
SolonConfigClass::characters ( const QString & chars )
{
    xmlElementChars += chars;
    return true;
}


void
SolonConfigClass::open()
{
    // open configuration file -- create if not exists yet
    QFile f( configFileName );
    if ( !f.open( QFile::ReadOnly| QFile::Text ) )
    {
        firstTimeStart = true;
        save();
        if ( !f.open( QFile::ReadOnly| QFile::Text ) ) return;
    }
    
    QXmlInputSource source( &f );
    QXmlSimpleReader reader;
    
    //Handler *handler = new Handler();
    reader.setContentHandler(this);
    reader.setErrorHandler(this);
    
    bool ok = reader.parse( &source, false );
    
    if (!ok)
    {
        QMessageBox::critical(NULL, "SymSolon", tr("Configuration ERROR: XML Parse error."));
    }
}


void
SolonConfigClass::appendXmlTag( QDomDocument &doc, QDomElement &root, QString name, QString value )
{
    QDomElement tag = doc.createElement( name );
    root.appendChild(tag);
    QDomText t = doc.createTextNode( value );
    tag.appendChild(t);
}


int
SolonConfigClass::save()
{
    int                 i=0, j=0;
    QDomElement         tag;
    QString             str;
    
    QString houseSystemStr = HouseSystemInfoTable[houseSystem].name;
    QString ayanamsaTypeStr = AyanamsaInfoTable[ayanamsaType].name;
    
    // ----- create xml document -----
    QDomDocument doc("SymSolonXML");
    QDomElement root = doc.createElement("SymSolonProgramSettings");
    doc.appendChild(root);
    
    // basic settings
    appendXmlTag( doc, root, "language", language );
    appendXmlTag( doc, root, "houseSystem", houseSystemStr );
    appendXmlTag( doc, root, "ayanamsaType", ayanamsaTypeStr );
    appendXmlTag( doc, root, "topocentricCalculationUsed", topocentricCalculationUsed ? "true" : "false" );
    appendXmlTag( doc, root, "toolTipsEnabled", toolTipsEnabled ? "true" : "false" );
    appendXmlTag( doc, root, "detailedToolTipsEnabled", detailedToolTipsEnabled ? "true" : "false" );
    appendXmlTag( doc, root, "cardTopTextEnabled", cardTopTextEnabled ? "true" : "false" );
    appendXmlTag( doc, root, "cardBottomTextEnabled", cardBottomTextEnabled ? "true" : "false" );
    appendXmlTag( doc, root, "clientDataPath", clientDataPath );
    appendXmlTag( doc, root, "aspectOrbitAsLimit", aspectOrbitAsLimit ? "true" : "false" );
    appendXmlTag( doc, root, "printingHeaderText", printingHeaderText );
    appendXmlTag( doc, root, "backgroundColor", str.sprintf( "%06X", backgroundColor ) );
    appendXmlTag( doc, root, "foregroundColor", str.sprintf( "%06X", foregroundColor ) );
    appendXmlTag( doc, root, "printingColor", str.sprintf( "%06X", printingColor ) );
    
    if (Symbol)
    {
        // --- tables
        // --- planets
        for (i=1; i<PLANET_MAX; i++)
        {
            tag = doc.createElement( "planet" );
            root.appendChild(tag);
            tag.setAttribute( "indexname",
                Symbol->index_to_english_name( INFOTYPE_PLANET, Symbol->planetInfo[i].index ) );
            tag.setAttribute( "name", QString::fromUtf8(Symbol->planetInfo[i].name) );
            tag.setAttribute( "orbit", QString::number(Symbol->planetInfo[i].orbit) );
            tag.setAttribute( "enabled", Symbol->planetInfo[i].enabled?"true":"false" );
        }
        // --- signs
        for (i=1; i<SIGN_MAX; i++)
        {
            tag = doc.createElement( "sign" );
            root.appendChild(tag);
            tag.setAttribute( "indexname",
                Symbol->index_to_english_name( INFOTYPE_SIGN, Symbol->signInfo[i].index) );
            tag.setAttribute( "name", QString::fromUtf8(Symbol->signInfo[i].name) );
        }
        // --- houses
        for (i=1; i<=HOUSE_MAX; i++)
        {
            tag = doc.createElement( "house" );
            root.appendChild(tag);
            tag.setAttribute( "indexname",
                Symbol->index_to_english_name( INFOTYPE_HOUSE, Symbol->houseInfo[i].index) );
            tag.setAttribute( "name", QString::fromUtf8(Symbol->houseInfo[i].name) );
        }
        // --- aspects
        for (i=1; i<ASPECT_MAX; i++)
        {
            tag = doc.createElement( "aspect" );
            root.appendChild(tag);
            tag.setAttribute( "indexname",
                Symbol->index_to_english_name( INFOTYPE_ASPECT, Symbol->aspectInfo[i].index) );
            tag.setAttribute( "name", QString::fromUtf8(Symbol->aspectInfo[i].name) );
            tag.setAttribute( "abbreviation", Symbol->aspectInfo[i].abbreviation );
            tag.setAttribute( "angle", QString::number(Symbol->aspectInfo[i].angle) );
            tag.setAttribute( "orbit", QString::number(Symbol->aspectInfo[i].orbit) );
            tag.setAttribute( "harmony", QString::number(Symbol->aspectInfo[i].harmony) );
            tag.setAttribute( "planetenergy", Symbol->index_to_english_name( INFOTYPE_PLANET, Symbol->aspectInfo[i].planetEnergy) );
            tag.setAttribute( "color", QString::number(Symbol->aspectInfo[i].color, 16) );
            tag.setAttribute( "enabled", Symbol->aspectInfo[i].enabled?"true":"false" );
        }
        // --- transits
        QString     transitName;
        int         transitMode;
        for (i=0; i<4; i++)
        {
            switch (i)
            {
                default:
                case 0:
                    transitName = "transitInMonthPlanets";
                    transitMode = TRANSITMODE_MONTH;
                    break;
                
                case 1:
                    transitName = "transitInYearPlanets";
                    transitMode = TRANSITMODE_YEAR;
                    break;
                
                case 2:
                    transitName = "transitIn12YearPlanets";
                    transitMode = TRANSITMODE_12YEAR;
                    break;
                
                case 3:
                    transitName = "transitIn100YearPlanets";
                    transitMode = TRANSITMODE_100YEAR;
                    break;
            }
            for (str="",j=0; j<PLANET_MAX; j++)
            {
                if ( !transitPlanets[transitMode][j] ) continue;
                str += Symbol->index_to_english_name( INFOTYPE_PLANET, j ) + ", ";
            }
            appendXmlTag( doc, root, transitName, str );
        }
        // --- symbolons
        for (i=1; i<SYMBOLON_MAX; i++)
        {
            tag = doc.createElement( "symbolon" );
            root.appendChild(tag);
            tag.setAttribute( "indexname",
                Symbol->index_to_english_name( INFOTYPE_SYMBOLON, Symbol->symbolonInfo[i].index) );
            tag.setAttribute( "name", QString::fromUtf8(Symbol->symbolonInfo[i].name) );
        }
    }
    
    // --- save to file ---
    QFile f( configFileName );
    if (f.open(QFile::WriteOnly | QFile::Truncate))
    {
        QTextStream stream( &f );
        doc.save( stream, 4 );
        f.close();
    }
    else
    {
        QMessageBox::critical(NULL, "SymSolon", tr("ERROR: Couldn't save config file:\n") +
                                    configFileName);
        return false;
    }
    
    return true;
}


