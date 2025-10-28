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

#include "preferences.h"
#include "prognosis.h"
#include "framepainter.h"
#include "colorselector.h"


PreferencesClass::PreferencesClass() : StudioWindowClass()
{
    int                    i=0, j=0;
    QString                qstr("");
    QTableWidgetItem       *newItem = NULL;
    
    UI_TO_WORKSPACE( new Ui::Preferences() );
    
    // ------------ languages -------------
    for (i=j=0; SolonConfig->LanguageInfoTable[i].name!=NULL; i++)
    {
        m_ui->language_combo->addItem( SolonConfig->LanguageInfoTable[i].name );
        if ( SolonConfig->language.compare( SolonConfig->LanguageInfoTable[i].id)==0 ) j = i;
    }
    m_ui->language_combo->setCurrentIndex( j );
    
    // --- tooltips
    m_ui->tooltip_check->setCheckState(
        SolonConfig->toolTipsEnabled ? Qt::Checked : Qt::Unchecked );
    
    m_ui->detailed_tooltip_check->setCheckState(
        SolonConfig->detailedToolTipsEnabled ? Qt::Checked : Qt::Unchecked );
    
    // --- background color
    FramePainterClass *fpainter = new FramePainterClass();
    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget( fpainter );
    layout->setMargin( 0 );
    layout->setSpacing( 0 );
    m_ui->background_color_frame->setLayout( layout );
    
    connect( fpainter, SIGNAL( paintFrame(QWidget*, QPaintEvent*) ),
                this, SLOT( paint_backgroundcolor_frame( QWidget*, QPaintEvent* ) ) );
    
    connect( m_ui->background_color_button, SIGNAL( clicked() ),
             this, SLOT( popup_bg_color_selector() ) );
    
    // --- foreground color
    FramePainterClass *fpainter2 = new FramePainterClass();
    QVBoxLayout *layout2 = new QVBoxLayout;
    layout2->addWidget( fpainter2 );
    layout2->setMargin( 0 );
    layout2->setSpacing( 0 );
    m_ui->foreground_color_frame->setLayout( layout2 );
    
    connect( fpainter2, SIGNAL( paintFrame(QWidget*, QPaintEvent*) ),
                this, SLOT( paint_foregroundcolor_frame( QWidget*, QPaintEvent* ) ) );
    
    connect( m_ui->foreground_color_button, SIGNAL( clicked() ),
             this, SLOT( popup_fg_color_selector() ) );
    
    // --- printing color
    FramePainterClass *fpainter3 = new FramePainterClass();
    QVBoxLayout *layout3 = new QVBoxLayout;
    layout3->addWidget( fpainter3 );
    layout3->setMargin( 0 );
    layout3->setSpacing( 0 );
    m_ui->printing_color_frame->setLayout( layout3 );
    
    connect( fpainter3, SIGNAL( paintFrame(QWidget*, QPaintEvent*) ),
                this, SLOT( paint_printingcolor_frame( QWidget*, QPaintEvent* ) ) );
    
    connect( m_ui->printing_color_button, SIGNAL( clicked() ),
             this, SLOT( popup_print_color_selector() ) );
    
    // --- printing header text
    m_ui->printing_header_text->setText( SolonConfig->printingHeaderText );
    
    // ------------ ayanamsa -------------
    for (i=j=0; i<AYANAMSA_MAX; i++)
    {
        m_ui->sign_ayanamsa_combo->addItem( SolonConfigClass::AyanamsaInfoTable[i].name );
        if ( strcasecmp( SolonConfigClass::AyanamsaInfoTable[SolonConfig->ayanamsaType].name,
                         SolonConfigClass::AyanamsaInfoTable[i].name) == 0 ) j = i;
    }
    m_ui->sign_ayanamsa_combo->setCurrentIndex( j );
    
    // ------------ planets -------------
    m_ui->planets_table->setColumnCount( 3 );
    m_ui->planets_table->setRowCount( PLANET_MAX-1 );
    m_ui->planets_table->setHorizontalHeaderLabels( QStringList() <<
                            tr("Name") << tr("Orbit") << tr("Enabled") );
    for (i=1; i<PLANET_MAX; i++)
    {
        // name
        newItem = new QTableWidgetItem( QString::fromUtf8(Symbol->planetInfo[i].name) );
        m_ui->planets_table->setItem(i-1, 0, newItem);
        // orbit
        newItem = new QTableWidgetItem( QString::number( Symbol->planetInfo[i].orbit ) );
        m_ui->planets_table->setItem(i-1, 1, newItem);
        // enabled
        newItem = new QTableWidgetItem();
        newItem->setFlags( Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsUserCheckable );
        newItem->setCheckState( Symbol->planetInfo[i].enabled ? Qt::Checked : Qt::Unchecked );
        m_ui->planets_table->setItem(i-1, 2, newItem);
    }
    m_ui->planets_table->resizeColumnsToContents();
    
    // --- topocentric
    m_ui->planet_topocentic_check->setCheckState(
        SolonConfig->topocentricCalculationUsed ? Qt::Checked : Qt::Unchecked );
    
    // ------------ houses --------------
    m_ui->houses_table->setColumnCount( 1 );
    m_ui->houses_table->setRowCount( HOUSE_MAX-1 );
    m_ui->houses_table->setHorizontalHeaderLabels( QStringList() << tr("Name") );
    for (i=1; i<HOUSE_MAX; i++)
    {    
        // name
        newItem = new QTableWidgetItem( QString::fromUtf8(Symbol->houseInfo[i].name) );
        m_ui->houses_table->setItem(i-1, 0, newItem);
    }
    m_ui->houses_table->resizeColumnsToContents();
    
    // --- house-systems
    for (i=j=1; i<HOUSESYSTEM_MAX; i++)
    {
        m_ui->house_system_combo->addItem( SolonConfigClass::HouseSystemInfoTable[i].name );
        if ( strcasecmp( SolonConfigClass::HouseSystemInfoTable[SolonConfig->houseSystem].name,
                         SolonConfigClass::HouseSystemInfoTable[i].name ) == 0 ) j = i-1;
    }
    m_ui->house_system_combo->setCurrentIndex( j );
    
    // ------------ aspects -------------
    m_ui->aspects_table->setColumnCount( 8 );
    m_ui->aspects_table->setRowCount( ASPECT_MAX-1 );
    m_ui->aspects_table->setHorizontalHeaderLabels( QStringList() <<
                            tr("Name") << tr("Abbrev.") << tr("Angle") <<
                            tr("Orbit") << tr("Harmony") <<
                            tr("PlanetEnergy") << tr("Color") <<
                            tr("Enabled") );
    for (i=1; i<ASPECT_MAX; i++)
    {
        // name
        newItem = new QTableWidgetItem( QString::fromUtf8(Symbol->aspectInfo[i].name) );
        m_ui->aspects_table->setItem(i-1, 0, newItem);
        // abbrev.
        newItem = new QTableWidgetItem( Symbol->aspectInfo[i].abbreviation );
        m_ui->aspects_table->setItem(i-1, 1, newItem);
        // angle
        newItem = new QTableWidgetItem( QString::number( Symbol->aspectInfo[i].angle ) );
        m_ui->aspects_table->setItem(i-1, 2, newItem);
        // orbit
        newItem = new QTableWidgetItem( QString::number( Symbol->aspectInfo[i].orbit ) );
        m_ui->aspects_table->setItem(i-1, 3, newItem);
        // harmony
        newItem = new QTableWidgetItem( QString::number( Symbol->aspectInfo[i].harmony ) );
        m_ui->aspects_table->setItem(i-1, 4, newItem);
        // planetEnergy
        newItem = new QTableWidgetItem( QString::fromUtf8( Symbol->planetInfo[ Symbol->aspectInfo[i].planetEnergy ].name ) );
        m_ui->aspects_table->setItem(i-1, 5, newItem);
        // color
        newItem = new QTableWidgetItem(
            QString::number( Symbol->aspectInfo[i].color, 16 ).rightJustified(6, '0') );    
        m_ui->aspects_table->setItem(i-1, 6, newItem);
        // enabled
        newItem = new QTableWidgetItem();
        newItem->setFlags( Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsUserCheckable );
        newItem->setCheckState( Symbol->aspectInfo[i].enabled ? Qt::Checked : Qt::Unchecked );
        m_ui->aspects_table->setItem(i-1, 7, newItem);
    }
    m_ui->aspects_table->resizeColumnsToContents();
    
    // --- tooltips
    m_ui->aspect_orbit_as_limit_check->setCheckState(
        SolonConfig->aspectOrbitAsLimit ? Qt::Checked : Qt::Unchecked );
    
    // ----------- symbolon -------------
    m_ui->symbolon_table->setColumnCount( 1 );
    m_ui->symbolon_table->setRowCount( SYMBOLON_MAX-1 );
    m_ui->symbolon_table->setHorizontalHeaderLabels( QStringList() << tr("Name") );
    for (i=1; i<SYMBOLON_MAX; i++)
    {
        // name
        newItem = new QTableWidgetItem( Symbol->get_name_of_symbolon(i) );
        m_ui->symbolon_table->setItem(i-1, 0, newItem);
    }
    m_ui->symbolon_table->resizeColumnsToContents();
    
    // --- top-text & bottom-text
    m_ui->symbolon_top_label_check->setCheckState(
        SolonConfig->cardTopTextEnabled ? Qt::Checked : Qt::Unchecked );
    m_ui->symbolon_bottom_label_check->setCheckState(
        SolonConfig->cardBottomTextEnabled ? Qt::Checked : Qt::Unchecked );
    
    // ---------- life events -----------    
    m_ui->life_events_table->setColumnCount( 4 );
    m_ui->life_events_table->setHorizontalHeaderLabels( QStringList()
                << tr("Event") << tr("Start") << tr("End") << tr("Affector") );
    for (i=0; PrognosisClass::defaultLifeEvents[i].name.size()>0; i++)
    {
        // name
        newItem = new QTableWidgetItem( PrognosisClass::defaultLifeEvents[i].name );
        m_ui->life_events_table->setItem(i-1, 0, newItem);
    }
    m_ui->life_events_table->resizeColumnsToContents();
    
    // ---------- transits -----------
    // planet dropdown menu
    for (i=1; i<PLANET_MAX; i++)
    {
        // planet name
        m_ui->transit_planet_combo->addItem( QString::fromUtf8(Symbol->planetInfo[i].name) );
    }
    // planets of month transit
    for (qstr="",i=0; i<PLANET_MAX; i++)
    {
        if ( !SolonConfig->transitPlanets[TRANSITMODE_MONTH][i] ) continue;
        qstr += QString::fromUtf8( Symbol->planetInfo[i].name ) + ", ";
    }
    m_ui->transit_month_line->setText(qstr);
    // planets of year transit
    for (qstr="",i=0; i<PLANET_MAX; i++)
    {
        if ( !SolonConfig->transitPlanets[TRANSITMODE_YEAR][i] ) continue;
        qstr += QString::fromUtf8( Symbol->planetInfo[i].name ) + ", ";
    }
    m_ui->transit_year_line->setText(qstr);
    // planets of 12 years transit
    for (qstr="",i=0; i<PLANET_MAX; i++)
    {
        if ( !SolonConfig->transitPlanets[TRANSITMODE_12YEAR][i] ) continue;
        qstr += QString::fromUtf8( Symbol->planetInfo[i].name ) + ", ";
    }
    m_ui->transit_12year_line->setText(qstr);
    // planets of 100 years transit
    for (qstr="",i=0; i<PLANET_MAX; i++)
    {
        if ( !SolonConfig->transitPlanets[TRANSITMODE_100YEAR][i] ) continue;
        qstr += QString::fromUtf8( Symbol->planetInfo[i].name ) + ", ";
    }
    m_ui->transit_100year_line->setText(qstr);
    // button signals
    connect( m_ui->transit_month_planet_button, SIGNAL( clicked(void) ),
             this, SLOT( add_to_transit_month_line() ) );
    connect( m_ui->transit_year_planet_button, SIGNAL( clicked(void) ),
             this, SLOT( add_to_transit_year_line() ) );
    connect( m_ui->transit_12year_planet_button, SIGNAL( clicked(void) ),
             this, SLOT( add_to_transit_12year_line() ) );
    connect( m_ui->transit_100year_planet_button, SIGNAL( clicked(void) ),
             this, SLOT( add_to_transit_100year_line() ) );
    
    // --- connect signals ---
    connect( m_ui->apply_button, SIGNAL( clicked(void) ),
             this, SLOT( apply_settings() ) );
    connect( m_ui->save_button, SIGNAL( clicked(void) ),
             this, SLOT( save_settings() ) );
}


