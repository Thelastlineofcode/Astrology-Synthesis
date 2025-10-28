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

#include "studiowindow.h"
#include <QtGui/QMessageBox>


StudioWindowClass::StudioWindowClass(QWidget *parent) : QWidget(parent)
{
    int        i=0;
    
    for (i=0; i<STUDIOWINDOW_CHILD_MAX; i++)    m_childWinArray[ i ] = NULL;
    setCreator( NULL );
    userInfo = "";
}


StudioWindowClass::~StudioWindowClass()
{
}


void
StudioWindowClass::messagebox( QString str )
{
    QMessageBox::warning( NULL, "SymSolon", str );
}


void
StudioWindowClass::add_child_window( StudioWindowClass *aChildWin )
{
    int i;
    
    if ( aChildWin == NULL ) return;
    
    for (i=0; i<STUDIOWINDOW_CHILD_MAX; i++)
        if ( m_childWinArray[ i ] == NULL ) break;
    
    if ( i >= STUDIOWINDOW_CHILD_MAX ) return;
    
    m_childWinArray[ i ] = aChildWin;
    
    aChildWin->setCreator( this );
    aChildWin->show();
}


void
StudioWindowClass::remove_child_window( StudioWindowClass *aChildWin )
{
    int i;
    
    for (i=0; i<STUDIOWINDOW_CHILD_MAX; i++)
        if ( (QObject*)m_childWinArray[ i ] == aChildWin ) break;
    
    if ( i >= STUDIOWINDOW_CHILD_MAX ) return;
    
    m_childWinArray[ i ] = NULL;
}


void
StudioWindowClass::closeEvent( QCloseEvent* )
{
    remove_all_child_windows();
}


void
StudioWindowClass::remove_all_child_windows()
{
    int        i=0;
    
    // first close child windows
    for (i=0; i<STUDIOWINDOW_CHILD_MAX; i++)
    {
        if ( m_childWinArray[ i ] )
        {
            m_childWinArray[ i ]->close();
        }
        m_childWinArray[ i ] = NULL;
    }
    
    // remove itself from the child-list of creator window
    if ( getCreator() ) getCreator()->remove_child_window( this );
}


void
StudioWindowClass::setCreator( StudioWindowClass *aCreatorWin )
{
    m_creatorWin = aCreatorWin;
}


StudioWindowClass*
StudioWindowClass::getCreator( void )
{
    return m_creatorWin;
}


void
StudioWindowClass::set_user_info( QString str )
{
    userInfo = str;
}


QString
StudioWindowClass::get_user_info()
{
    return userInfo;
}

