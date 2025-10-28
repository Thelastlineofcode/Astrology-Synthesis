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
#include "client.h"

#include <QtGui/QToolTip>

#include "classicscope.h"
#include "symbolonscope.h"
#include "transitscope.h"
#include "lifecyrclescope.h"
#include "synastryscope.h"
#include "locationfinder.h"
#include "synastrychooser.h"
#include "clientprinter.h"


ClientClass::SexInfoType ClientClass::SexInfoList[] =
    {
        { SEX_MALE,         QT_TR_NOOP("Male") },
        { SEX_FEMALE,       QT_TR_NOOP("Female") },
        { SEX_OTHER,        QT_TR_NOOP("Other") },
        { SEX_UNKNOWN,      QT_TR_NOOP("Unknown") }
    };


ClientClass::ClientClass(QWidget *parent) : StudioWindowClass(parent)
{
    int                 i=0;
    char                str[512];
    QTableWidgetItem    *newItem = NULL;
    
    UI_TO_WORKSPACE( new Ui::Client () );
    set_user_info("ClientClass");
    
    // fillup sex list
    for (i=0; i<(int)DIM_OF(SexInfoList); i++)
    {
        m_ui->sex_combo->addItem( tr(SexInfoList[i].sex.toLatin1().data()) );
        /*
        m_ui->sex_combo->addItem( 
            QCoreApplication::translate("@default",
                    SexInfoList[i].sex.toLatin1().data()) );
        */
    }
    
    // fill up life events list
    m_ui->events_table->setColumnCount( 4 );
    m_ui->events_table->setHorizontalHeaderLabels( QStringList()
                << tr("Event") << tr("Start") << tr("End") << tr("Affector") );
    for (i=0; PrognosisClass::defaultLifeEvents[i].name.size()>0; i++)
    {
        // name
        newItem = new QTableWidgetItem( PrognosisClass::defaultLifeEvents[i].name );
        m_ui->events_table->setItem(i-1, 0, newItem);
    }
    m_ui->events_table->resizeColumnsToContents();
    
    // fill up longitude and latitude combo boxes
    m_ui->latitude_combo->addItem( tr("North") );
    m_ui->latitude_combo->addItem( tr("South") );
    m_ui->longitude_combo->addItem( tr("East") );
    m_ui->longitude_combo->addItem( tr("West") );
    
    // fill up timezone combo box
    for (i=0; SolonConfigClass::TimeZoneListInfoTable[i].seconds<1000000; i++)
    {
        sprintf( str, "%0.1f / %s",
            (double)SolonConfigClass::TimeZoneListInfoTable[i].seconds/3600,
            SolonConfigClass::TimeZoneListInfoTable[i].text
            );
        m_ui->zone_combo->addItem( str );
    }
    
    connect( m_ui->zone_combo, SIGNAL( highlighted ( const QString& ) ),
             this, SLOT( zone_combo_highlighted( const QString& ) ) );
    
    // --- connect button signals ---
    
    // connect signals
    connect( m_ui->find_city_button, SIGNAL( clicked(void) ),
             this, SLOT( show_location_finder() ) );
    
    connect( m_ui->birthdate_button, SIGNAL( clicked(void) ),
             this, SLOT( show_birthdate_calendar() ) );
    
    connect( m_ui->apply_button, SIGNAL( clicked(void) ),
             this, SLOT( apply() ) );
    
    connect( m_ui->set_zone_button, SIGNAL( clicked() ),
             this, SLOT( set_auto_zone() ) );
    
    // signals to other window
    connect( m_ui->name_line, SIGNAL( textChanged(QString) ),
             SymSolon, SLOT( header_name_changed() ) );
    connect( m_ui->year_line, SIGNAL( textChanged(QString) ),
             SymSolon, SLOT( refresh_header() ) );
    connect( m_ui->name_line, SIGNAL( textChanged(QString) ),
             this, SLOT( sync_window_title() ) );
    connect( m_ui->month_line, SIGNAL( textChanged(QString) ),
             SymSolon, SLOT( refresh_header() ) );
    connect( m_ui->day_line, SIGNAL( textChanged(QString) ),
             SymSolon, SLOT( refresh_header() ) );
    connect( m_ui->hour_line, SIGNAL( textChanged(QString) ),
             SymSolon, SLOT( refresh_header() ) );
    connect( m_ui->minute_line, SIGNAL( textChanged(QString) ),
             SymSolon, SLOT( refresh_header() ) );
    
    fileName = "";
    xmlElementName = "";
}