void
PreferencesClass::closeEvent( QCloseEvent *event )
{
    StudioWindowClass::closeEvent( event );
    SymSolon->close_preferences();
}


PreferencesClass::~PreferencesClass()
{
}


void
PreferencesClass::apply_settings()
{
    int                     i=0, j=0, k=0, index=0;
    QString                 str="";
    double                  dnum=0;
    Qt::CheckState          state=Qt::Unchecked;
    bool                    ok=false;
    QString                 oldLanguage = SolonConfig->language;
    QStringList             strl;
    
    // get basic settings
    SolonConfig->language =
        SolonConfig->LanguageInfoTable[ m_ui->language_combo->currentIndex() ].id;
        
    SolonConfig->houseSystem =
        m_ui->house_system_combo->currentIndex() + 1;

    SolonConfig->ayanamsaType =
        m_ui->sign_ayanamsa_combo->currentIndex();
        
    SolonConfig->topocentricCalculationUsed =
        (m_ui->planet_topocentic_check->checkState() == Qt::Checked);
        
    SolonConfig->toolTipsEnabled =
        (m_ui->tooltip_check->checkState() == Qt::Checked);
    
    SolonConfig->detailedToolTipsEnabled =
        (m_ui->detailed_tooltip_check->checkState() == Qt::Checked);
    
    SolonConfig->cardTopTextEnabled =
        (m_ui->symbolon_top_label_check->checkState() == Qt::Checked);
        
    SolonConfig->cardBottomTextEnabled =
        (m_ui->symbolon_bottom_label_check->checkState() == Qt::Checked);
    
    SolonConfig->printingHeaderText = m_ui->printing_header_text->toPlainText();
    
    // read settings from tables
    
    // --- Planets ---
    for (i=0; i<m_ui->planets_table->rowCount(); i++)
    {
        index = i+1;
        // Name
        str = m_ui->planets_table->item( i, 0 )->text();
        strcpy( Symbol->planetInfo[index].name, str.toUtf8().constData() );
        // Orbit
        dnum = m_ui->planets_table->item( i, 1 )->text().toDouble();
        Symbol->planetInfo[index].orbit = dnum;
        // Enabled
        state = m_ui->planets_table->item( i, 2 )->checkState();
        if (state == Qt::Checked) Symbol->planetInfo[index].enabled = true;
        else Symbol->planetInfo[index].enabled = false;
    }
    
    // --- Houses ---
    for (i=0; i<m_ui->houses_table->rowCount(); i++)
    {
        index = i+1;
        // Name
        str = m_ui->houses_table->item( i, 0 )->text();
        strcpy( Symbol->houseInfo[index].name, str.toUtf8().constData() );
    }
    
    // --- Aspects ---
    for (i=0; i<m_ui->aspects_table->rowCount(); i++)
    {
        index = i+1;
        // Name
        str = m_ui->aspects_table->item( i, 0 )->text();
        strcpy( Symbol->aspectInfo[index].name, str.toUtf8().constData() );
        // Abbrev.
        str = m_ui->aspects_table->item( i, 1 )->text();
        strcpy( Symbol->aspectInfo[index].abbreviation, str.toUtf8().constData() );
        // Angle
        str = m_ui->aspects_table->item( i, 2 )->text();
        Symbol->aspectInfo[index].angle = str.toDouble();
        // Orbit
        str = m_ui->aspects_table->item( i, 3 )->text();
        Symbol->aspectInfo[index].orbit = str.toDouble();
        // Harmony
        str = m_ui->aspects_table->item( i, 4 )->text();
        Symbol->aspectInfo[index].harmony = str.toDouble();
        // PlanetEnergy
        Symbol->aspectInfo[index].planetEnergy = PLANET_NONE;
        str = m_ui->aspects_table->item( i, 5 )->text();
        for ( j=0; j<PLANET_MAX; j++ )
        {
            if (str == QString::fromUtf8(Symbol->planetInfo[j].name))
            {
                Symbol->aspectInfo[index].planetEnergy = j;
                break;
            }
        }
        // Color
        str = m_ui->aspects_table->item( i, 6 )->text();
        Symbol->aspectInfo[index].color = str.toLong( &ok, 16 );
        // Enabled
        state = m_ui->aspects_table->item( i, 7 )->checkState();
        if (state == Qt::Checked) Symbol->aspectInfo[index].enabled = true;
        else Symbol->aspectInfo[index].enabled = false;
    }
    
    SolonConfig->aspectOrbitAsLimit =
        (m_ui->aspect_orbit_as_limit_check->checkState() == Qt::Checked);
    
    // --- Transits ---
    int transitMode = TRANSITMODE_NONE;
    for (k=0; k<4; k++)
    {
        switch (k)
        {
            default:
            case 0:
                str = m_ui->transit_month_line->text();
                transitMode = TRANSITMODE_MONTH;
                break;
            case 1:
                str = m_ui->transit_year_line->text();
                transitMode = TRANSITMODE_YEAR;
                break;
            case 2:
                str = m_ui->transit_12year_line->text();
                transitMode = TRANSITMODE_12YEAR;
                break;
            case 3:
                str = m_ui->transit_100year_line->text();
                transitMode = TRANSITMODE_100YEAR;
                break;
        }
        strl = str.split( ",", QString::SkipEmptyParts );
        for (i=0; i<strl.size(); i++) strl.replace( i, strl.at(i).trimmed() );
        for (i=0; i<PLANET_MAX; i++) SolonConfig->transitPlanets[transitMode][i] = false;
        for (i=0; i<strl.size(); i++)
            for (j=0; j<PLANET_MAX; j++)
                if ( strl.at(i) == QString::fromUtf8(Symbol->planetInfo[j].name) )
                    SolonConfig->transitPlanets[transitMode][j] = true;
    }
    
    // --- Symbolons ---
    for (i=0; i<m_ui->symbolon_table->rowCount(); i++)
    {
        index = i+1;
        // Name
        str = m_ui->symbolon_table->item( i, 0 )->text();
        strcpy( Symbol->symbolonInfo[index].name, str.toUtf8().constData() );
    }
    
    // repaint windows
    if ( SolonConfig->language != oldLanguage ) set_translation();
    SymSolon->repaint_all_windows();
}


