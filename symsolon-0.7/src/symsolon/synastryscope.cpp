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
#include "synastryscope.h"

SynastryScopeClass::SynastryDataType SynastryScopeClass::SynastryDataList[] =
{
    { SCOPE_ASPECTMATRIX,               QT_TR_NOOP("Aspect matrix") },
    { SCOPE_SYNASTRY_VENUSMARS_INFO,    QT_TR_NOOP("Venus-Mars") },
    { SCOPE_SYNASTRY_SUNASC_INFO,       QT_TR_NOOP("Sun/Asc") },
    { SCOPE_SYNASTRY_PLUTO_INFO,        QT_TR_NOOP("Pluto") },
    { SCOPE_SYNASTRY_INFO,              QT_TR_NOOP("Summary") },
    { SCOPE_NONE,                       "" }
};


SynastryScopeClass::SynastryScopeClass(QWidget *parent) : StudioWindowClass(parent)
{
    UI_TO_WORKSPACE( new Ui::SynastryScopeForm () );
    set_user_info("SynastryScopeClass");
    
    // fillup data list
    for (int i=0; SynastryDataList[i].index!=SCOPE_NONE; i++)
    {
        m_ui->data_combo->addItem( tr( SynastryDataList[i].name.toUtf8().constData() ) );
    }
    
    // add a scope object to the middle of this window
    scope = new ScopeWidgetClass();
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(scope);
    layout->setMargin(0);
    layout->setSpacing(0);
    m_ui->scope_frame->setLayout( layout );
    scope->show();
    
    // add a scope object to the middle of this window
    dataScope = new ScopeWidgetClass();
    QVBoxLayout *layout2 = new QVBoxLayout();
    layout2->addWidget(dataScope);
    layout2->setMargin(0);
    layout2->setSpacing(0);
    m_ui->data_scope_frame->setLayout( layout2 );
    dataScope->show();
    
    // connect signals
    connect( m_ui->data_combo, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( method_or_data_changed() ) );
    
    method_or_data_changed();
}


SynastryScopeClass::~SynastryScopeClass()
{
}


void
SynastryScopeClass::setHoroscope( HoroscopeClass *h1, HoroscopeClass *h2 )
{
    scope->setHoroscope( h1, h2 );
    dataScope->setHoroscope( h1, h2 );
    refresh_horoscope();
    method_or_data_changed();
}


void
SynastryScopeClass::refresh_horoscope()
{
    scope->refresh_horoscope();
    dataScope->refresh_horoscope();
}


void
SynastryScopeClass::method_or_data_changed()
{
    ScopeStyleType         style = SCOPE_NONE;
    int                    index = 0;
    
    // method
    scope->setStyle( SCOPE_SYNASTRY );
    
    // get and set the data-method style
    index = m_ui->data_combo->currentIndex();
    if (index>=0 && index<(int)DIM_OF(SynastryDataList))
    {
        style = SynastryDataList[ index ].index;
    }
    dataScope->setStyle( style );
    
    scope->repaint();
    dataScope->repaint();
}


