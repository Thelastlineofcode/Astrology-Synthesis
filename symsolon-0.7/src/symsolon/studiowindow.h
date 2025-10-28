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

#ifndef _PSTUDIO_GLOBAL_H
#define _PSTUDIO_GLOBAL_H

#include <solon_global.h>
#include <symsolon.h>


class StudioWindowClass : public QWidget
{
    Q_OBJECT

#define STUDIOWINDOW_CHILD_MAX  100

public:    
    StudioWindowClass    *m_creatorWin;
    QString              userInfo;
    StudioWindowClass    *m_childWinArray[ STUDIOWINDOW_CHILD_MAX ];
    
    StudioWindowClass(QWidget *parent = 0);
    ~StudioWindowClass();
    
    void messagebox( QString );
    void setCreator( StudioWindowClass* );
    StudioWindowClass* getCreator( void );
    void remove_child_window( StudioWindowClass* );
    void remove_all_child_windows();
    void set_user_info( QString str );
    QString get_user_info();
    
protected:
    
    void add_child_window( StudioWindowClass* );
    void closeEvent( QCloseEvent *ce );

};

#define UI_TO_WORKSPACE( UI ) \
    { \
    m_ui = UI; \
    m_ui->setupUi( this ); \
    setParent( SymSolon->workspace ); \
    SymSolon->workspace->addWindow( this ); \
    hide(); \
    }

#endif
