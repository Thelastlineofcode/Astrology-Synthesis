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
#include "classicscope.h"
#include "client.h"

ClassicScopeClass::ClassicStyleListStruct ClassicScopeClass::ClassicStyleList[] =
{
    { SCOPE_CIRCLE,             QT_TR_NOOP("Classic Circle") },
    { SCOPE_RECTANGLE,          QT_TR_NOOP("Rectangle Style") },
    { SCOPE_BOX,                QT_TR_NOOP("Boxes") },
    { SCOPE_MAX,                "" }
};


ClassicScopeClass::DataStyleListStruct ClassicScopeClass::DataStyleList[] =
{
    { SCOPE_BASIC_DATA,         QT_TR_NOOP("Basic Datas") },
    { SCOPE_ASPECTMATRIX,       QT_TR_NOOP("Aspect Matrix") },
    { SCOPE_QUALITY_MATRICES,   QT_TR_NOOP("Quality Matrices") },
    { SCOPE_PLANET_INFO,        QT_TR_NOOP("Planet Info") },
    { SCOPE_MAX,                "" }
};


ClassicScopeClass::TimeStepStruct ClassicScopeClass::TimeStepList[] =
{
    { TIMESTEP_YEAR,            QT_TR_NOOP("Year") },
    { TIMESTEP_MONTH,           QT_TR_NOOP("Month") },
    { TIMESTEP_WEEK,            QT_TR_NOOP("Week") },
    { TIMESTEP_DAY,             QT_TR_NOOP("Day") },
    { TIMESTEP_HOUR,            QT_TR_NOOP("hour") },
    { TIMESTEP_MINUTE,          QT_TR_NOOP("minute") },
    { TIMESTEP_SECOND,          QT_TR_NOOP("second") },
    { TIMESTEP_MAX,             "" }
};


ClassicScopeClass::ClassicScopeClass(QWidget *parent) : StudioWindowClass(parent)
{
    int        i=0;
    
    UI_TO_WORKSPACE( new Ui::ClassicScope() );
    
    set_user_info("ClassicScopeClass");
    
    // fillup style list
    for (i=0; ClassicStyleList[i].index!=SCOPE_MAX; i++)
    {
        m_ui->style_combo->addItem( tr(ClassicStyleList[i].name) );
    }
    
    // fillup data style list
    for (i=0; DataStyleList[i].index!=SCOPE_MAX; i++)
    {
        m_ui->data_combo->addItem( tr(DataStyleList[i].name) );
    }
    
    // fillup time-step list
    for (i=0; TimeStepList[i].index!=TIMESTEP_MAX; i++)
    {
        m_ui->time_combo->addItem( tr(TimeStepList[i].name) );
    }
    
    // connect signals
    connect( m_ui->style_combo, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( style_changed() ) );
    connect( m_ui->data_combo, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( data_style_changed() ) );
    connect( m_ui->decrease_button, SIGNAL( clicked() ),
             this, SLOT( time_decrease() ) );
    connect( m_ui->increase_button, SIGNAL( clicked() ),
             this, SLOT( time_increase() ) );
    
    // add a scope object to the middle of this window
    scope = new ScopeWidgetClass();
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(scope);
    layout->setMargin(0);
    layout->setSpacing(0);
    m_ui->scope_frame->setLayout( layout );
    scope->show();
    
    // add a second scope object to the data place
    dataScope = new ScopeWidgetClass();
    QVBoxLayout *layout2 = new QVBoxLayout();
    layout2->addWidget(dataScope);
    layout2->setMargin(0);
    layout2->setSpacing(0);
    m_ui->data_frame->setLayout( layout2 );
    dataScope->show();
    
    scope->set_neighbour( dataScope );
    
    // set default method and planet
    style_changed();
    data_style_changed();
}


ClassicScopeClass::~ClassicScopeClass()
{
}


void
ClassicScopeClass::setHoroscope( HoroscopeClass *h )
{
    scope->setHoroscope( h );
    dataScope->setHoroscope( h );
    style_changed();
    data_style_changed();
    set_title();
}


void
ClassicScopeClass::refresh_horoscope()
{
    scope->refresh_horoscope();
}


void
ClassicScopeClass::setStyle( ScopeStyleType s )
{
    int i=0;
    
    scope->setStyle( s );
    
    for (i=0; i<(int)DIM_OF(ClassicStyleList); i++)
        if ( ClassicStyleList[ i ].index == s )
        {
            m_ui->style_combo->setCurrentIndex( i );
            break;
        }
    
    style_changed();
}


void
ClassicScopeClass::setDataStyle( ScopeStyleType s )
{
    int i=0;
    
    dataScope->setStyle( s );
    
    for (i=0; i<(int)DIM_OF(DataStyleList); i++)
        if ( DataStyleList[ i ].index == s )
        {
            m_ui->data_combo->setCurrentIndex( i );
            break;
        }
    
    data_style_changed();
}


void
ClassicScopeClass::style_changed()
{
    ScopeStyleType        style = SCOPE_NONE;
    int                    index;
    
    // get and set the method style
    index = m_ui->style_combo->currentIndex();
    if (index>=0 && index<(int)DIM_OF(ClassicStyleList))
    {
        style = ClassicStyleList[ index ].index;
    }
    scope->setStyle( style );
    scope->repaint();
}


void
ClassicScopeClass::data_style_changed()
{
    ScopeStyleType        dstyle = SCOPE_NONE;
    int                    index;
    
    // get and set the analysed planet
    index = m_ui->data_combo->currentIndex();
    if (index>=0 && index<(int)DIM_OF(DataStyleList))
    {
        dstyle = DataStyleList[ index ].index;
    }
    dataScope->setStyle( dstyle );
    dataScope->repaint();
}


void
ClassicScopeClass::time_increase()
{
    time_shift(1);
}


void
ClassicScopeClass::time_decrease()
{
    time_shift(-1);
}


void
ClassicScopeClass::time_shift( int direction )
{
    TimeStepType tstep = TIMESTEP_NONE;
    
    int index = m_ui->time_combo->currentIndex();
    
    if (index>=0 && index<(int)DIM_OF(TimeStepList))
        tstep = TimeStepList[ index ].index;

/*    
qDebug("tstep=%d, value=%d", tstep, direction);
qDebug("BEFORE:%04i-%02i-%02i %f",
		scope->horoscope->observer.year,
		scope->horoscope->observer.month,
		scope->horoscope->observer.day,
		scope->horoscope->observer.UT
		);
*/
    scope->horoscope->shift_date( tstep, direction );
/*
qDebug("AFTER:%04i-%02i-%02i %f",
		scope->horoscope->observer.year,
		scope->horoscope->observer.month,
		scope->horoscope->observer.day,
		scope->horoscope->observer.UT
		);
*/
    set_title();
    scope->repaint();
    dataScope->repaint();
}


void
ClassicScopeClass::set_title()
{
    StudioWindowClass *swin = (ClientClass*)m_creatorWin;
    if (swin && swin->userInfo == "ClientClass")
    {
        ClientClass *client = (ClientClass*)swin;
        setWindowTitle( "H:" + client->get_name() + " @ " + get_time() );
    }
}


QString
ClassicScopeClass::get_time()
{
    char    str[256] = "";
    scope->horoscope->get_date( str );
    return QString( str );
}