ClientClass::~ClientClass()
{
}


void
ClientClass::closeEvent ( QCloseEvent * event )
{
    hide();
    event->setAccepted(false);
}


void
ClientClass::zone_combo_highlighted( const QString& itemStr )
{
    QToolTip::showText( m_ui->zone_combo->mapToGlobal(QPoint(0,-20)), itemStr );
}


QString
ClientClass::get_name()
{
    if (m_ui==NULL) return "";
    if (m_ui->name_line==NULL) return "";
    return m_ui->name_line->text();
}


QString
ClientClass::get_birth()
{
    QString        qstr;
    int            birthYear = m_ui->year_line->text().toInt();
    int            birthMonth = m_ui->month_line->text().toInt();
    int            birthDay = m_ui->day_line->text().toInt();
    int            birthHour = m_ui->hour_line->text().toInt();
    int            birthMinute = m_ui->minute_line->text().toInt();
    QString        city = m_ui->city_line->text();
    QString        zone = m_ui->zone_combo->currentText();
    
    qstr.sprintf( "%04i.%02i.%02i %02i:%02i",
                 birthYear, birthMonth, birthDay, birthHour, birthMinute );
    
    return qstr + " - " + city;
}


void
ClientClass::sync_window_title()
{
    QString     title;
    
    title = tr("Personal Info") + " - " + get_name();
    setWindowTitle( title );
}


void
ClientClass::create()
{
    m_ui->name_line->setText("");
    m_ui->maiden_line->setText("");
    m_ui->sex_combo->setCurrentIndex(0);
    
    m_ui->longitude_deg_line->setText("0");
    m_ui->longitude_min_line->setText("0");
    m_ui->latitude_deg_line->setText("0");
    m_ui->latitude_min_line->setText("0");
    m_ui->longitude_combo->setCurrentIndex(0);
    m_ui->latitude_combo->setCurrentIndex(0);
    
    m_ui->city_line->setText("");
    m_ui->zone_combo->setCurrentIndex(13);
    m_ui->dst_check->setCheckState( Qt::Unchecked );
    
    m_ui->year_line->setText("1900");
    m_ui->month_line->setText("01");
    m_ui->day_line->setText("01");
    m_ui->hour_line->setText("00");
    m_ui->minute_line->setText("00");
    
    m_ui->phone1_line->setText("");
    m_ui->phone2_line->setText("");
    m_ui->mobile1_line->setText("");
    m_ui->mobile2_line->setText("");
    m_ui->email_line->setText("");
    m_ui->address_text->clear();
    
    /*TABLE*/ //m_ui->events_table;
    
    m_ui->comment_text->clear();
}


bool
ClientClass::fatalError (const QXmlParseException & exception)
{
    QString qstr("");
     
    qstr = QString("") + "Fatal error on line" + exception.lineNumber() +
            ", column" + exception.columnNumber() + ":" +
            exception.message();
    
    QMessageBox::critical(this, "Error", qstr);
    
    return false;
}


bool ClientClass::startElement ( const QString &/*namespaceURI*/,
            const QString &/*localName*/, const QString &qName,
            const QXmlAttributes &/*atts*/ )
{
    xmlElementName  = qName;
    xmlElementChars = "";
    return true;
}


