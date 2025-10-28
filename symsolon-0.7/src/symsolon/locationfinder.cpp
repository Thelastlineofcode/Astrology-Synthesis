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
#include "locationfinder.h"

#include <QFile>
#include <QTextStream>
#include <QList>
#include <QtGui/QTableView>
#include <QtGui/QTableWidgetItem>

#include <client.h>
#include <quazip.h>
#include <quazipfile.h>

#include "symsolon_zoneinfo.h"

#ifndef TM_YEAR_BASE
#define TM_YEAR_BASE    1900
#endif /* !defined TM_YEAR_BASE */


LocationFinderClass::LocationFinderClass()
{
    UI_TO_WORKSPACE( new Ui::LocationFinder() );
    
    cityArchiveFileName = SolonConfig->sharePath + "/geograph/cities-az.zip";
    if (!QFile::exists( cityArchiveFileName ))
    {
        cityArchiveFileName = SolonConfig->sharePath + "/geograph/selected-cities-az.zip";
    }
    
    // set progress bar
    m_ui->progressBar->setRange(0,100);
    m_ui->progressBar->setValue(0);
    
    // table
    m_ui->locations_table->setColumnCount( 6 );
    m_ui->locations_table->setRowCount( 0 );
    m_ui->locations_table->setHorizontalHeaderLabels( QStringList() <<
                            tr("Country") << tr("Simple City Name") <<
                            tr("Accent City Name") << tr("Region") <<
                            tr("Latitude") << tr("Longitude") );
    
    m_ui->locations_table->setSelectionBehavior( QAbstractItemView::SelectRows );
    m_ui->locations_table->setSelectionMode( QAbstractItemView::SingleSelection );
    //m_ui->locations_table->setStyleSheet("background-color: yellow");
    
    // connect signals
    connect( m_ui->search_button, SIGNAL( clicked(void) ),
             this, SLOT( search() ) );
    connect( m_ui->search_line, SIGNAL( returnPressed() ),
             this, SLOT( search() ) );
    connect( m_ui->ok_button, SIGNAL( clicked(void) ),
             this, SLOT( ok() ) );
}


LocationFinderClass::~LocationFinderClass()
{
}


void
LocationFinderClass::search()
{
    QString                searchName = m_ui->search_line->text();
    QTableWidgetItem    *newItem = NULL;
    QString                line="", cityName="", fileName="";
    quint64                size=0, pos=0, lineNumber=0;
    long                foundCounter=0;
    QChar                firstChar;
    
    // construct fileName from the first character of search string
    firstChar = searchName.at(0);
    if ( firstChar.isLetter() )
    {
        fileName = QString("cities-") + firstChar + ".txt";
    }
    else
    {
        fileName = "cities-0.txt";
    }
    
    // clear table lines
    m_ui->locations_table->setRowCount( 0 );
    
    // open zip file
    QuaZip zip( cityArchiveFileName );
    if (!zip.open(QuaZip::mdUnzip))
    {
        QMessageBox::critical(this, "SymSolon",
                tr("Couldn't open zip archive: ") + zip.getZipError());
        return;
    }
    
    // go to the appropriate file
    if ( !zip.setCurrentFile( fileName ) )
    {
        QMessageBox::critical(this, "SymSolon",
                tr("Couldn't go to file inside zip: ") + zip.getZipError());
        return;
    }
    
    QuaZipFile file(&zip);
    
    if( !file.open( QIODevice::ReadOnly ) )
    {
        QMessageBox::critical(this, "SymSolon",
                tr("Couldn't open file inside zip: ") + zip.getZipError());
        return;
    }
    
    QTextStream        text( &file );
    
    size = file.size();
    
    // 1st line is just header
    line = text.readLine();
    
    while ( !text.atEnd() )
    {
        line = text.readLine();
        if ( line.section(',', 1, 1).startsWith( searchName, Qt::CaseInsensitive ) )
        {
            foundCounter++;
            if (foundCounter > 1000)
            {
                QMessageBox::critical(this, "SymSolon",
                    tr("The program shows only the first 1000 hit.") );
                break;
            }
            m_ui->locations_table->setRowCount( foundCounter );
            // Simple City Name
            newItem = new QTableWidgetItem( line.section(',', 0, 0) );
            newItem->setFlags( Qt::ItemIsEnabled );
            m_ui->locations_table->setItem( foundCounter-1, 0, newItem );
            // Accent City Name
            newItem = new QTableWidgetItem( line.section(',', 1, 1) );
            newItem->setFlags( Qt::ItemIsEnabled );
            m_ui->locations_table->setItem( foundCounter-1, 1, newItem );
            // Country
            newItem = new QTableWidgetItem( line.section(',', 2, 2) );
            newItem->setFlags( Qt::ItemIsEnabled );
            m_ui->locations_table->setItem( foundCounter-1, 2, newItem );
            // Region
            newItem = new QTableWidgetItem( line.section(',', 3, 3) );
            newItem->setFlags( Qt::ItemIsEnabled );
            m_ui->locations_table->setItem( foundCounter-1, 3, newItem );
            // Latitude
            newItem = new QTableWidgetItem( line.section(',', 4, 4) );
            newItem->setFlags( Qt::ItemIsEnabled );
            m_ui->locations_table->setItem( foundCounter-1, 4, newItem );
            // Longitude
            newItem = new QTableWidgetItem( line.section(',', 5, 5) );
            newItem->setFlags( Qt::ItemIsEnabled );
            m_ui->locations_table->setItem( foundCounter-1, 5, newItem );
        }
        
        if (lineNumber++ % 3000 == 0)
        {
            pos = (100*file.pos())/size;
            m_ui->progressBar->setValue( (int)pos );
            QCoreApplication::processEvents();
        }
    }
    
    // set progress bar to 100%
    m_ui->progressBar->setValue( 100 );
    
    m_ui->locations_table->resizeColumnsToContents();
    m_ui->locations_table->selectRow(0);
    m_ui->locations_table->setFocus();
    
    //m_ui->locations_table->item( 0, 0 )->setBackground(  );
    
    file.close();
    
    if( zip.getZipError()!=UNZ_OK )
    {
        QMessageBox::critical(this, "SymSolon",
                tr("File close error inside zip archive: ") + zip.getZipError());
        return;
    }
    
    zip.close();
    
    if(zip.getZipError()!=UNZ_OK)
    {
        QMessageBox::critical(this, "SymSolon",
                tr("Zip archive close error: ") + zip.getZipError());
        return;
    }
}


