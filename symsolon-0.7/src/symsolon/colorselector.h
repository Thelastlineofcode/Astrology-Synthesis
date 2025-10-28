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

#ifndef COLORSELECTOR_H
#define COLORSELECTOR_H

#include <QWidget>
#include <QImage>

#include "studiowindow.h"
#include "ui_colorselector.h"


class ColorSelectorClass : public StudioWindowClass
{
    Q_OBJECT

public:
    
    Ui::ColorSelectorForm    *m_ui;
    quint32                  *m_color;
    QWidget                  *m_widget;
    
    ColorSelectorClass();
    ~ColorSelectorClass();

    static quint32 interpolate( quint32 c0, quint32 c1, float rate );
    static quint32 lightness( quint32 c0, float lightness );

public slots:

    virtual void color_selected();
    virtual void frame_event( QEvent* );
    virtual void paint_frame( QWidget*, QPaintEvent* );
    virtual void paint_selectedcolor_frame( QWidget*, QPaintEvent* );

private:

    QWidget                 *m_localWidget;

};


#endif
