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

#ifndef _PSTUDIO_TEXTEDITOR_H
#define _PSTUDIO_TEXTEDITOR_H

#include "solon_global.h"
#include "studiowindow.h"
#include "ui_texteditor.h"

class TextEditorClass : public StudioWindowClass
{
    Q_OBJECT
    
public:
    Ui::texteditor        *m_ui;
    
    TextEditorClass();
    ~TextEditorClass();
    
    void append( QString &text );
    void append( char *ctext );
};

#endif

