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
#ifndef _SYMSOLON_CLIENT_H
#define _SYMSOLON_CLIENT_H

#include "solon_global.h"
#include "studiowindow.h"
#include "prognosis.h"
#include "ui_client.h"
#include "horoscope.h"

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

class ClientClass : public StudioWindowClass, QXmlDefaultHandler
{
    Q_OBJECT
    
    typedef enum { SEX_MALE, SEX_FEMALE, SEX_OTHER, SEX_UNKNOWN } SexType;
    
    typedef struct _SexInfoType
    {
        SexType            index;
        QString            sex;
    } SexInfoType;

public:
    Ui::Client         *m_ui;
    QString            fileName;
    
    ClientClass(QWidget *parent = 0);
    ~ClientClass();
    
    QString get_name();
    QString get_birth();
    
    void shoot_classic_scope();
    void shoot_symbolon_table();
    void shoot_transit_scope();
    void shoot_life_cyrcle_scope();
    void shoot_synastry_chooser();
    void shoot_synastry_scope( ClientClass* otherClient=NULL );
    HoroscopeClass* new_horoscope();
    int open(QString);
    
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
    
    virtual void create();
    virtual void save();
    virtual void print();
    virtual void save_and_hide();
    virtual void show_birthdate_calendar();
    virtual void show_location_finder();
    virtual void apply();
    virtual void set_auto_zone();
    virtual void sync_window_title();
    virtual void zone_combo_highlighted( const QString& itemStr );

protected:

    void closeEvent ( QCloseEvent * event );

private:
    
    QString                 xmlElementName;
    QString                 xmlElementChars;
    static SexInfoType      SexInfoList[];
    
    void appendXmlTag( QDomDocument &doc, QDomElement &root, QString name, QString value );

};

#endif
