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
#ifndef CLIENTPRINTER_H
#define CLIENTPRINTER_H

#include <QPrinter>

#include "solon_global.h"
#include "studiowindow.h"
#include "ui_clientprinter.h"
#include "horoscope.h"
#include "scopewidget.h"


class ClientPrinterClass : public StudioWindowClass
{
    Q_OBJECT

public:

    Ui::ClientPrinterForm         *m_ui;

    ClientPrinterClass(QWidget *parent = 0);
    ~ClientPrinterClass();

    void setHoroscope( HoroscopeClass* );
    void set_header_info( QString, QString );

public slots:

    virtual void print();

protected:

    void closeEvent( QCloseEvent* );

private:

    HoroscopeClass      *m_horoscope;
    
    QPrinter            *printer;
    ScopeWidgetClass    *scope;
    
    bool                m_firstPage;
    
    void print_one_page( ScopeStyleType scopeStyle );

};

#endif
