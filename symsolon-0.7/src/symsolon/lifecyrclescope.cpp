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
#include "lifecyrclescope.h"


LifeCyrcleScopeClass::LifeCyrcleScopeClass(QWidget *parent) : StudioWindowClass(parent)
{
    UI_TO_WORKSPACE( new Ui::LifeCyrcleScopeForm () );
    set_user_info("LifeCyrcleScopeClass");
    
    // add a scope object to the middle of this window
    scope = new ScopeWidgetClass();
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(scope);
    layout->setMargin(0);
    layout->setSpacing(0);
    m_ui->scope_frame->setLayout( layout );
    scope->setStyle( SCOPE_LIFECYRCLE );
    scope->show();
    
    // add a dataScope object to the right side of this window
    dataScope = new ScopeWidgetClass();
    QVBoxLayout *layout2 = new QVBoxLayout();
    layout2->addWidget(dataScope);
    layout2->setMargin(0);
    layout2->setSpacing(0);
    m_ui->data_frame->setLayout( layout2 );
    dataScope->setStyle( SCOPE_LIFECYRCLE_INFO );
    dataScope->show();
    
    scope->set_neighbour( dataScope );
}


LifeCyrcleScopeClass::~LifeCyrcleScopeClass()
{
}


void
LifeCyrcleScopeClass::setHoroscope( HoroscopeClass *h )
{
    scope->setHoroscope( h );
    dataScope->setHoroscope( h );
    refresh_horoscope();
}


void
LifeCyrcleScopeClass::refresh_horoscope()
{
    scope->refresh_horoscope();
}