void
LocationFinderClass::ok()
{
    int row=0;
    
    ClientClass  *client = (ClientClass*)getCreator();
    QItemSelectionModel *model = m_ui->locations_table->selectionModel();
    if ( model->hasSelection() )
    {
        QModelIndexList indexes = model->selectedRows();
        QModelIndex index = indexes.at(0);
        row = index.row();
        QString country = m_ui->locations_table->item( row, 0 )->text();
        QString city = m_ui->locations_table->item( row, 1 )->text();
        client->m_ui->city_line->setText( city+","+country );
        
        double latitude  = m_ui->locations_table->item( row, 4 )->text().toDouble();
        double longitude = m_ui->locations_table->item( row, 5 )->text().toDouble();
        
        if ( latitude < 0 )
        {
            client->m_ui->latitude_combo->setCurrentIndex(1);
            latitude *= -1;
        }
        else
        {
            client->m_ui->latitude_combo->setCurrentIndex(0);
        }
        
        if ( longitude < 0 )
        {
            client->m_ui->longitude_combo->setCurrentIndex(1);
            longitude *= -1;
        }
        else
        {
            client->m_ui->longitude_combo->setCurrentIndex(0);
        }
        
        client->m_ui->longitude_deg_line->setText( QString::number((int)longitude) );
        client->m_ui->longitude_min_line->setText( QString::number(60*(longitude-(int)longitude)) );
        client->m_ui->latitude_deg_line->setText( QString::number((int)latitude) );
        client->m_ui->latitude_min_line->setText( QString::number(60*(latitude-(int)latitude)) );
        
    }
    close();
}


void
LocationFinderClass::print_tm( struct tm *tmp )
{
    qDebug("%04d-%02d-%02d %02d:%02d %s",
        TM_YEAR_BASE+tmp->tm_year, 1+tmp->tm_mon, tmp->tm_mday,
        tmp->tm_hour, tmp->tm_min, (tmp->tm_isdst ? "DST" : "NODST")
        );
}


