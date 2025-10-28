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
#ifndef SYMSOLONSCOPE_H
#define SYMSOLONSCOPE_H

#include "solon_global.h"
#include "solonmath.h"
#include "studiowindow.h"
#include "symsolon.h"
#include "horoscope.h"
#include "scopewidget.h"
#include "ui_symbolonscope.h"

class SymbolonScopeClass : public StudioWindowClass
{
    Q_OBJECT

    typedef struct _SymbolonMethodType
    {
        ScopeStyleType     index;
        QString            name;
    } SymbolonMethodType;

public:
    
    Ui::SymbolonScope       *m_ui;
    ScopeWidgetClass        *scope;
    
    static PlanetIndexType SymbolonPlanetList[];
    
    SymbolonScopeClass(QWidget *parent = 0);
    ~SymbolonScopeClass();
    
    void setHoroscope( HoroscopeClass *h );
    void setMethod( ScopeStyleType m );
    void refresh_horoscope();
    
public slots:
    
    virtual void method_or_planet_changed();

private:

    static SymbolonMethodType   SymbolonMethodList[];

};

#endif
