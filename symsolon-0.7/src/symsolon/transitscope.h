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
#ifndef TRANSITSCOPE_H
#define TRANSITSCOPE_H

#include "solon_global.h"
#include "solonmath.h"
#include "studiowindow.h"
#include "symsolon.h"
#include "horoscope.h"
#include "scopewidget.h"
#include "ui_transitscope.h"


class TransitScopeClass : public StudioWindowClass
{
    Q_OBJECT

typedef struct TransitModeStruct
{
    TransitModeType     index;
    char               name[24];
} TransitModeStruct;

public:
    Ui::TransitScopeForm        *m_ui;
    ScopeWidgetClass            *scope;
    ScopeWidgetClass            *dataScope;
    
    TransitScopeClass(QWidget *parent = 0);
    ~TransitScopeClass();

    void setHoroscope( HoroscopeClass *h1, HoroscopeClass *h2 = NULL );
    void refresh_horoscope();

public slots:
    
    virtual void year_changed();
    virtual void month_changed();
    virtual void show_text_version();
    virtual void mode_changed();
    virtual void refresh_scope();
    
private:
    static TransitModeStruct    TransitModeList[];
    int                         year;
    int                         month;

};

#endif