bool
ClientClass::endElement ( const QString &/*namespaceURI*/,
            const QString &/*localName*/, const QString & /*qName*/ )
{
         if ( xmlElementName == "name" ) { m_ui->name_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "maidenname" ) { m_ui->maiden_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "sex" )
    {
        int index = 0;
        switch ( (char)xmlElementChars.at(0).toAscii() )
        {
            case 'M': index = 0; break;
            case 'F': index = 1; break;
            case 'O': index = 2; break;
            case 'U': index = 3; break;
        }
        m_ui->sex_combo->setCurrentIndex(index);
    }
    else if ( xmlElementName == "longitude" )
    {
        float    deg=0, min=0;
        char    *data = xmlElementChars.toLatin1().data();
        sscanf( data, "%f:%f", &deg, &min );
        if (deg<0)
        {
            m_ui->longitude_combo->setCurrentIndex(1);
            deg = -deg;
        }
        else
        {
            m_ui->longitude_combo->setCurrentIndex(0);
        }
        m_ui->longitude_deg_line->setText( QString::number( deg ) );
        m_ui->longitude_min_line->setText( QString::number( min ) );
    }
    else if ( xmlElementName == "latitude" )
    {
        float    deg=0, min=0;
        char    *data = xmlElementChars.toLatin1().data();
        sscanf( data, "%f:%f", &deg, &min );
        if (deg<0)
        {
            m_ui->latitude_combo->setCurrentIndex(1);
            deg = -deg;
        }
        else
        {
            m_ui->latitude_combo->setCurrentIndex(0);
        }
        m_ui->latitude_deg_line->setText( QString::number( deg ) );
        m_ui->latitude_min_line->setText( QString::number( min ) );
    }
    else if ( xmlElementName == "city" ) { m_ui->city_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "zone" )
    {
        int i=0;
        int seconds = (int)(xmlElementChars.toDouble() * 3600);
        for (i=0; SolonConfigClass::TimeZoneListInfoTable[i].seconds<1000000; i++)
        {
            if (SolonConfigClass::TimeZoneListInfoTable[i].seconds == seconds)
            {
                m_ui->zone_combo->setCurrentIndex(i);
                seconds = 1000000;
                break;
            }
        }
        if (seconds != 1000000) m_ui->zone_combo->setCurrentIndex(12);
    }
    else if ( xmlElementName == "birthdate" )
    {
        int     year=0, month=0, day=0;
        char    *data = xmlElementChars.toLatin1().data();
        sscanf( data, "%i.%i.%i", &year, &month, &day );
        m_ui->year_line->setText( QString::number(year) );
        m_ui->month_line->setText( QString::number(month) );
        m_ui->day_line->setText( QString::number(day) );
    }
    else if ( xmlElementName == "birthtime" )
    {
        int     hour=0, min=0;
        char    *data = xmlElementChars.toLatin1().data();
        sscanf( data, "%i:%i", &hour, &min );
        m_ui->hour_line->setText( QString::number(hour) );
        m_ui->minute_line->setText( QString::number(min) );
    }
    else if ( xmlElementName == "dst" )
    {
        if ( xmlElementChars == "yes" )
        {
            m_ui->dst_check->setCheckState( Qt::Checked );
        }
        else
        {
            m_ui->dst_check->setCheckState( Qt::Unchecked );
        }
    }
    else if ( xmlElementName == "phone1" ) { m_ui->phone1_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "phone2" ) { m_ui->phone2_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "mobile1" ) { m_ui->mobile1_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "mobile2" ) { m_ui->mobile2_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "email" ) { m_ui->email_line->setText( xmlElementChars ); }
    else if ( xmlElementName == "address" ) { m_ui->address_text->setPlainText( xmlElementChars ); }
    else if ( xmlElementName == "comment" ) { m_ui->comment_text->setPlainText( xmlElementChars ); }
    
    // clear element buffer
    xmlElementName = "";
    xmlElementChars = "";
    
    return true;
}


bool
ClientClass::characters ( const QString & chars )
{
    xmlElementChars += chars;
    return true;
}


int
ClientClass::open( QString inFileName )
{
    fileName = inFileName;
    
    QFile f( fileName );
    if ( !f.open( QFile::ReadOnly| QFile::Text ) )
    {
        QMessageBox::critical(this, "Error", "Can't open file.");
        return false;
    }
    
    QXmlInputSource source( &f );
    QXmlSimpleReader reader;
    
    //Handler *handler = new Handler();
    reader.setContentHandler(this);
    reader.setErrorHandler(this);
    
    bool ok = reader.parse( &source, false );
    
    if (!ok)
    {
        QMessageBox::critical(this, "Error", "XML Parse error.");
        return false;
    }
     
    return true;
}


