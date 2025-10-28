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
#include "aboutsymbolon.h"
#include "symsolon.h"

AboutSymbolonClass::AboutSymbolonClass( QWidget */*creator*/ )
{
    m_ui = new Ui::AboutSymbolonForm();
    m_ui->setupUi( this );
    
    // signals to other window
    connect( m_ui->ok_button, SIGNAL( clicked(void) ),
             SymSolon, SLOT( close_about_symbolon() ) );
}


AboutSymbolonClass::~AboutSymbolonClass()
{
}


void
AboutSymbolonClass::closeEvent( QCloseEvent* )
{
    SymSolon->close_about_symbolon();
}

