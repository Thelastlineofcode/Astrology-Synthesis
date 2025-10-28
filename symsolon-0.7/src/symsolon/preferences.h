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
#ifndef PREFERENCES_H
#define PREFERENCES_H

#include "solon_global.h"
#include "studiowindow.h"
#include "ui_preferences.h"


class PreferencesClass : public StudioWindowClass
{
    Q_OBJECT;

public:
    
    Ui::Preferences        *m_ui;
    
    PreferencesClass();
    ~PreferencesClass();


public slots:

    void apply_settings();
    void save_settings();
    static void load_settings();
    virtual void add_to_transit_month_line();
    virtual void add_to_transit_year_line();
    virtual void add_to_transit_12year_line();
    virtual void add_to_transit_100year_line();
    virtual void paint_backgroundcolor_frame( QWidget*, QPaintEvent* );
    virtual void paint_foregroundcolor_frame( QWidget*, QPaintEvent* );
    virtual void paint_printingcolor_frame( QWidget*, QPaintEvent* );
    virtual void popup_bg_color_selector();
    virtual void popup_fg_color_selector();
    virtual void popup_print_color_selector();

protected:

    void closeEvent( QCloseEvent* );

};

#endif