void
ClientClass::save_and_hide()
{
    save();
    hide();
}


void
ClientClass::apply()
{
    SymSolon->repaint_all_windows();
}


void
ClientClass::appendXmlTag( QDomDocument &doc, QDomElement &root, QString name, QString value )
{
    QDomElement tag = doc.createElement( name );
    root.appendChild(tag);
    QDomText t = doc.createTextNode( value );
    tag.appendChild(t);
}


void
ClientClass::save()
{
    QString        name = m_ui->name_line->text();
    QString        maidenName = m_ui->maiden_line->text();
    int            sexIndex = m_ui->sex_combo->currentIndex();
    QString        sex;
    switch ( sexIndex )
    {
        case 0: sex = "M"; break;
        case 1: sex = "F"; break;
        case 2: sex = "O"; break;
        case 3: sex = "U"; break;
    }
    
    int            longitude_pol = (m_ui->longitude_combo->currentIndex()==0) ? 1 : -1;
    int            longitude_deg = m_ui->longitude_deg_line->text().toInt();
    int            longitude_min = m_ui->longitude_min_line->text().toInt();
    int            latitude_pol  = (m_ui->latitude_combo->currentIndex()==0) ? 1 : -1;
    int            latitude_deg  = m_ui->latitude_deg_line->text().toInt();
    int            latitude_min  = m_ui->latitude_min_line->text().toInt();
    
    QString        city = m_ui->city_line->text();
    QString        zone = m_ui->zone_combo->currentText().section('/', 0, 0).trimmed();
    
    int            birthYear = m_ui->year_line->text().toInt();
    int            birthMonth = m_ui->month_line->text().toInt();
    int            birthDay = m_ui->day_line->text().toInt();
    int            birthHour = m_ui->hour_line->text().toInt();
    int            birthMinute = m_ui->minute_line->text().toInt();
    
    int            dst = (m_ui->dst_check->checkState()==Qt::Checked) ? 1 : 0 ;
    
    QString        phone1 = m_ui->phone1_line->text();
    QString        phone2 = m_ui->phone2_line->text();
    QString        mobile1 = m_ui->mobile1_line->text();
    QString        mobile2 = m_ui->mobile2_line->text();
    QString        email = m_ui->email_line->text();
    QString        address = m_ui->address_text->toPlainText();
    
    /*TABLE*/ //m_ui->events_table;
    
    QString        comment = m_ui->comment_text->toPlainText();
    
    // ----- Save -----
    QDomDocument doc("SymSolonXML");
    QDomElement root = doc.createElement("SymSolonClient");
    doc.appendChild(root);
    
    appendXmlTag( doc, root, "name", name );
    appendXmlTag( doc, root, "maidenname", maidenName );
    appendXmlTag( doc, root, "sex", sex );
    appendXmlTag( doc, root, "longitude",
            QString("") + ((longitude_pol>0)?"+":"-") +
            QString::number(longitude_deg) + ":" +
            QString::number(longitude_min) );
    appendXmlTag( doc, root, "latitude",
            QString("") + ((latitude_pol>0)?"+":"-") +
            QString::number(latitude_deg) + ":" +
            QString::number(latitude_min) );
    appendXmlTag( doc, root, "city", city );
    appendXmlTag( doc, root, "zone", zone );
    appendXmlTag( doc, root, "birthdate",
            QString::number(birthYear) + "." +
            QString::number(birthMonth) + "." +
            QString::number(birthDay) );
    appendXmlTag( doc, root, "birthtime",
            QString::number(birthHour) + ":" +
            QString::number(birthMinute) );
    appendXmlTag( doc, root, "dst", (dst?"yes":"no") );
    appendXmlTag( doc, root, "phone1", phone1 );
    appendXmlTag( doc, root, "phone2", phone2 );
    appendXmlTag( doc, root, "mobile1", mobile1 );
    appendXmlTag( doc, root, "mobile2", mobile2 );
    appendXmlTag( doc, root, "email", email );
    appendXmlTag( doc, root, "address", address );
    appendXmlTag( doc, root, "comment", comment );
    
    // --- save to file ---
    //if (fileName.size() <= 0)
    {
//qDebug( "[s]path=%s", SolonConfig->clientDataPath.toLatin1().data() );
        fileName = QFileDialog::getSaveFileName(
            this, tr("Choose a file name"),
            SolonConfig->clientDataPath + fileName,
            "SymSolon File (*.sol)");
        if ( fileName == "" ) return;
        if ( !fileName.endsWith(".sol") ) fileName.append(".sol");
        SolonConfig->clientDataPath = fileName.section( '/', 0, -2 );
    }
    QFile f(fileName);
    if (f.open(QFile::WriteOnly | QFile::Truncate))
    {
        QTextStream stream( &f );
        doc.save( stream, 4 );
        f.close();
        QMessageBox::information(this, "SymSolon", tr("File saved.") );
    }
    else
    {
        QMessageBox::critical(this, "SymSolon", tr("File is not saved.") );
    }

}

