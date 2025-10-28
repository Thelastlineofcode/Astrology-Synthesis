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
#include "transitscope.h"


TransitScopeClass::TransitModeStruct TransitScopeClass::TransitModeList[] =
{
    { TRANSITMODE_MONTH,    QT_TR_NOOP("One Month") },
    { TRANSITMODE_YEAR,     QT_TR_NOOP("One Year") },
    { TRANSITMODE_12YEAR,   QT_TR_NOOP("12 Year") },
    { TRANSITMODE_100YEAR,  QT_TR_NOOP("100 Year") },
    { TRANSITMODE_MAX,      "" }
};


TransitScopeClass::TransitScopeClass(QWidget *parent) : StudioWindowClass(parent)
{
    int     i=0;
    
    UI_TO_WORKSPACE( new Ui::TransitScopeForm () );
    set_user_info("TransitScopeClass");
    
    // add a scope object to the middle of this window
    scope = new ScopeWidgetClass();
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(scope);
    layout->setMargin(0);
    layout->setSpacing(0);
    m_ui->scope_frame->setLayout( layout );
    scope->show();
    scope->setStyle( SCOPE_TRANSITS );
    scope->setHoroscope( NULL, NULL );
    
    // add a dataScope object to the right side of this window
    dataScope = new ScopeWidgetClass();
    QVBoxLayout *layout2 = new QVBoxLayout();
    layout2->addWidget(dataScope);
    layout2->setMargin(0);
    layout2->setSpacing(0);
    m_ui->symbolon_frame->setLayout( layout2 );
    dataScope->show();
    dataScope->setStyle( SCOPE_TRANSIT_INFO );
    dataScope->setHoroscope( NULL, NULL );
    
    scope->set_neighbour( dataScope );
    
    // fill up transitmode combobox
    for (i=0; TransitModeList[i].index!=TRANSITMODE_MAX; i++)
    {
        m_ui->mode_combo->addItem( tr(TransitModeList[i].name) );
    }
    
    // connect signals
    connect( m_ui->mode_combo, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( mode_changed() ) );
    connect( m_ui->year_spinbox, SIGNAL( valueChanged(int) ),
             this, SLOT( year_changed() ) );
    connect( m_ui->month_spinbox, SIGNAL( valueChanged(int) ),
             this, SLOT( month_changed() ) );
    connect( m_ui->text_button, SIGNAL( clicked(void) ),
             this, SLOT( show_text_version() ) );
    connect( m_ui->refresh_button, SIGNAL( clicked(void) ),
             this, SLOT( refresh_scope() ) );
}


TransitScopeClass::~TransitScopeClass()
{
}


void
TransitScopeClass::setHoroscope( HoroscopeClass *h1, HoroscopeClass *h2 )
{
    if (!h1) return;
    
    if (!h2)
    {
        year  = h1->observer.year;
        month = h1->observer.month;
        h2 = new HoroscopeClass();
        h2->set_date( year, month, 1, 0 );
    }
    
    m_ui->year_spinbox->setValue( year );
    m_ui->month_spinbox->setValue( month );
    
    scope->setHoroscope( h1, h2 );
    dataScope->setHoroscope( h1, h2 ); 
    
    refresh_horoscope();
}


void
TransitScopeClass::refresh_horoscope()
{
    scope->refresh_horoscope();
    dataScope->refresh_horoscope();
    scope->repaint();
    dataScope->repaint();
}


void
TransitScopeClass::refresh_scope()
{
    scope->getHoroscope2()->set_date( year, month, 1, 0 );
    refresh_horoscope();
}


void
TransitScopeClass::mode_changed()
{
    TransitModeType     mode = TRANSITMODE_NONE;
    int                 index = 0;
    
    if (scope->getHoroscope() == NULL) return;
    
    index = m_ui->mode_combo->currentIndex();
    if (index>=0 && index<(int)DIM_OF(TransitModeList))
    {
        mode = TransitModeList[ index ].index;
    }
    
    scope->transitMode = mode;
    scope->getHoroscope2()->set_date( year, month, 1, 0 );
}


void
TransitScopeClass::year_changed()
{
    if (scope->getHoroscope() == NULL) return;
    year = m_ui->year_spinbox->value();
    scope->getHoroscope2()->set_date( year, month, 1, 0 );
}


void
TransitScopeClass::month_changed()
{
    if (scope->getHoroscope() == NULL) return;
    month = m_ui->month_spinbox->value();
    scope->getHoroscope2()->set_date( year, month, 1, 0 );
}


void
TransitScopeClass::show_text_version()
{
}

