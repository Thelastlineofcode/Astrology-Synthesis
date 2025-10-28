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

#include <QtGui/QApplication>
#include <QCoreApplication>
#include <QRect>
#include <QPoint>
#include <QtGui/QDesktopWidget>
#include <QTranslator>

#include "solon_global.h"
#include "symsolon.h"
#include "solarsystem.h"
#include "texteditor.h"
#include "scopewidget.h"
#include "symbolonscope.h"
#include "startup.h"
#include "languageselector.h"
#include "solontables.h"

#include "horoscope.h"

QApplication    *App= NULL;
QTranslator        Translator;


void
set_translation()
{
    Translator.load( SolonConfig->sharePath + "/translations/symsolon_" + SolonConfig->language );
    App->installTranslator( &Translator );
}


int
main( int argc, char ** argv )
{
    int                 ret = 0;
    QApplication        a( argc, argv );
    
    App = &a;
    
    a.connect( &a, SIGNAL(lastWindowClosed()), &a, SLOT(quit()) );
    
    // get screen geometry (width, height)
    QRect screen = QApplication::desktop()->screenGeometry();
    
    // load configuration files and language settings
    SolonConfig = new SolonConfigClass( argc, argv );
    set_translation();
    if ( SolonConfig->firstTimeStart )
    {
        LanguageSelectorClass  *lansel = new LanguageSelectorClass();
        lansel->move( screen.center() - QPoint( lansel->width()/2,lansel->height()/2 ) );
        lansel->show();
        a.exec();
        SolonConfig->save();
        set_translation();
    }
    
    // set application icon
    QIcon   appIcon( SolonConfig->sharePath + "/icons/symsolon.png" );
    App->setWindowIcon( appIcon );
    
    // show Startup window
    Startup = new StartupClass();
    Startup->setWindowIcon( appIcon );
    Startup->move( screen.center() - QPoint( Startup->width()/2, Startup->height()/2 ) );
    Startup->show();
    Startup->repaint();
    QCoreApplication::processEvents();
    
    // load date into Symbol object
    Symbol = new SymbolClass(&a);
    
    // load configuration file again after Symbols are loaded
    SolonConfig->open();
    
    // load tables
    SolonTables = new SolonTablesClass( SolonConfig->sharePath );
    
    // create main window: SymSolon
    SymSolon = new SymSolonClass();
    SymSolon->setWindowIcon( appIcon );
    SymSolon->setGeometry(0,0,800,600);
    SymSolon->move( screen.center() - QPoint( SymSolon->width()/2, SymSolon->height()/2 ) );
    SymSolon->show();
    
    // open swiss ephemerids
    SolarSystemClass::open_swiss_ephem();
    
    // close startup window
    Startup->close();
    
    // RUN MAIN APPLICATION LOOP
    ret = a.exec();
    
    // close resources used by swiss ephemerids
    SolarSystemClass::close_swiss_ephem();
    
    return ret;
}