void
PreferencesClass::save_settings()
{
    apply_settings();
    if (SolonConfig->save())
    {
        QMessageBox::information(NULL, "SymSolon", tr("Configuration saved.\n") );
    }
}


void
PreferencesClass::load_settings()
{
    SolonConfig->open();
}


void
PreferencesClass::add_to_transit_month_line()
{
    QString str = m_ui->transit_month_line->text();
    str += ", " + m_ui->transit_planet_combo->currentText();
    m_ui->transit_month_line->setText(str);
}


void
PreferencesClass::add_to_transit_year_line()
{
    QString str = m_ui->transit_year_line->text();
    str += ", " + m_ui->transit_planet_combo->currentText();
    m_ui->transit_year_line->setText(str);
}


void
PreferencesClass::add_to_transit_12year_line()
{
    QString str = m_ui->transit_12year_line->text();
    str += ", " + m_ui->transit_planet_combo->currentText();
    m_ui->transit_12year_line->setText(str);
}


void
PreferencesClass::add_to_transit_100year_line()
{
    QString str = m_ui->transit_100year_line->text();
    str += ", " + m_ui->transit_planet_combo->currentText();
    m_ui->transit_100year_line->setText(str);
}

void
PreferencesClass::paint_backgroundcolor_frame( QWidget *widget, QPaintEvent* )
{
    if ( !widget ) return;
    
    QPainter p( widget );
    QColor *color = new QColor( SolonConfig->backgroundColor );
    
    p.setBrush( Qt::SolidPattern );
    p.setPen( *color );
    p.fillRect( 0, 0, widget->width(), widget->height(), *color );
}