void
ClientClass::show_birthdate_calendar()
{
}


HoroscopeClass*
ClientClass::new_horoscope()
{
    int            birthYear = m_ui->year_line->text().toInt();
    int            birthMonth = m_ui->month_line->text().toInt();
    int            birthDay = m_ui->day_line->text().toInt();
    int            birthHour = m_ui->hour_line->text().toInt();
    int            birthMinute = m_ui->minute_line->text().toInt();
    
    int            longitude_pol = (m_ui->longitude_combo->currentIndex()==0) ? 1 : -1;
    int            longitude_deg = m_ui->longitude_deg_line->text().toInt();
    int            longitude_min = m_ui->longitude_min_line->text().toInt();
    int            latutude_pol  = (m_ui->latitude_combo->currentIndex()==0) ? 1 : -1;
    int            latitude_deg  = m_ui->latitude_deg_line->text().toInt();
    int            latitude_min  = m_ui->latitude_min_line->text().toInt();
    
    bool        dst = (m_ui->dst_check->checkState()==Qt::Checked) ? true : false ;
    double        zone = m_ui->zone_combo->currentText().section('/', 0, 0).trimmed().toDouble();
    double        correction = -zone - (dst ? 1 : 0);
    
    double      ayanamsa = 0;
    
    for (int i=0; SolonConfigClass::AyanamsaInfoTable[i].index!=AYANAMSA_MAX; i++)
        if (SolonConfigClass::AyanamsaInfoTable[i].index == SolonConfig->ayanamsaType)
        {
            ayanamsa = SolonConfigClass::AyanamsaInfoTable[i].degreeShift;;
            break;
        }
    
    return new HoroscopeClass( birthYear, birthMonth, birthDay,
                               birthHour + ((double)birthMinute/60.0) + correction,
                               longitude_pol * (longitude_deg + (double)longitude_min/60.0),
                               latutude_pol * (latitude_deg + (double)latitude_min/60.0),
                               ayanamsa );
}


void
ClientClass::shoot_classic_scope()
{
    HoroscopeClass *h = new_horoscope();
    ClassicScopeClass  *classicscope = new ClassicScopeClass(this);
    add_child_window(classicscope);
    classicscope->setHoroscope( h );
    classicscope->show();
}


void
ClientClass::shoot_symbolon_table()
{
    HoroscopeClass *h = new_horoscope();
    SymbolonScopeClass  *symbolonscope = new SymbolonScopeClass(this);
    add_child_window(symbolonscope);
    symbolonscope->setWindowTitle( get_name() + " " + tr("symbolon tables") );
    symbolonscope->setHoroscope( h );
    symbolonscope->show();
}


void
ClientClass::shoot_transit_scope()
{
    HoroscopeClass *h = new_horoscope();
    TransitScopeClass  *transitscope = new TransitScopeClass(this);
    transitscope->setWindowTitle( get_name() + " " + tr("transits") );
    transitscope->setHoroscope( h );
    transitscope->show();
    add_child_window(transitscope);
}


