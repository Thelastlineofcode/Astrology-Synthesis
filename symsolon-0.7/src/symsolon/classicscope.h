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
#ifndef CLASSICSCOPE_H
#define CLASSICSCOPE_H

#include "solon_global.h"
#include "studiowindow.h"
#include "ui_classicscope.h"

#include "scopewidget.h"


class ClassicScopeClass : public StudioWindowClass
{
    Q_OBJECT;

typedef struct _ClassicStyleListStruct
{
    ScopeStyleType    index;
    char            name[64];
} ClassicStyleListStruct;


typedef struct _DataStyleListStruct
{
    ScopeStyleType    index;
    char            name[64];
} DataStyleListStruct;


typedef struct _TimeStepStruct
{
    TimeStepType    index;
    char            name[64];
} TimeStepStruct;


public:
    Ui::ClassicScope            *m_ui;
    
    ClassicScopeClass(QWidget *parent = 0);
    ~ClassicScopeClass();

    ScopeWidgetClass        *scope;
    ScopeWidgetClass        *dataScope;
    
    void setHoroscope( HoroscopeClass *h );
    void setStyle( ScopeStyleType s );
    void setDataStyle( ScopeStyleType s );
    void refresh_horoscope();
    QString get_time();
    
public slots:

    virtual void style_changed();
    virtual void data_style_changed();
    virtual void time_shift( int direction );
    virtual void time_increase();
    virtual void time_decrease();

private:
    static ClassicStyleListStruct ClassicStyleList[];
    static DataStyleListStruct DataStyleList[];
    static TimeStepStruct TimeStepList[];
    
    void set_title();

};

#endif