void
PreferencesClass::paint_foregroundcolor_frame( QWidget *widget, QPaintEvent* )
{
    if ( !widget ) return;
    
    QPainter p( widget );
    QColor *color = new QColor( SolonConfig->foregroundColor );
    
    p.setBrush( Qt::SolidPattern );
    p.setPen( *color );
    p.fillRect( 0, 0, widget->width(), widget->height(), *color );
}


void
PreferencesClass::paint_printingcolor_frame( QWidget *widget, QPaintEvent* )
{
    if ( !widget ) return;
    
    QPainter p( widget );
    QColor *color = new QColor( SolonConfig->printingColor );
    
    p.setBrush( Qt::SolidPattern );
    p.setPen( *color );
    p.fillRect( 0, 0, widget->width(), widget->height(), *color );
}


void
PreferencesClass::popup_bg_color_selector()
{
    ColorSelectorClass *colorSelector = new ColorSelectorClass();
    colorSelector->m_widget = m_ui->background_color_frame;
    colorSelector->m_color = &SolonConfig->backgroundColor;
    colorSelector->show();
}


void
PreferencesClass::popup_fg_color_selector()
{
    ColorSelectorClass *colorSelector = new ColorSelectorClass();
    colorSelector->m_widget = m_ui->foreground_color_frame;
    colorSelector->m_color = &SolonConfig->foregroundColor;
    colorSelector->show();
}


void
PreferencesClass::popup_print_color_selector()
{
    ColorSelectorClass *colorSelector = new ColorSelectorClass();
    colorSelector->m_widget = m_ui->printing_color_frame;
    colorSelector->m_color = &SolonConfig->printingColor;
    colorSelector->show();
}