void
ClientClass::shoot_life_cyrcle_scope()
{
    HoroscopeClass *h = new_horoscope();
    LifeCyrcleScopeClass  *lifescope = new LifeCyrcleScopeClass(this);
    lifescope->setWindowTitle( get_name() + " " + tr("life cyrcle") );
    lifescope->setHoroscope( h );
    lifescope->show();
    add_child_window(lifescope);
}


void
ClientClass::shoot_synastry_chooser()
{
    SynastryChooserClass *chooser = new SynastryChooserClass(this);
    add_child_window(chooser);
    chooser->show();
}


void
ClientClass::shoot_synastry_scope( ClientClass* otherClient )
{
    int  i=0;
    
    if (otherClient == NULL) return;
    
    // search that otherClient is exists
    for (i=0; i<SymSolon->clientList.count(); i++)
        if (SymSolon->clientList.at(i) == otherClient) break;
    if (i == SymSolon->clientList.count()) return;
    
    // crate new horoscope and shoot synastry window
    HoroscopeClass *h1 = new_horoscope();
    HoroscopeClass *h2 = otherClient->new_horoscope();
    SynastryScopeClass  *synastryscope = new SynastryScopeClass(this);
    synastryscope->setWindowTitle( get_name() + " " + tr("synastry") );
    synastryscope->setHoroscope( h1, h2 );
    synastryscope->show();
    add_child_window(synastryscope);
}


void
ClientClass::show_location_finder()
{
    LocationFinderClass *locfind = new LocationFinderClass();
    add_child_window( locfind );
    locfind->show();
}


void
ClientClass::set_auto_zone()
{
    QString tzQStr = QString( SolonConfig->sharePath + "/tz" );
    char *tzDir  = (char*)tzQStr.toUtf8().constData();
    
    QString countryQStr = m_ui->city_line->text().section(',', 1, 1);
    char *country = strdup( countryQStr.toLatin1().constData() );
    if (country == NULL) return;
    
    int birthYear = m_ui->year_line->text().toInt();
    int birthMonth = m_ui->month_line->text().toInt();
    int birthDay = m_ui->day_line->text().toInt();
    int birthHour = m_ui->hour_line->text().toInt();
    int birthMinute = m_ui->minute_line->text().toInt();
    
    int longitude_pol = (m_ui->longitude_combo->currentIndex()==0) ? 1 : -1;
    int longitude_deg = m_ui->longitude_deg_line->text().toInt();
    int longitude_min = m_ui->longitude_min_line->text().toInt();
    int latutude_pol  = (m_ui->latitude_combo->currentIndex()==0) ? 1 : -1;
    int latitude_deg  = m_ui->latitude_deg_line->text().toInt();
    int latitude_min  = m_ui->latitude_min_line->text().toInt();
    
    double longitude = longitude_pol * (longitude_deg + (double)longitude_min/60.0);
    double latitude  = latutude_pol * (latitude_deg + (double)latitude_min/60.0);
    
    double zoneShift=0;
    int dst=0, i=0;
    
    LocationFinderClass::get_zone_and_dst(
            tzDir, country, longitude, latitude,
            birthYear, birthMonth, birthDay, birthHour + ((double)birthMinute/60.0),
            &zoneShift, &dst );
    
    // fill up timezone combo box
    for (i=0; SolonConfigClass::TimeZoneListInfoTable[i].seconds<1000000; i++)
    {
        if (SolonConfigClass::TimeZoneListInfoTable[i].seconds == zoneShift)
        {
            m_ui->zone_combo->setCurrentIndex(i);
            break;
        }
    }
    
    m_ui->dst_check->setCheckState( dst ? Qt::Checked : Qt::Unchecked );
    
    free(country);
}


void
ClientClass::print()
{
    HoroscopeClass *h = new_horoscope();
    ClientPrinterClass *clipri = new ClientPrinterClass();
    clipri->setWindowTitle( QString("Print") + ": " + get_name() );
    clipri->setHoroscope( h );
    clipri->set_header_info(
        tr("Name") + ": " + get_name() + "\n" +
        tr("Birth Date") + ": " +  get_birth(),
        SolonConfig->printingHeaderText );
    add_child_window( clipri );
    clipri->show();
}

