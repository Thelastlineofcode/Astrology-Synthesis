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
#include "symbolonscope.h"

#include <QtGui/QVBoxLayout>


SymbolonScopeClass::SymbolonMethodType SymbolonScopeClass::SymbolonMethodList[] =
    {
        { SCOPE_SYMBOLON_ASCSUN,                QT_TR_NOOP("Ascendant + SunSign") },
        { SCOPE_SYMBOLON_DIALECTIC,             QT_TR_NOOP("Horoscope's Dialectic") },
        { SCOPE_SYMBOLON_ASC_INFLUENCE,         QT_TR_NOOP("Ascendant Influence") },
        { SCOPE_SYMBOLON_SUN_INFLUENCE,         QT_TR_NOOP("Sun Influence") },
        { SCOPE_SYMBOLON_MC_INFLUENCE,          QT_TR_NOOP("MC Influence") },
        { SCOPE_SYMBOLON_HOUSE_MANDAL,          QT_TR_NOOP("House mandala") },
        { SCOPE_SYMBOLON_PLANET_HOUSE_MANDAL,   QT_TR_NOOP("Planets in houses (destiny)") },
        { SCOPE_SYMBOLON_PLANET_SIGN_MANDAL,    QT_TR_NOOP("Planets in signs (personality)") },
        { SCOPE_SYMBOLON_PLANET_ANALYSIS,       QT_TR_NOOP("Planet Analysis") },
        { SCOPE_SYMBOLON_PLANET_ASPECTS,        QT_TR_NOOP("Planet Aspects") },
        { SCOPE_NONE,                            "" }
    };


PlanetIndexType SymbolonScopeClass::SymbolonPlanetList[] =
    {
        PLANET_MOON,
        PLANET_SUN,
        PLANET_MERCURY,
        PLANET_VENUS,
        PLANET_MARS,
        PLANET_JUPITER,
        PLANET_SATURN,
        PLANET_URANUS,
        PLANET_NEPTUNE,
        PLANET_PLUTO,
        PLANET_NONE
    };


SymbolonScopeClass::SymbolonScopeClass(QWidget *parent) : StudioWindowClass(parent)
{
    int        i=0;
    
    UI_TO_WORKSPACE( new Ui::SymbolonScope () );
    set_user_info("SymbolonScopeClass");
    
    // fillup method list
    for (i=0; SymbolonMethodList[i].index!=SCOPE_NONE; i++)
    {
        m_ui->method_combo->addItem( tr( SymbolonMethodList[i].name.toUtf8().constData() ) );
    }
    
    // fillup planet list
    for (i=0; SymbolonPlanetList[i]!=PLANET_NONE; i++)
    {
        m_ui->planet_combo->addItem( QString::fromUtf8( Symbol->planetInfo[ SymbolonPlanetList[i] ].name ) );
    }
    
    // connect signals
    connect( m_ui->method_combo, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( method_or_planet_changed() ) );
    connect( m_ui->planet_combo, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( method_or_planet_changed() ) );
    
    // add a scope object to the middle of this window
    scope = new ScopeWidgetClass();
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(scope);
    layout->setMargin(0);
    layout->setSpacing(0);
    m_ui->frame->setLayout( layout );
    scope->show();
    
    connect( scope, SIGNAL( on_object_clicked( InfoType, int ) ),
             SymSolon, SLOT( explorer( InfoType, int ) ) );
    
    // set default method and planet
    method_or_planet_changed();
}


SymbolonScopeClass::~SymbolonScopeClass()
{
}


void
SymbolonScopeClass::setHoroscope( HoroscopeClass *h )
{
    scope->setHoroscope( h );
    method_or_planet_changed();
}


void
SymbolonScopeClass::refresh_horoscope()
{
    scope->refresh_horoscope();
}


void
SymbolonScopeClass::setMethod( ScopeStyleType m )
{
    int i=0;
    
    scope->setStyle( m );
    
    for (i=0; i<(int)DIM_OF(SymbolonMethodList); i++)
        if ( SymbolonMethodList[ i ].index == m )
        {
            m_ui->method_combo->setCurrentIndex( i );
            break;
        }
    
    method_or_planet_changed();
}


void
SymbolonScopeClass::method_or_planet_changed()
{
    ScopeStyleType        style = SCOPE_NONE;
    PlanetIndexType        planet = PLANET_NONE;
    int                    index = 0;
    
    // get and set the method style
    index = m_ui->method_combo->currentIndex();
    if (index>=0 && index<(int)DIM_OF(SymbolonMethodList))
    {
        style = SymbolonMethodList[ index ].index;
    }
    scope->setStyle( style );
    
    // get and set the analysed planet
    index = m_ui->planet_combo->currentIndex();
    if (index>=0 && index<(int)DIM_OF(SymbolonPlanetList))
    {
        planet = SymbolonPlanetList[ index ];
    }
    scope->setAnalysedPlanet( planet );
    
    switch ( style )
    {
        default:
            m_ui->planet_combo->setDisabled( true );
            break;
        
        case SCOPE_SYMBOLON_PLANET_ANALYSIS:
        case SCOPE_SYMBOLON_PLANET_ASPECTS:      
            m_ui->planet_combo->setEnabled( true );
            break;
    }
    
    scope->repaint();
}

