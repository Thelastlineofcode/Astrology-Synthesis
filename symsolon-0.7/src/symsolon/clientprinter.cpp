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

#include "clientprinter.h"
#include "client.h"
#include "symbolonscope.h"

#include <QPrintDialog>


ClientPrinterClass::ClientPrinterClass(QWidget *parent) : StudioWindowClass(parent)
{
    UI_TO_WORKSPACE( new Ui::ClientPrinterForm() );
    set_user_info("ClientPrinterClass");
    
    connect( m_ui->print_button, SIGNAL( clicked(void) ),
             this, SLOT( print() ) );
    
    printer = new QPrinter();
    scope = new ScopeWidgetClass();
    m_firstPage = true;
}


ClientPrinterClass::~ClientPrinterClass()
{
}


void
ClientPrinterClass::closeEvent( QCloseEvent* )
{
    delete scope;
    delete printer;
}


void
ClientPrinterClass::setHoroscope( HoroscopeClass *h )
{
    m_horoscope = h;
    scope->setHoroscope( h , NULL );
}


void
ClientPrinterClass::set_header_info( QString left, QString right )
{
    scope->set_header_info( left, right );
}


void
ClientPrinterClass::print_one_page( ScopeStyleType scopeStyle )
{
    if ( !m_firstPage )
    {
        printer->newPage();
    }
    
    m_firstPage = false;
    
    scope->setStyle( scopeStyle );
    
    scope->call_paint_handler();
    
}


void
ClientPrinterClass::print()
{
    //ClientClass *client = (ClientClass*)m_creatorWin;
    
    QPrintDialog *dialog = new QPrintDialog( printer, this );
    dialog->setWindowTitle( tr("SymSolon Print") );
    if ( dialog->exec() != QDialog::Accepted ) return;
    
    m_firstPage = true;
    
    scope->print_begin( printer );
    
    if ( m_ui->symbolon_ascsun_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_ASCSUN );
    
    if ( m_ui->symbolon_dialectic_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_DIALECTIC );
    
    if ( m_ui->symbolon_ascinfluence_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_ASC_INFLUENCE );
    
    if ( m_ui->symbolon_suninfluence_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_SUN_INFLUENCE );
    
    if ( m_ui->symbolon_mcinfluence_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_MC_INFLUENCE );
    
    if ( m_ui->symbolon_housemandala_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_HOUSE_MANDAL );
    
    if ( m_ui->symbolon_planetsinhouses_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_PLANET_HOUSE_MANDAL );
    
    if ( m_ui->symbolon_planetsinsigns_check->isChecked() )
        print_one_page( SCOPE_SYMBOLON_PLANET_SIGN_MANDAL );
    
    if ( m_ui->symbolon_planetanalysis_check->isChecked() )
    {
        PlanetIndexType planet;
        int index;
        
        for ( index=0; SymbolonScopeClass::SymbolonPlanetList[index]!=PLANET_NONE; index++)
        {
            planet = SymbolonScopeClass::SymbolonPlanetList[ index ];
            scope->setAnalysedPlanet( planet );
            print_one_page( SCOPE_SYMBOLON_PLANET_ANALYSIS );
        }
    }
    
    if ( m_ui->symbolon_planetaspects_check->isChecked() )
    {
        PlanetIndexType planet;
        int index;
        
        for ( index=0; SymbolonScopeClass::SymbolonPlanetList[index]!=PLANET_NONE; index++)
        {
            planet = SymbolonScopeClass::SymbolonPlanetList[ index ];
            scope->setAnalysedPlanet( planet );
            print_one_page( SCOPE_SYMBOLON_PLANET_ASPECTS );
        }
    }
    
    if ( m_ui->classic_circular_check->isChecked() )
        print_one_page( SCOPE_CIRCLE );
    
    if ( m_ui->classic_rectangular_check->isChecked() )
        print_one_page( SCOPE_RECTANGLE );
    
    if ( m_ui->classic_box_check->isChecked() )
        print_one_page( SCOPE_BOX );
    
    if ( m_ui->classicdata_basic_check->isChecked() )
        print_one_page( SCOPE_BASIC_DATA );
    
    if ( m_ui->classicdata_aspectmatrix_check->isChecked() )
        print_one_page( SCOPE_ASPECTMATRIX );
    
    if ( m_ui->classicdata_qulaitymatrices_check->isChecked() )
    {
        print_one_page( SCOPE_QUALITY_MATRICES );
    }
    
    if ( m_ui->classicdata_planetinfo_check->isChecked() )
    {
        PlanetIndexType planet;
        int index;
        
        for ( index=0; SymbolonScopeClass::SymbolonPlanetList[index]!=PLANET_NONE; index++)
        {
            planet = SymbolonScopeClass::SymbolonPlanetList[ index ];
            scope->setAnalysedPlanet( planet );
            print_one_page( SCOPE_PLANET_INFO );
        }
    }
    
    /*
    SCOPE_SYNASTRY,
    SCOPE_TRANSITS,
    SCOPE_LIFECYRCLE,
    SCOPE_TRANSIT_INFO,
    SCOPE_LIFECYRCLE_INFO,
    SCOPE_SYNASTRY_INFO,
    SCOPE_SYNASTRY_VENUSMARS_INFO,
    SCOPE_SYNASTRY_SUNASC_INFO,
    SCOPE_SYNASTRY_PLUTO_INFO,
    */
    
    scope->print_end();
    
    close();
}