void
LocationFinderClass::get_zone_and_dst(
    char *tzDir,
    char *country, double longitude, double latitude,
    int year, int month, int day, double localTime,
    double *zoneShift, int *dst )
{
    typedef enum    { SECTION_NONE, SECTION_COUNTRY, SECTION_AFTER_COUNTRY,
                      SECTION_LONGITUDE, SECTION_LATITUDE, SECTION_AFTER_LATITUDE,
                      SECTION_ZONE, SECTION_CLOSED } sectionEnum;
    int             pos=0, l=0, section=SECTION_NONE, size=0;
    char            countryBuf[65]="", longBuf[65]="", latBuf[65]="", zoneBuf[65]="",
                    bestZone[256]="", *tzEnv = (char*)"", sbuf[256], sbuf2[256]="",
                    *buffer = NULL, co[4]="";
    FILE            *f = NULL;
    time_t          tLocal=0, tGMT=0;
    struct tm       tmLocal, tmGMT, tms, *tmPtr=NULL;
    double          longZone=0, latZone=0, distance=0, closestDistance=1000000;
    
    if (country == NULL) return;
    if (zoneShift == NULL) return;
    if (dst == NULL) return;
    
    *zoneShift = 0;
    *dst = 0;
    
    // get default value of "TZ" environment variable
    tzEnv = getenv( "TZ" );
    
    // set "TZDIR" environment variable
    /*
    if (tzDir)
    {
        sprintf( sbuf, "TZDIR=%s", tzDir );
        putenv( sbuf );
#ifdef ZONEFINDER_TEST
        qDebug("%s\n", sbuf);
#endif
    }
    */
    
#ifdef ZONEFINDER_TEST
    qDebug("%s", tzDir);
#endif
    
    // convert country code to upper case characters
    co[0] = toupper( country[0] );
    co[1] = toupper( country[1] );
    co[2] = '\0';
    // open "zone.tab" and read content
    sprintf( sbuf, "%s/zone.tab", tzDir );
#ifdef ZONEFINDER_TEST
    qDebug("%s", sbuf);
#endif
    f = fopen( sbuf, "r" );
    if (f == NULL) return;
    fseek( f, 0, SEEK_END );
    size = ftell( f );
    fseek( f, 0, SEEK_SET );
    buffer = (char*)malloc( size+2 );
    if (buffer == NULL)
    {
        fclose(f);
        return;
    }
    fread( buffer, size, 1, f );
    buffer[size] = '\0';
    fclose( f );
    
    // search the closest city to the given location+latitude in the given country
    section = SECTION_NONE;
    for (pos=l=0; pos<=size; pos++)
    {
        if ( buffer[pos]=='\n' || buffer[pos]=='\r' || buffer[pos]=='\0' )
        {
            if (section == SECTION_CLOSED)
            {
                countryBuf[0] = toupper( countryBuf[0] );
                countryBuf[1] = toupper( countryBuf[1] );
                if ( strcmp( countryBuf, co ) == 0 )
                {
                    // convert longitude and latitude to double numbers
                    // * longitude
                    sbuf2[0]  = longBuf[0];
                    sbuf2[1]  = longBuf[1];
                    sbuf2[2]  = longBuf[2];
                    sbuf2[3]  = '\0';
                    longZone  = atof( sbuf2 );
                    sbuf2[0]  = longBuf[3];
                    sbuf2[1]  = longBuf[4];
                    sbuf2[2]  = '\0';\
                    if (longZone >= 0) longZone += atof( sbuf2 ) / 60.0;
                    else longZone -= atof( sbuf2 ) / 60.0;
                    // * latuitude
                    sbuf2[0]  = latBuf[0];
                    sbuf2[1]  = latBuf[1];
                    sbuf2[2]  = latBuf[2];
                    sbuf2[3]  = latBuf[3];
                    sbuf2[4]  = '\0';
                    latZone   = atof( sbuf2 );
                    sbuf2[0]  = latBuf[4];
                    sbuf2[1]  = latBuf[5];
                    sbuf2[2]  = '\0';
                    if (latZone >= 0) latZone += atof( sbuf2 ) / 60.0;
                    else latZone -= atof( sbuf2 ) / 60.0;
                    // calculate city distance
                    distance = sqrt( SQUARE(longitude-longZone)+SQUARE(latitude-latZone) );
                    if (distance < closestDistance)
                    {
                        closestDistance = distance;
                        strcpy(bestZone, zoneBuf);
#ifdef ZONEFINDER_TEST
                        qDebug("<DEBUG> CLOSEST: ");
#endif
                    }
#ifdef ZONEFINDER_TEST
                qDebug("<DEBUG> %s:%0.2f:%0.2f:%s", countryBuf, longZone, latZone, zoneBuf);
#endif
                }
            }

            if ( buffer[pos+1] != '#' ) section = SECTION_COUNTRY;
            else section = SECTION_NONE;

            countryBuf[0] = '\0';
            longBuf[0]    = '\0';
            latBuf[0]     = '\0';
            zoneBuf[0]    = '\0';

            continue;
        }
        
        switch (section)
        {
            default:
                break;

            case SECTION_COUNTRY:
                countryBuf[l++] = buffer[pos];
                if (buffer[pos+1]==' ' || buffer[pos+1]=='\t')
                {
                    countryBuf[l] = '\0';
                    l = 0;
                    section = SECTION_AFTER_COUNTRY;
                }
                break;

            case SECTION_AFTER_COUNTRY:
                if (buffer[pos+1]!=' ' && buffer[pos+1]!='\t')
                    section = SECTION_LONGITUDE;
                break;

            case SECTION_LONGITUDE:
                longBuf[l++] = buffer[pos];
                if (buffer[pos+1]=='+' || buffer[pos+1]=='-')
                {
                    longBuf[l] = '\0';
                    l = 0;
                    section = SECTION_LATITUDE;
                }
                break;

            case SECTION_LATITUDE:
                latBuf[l++] = buffer[pos];
                if (buffer[pos+1]==' ' || buffer[pos+1]=='\t')
                {
                    latBuf[l] = '\0';
                    l = 0;
                    section = SECTION_AFTER_LATITUDE;
                }
                break;

            case SECTION_AFTER_LATITUDE:
                if (buffer[pos+1]!=' ' && buffer[pos+1]!='\t')
                    section = SECTION_ZONE;
                break;

            case SECTION_ZONE:
                zoneBuf[l++] = buffer[pos];
                if (buffer[pos+1]==' ' || buffer[pos+1]=='\t' ||
                    buffer[pos+1]=='\n' || buffer[pos+1]=='\r')
                {
                    zoneBuf[l] = '\0';
                    l = 0;
                    section = SECTION_CLOSED;
                }
                break;

        }
    }

#ifdef ZONEFINDER_TEST
    qDebug( "<DEBUG> bestZone=%s", bestZone );
#endif

    // set zone for TZ system
    sprintf( sbuf, "TZ=%s", bestZone );
    putenv( sbuf );
    strcpy( symsolon_tzdir, tzDir );
    //strcpy( tzname[0], bestZone );
    
    // get TZ time for bestZone
    memset( &tms, 0, sizeof(tms) );
    tms.tm_year = year - TM_YEAR_BASE;
    tms.tm_mon  = month - 1;
    tms.tm_mday = day;
    tms.tm_hour = 24 * (int)(localTime/24);
    tms.tm_min  = (int)(60 * ((double)localTime - tms.tm_hour));
    tms.tm_sec  = (int)(3600 * ((double)localTime - tms.tm_hour - (double)tms.tm_min/60.0));
    tms.tm_isdst = 0;
    tLocal = symsolon_mktime( &tms );
    tmPtr = symsolon_localtime(&tLocal);
    if (tmPtr) memcpy( &tmLocal, tmPtr, sizeof(tmLocal) );
    if ( tmLocal.tm_isdst )
    {
        tms.tm_isdst = 1;
        tLocal = symsolon_mktime( &tms );
        tmPtr = symsolon_localtime(&tLocal);
        if (tmPtr) memcpy( &tmLocal, tmPtr, sizeof(tmLocal) );
    }
    
    *dst = tmLocal.tm_isdst;
    
    tmPtr = symsolon_gmtime(&tLocal);
    if (tmPtr) memcpy( &tmGMT, tmPtr, sizeof(tmGMT) );

#ifdef ZONEFINDER_TEST
    print_tm( &tmLocal );
    print_tm( &tmGMT );
#endif

    tGMT = symsolon_mktime( &tmGMT );
    *zoneShift = (double)symsolon_difftime( tLocal, tGMT );
    
    // set "TZ" environment variable back to original value
    sprintf( sbuf, "TZ=%s", ((tzEnv==NULL) ? "" : tzEnv) );
    putenv( sbuf );
    
    if (buffer) free(buffer);
}
