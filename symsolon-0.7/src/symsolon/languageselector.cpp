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
#include "languageselector.h"

LanguageSelectorClass::LanguageSelectorClass()
{
    int i=0, j=0;
    
    m_ui = new Ui::language_selector();
    m_ui->setupUi( this );
    
    // ------------ languages -------------
    for (i=j=0; SolonConfig->LanguageInfoTable[i].name!=NULL; i++)
    {
        m_ui->language_combo->addItem( SolonConfig->LanguageInfoTable[i].name );
        if ( SolonConfig->language.compare( SolonConfig->LanguageInfoTable[i].id)==0 ) j = i;
    }
    m_ui->language_combo->setCurrentIndex( j );
    
    // connect signals
    connect( m_ui->next_button, SIGNAL( clicked(void) ),
             this, SLOT( next() ) );
}


LanguageSelectorClass::~LanguageSelectorClass()
{
}


void
LanguageSelectorClass::next()
{
    SolonConfig->language =
        SolonConfig->LanguageInfoTable[ m_ui->language_combo->currentIndex() ].id;
    close();
}

