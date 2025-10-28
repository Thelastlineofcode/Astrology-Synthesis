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
#include "scopewidget.h"
#include "solontables.h"
#include "colorselector.h"

#include <QtGui/QHelpEvent>
#include <QtGui/QToolTip>
#include <QtGui/QWheelEvent>


ScopeWidgetClass::ScopeWidgetClass(QWidget *parent) : QWidget(parent)
{
    setParent( SymSolon->workspace );
    SymSolon->workspace->addWindow( this );
    hide();
    
    m_bgColor = SolonConfig->backgroundColor;
    setPalette( QPalette(m_bgColor) );
    setAutoFillBackground(true);
    
    m_fgColor = SolonConfig->foregroundColor;
    whitePen.setColor( QColor(m_fgColor) );
    
    quint32 darkColor = ColorSelectorClass::lightness( m_fgColor, 0.1875 );
    darkPen.setColor( QColor( darkColor ) );  
    
    quint32 houseColor = ColorSelectorClass::lightness( m_fgColor, 0.3 );
    housePen.setColor( QColor( houseColor ) );
    housePen.setWidth( 1 );
    housePen.setStyle( Qt::DashLine );
    
    multiColor.setRgb( 0, 0, 0 );
    
    style = SCOPE_NONE;
    analysedPlanet   = PLANET_NONE;
    analysedSymbolon = 0;
    
    // fonts
    bigFont.setStyleHint( QFont::SansSerif );
    bigFont.setBold(true);
    normalFont.setStyleHint( QFont::SansSerif );
    normalFont.setBold(true);
    smallFont.setStyleHint( QFont::SansSerif );
    smallFont.setBold(false);
    dataFont.setStyleHint( QFont::SansSerif );
    dataFont.setBold(false);
    printingFont.setStyleHint( QFont::SansSerif );
    printingFont.setBold(false);
    
    bigMetrics = NULL;
    normalMetrics = NULL;
    smallMetrics = NULL;
    dataMetrics = NULL;
    printingMetrics = NULL;
    horoscope = NULL;
    
    // scale & translate
    scaleXY = 1;
    translateX = 0;
    translateY = 0;
    
    // horoscopes
    horoscope = NULL;
    horoscope2 = NULL;
    transitMode = TRANSITMODE_MONTH;
    neighbourWidget = NULL;
    
    // printing
    m_printer = NULL;
    
    // cursor
    cursorOverInfoType = INFOTYPE_NONE;
    cursorOverIndex = 0;
    cursorSelectedInfoType = INFOTYPE_NONE;
    cursorSelectedIndex = 0;
    refToolTipList = &toolTipList;
}


ScopeWidgetClass::~ScopeWidgetClass()
{
}


void
ScopeWidgetClass::setHoroscope( HoroscopeClass *h1, HoroscopeClass *h2 )
{
    horoscope  = h1;
    horoscope2 = h2;
}


HoroscopeClass*
ScopeWidgetClass::getHoroscope()
{
    return horoscope;
}


HoroscopeClass*
ScopeWidgetClass::getHoroscope2()
{
    return horoscope2;
}


void
ScopeWidgetClass::print_begin( QPrinter *printer )
{
    m_printer = printer;
    p.begin( m_printer );
    Symbol->set_label_color( SolonConfig->printingColor );
}


void
ScopeWidgetClass::print_end()
{
    m_printer = NULL;
    p.end();
    Symbol->set_label_color( SolonConfig->foregroundColor );
}


void
ScopeWidgetClass::call_paint_handler()
{
    paintEvent( NULL );
}


void
ScopeWidgetClass::set_header_info( QString left, QString right )
{
    m_printigLeftHeaderText = left;
    m_printigRightHeaderText = right;
}


void
ScopeWidgetClass::refresh_horoscope()
{
    double      ayanamsa = 0;
    
    for (int i=0; SolonConfigClass::AyanamsaInfoTable[i].index!=AYANAMSA_MAX; i++)
        if (SolonConfigClass::AyanamsaInfoTable[i].index == SolonConfig->ayanamsaType)
        {
            ayanamsa = SolonConfigClass::AyanamsaInfoTable[i].degreeShift;;
            break;
        }

    horoscope->set_ayanamsa( ayanamsa );
    horoscope->calculate_scope();
    if ( horoscope2 )
    {
        horoscope2->aspects.calculate( &horoscope->solarSystem, &horoscope2->solarSystem );
    }
}


void
ScopeWidgetClass::setStyle( ScopeStyleType sType )
{
    style = sType;
}


void
ScopeWidgetClass::setAnalysedPlanet( PlanetIndexType pIndex )
{
    analysedPlanet = pIndex;
}


void
ScopeWidgetClass::setAnalysedSymbolon( int sym )
{
    analysedSymbolon = sym;
}


void
ScopeWidgetClass::set_neighbour( ScopeWidgetClass *neighbour )
{
    if ( neighbour != this ) neighbourWidget = neighbour;
}


void
ScopeWidgetClass::get_object_under_mouse( int x, int y )
{
    int i=0, j=0;
    
    cursorOverTooltips.clear();
    cursorOverInfoType = INFOTYPE_NONE;
    cursorOverIndex = 0;
    
    for (i=0, j=0; i < toolTipList.size(); i++)
    {
        if ( toolTipList.at(i)->rect.contains(x,y) )
        {
            cursorOverTooltips.push_back( i );
            j++;
        }
    }
    
    if (j==0)
    {
        cursorOverTooltips.push_back( 0 );
    }
    else
    {
        cursorOverInfoType = toolTipList.at(cursorOverTooltips[0])->infoType;
        cursorOverIndex = toolTipList.at(cursorOverTooltips[0])->index;
    }
}


bool
ScopeWidgetClass::event(QEvent *event)
{
    static int  rightClickX, rightClickY, translateBaseX, translateBaseY;
    
    if ( (event->type() == QEvent::ToolTip) && SolonConfig->toolTipsEnabled )
    {
        QHelpEvent *helpEvent = static_cast<QHelpEvent *>(event);
        get_object_under_mouse( helpEvent->x(), helpEvent->y() );
        if ( cursorOverInfoType > INFOTYPE_NONE )
        {
            QString str = "";
            for ( int i=0; i<(int)cursorOverTooltips.size(); i++ )
            {
                str += toolTipList.at( cursorOverTooltips[i] )->str;
                if ( SolonConfig->detailedToolTipsEnabled )
                {
                    str += toolTipList.at( cursorOverTooltips[i] )->strDetailed;
                }
                if ( i < (int)cursorOverTooltips.size()-1 ) str += "\n\n";
            }
            QToolTip::showText( helpEvent->globalPos(), str );
        }
    }
    else if ( event->type() == QEvent::MouseButtonPress )
    {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent *>(event);
        Qt::MouseButtons buttons = mouseEvent->buttons();
        get_object_under_mouse( mouseEvent->x(), mouseEvent->y() );
        if ( buttons.testFlag( Qt::LeftButton ) )
        {
            if ( cursorOverInfoType > INFOTYPE_NONE )
            {
                if ( neighbourWidget &&
                     (neighbourWidget->style == SCOPE_PLANET_INFO ||
                      neighbourWidget->style == SCOPE_TRANSIT_INFO ||
                      neighbourWidget->style == SCOPE_LIFECYRCLE_INFO ) )
                {
                    neighbourWidget->refToolTipList = &toolTipList;
                    neighbourWidget->cursorSelectedTooltips.clear();
                    neighbourWidget->cursorSelectedTooltips = cursorOverTooltips;
                    neighbourWidget->cursorSelectedInfoType = cursorOverInfoType;
                    neighbourWidget->cursorSelectedIndex = cursorOverIndex;
                    neighbourWidget->repaint();
                }
                emit on_object_clicked( (InfoType)cursorOverInfoType, cursorOverIndex );
            }
        }
        else if ( buttons.testFlag( Qt::RightButton ) )
        {
            rightClickX = mouseEvent->x();
            rightClickY = mouseEvent->y();
            translateBaseX = translateX;
            translateBaseY = translateY;
        }
    }
    else if ( event->type() == QEvent::Wheel )
    {
        QWheelEvent  *wheel = static_cast<QWheelEvent *>(event);
        int numDegrees = wheel->delta();
        scaleXY += numDegrees / 360.0;
        repaint();
    }
    else if ( event->type() == QEvent::MouseButtonDblClick )
    {
        scaleXY = 1;
        translateX = 0;
        translateY = 0;
        repaint();
    }
    else if ( event->type() == QEvent::MouseMove )
    {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent *>(event);
        Qt::MouseButtons buttons = mouseEvent->buttons();
        if ( buttons.testFlag( Qt::RightButton ) )
        {
            translateX = translateBaseX + mouseEvent->x() - rightClickX;
            translateY = translateBaseY + mouseEvent->y() - rightClickY;
            repaint();
        }
    }
    
    return QWidget::event(event);
}


void
ScopeWidgetClass::paintEvent(QPaintEvent *)
{
    if ( !m_printer ) p.begin(this);
    
    p.setRenderHints(
        QPainter::Antialiasing |
        QPainter::TextAntialiasing |
        QPainter::SmoothPixmapTransform
        );
    
    p.scale( scaleXY, scaleXY );
    p.translate( translateX, translateY );
    
    // clear popup tooltips
    clear_tooltip_list();
    
    // "constants"
    inMarginRatio = 0.01;
    belt1Ratio = 0.090;
    belt2Ratio = 0.04;
    belt3Ratio = 0.0125;
    beltDirection = 1;
    // calculate variables
    if ( m_printer )
    {
        inMarginRatio = 0.05;
        ww = m_printer->pageRect().width();
        wh = m_printer->pageRect().height();
    }
    else // normal mode
    {
        ww = width();
        wh = height();
    }
    a0 = (ww < wh) ? ww : wh;
    inMargin = int( a0 * inMarginRatio );
    xm = ww / 2;
    ym = wh / 2;
    w = ww - 2*inMargin; 
    h = wh - 2*inMargin;
    a = ( w < h ) ? w : h;
    
    // font metrics
    bigFont.setPointSize(a/15);
    normalFont.setPointSize(a/25);
    smallFont.setPointSize(a/50);
    dataFont.setPointSize( 8 );
    if (bigMetrics) delete bigMetrics;
    if (normalMetrics) delete normalMetrics;
    if (smallMetrics) delete smallMetrics;
    if (dataMetrics) delete dataMetrics;
    
    bigMetrics = new QFontMetrics( bigFont );
    normalMetrics = new QFontMetrics( normalFont );
    smallMetrics = new QFontMetrics( smallFont );
    dataMetrics = new QFontMetrics( dataFont );
    
    // fill background
    if ( m_bgColor != SolonConfig->backgroundColor )
    {
        m_bgColor = SolonConfig->backgroundColor;
        setPalette( QPalette( QColor( m_bgColor ) ) );
        setAutoFillBackground(true);
    }
    
    // set foreground color
    if ( m_fgColor != SolonConfig->foregroundColor )
    {
        m_fgColor = SolonConfig->foregroundColor;
        whitePen.setColor( QColor(m_fgColor) );
        
        quint32 darkColor = ColorSelectorClass::lightness( m_fgColor, 0.1875 );
        darkPen.setColor( QColor( darkColor ) );  
        
        quint32 houseColor = ColorSelectorClass::lightness( m_fgColor, 0.3 );
        housePen.setColor( QColor( houseColor ) );
    }
    
    // printing colors
    if ( m_printer )
    {
        m_fgColor = SolonConfig->printingColor;
        whitePen.setColor( QColor(m_fgColor) );
        
        quint32 darkColor = ColorSelectorClass::lightness( m_fgColor, 0.1875 );
        darkPen.setColor( QColor( darkColor ) );  
        
        quint32 houseColor = ColorSelectorClass::lightness( m_fgColor, 0.3 );
        housePen.setColor( QColor( houseColor ) );
    }
    
    // print header
    if ( m_printer )
    {
        printingFont.setPointSize(a/80);
        if (printingMetrics) delete printingMetrics;
        printingMetrics = new QFontMetrics( printingFont );
        p.setFont( printingFont );
        p.setPen( whitePen );
        
        int px = inMargin;
        int py = 0;
        
        QStringList hedlist = m_printigLeftHeaderText.split("\n");
        for ( int hi=0; hi<hedlist.size(); hi++ )
        {
            p.drawText( px, py, hedlist.at(hi) );
            py += printingMetrics->height();
        }
        
        px = inMargin + w;
        py = 0;
        
        hedlist = m_printigRightHeaderText.split("\n");
        for ( int hi=0; hi<hedlist.size(); hi++ )
        {
            p.drawText( px-printingMetrics->width(hedlist.at(hi)), py, hedlist.at(hi) );
            py += printingMetrics->height();
        }
    }
    
    /*
    p.setBrush( Qt::SolidPattern );
    p.setBrush( Qt::black );
    p.setPen( Qt::NoPen );
    p.fillRect( 0, 0, ww, wh, QColor( SolonConfig->backgroundColor ) );
    */
    
    if (horoscope == NULL)
    {
        if ( style == SCOPE_SYMBOLON_EXPLORE ) paint_symbolon_explore();
        if ( !m_printer ) p.end();
        return;
    }
    
    switch ( style )
    {
        default:
        case SCOPE_NONE: break;
        case SCOPE_CIRCLE: paint_circle_scope(); break;
        case SCOPE_RECTANGLE: paint_rectangle_scope(); break;
        case SCOPE_BOX: paint_box_scope(); break;
        case SCOPE_SYMBOLON_ASCSUN: paint_symbolon_asc_and_sun(); break;
        case SCOPE_SYMBOLON_DIALECTIC: paint_symbolon_dialectic(); break;
        case SCOPE_SYMBOLON_ASC_INFLUENCE: paint_symbolon_asc_influence(); break;
        case SCOPE_SYMBOLON_SUN_INFLUENCE: paint_symbolon_sun_influence(); break;
        case SCOPE_SYMBOLON_MC_INFLUENCE: paint_symbolon_mc_influence(); break;
        case SCOPE_SYMBOLON_HOUSE_MANDAL: paint_symbolon_house_mandal(); break;
        case SCOPE_SYMBOLON_PLANET_HOUSE_MANDAL: paint_symbolon_planet_mandal(INFOTYPE_HOUSE); break;
        case SCOPE_SYMBOLON_PLANET_SIGN_MANDAL: paint_symbolon_planet_mandal(INFOTYPE_SIGN); break;
        case SCOPE_SYMBOLON_PLANET_ANALYSIS: paint_symbolon_planet_analysis(analysedPlanet); break;
        case SCOPE_SYMBOLON_PLANET_ASPECTS: paint_symbolon_planet_aspects(analysedPlanet); break;
        case SCOPE_SYMBOLON_EXPLORE: paint_symbolon_explore(); break;
        case SCOPE_SYNASTRY: paint_synastry(); break;
        case SCOPE_TRANSITS: paint_transits(); break;
        case SCOPE_LIFECYRCLE: paint_lifecyrcle(); break;
        case SCOPE_BASIC_DATA: paint_basic_datas(); break;
        case SCOPE_ASPECTMATRIX: paint_aspect_matrix(); break;
        case SCOPE_QUALITY_MATRICES: paint_quality_matrices(); break;
        case SCOPE_PLANET_INFO: paint_planet_info(); break;
        case SCOPE_TRANSIT_INFO: paint_transit_info(); break;
        case SCOPE_LIFECYRCLE_INFO: paint_lifecyrcle_info(); break;
        case SCOPE_SYNASTRY_INFO: paint_synastry_info(); break;
        case SCOPE_SYNASTRY_VENUSMARS_INFO: paint_synastry_venusmars_info(); break;
        case SCOPE_SYNASTRY_SUNASC_INFO: paint_synastry_sunasc_info(); break;
        case SCOPE_SYNASTRY_PLUTO_INFO: paint_synastry_pluto_info(); break;
    }
    
    if ( !m_printer ) p.end();
}


/****************************************************************************
 *  SYMBOLON:  Ascendant  +  SUN_Sign
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_asc_and_sun()
{
    double                ascPos=0, sunPos=0;
    int                   ascSign=0, sunSign=0;
    int                   ascSym=0, sunSym=0, sumSym=0;
    int                   fw=0, fh=0;
    
    ascPos  = horoscope->houses.cusp[1];
    sunPos  = horoscope->solarSystem.Sun.Long;
    
    ascSign = ((int)(ascPos / 30)) + 1;
    sunSign = ((int)(sunPos / 30)) + 1;
    
    ascSym  = Symbol->two_sign_to_symbolon( ascSign, 0 );
    sunSym  = Symbol->two_sign_to_symbolon( sunSign, 0 );
    sumSym  = Symbol->two_sign_to_symbolon( ascSign, sunSign );
    
    fw = (int)(w/5);
    fh = (int)(h/1.2);
    
    paint_symbolon( ascSym, xm-4*fw/2, ym-fh/2, fw, fh );
    paint_symbolon( sunSym, xm-fw/2,   ym-fh/2, fw, fh );
    paint_symbolon( sumSym, xm+2*fw/2, ym-fh/2, fw, fh );
    
    paint_planet( PLANET_SUN, xm-a/20, ym-fh/2-a/20, a/10, a/10 );
    p.setFont( bigFont );
    p.setPen( whitePen );
    p.drawText( xm-13*fw/8-bigMetrics->width("Asc")/2, ym-fh/2+bigMetrics->height()/4, "Asc" );
    p.drawText( xm-3*fw/4-bigMetrics->width("+")/2, ym, "+" );
    p.drawText( xm+3*fw/4-bigMetrics->width("=")/2, ym, "=" );
}


/****************************************************************************
 *  SYMBOLON:  Horoscope Dialectic
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_dialectic()
{
    int                    ascSign=0, mcSign=0;
    int                    ascSym=0, mcSym=0, sunSym=0, sunSignSym=0;
    int                    ascPlanet=0, mcPlanet=0;
    int                    ascPlanetSign=0, mcPlanetSign=0, sunSign=0;
    int                    ascPlanetHouse=0, mcPlanetHouse=0, sunHouse=0;
    int                    ascPlanetSignSym=0, mcPlanetSignSym=0, sunInSignSym=0;
    int                    ascPlanetHouseSym=0, mcPlanetHouseSym=0, sunInHouseSym=0;
    
    // Ascendant
    ascSign            = horoscope->get_sign_where_house_cusp( 1 );
    ascPlanet          = Symbol->get_planet_of_sign( ascSign );
    ascPlanetSign      = horoscope->get_sign_where_planet( ascPlanet );
    ascPlanetHouse     = horoscope->get_house_where_planet( ascPlanet );
    ascSym             = Symbol->two_sign_to_symbolon( ascSign, 0 );
    ascPlanetSignSym   = Symbol->two_sign_to_symbolon( ascSign, ascPlanetSign );
    ascPlanetHouseSym  = Symbol->two_sign_to_symbolon( ascSign, ascPlanetHouse );
    
    // Medium Coeli
    mcSign             = horoscope->get_sign_where_house_cusp( 10 );
    mcPlanet           = Symbol->get_planet_of_sign( mcSign );
    mcPlanetSign       = horoscope->get_sign_where_planet( mcPlanet );
    mcPlanetHouse      = horoscope->get_house_where_planet( mcPlanet );
    mcSym              = Symbol->two_sign_to_symbolon( mcSign, 0 );
    mcPlanetSignSym    = Symbol->two_sign_to_symbolon( mcSign, mcPlanetSign );
    mcPlanetHouseSym   = Symbol->two_sign_to_symbolon( mcSign, mcPlanetHouse );
    
    // Sun
    sunSym             = Symbol->planet_to_symbolon( PLANET_SUN );
    sunSign            = horoscope->get_sign_where_planet( PLANET_SUN );
    sunHouse           = horoscope->get_house_where_planet( PLANET_SUN );
    sunSignSym         = Symbol->two_sign_to_symbolon( sunSign, sunSign );
    sunInSignSym       = Symbol->two_sign_to_symbolon( sunSym, sunSign );
    sunInHouseSym      = Symbol->two_sign_to_symbolon( sunSym, sunHouse );
    
    int  u = w / 6;
    int  v = h / 6;
    int  m = 2;
    int  bx=0, by=0, bw=0, bh=0;
    
    // --- problem box ---
    bx = xm - 3*u + m;
    by = ym - 2*v;
    bw = 2 * u - 2*m;
    bh = 5 * v;
    p.setPen( darkPen );
    p.drawRoundRect( bx, by, bw, bh );
    paint_symbolon( ascSym, bx+0.02*bw, by+0.02*bh, 0.96*bw, 0.6*bh,
                        tr("The Problem") );
    paint_symbolon( ascPlanetHouseSym, bx+0.02*bw,  by+0.64*bh, 0.48*bw, 0.34*bh,
                        tr("Where?"),
                        QString::fromUtf8( Symbol->effectInfo[ascPlanetHouse].inHouse ),
                        ALIGN_RIGHT );
    paint_symbolon( ascPlanetSignSym, bx+0.51*bw, by+0.64*bh, 0.48*bw, 0.34*bh,
                        tr("How works?"),
                        QString::fromUtf8( Symbol->effectInfo[ascPlanetSign].inSign ),
                        ALIGN_LEFT );
    
    // --- outcome box ---
    bx = xm - 1*u + m;
    by = ym - 3*v;
    bw = 2 * u - 2*m;
    bh = 5 * v;
    p.setPen( darkPen );
    p.drawRoundRect( bx, by, bw, bh );
    paint_symbolon( mcSym, bx+0.02*bw, by+0.02*bh, 0.96*bw, 0.6*bh,
                        tr("The Outcome") );
    paint_symbolon( mcPlanetHouseSym, bx+0.02*bw,  by+0.64*bh, 0.47*bw, 0.34*bh,
                        tr("Where?"),
                        QString::fromUtf8( Symbol->effectInfo[mcPlanetHouse].inHouse ),
                        ALIGN_RIGHT );
    paint_symbolon( mcPlanetSignSym, bx+0.51*bw, by+0.64*bh, 0.47*bw, 0.34*bh,
                        tr("How works?"),
                        QString::fromUtf8( Symbol->effectInfo[mcPlanetSign].inSign ),
                        ALIGN_LEFT );
    
    // --- way box ---
    bx = xm + 1*u + m;
    by = ym - 2*v;
    bw = 2 * u - 2*m;
    bh = 5 * v;
    p.setPen( darkPen );
    p.drawRoundRect( bx, by, bw, bh );
    paint_symbolon( sunSignSym, bx+0.02*bw, by+0.02*bh, 0.96*bw, 0.6*bh,
                        tr("The Way") );
    paint_symbolon( sunInHouseSym, bx+0.02*bw,  by+0.64*bh, 0.47*bw, 0.34*bh,
                        tr("Where?"),
                        QString::fromUtf8( Symbol->effectInfo[sunHouse].inHouse ),
                        ALIGN_RIGHT );
    paint_symbolon( sunInSignSym, bx+0.51*bw, by+0.64*bh, 0.47*bw, 0.34*bh,
                        tr("How works?"),
                        QString::fromUtf8( Symbol->effectInfo[sunSign].inSign ),
                        ALIGN_LEFT );
}


/****************************************************************************
 *  SYMBOLON:  Ascendant analysis
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_asc_influence()
{
    int                    baseSign=0, basePlanet=0;
    
    // Ascendant
    baseSign            = horoscope->get_sign_where_house_cusp( 1 );
    basePlanet          = Symbol->get_planet_of_sign( baseSign );
    
    // draw aspects
    paint_symbolon_planet_aspects( basePlanet, baseSign, true );
}


/****************************************************************************
 *  SYMBOLON:  Sun analysis
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_sun_influence()
{
    paint_symbolon_planet_aspects( PLANET_SUN, SIGN_LEO, true );
}


/****************************************************************************
 *  SYMBOLON:  MC analysis
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_mc_influence()
{
    int                    baseSign=0, basePlanet=0;
    
    // MC
    baseSign            = horoscope->get_sign_where_house_cusp( 10 );
    basePlanet          = Symbol->get_planet_of_sign( baseSign );
    
    // draw aspects
    paint_symbolon_planet_aspects( basePlanet, baseSign, true );
}


/****************************************************************************
 *  SYMBOLON:  planet analysis
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_planet_analysis( int planet )
{
    int         wf=a/5, hf=a/4, x=xm, y=ym-hf/4;
    int         house=0, sign=0, planetSym1=0, planetSym2=0,
                houseSym=0, signSym=0, houseInSignSym=0,
                planetInHouseSym1=0, planetInSignSym1=0,
                planetInHouseSym2=0, planetInSignSym2=0;
    
    if ( planet == PLANET_VENUS )
    {
        planetSym1 = Symbol->two_sign_to_symbolon( SIGN_TAURUS, 0 );
        planetSym2 = Symbol->two_sign_to_symbolon( SIGN_LIBRA, 0 );
    }
    else if ( planet == PLANET_MERCURY )
    {
        planetSym1 = Symbol->two_sign_to_symbolon( SIGN_GEMINI, 0 );
        planetSym2 = Symbol->two_sign_to_symbolon( SIGN_VIRGO, 0 );
    }
    else
    {
        planetSym1 = Symbol->planet_to_symbolon( planet );
        planetSym2 = PLANET_NONE;
    }
    
    house    = horoscope->get_house_where_planet( planet );
    houseSym = Symbol->two_sign_to_symbolon( house, 0 );
    
    sign     = horoscope->get_sign_where_planet( planet );
    signSym  = Symbol->two_sign_to_symbolon( sign, 0 );
    
    houseInSignSym = Symbol->two_sign_to_symbolon( house, sign );
    
    if ( planetSym2 == PLANET_NONE )
    {
        planetInHouseSym1 = Symbol->two_sign_to_symbolon( house, planetSym1 );
        planetInSignSym1  = Symbol->two_sign_to_symbolon( sign, planetSym1 );
        
        // symbolon of planet
        paint_symbolon( planetSym1, x-1*wf/2, y-3*hf/2, wf, hf, tr("internal person") );
        // house
        paint_symbolon( houseSym, x+1*wf/2, y-2*hf/2, wf, hf, tr("in house") );
        // combination with house
        paint_symbolon( planetInHouseSym1, x-1*wf/2, y-1*hf/2, wf, hf,
                        tr("Where?"),
                        QString::fromUtf8( Symbol->effectInfo[house].inHouse ) );
        // sign
        paint_symbolon( signSym, x+1*wf/2, y-0*hf/2, wf, hf , tr("in sign") );
        // combination with sign
        paint_symbolon( planetInSignSym1, x-1*wf/2, y+2*hf/2, wf, hf,
                        tr("How works?"),
                        QString::fromUtf8( Symbol->effectInfo[sign].inSign ) );
        paint_symbolon( houseInSignSym, x+1*wf/2, y+2*hf/2, wf, hf, tr("house+sign") );
    }
    else
    {
        planetInHouseSym1 = Symbol->two_sign_to_symbolon( house, planetSym1 );
        planetInSignSym1  = Symbol->two_sign_to_symbolon( sign, planetSym1 );
        planetInHouseSym2 = Symbol->two_sign_to_symbolon( house, planetSym2 );
        planetInSignSym2  = Symbol->two_sign_to_symbolon( sign, planetSym2 );
        
        // two symbolon of planet
        paint_symbolon( planetSym1, x-3*wf/2, y-3*hf/2, wf, hf, tr("internal person") );
        paint_symbolon( planetSym2, x+1*wf/2, y-3*hf/2, wf, hf, tr("internal person") );
        // house
        paint_symbolon( houseSym, x-1*wf/2, y-2*hf/2, wf, hf, tr("in house") );
        // combination with house
        paint_symbolon( planetInHouseSym1, x-3*wf/2, y-1*hf/2, wf, hf,
                        tr("Where?"),
                        QString::fromUtf8( Symbol->effectInfo[house].inHouse ) );
        paint_symbolon( planetInHouseSym2, x+1*wf/2, y-1*hf/2, wf, hf,
                        tr("Where?"),
                        QString::fromUtf8( Symbol->effectInfo[house].inHouse ) );
        // sign
        paint_symbolon( signSym, x-1*wf/2, y-0*hf/2, wf, hf,  tr("in sign") );
        // combination with sign
        paint_symbolon( planetInSignSym1, x-3*wf/2, y+2*hf/2, wf, hf,
                        tr("How works?"),
                        QString::fromUtf8( Symbol->effectInfo[sign].inSign ) );
        paint_symbolon( planetInSignSym2, x+1*wf/2, y+2*hf/2, wf, hf,
                        tr("How works?"),
                        QString::fromUtf8( Symbol->effectInfo[sign].inSign ) );
        paint_symbolon( houseInSignSym, x-1*wf/2, y+2*hf/2, wf, hf, tr("house+sign") );
    }
}


/****************************************************************************
 *  SYMBOLON:  planet aspects
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_planet_aspects(
        int basePlanet, int baseSign, int enforceAspectPower )
{
    int                  baseSym=0;
    int                  basePlanetSign=0, basePlanetHouse=0, basePlanetSignSym=0, basePlanetHouseSym=0;
    
    // base planet
    if ( baseSign == SIGN_NONE )
    {
        baseSign = planet2sign_according_to_constellation( basePlanet );
    }
    
    basePlanetSign      = horoscope->get_sign_where_planet( basePlanet );
    basePlanetHouse     = horoscope->get_house_where_planet( basePlanet );
    baseSym             = Symbol->two_sign_to_symbolon( baseSign, 0 );
    basePlanetSignSym   = Symbol->two_sign_to_symbolon( baseSign, basePlanetSign );
    basePlanetHouseSym  = Symbol->two_sign_to_symbolon( baseSign, basePlanetHouse );
    
    int                 wf = w / 6; // figure width
    int                 hf = h / 3; // figure height
    int                 m = 2; // margin
    int                 i = 0; // general
    int                 harmonicAspects=0, disharmonicAspects=0, biAspects=0,
                        allAspects=0, aspectPlaces=0;
    int                 aspect = 0, planet=0;
    PlanetClass         **planetVector = horoscope->solarSystem.planetVector;
    
    // calculate the number of aspected planets
    harmonicAspects = disharmonicAspects = 0;
    for (i=0; i<horoscope->solarSystem.numberOfPlanets; i++)
    {
        planet = planetVector[i]->index;
        if ( !Symbol->is_symbolon_planet(planet) ) continue;
        
        aspect = horoscope->aspects.matrix[ basePlanet ][ planet ];
        if ( !Symbol->is_symbolon_aspect(aspect) ) continue;
        
        switch ( aspect )
        {
            default: continue;
            case ASPECT_SEXTIL:
            case ASPECT_TRIGON:
                harmonicAspects++;
                break;
            
            case ASPECT_SEMIQUADRAT:
            case ASPECT_QUADRAT:
            case ASPECT_MIRROR:
                disharmonicAspects++;
                break;
            
            case ASPECT_OPPOSITE:
            case ASPECT_CONJUCT:
                biAspects++;
                break;
        }
    }
    allAspects = harmonicAspects + disharmonicAspects + biAspects;
    if ( (int)(allAspects/2) == ((float)allAspects/2.0) ) aspectPlaces = allAspects;
                                                     else aspectPlaces = allAspects + 1;
    
    // ----- draw aspected planets -----
    int                 pos=0, u=0, v=0;
    int                 biPos=0, harmonicPos=0, disharmonicPos=0, allPos=0;
    int                 aspectPower=0, aspectEnergy=0, planetInHouse=0;
    int                 aspectSym=0, planetSym=0, aspectModifiedPlanetSym=0, planetCombinationSym=0;
    int                 x1=0, y1=0, x2=0, y2=0, x3=0, y3=0, x4=0, y4=0, xArrow=0, yArrow=0;
    QPointF             arrowPoints[3];
    QString             aspectStr;
    
    // calculate with and height of aspected planets
    u = (int)(h / (aspectPlaces / 2));
    v = (int)(w / 7);
    if (u > wf) u = wf;
    if (v > hf) v = hf;
    
    // starting positions
    disharmonicPos = 0;
    biPos          = disharmonicAspects;
    harmonicPos    = biAspects + disharmonicAspects;
    allPos         = 2*(int)((allAspects+1)/2);
    
    // middle of aspect lines
    x1 = xm;
    y1 = ym - hf/2;
    
    for (i=0; i<horoscope->solarSystem.numberOfPlanets; i++)
    {
        planet = planetVector[i]->index;
        if ( !Symbol->is_symbolon_planet(planet) ) continue;
        
        aspect = horoscope->aspects.matrix[ basePlanet ][ planet ];
        if ( !Symbol->is_symbolon_aspect(aspect) ) continue;
        
        switch ( aspect )
        {
            default:
                continue;
            
            case ASPECT_SEXTIL:
            case ASPECT_TRIGON:
                pos = harmonicPos++;
                break;
            
            case ASPECT_SEMIQUADRAT:
            case ASPECT_QUADRAT:
            case ASPECT_MIRROR:
                pos = disharmonicPos++;
                break;
            
            case ASPECT_OPPOSITE:
            case ASPECT_CONJUCT:
                pos = biPos++;
                break;
        }
        
        aspectPower  = horoscope->aspects.powerMatrix[ basePlanet ][ planet ];
        aspectEnergy = Symbol->aspectInfo[ aspect ].planetEnergy;
        aspectStr    = QString::number( aspectPower ) + "%";
        
        // pure planet representator of aspect and planet itself
        aspectSym = planet2sign_according_to_constellation( aspectEnergy, /*withPlanet=*/basePlanet );
        planetSym = planet2sign_according_to_constellation( planet, /*withPlanet=*/basePlanet );
        
        // combinated symbolons of base planet
        aspectModifiedPlanetSym = Symbol->two_sign_to_symbolon( planetSym, aspectSym );
        planetCombinationSym = Symbol->two_sign_to_symbolon( baseSym, planetSym );
        
        // set pen to draw aspect line
        multiColor.setRgb( (QRgb)(Symbol->aspectInfo[aspect].color) );
        multiPen.setColor( multiColor );
        multiPen.setWidth( a/40 );
        if ( aspect == ASPECT_MIRROR ) multiPen.setStyle( Qt::DotLine );
                                  else multiPen.setStyle( Qt::SolidLine );
        aspectArrowPen.setColor( multiColor );
        aspectArrowPen.setWidth( 1 );
        aspectArrowBrush.setColor( multiColor );
        aspectArrowBrush.setStyle( Qt::SolidPattern );
        
        // calculate positions of the cards      
        if (allAspects == 1) // only one aspect (put on right side middle)
        {
            x3     = inMargin + w - 3*v/2;
            y3     = inMargin + ym;
            x4     = x3 + v;
            y4     = y3;
            xArrow = x3 - v/2;
            yArrow = y3;
            arrowPoints[0]  = QPointF(x3+v/2-a/30, y3-a/40);
            arrowPoints[1]  = QPointF(x3+v/2-a/30, y3+a/40);
            arrowPoints[2]  = QPointF(x3+v/2+a/30, y3);
        }
        else if ( pos < allPos / 2 ) // left side
        {
            x3     = inMargin + 3*v/2;
            y3     = inMargin + h - ( pos * (2 * h / allPos) + (h / allPos) );
            x4     = x3 - v;
            y4     = y3;
            xArrow = x3 + v/2;
            yArrow = y3;
            arrowPoints[0]  = QPointF(x3-v/2+a/30, y3-a/40);
            arrowPoints[1]  = QPointF(x3-v/2+a/30, y3+a/40);
            arrowPoints[2]  = QPointF(x3-v/2-a/30, y3);
        }
        else // right side
        {
            x3              = inMargin + w - 3*v/2;
            y3              = inMargin + (pos-allPos/2) * (2 * h / allPos) + (h / allPos);
            x4              = x3 + v;
            y4              = y3;
            arrowPoints[0]  = QPointF(x3+v/2-a/30, y3-a/40);
            arrowPoints[1]  = QPointF(x3+v/2-a/30, y3+a/40);
            arrowPoints[2]  = QPointF(x3+v/2+a/30, y3);
        }
        
        // planet in which house?
        planetInHouse = horoscope->get_house_where_planet( planet );
        
        if (enforceAspectPower)
        {
            /*
             * x1, y1 - ascendant
             * x2, y2 - aspect power (pure symbolon)
             * x3, y3 - planet (pure symbolon)
             * x4, y4 - aspect modified symbolon
             */
            x2 = (int)( x1 - ( x1 - x3 )*0.6 );
            y2 = (int)( y1 - ( y1 - y3 )*0.6 );
            
            p.setPen( multiPen );
            p.setBrush( Qt::NoBrush );
            p.drawLine( x1, y1, x3, y3 );
            
            p.setPen( aspectArrowPen );
            p.setBrush( aspectArrowBrush );
            p.drawConvexPolygon(arrowPoints, 3);
            
            p.setPen( whitePen );
            p.setFont( smallFont );
            p.drawText( ((x2+x1)/2)-smallMetrics->width(aspectStr)/2,
                        ((y2+y1)/2)-smallMetrics->height()/3, aspectStr );
            
            paint_symbolon( aspectSym, x2-v*0.3, y2-u*0.3, v*0.6, u*0.6 );
            paint_symbolon( planetSym, x3-v/2, y3-u/2, v, u );
            paint_symbolon( aspectModifiedPlanetSym, x4-v/2, y4-u/2, v, u,
                                QString::fromUtf8( Symbol->houseInfo[planetInHouse].name ) );
        }
        else
        {
            x2 = (int)( x1 - ( x1 - x4 )*0.6 );
            y2 = (int)( y1 - ( y1 - y4 )*0.6 );
            
            p.setPen( multiPen );
            p.setBrush( Qt::NoBrush );
            p.drawLine( x1, y1, x4, y4 );
            
            p.setPen( whitePen );
            p.setFont( smallFont );         
            p.drawText( ((x2+x1)/2)-smallMetrics->width(aspectStr)/2,
                        ((y2+y1)/2)-smallMetrics->height()/3, aspectStr );
            
            paint_symbolon( aspectSym, x2-v*0.3, y2-u*0.3, v*0.6, u*0.6 );
            paint_symbolon( planetCombinationSym, x4-v/2, y4-u/2, v, u,
                                    QString::fromUtf8( Symbol->houseInfo[planetInHouse].name ) );
        }        
    }
    
    // ----- put base planet at cusp-middle -----
    paint_symbolon( baseSym, x1-wf/2, y1-hf/2, wf, hf, "", ALIGN_CENTER, ALIGN_MIDDLE );
    
    // ----- put house and sign at bottom of base planet -----
    paint_symbolon( basePlanetHouseSym, x1-wf*0.9, y1+hf/2+m, wf*0.9, hf*0.9,
                            tr("Where?"),
                            QString::fromUtf8( Symbol->effectInfo[basePlanetHouse].inHouse ),
                            ALIGN_RIGHT, ALIGN_TOP );
    paint_symbolon( basePlanetSignSym, x1+m, y1+hf/2+m, wf*0.9, hf*0.9,
                            tr("How works?"),
                            QString::fromUtf8( Symbol->effectInfo[basePlanetSign].inSign ),
                            ALIGN_LEFT, ALIGN_TOP );
}


/****************************************************************************
 *  SYMBOLON SUBRUTIN: returns the sign of the givent planet +
 *                     selects between two type of VENUS and two MERCURY
 *                     according to horoscope constellation.
 ****************************************************************************/
int
ScopeWidgetClass::planet2sign_according_to_constellation( int planet, int withPlanet )
{
    int                 j=0, planet2=0, aspect2=0, s=0;
    std::vector<int>    constellationVector;
    
    constellationVector.clear();
    
    s = horoscope->get_house_where_planet( planet );
    constellationVector.push_back( Symbol->get_forced_sign( s ) );
    
    s = horoscope->get_sign_where_planet( planet );
    constellationVector.push_back( Symbol->get_forced_sign( s ) );
    
    if ( withPlanet != PLANET_NONE )
    {
        s = horoscope->get_house_where_planet( withPlanet );
        constellationVector.push_back( Symbol->get_forced_sign( s ) );
                
        s = horoscope->get_sign_where_planet( withPlanet );
        constellationVector.push_back( Symbol->get_forced_sign( s ) );
    }
    
    for (j=0; j<horoscope->solarSystem.numberOfPlanets; j++)
    {
        planet2 = horoscope->solarSystem.planetVector[j]->index;
        if ( !Symbol->is_symbolon_planet(planet2) ) continue;
        
        aspect2 = horoscope->aspects.matrix[ planet ][ planet2 ];
        if ( !Symbol->is_symbolon_aspect(aspect2) ) continue;
        
        constellationVector.push_back( horoscope->get_house_where_planet( planet2 ) );
        constellationVector.push_back( horoscope->get_sign_where_planet( planet2 ) );
    }
    
    s = Symbol->planet_to_symbolon( planet, constellationVector );;
    
    constellationVector.clear();
    
    return s;
}


/****************************************************************************
 *  SYMBOLON:  house mandal
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_house_mandal()
{
    int           sign=0, house=0, sym=0;
    double        x=0, y=0, wf=0, hf=0, xx=0;
    
    wf = w/7;
    hf = h/3;
    
    for (house=1; house<=12; house++)
    {
        if (house <= 6)
        {
            xx = house-1;
            x  = inMargin + (xx*w)/7 + w/14;
            y  = ym + ((h-hf)/2) * sin( acos( (xx-3) / 3.0 ) );
        }
        else
        {
            xx = 12-house;
            x  = inMargin + (xx*w)/7 + w/14 + w/7;
            xx = house-7;
            y  = ym - ((h-hf)/2) * sin( acos( (xx-3) / 3.0 ) );
        }
        sign = horoscope->get_sign_where_house_cusp( house );
        sym  = Symbol->two_sign_to_symbolon( house, sign );
        
        // x    = xm - (w-wf)/2 * cos( (2*M_PI*(double)(house-1)/12.0) );
        // y    = ym + (h-hf)/2 * sin( (2*M_PI*(double)(house-1)/12.0) );
        paint_symbolon( sym, x-wf/2, y-hf/2, wf, hf,
                        QString::fromUtf8( Symbol->houseInfo[house].name ) );
    }
}


/****************************************************************************
 *  CLASSIC: Planets in Houses/Signs Mandala (destiny/personality)
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_planet_mandal( InfoType type )
{
    int                 i=0, j=0, len=0, x=0, y=0, x2=0, y2=0, wf=0, hf=0, xx=0,
                        xArray[2*PLANET_MAX], yArray[2*PLANET_MAX],
                        info=0, prevInfo=0, sym1=0, sym2=0, planetSym1=0, planetSym2=0;
    PlanetClass         *planetArray[PLANET_MAX];
    PlanetClass         *planet=NULL;
    double              asc=0, angle=0, distance=0;
    QString             qtstr;
    
    asc = horoscope->houses.Asc;
    
    // clear 'planetArray' and 'xArray' and 'yArray'
    for (i=0; i<PLANET_MAX; i++)
    {
        planetArray[i] = NULL;
        xArray[i] = 0;
        yArray[i] = 0;
    }
    
    // find symbolon planets and put them to 'planetArray'
    for (i=len=0; i<horoscope->solarSystem.numberOfPlanets; i++)
    {
        planet = horoscope->solarSystem.planetVector[i];
        if ( !Symbol->is_symbolon_planet(planet->index) ) continue;
        planetArray[len++] = planet;
    }
    
    // order 'planetArray' according to Longitude
    for (i=0; i<len; i++)
        for (j=0; j<len-1; j++)
        {
            if ( ROUND_DEG( planetArray[j]->Long - asc ) >
                    ROUND_DEG( planetArray[j+1]->Long - asc ) )
            {
                planet = planetArray[j];
                planetArray[j] = planetArray[j+1];
                planetArray[j+1] = planet;
            }
        }
    
    // calculate painting positions
    wf = w / 6;
    hf = h / 3;
    for (i=0; i<len; i++)
    {
        if (i < len/2)
        {
            xx = i;
            x  = (xx * wf) + wf/2;
            y  = ym + (int)(((h-hf)/2) * sin( acos( (xx-len/4.0) / (len/4.0) ) ));
        }
        else
        {
            xx = len-i-1;
            x  = (xx * wf) + wf/2 + wf;
            xx = i-(len/2);
            y  = ym - (int)(((h-hf)/2) * sin( acos( (xx-len/4.0) / (len/4.0) ) ));
        }
        
        x += inMargin;
        
        xArray[i*2] = x;
        yArray[i*2] = y;
        
        if (i>0)
        {
            xArray[(i*2)-1] = ( x + xArray[(i-1)*2] ) / 2;
            yArray[(i*2)-1] = ( y + yArray[(i-1)*2] ) / 2;
        }
    }
    xArray[(len*2)-1] = ( xArray[0] + xArray[(len-1)*2] ) / 2;
    yArray[(len*2)-1] = ( yArray[0] + yArray[(len-1)*2] ) / 2;
    
    // paint pies
    p.setPen( housePen );
    p.setFont( smallFont );
    switch (type)
    {
        default:
        case INFOTYPE_HOUSE:
            prevInfo = horoscope->get_house_where_planet( planetArray[len-1]->index );
            break;
        case INFOTYPE_SIGN:
            prevInfo = horoscope->get_sign_where_planet( planetArray[len-1]->index );
            break;
    }
    for (i=0; i<len; i++)
    {
        planet = planetArray[i];
        switch (type)
        {
            default:
            case INFOTYPE_HOUSE:
                info = horoscope->get_house_where_planet( planet->index );
                break;
            case INFOTYPE_SIGN:
                info = horoscope->get_sign_where_planet( planet->index );
                break;
        }
        
        if (info == prevInfo)
        {
            prevInfo = info;
            continue;
        }
        prevInfo = info;    
        
        if (i==0)
        {
            x  = xArray[(len*2)-1];
            y  = yArray[(len*2)-1];
            x2 = xArray[0];
            y2 = yArray[0];
        }
        else
        {
            x  = xArray[(i*2)-1];
            y  = yArray[(i*2)-1];
            x2 = xArray[(i*2)];
            y2 = yArray[(i*2)];
        }
        
        // recalculate the posotion of points
        angle = SolonMath::arcustangent2( y-ym, x-xm );        
        x = xm + (int)(SolonMath::cosinus( angle ) * (h+w));
        y = ym + (int)(SolonMath::sinus( angle ) * (h+w));
        angle = SolonMath::arcustangent2( y2-ym, x2-xm );
        distance = sqrt( SQUARE(y2-ym) + SQUARE(x2-xm) );
        x2 = xm + (int)(SolonMath::cosinus( angle ) * (distance/4));
        y2 = ym + (int)(SolonMath::sinus( angle ) * (distance/4));
        
        // paint the line
        p.drawLine( xm, ym, x, y );
        
        // paint the sign
        switch (type)
        {
            default:
            case INFOTYPE_HOUSE:
                qtstr = QString::number(info);
                p.drawText( x2-smallMetrics->width(qtstr)/2, y2+smallMetrics->height()/3, qtstr );
                break;
            case INFOTYPE_SIGN:
                paint_sign( info, x2-a/60, y2-a/60, a/30, a/30 );
                break;
        }
    }
    
    // paint planets in signs
    for (i=0; i<len; i++)
    {
        planet = planetArray[i];
        switch (type)
        {
            default:
            case INFOTYPE_HOUSE:
                info = horoscope->get_house_where_planet( planet->index );
                break;
            case INFOTYPE_SIGN:
                info = horoscope->get_sign_where_planet( planet->index );
                break;
        }
        planetSym1 = Symbol->planet_to_symbolon( planet->index );
        planetSym2 = Symbol->planet_to_symbolon2( planet->index );
        if ( planetSym1 != planetSym2 )
        {
            sym1 = Symbol->two_sign_to_symbolon( planetSym1, info );
            sym2 = Symbol->two_sign_to_symbolon( planetSym2, info );
            paint_symbolon( sym2, xArray[i*2]-(2*wf/4), yArray[i*2]-(2*hf/4), 3*wf/4, 3*hf/4 );
            paint_symbolon( sym1, xArray[i*2]-(1*wf/3), yArray[i*2]-(1*hf/3), 3*wf/4, 3*hf/4 );
        }
        else
        {
            sym1 = Symbol->two_sign_to_symbolon( planetSym1, info );
            paint_symbolon( sym1, xArray[i*2]-wf/2, yArray[i*2]-hf/2, wf, hf );
        }
    }
}


/****************************************************************************
 *  SYMBOLON:  house mandal
 ****************************************************************************/
void
ScopeWidgetClass::paint_symbolon_explore()
{
    paint_symbolon( analysedSymbolon, inMargin, inMargin, w/2, h );
    
    int sign1   = Symbol->symbolonInfo[analysedSymbolon].sign1;
    int sign2   = Symbol->symbolonInfo[analysedSymbolon].sign2;
    int planet1 = Symbol->get_planet_of_sign( sign1 );
    int planet2 = Symbol->get_planet_of_sign( sign2 );
    
    int x0 = inMargin + 3 * w / 4;
    int y0 = inMargin + h / 2;
    
    Symbol->paint_sign( p, sign1, x0-a/4, y0-a/4, a/4, a/4 );
    Symbol->paint_sign( p, sign2, x0, y0-a/4, a/4, a/4 );
    Symbol->paint_planet( p, planet1, x0-a/4, y0, a/4, a/4 );
    Symbol->paint_planet( p, planet2, x0, y0, a/4, a/4 );
}


/****************************************************************************
 *  CLASSIC: Circle Scope
 ****************************************************************************/
void
ScopeWidgetClass::paint_circle_scope()
{
    QRect               rect;
    int                 belt1 = (int)(belt1Ratio * a); // belt of signs
    int                 belt2 = (int)(belt2Ratio * a); // belt of houses
    int                 belt3 = (int)(belt3Ratio * a); // belt of degrees
    int                 x1=0, y1=0, x2=0, y2=0, r1=0, r2=0, i=0;
    double              asc=0, desc=0, angle=0;
    double              _2PI=2*M_PI;
    
    asc   = horoscope->houses.Asc;
    desc  = ROUND_DEG( asc+180 );
    asc  *= _2PI / 360;
    desc *= _2PI / 360;
    
    p.setBrush(Qt::NoBrush);
    
    // belt1 - signs
    r1 = a / 2 - inMargin;
    r2 = (a - 2*belt1) / 2 - inMargin;
    draw_sign_belt( r1, r2, horoscope->houses.Asc );
    p.setPen( whitePen );
    p.drawEllipse( xm-r1, ym-r1, 2*r1, 2*r1 );
    p.drawEllipse( xm-r2, ym-r2, 2*r2, 2*r2 );
    
    // belt2 - houses
    r1  = (a - 2*belt1) / 2 - inMargin;
    r2  = (a - 2*belt1 - 2*belt2) / 2 - inMargin;
    draw_houses_belt( r1, r2, horoscope->houses.Asc, &horoscope->houses  );
    p.setPen( whitePen );
    p.drawEllipse( xm-r2, ym-r2, 2*r2, 2*r2 );
    
    // house lines
    for (i=0; i<12; i++)
    {
        if (i+1==1 || i+1==4 || i+1==7 || i+1==10)
        {
            p.setPen( whitePen );
            r1 = a / 2;
        }
        else
        {
            //housePen.setStyle( Qt::DashLine );
            p.setPen( housePen );
            r1 = (a - 2*belt1 - 2*belt2) / 2 - inMargin;
        }
        
        angle = M_PI + ( horoscope->houses.cusp[i+1] * _2PI / 360.0 ) - asc;
        x1 = xm;
        y1 = ym;
        x2 = (int)( xm + (r1-1) * cos(angle) );
        y2 = (int)( ym - (r1-1) * sin(angle) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
    }
    
    // belt3 - degrees
    r1 = (a - 2*belt1 - 2*belt2) / 2 - inMargin;
    r2 = (a - 2*belt1 - 2*belt2 - 2*belt3) / 2 - inMargin;
    draw_degrees_belt( r1, r2, horoscope->houses.Asc );
    
    // planets
    r1 = (a - 2*belt1 - 2*belt2 - 2*belt3) / 2 - inMargin;
    r2 = (a - 2*belt1 - 2*belt2 - 2*belt3) / 2 - a/10 - inMargin;
    draw_planets_belt( r1, r2, horoscope->houses.Asc, horoscope );
    
    // aspects
    r1 = (a - 2*belt1 - 2*belt2 - 2*belt3) / 2 - a/10 - inMargin; // planet orig. position belt
    draw_aspects_into_middle( r1, horoscope->houses.Asc );
}


/****************************************************************************
 *  CLASSIC: Rectangle Scope
 ****************************************************************************/
void
ScopeWidgetClass::paint_rectangle_scope()
{
    static double poligons[12][5][2] =
    {
        { {4, 0}, {0.00, 0.50}, {0.25, 0.25}, {0.50, 0.50}, {0.25, 0.75} },
        { {3, 0}, {0.00, 0.50}, {0.25, 0.75}, {0.00, 1.00}, {0.00, 0.00} },
        { {3, 0}, {0.00, 1.00}, {0.25, 0.75}, {0.50, 1.00}, {0.00, 0.00} },
        
        { {4, 0}, {0.50, 1.00}, {0.25, 0.75}, {0.50, 0.50}, {0.75, 0.75} },
        { {3, 0}, {0.50, 1.00}, {0.75, 0.75}, {1.00, 1.00}, {0.00, 0.00} },
        { {3, 0}, {1.00, 1.00}, {0.75, 0.75}, {1.00, 0.50}, {0.00, 0.00} },
        
        { {4, 0}, {1.00, 0.50}, {0.75, 0.75}, {0.50, 0.50}, {0.75, 0.25} },
        { {3, 0}, {1.00, 0.50}, {0.75, 0.25}, {1.00, 0.00}, {0.00, 0.00} },
        { {3, 0}, {1.00, 0.00}, {0.75, 0.25}, {0.50, 0.00}, {0.00, 0.00} },
        
        { {4, 0}, {0.50, 0.00}, {0.75, 0.25}, {0.50, 0.50}, {0.25, 0.25} },
        { {3, 0}, {0.50, 0.00}, {0.25, 0.25}, {0.00, 0.00}, {0.00, 0.00} },
        { {3, 0}, {0.00, 0.00}, {0.25, 0.25}, {0.00, 0.50}, {0.00, 0.00} }
    };
    int             i=0, j=0, k=0, sign=0, af=0, ascSign=0, titleWidth=0, titleHeight=0,
                    x1=0, y1=0, u=0, v=0, uu=0, vv=0, af2=0;
    QPointF         poligonPoints[4];
    int             xmid=0, ymid=0;
    QString         str;
    int             planetHouse[PLANET_MAX+1];
    int             nofPlanetInHouse[13];
    
    ascSign = (int)(horoscope->houses.Asc/30) + 1;
    
    for (i=0; i<PLANET_MAX; i++)
    {
        if ( !Symbol->planetInfo[i].enabled )
        {
            planetHouse[i] = 0;
            continue;
        }
        planetHouse[i] = ((horoscope->get_sign_where_planet( i )-1) - (ascSign-1) + 12) % 12 + 1;
    }
    
    memset( nofPlanetInHouse, 0, sizeof(nofPlanetInHouse) );
    for (i=1; i<=12; i++)
        for (j=0; j<PLANET_MAX; j++)
            if ( planetHouse[j] == i ) nofPlanetInHouse[i]++;
    
    titleHeight = normalMetrics->height();
    af = 2 * titleHeight / 3;
    
    for (i=0; i<12; i++)
    {
        p.setPen( whitePen );
        p.setFont( normalFont );
        p.setBrush( Qt::NoBrush );
        xmid = 0;
        ymid = 0;
        for (j=0; j<4; j++)
        {
            poligonPoints[j].setX( inMargin + poligons[i][j+1][0]*w );
            poligonPoints[j].setY( inMargin + poligons[i][j+1][1]*h );
            xmid += (int)poligonPoints[j].x();
            ymid += (int)poligonPoints[j].y();
        }
        p.drawConvexPolygon(poligonPoints, (int)poligons[i][0][0] );
        xmid = inMargin + (xmid / (int)poligons[i][0][0]);
        ymid = inMargin + (ymid / (int)poligons[i][0][0]);
        
        // mid point correction
        if (i!=8 && i!=10) ymid -= af;
        
        // put basic labels
        sign = (((ascSign-1) + i) % 12) + 1;
        str = QString::number(i+1);
        titleWidth = normalMetrics->width(str);
        p.drawText( xmid-titleWidth, ymid-2*titleHeight/3, str );
        paint_sign( sign, xmid, ymid-2*af, af, af );
        if (i==0)
        {
            p.setFont( smallFont );
            p.drawText( xmid + af, ymid - 2*titleHeight/3, "Asc" );
        }
        
        // draw planets
        if (nofPlanetInHouse[i+1] <= 6) { u=3; v=2; }
        else { u=4; v=(int)round(nofPlanetInHouse[i+1]/4.0); }
        uu = (int)((w*0.15) / u);
        vv = (int)((h*0.15) / v);
        af2 = uu < vv ? uu : vv;
        x1 = xmid - (int)((v/2.0)*vv) - af2/2;
        y1 = ymid - af2/2;
        for (j=k=0; j<PLANET_MAX; j++)
        {
            if (planetHouse[j] != i+1) continue;
            paint_planet( j, x1+(k%u)*uu, y1+(k/u)*vv, af2, af2 );
            k++;
        }
    }
}


/****************************************************************************
 *  CLASSIC: Box Scope
 ****************************************************************************/
void
ScopeWidgetClass::paint_box_scope()
{
    static const double BS = 0.25;
    static double boxes[12][4] =
    {
        { 0.00, 0.00, 1*BS,  1*BS }, // left-top
        { 0.00, 1*BS, 1*BS,  .5-BS },
        { 0.00, 0.50, 1*BS,  .5-BS },
        { 0*00, 1-BS, 1*BS,  1*BS }, // left-bottom
        { 1*BS, 1-BS, .5-BS, 1*BS },
        { 0.50, 1-BS, .5-BS, 1*BS },
        { 1-BS, 1-BS, 1*BS,  1*BS }, // right-bottom
        { 1-BS, 0.50, 1*BS,  .5-BS },
        { 1-BS, 1*BS, 1*BS,  .5-BS },
        { 1-BS, 0*00, 1*BS,  1*BS }, // right-top
        { 0.50, 0.00, .5-BS, 1*BS },
        { 1*BS, 0.00, .5-BS, 1*BS },
    };
    int         i=0, j=0, k=0, x1=0, y1=0, bw=0, bh=0, ascSign=0, sign=0,
                af=0, af2=0, u=0, v=0, uu=0, vv=0;
    QString     str;
    int         planetHouse[PLANET_MAX+1];
    int         nofPlanetInHouse[13];
    
    af = normalMetrics->height() / 2;
    p.setFont( normalFont );
    p.setPen( whitePen );
    
    ascSign = (int)(horoscope->houses.Asc/30) + 1;
    
    for (i=0; i<PLANET_MAX; i++)
    {
        if ( i==0 || !Symbol->planetInfo[i].enabled )
        {
            planetHouse[i] = 0;
            continue;
        }
        planetHouse[i] = ((horoscope->get_sign_where_planet( i )-1) - (ascSign-1) + 12) % 12 + 1;
    }
    
    memset( nofPlanetInHouse, 0, sizeof(nofPlanetInHouse) );
    for (i=1; i<=12; i++)
        for (j=0; j<PLANET_MAX; j++)
            if ( planetHouse[j] == i ) nofPlanetInHouse[i]++;
    
    for (i=0; i<12; i++)
    {
        p.setPen( whitePen );
        p.setBrush( Qt::NoBrush );
        
        // draw rectangle
        x1 = (int)(inMargin + boxes[i][0] * w);
        y1 = (int)(inMargin + boxes[i][1] * h);
        bw = (int)(boxes[i][2] * w);
        bh = (int)(boxes[i][3] * h);
        p.drawRect( x1, y1, bw, bh );
        
        // put basic labels
        x1 += 2;
        y1 += 2;
        sign = (((ascSign-1) + i) % 12) + 1;
        str = QString::number(i+1);
        p.drawText( x1, y1+2*normalMetrics->height()/3, str );
        paint_sign( sign, x1+normalMetrics->width(str)+2, y1, af, af );
        if (i==0)
        {
            p.drawText( x1+normalMetrics->width(str)+af+4,
                        y1+2*normalMetrics->height()/3,
                        "Asc" );
        }
        
        // draw planets
        y1 += normalMetrics->height();
        if (nofPlanetInHouse[i+1] <= 6) { u=3; v=2; }
        else { u=4; v=(int)round(nofPlanetInHouse[i+1]/4.0); }
        uu = bw / u;
        vv = (bh - normalMetrics->height()) / v;
        af2 = uu < vv ? uu : vv;
        for (j=k=0; j<PLANET_MAX; j++)
        {
            if (planetHouse[j] != i+1) continue;
            paint_planet( j, x1+(k%u)*uu, y1+(k/u)*vv, af2, af2 );
            k++;
        }
    }
}


/****************************************************************************
 *  Synastry
 ****************************************************************************/
void
ScopeWidgetClass::paint_synastry()
{
    const double        synastrySignBelt = 0.06;
    const double        synastryHouseBelt = 0.04;
    const double        synastryDegreeBelt = -0.005;
    const double        synastryPlanetBelt = 0.09;
    int                 middleBeltRadius = a/2 - inMargin - a/12;
    QRect               rect;
    int                 rS1=0, rS2=0, rH1=0, rH2=0, rD1=0, rD2=0, rP1=0, rP2=0;
    double              asc1=0, asc2=0;
    
    if (horoscope2 == NULL) return;
    
    asc1 = horoscope->houses.Asc;
    asc2 = horoscope2->houses.Asc;
    
    // radius of cyrcle of signs
    rS1 = middleBeltRadius - (int)(synastrySignBelt*a) - inMargin;    
    rS2 = middleBeltRadius - inMargin;
    // radius of cyrcle of houses-1 & houses-2
    rH1 = rS1 - (int)(synastryHouseBelt*a);
    rH2 = rS2 + (int)(synastryHouseBelt*a);
    // radius of degree belts
    rD1 = rH1 - (int)(synastryDegreeBelt*a);
    rD2 = rH2 + (int)(synastryDegreeBelt*a);
    // radius of planets belts
    rP1 = rD1 - (int)(synastryPlanetBelt*a);
    rP2 = rD2 + (int)(synastryPlanetBelt*a);
    
    // belt1 - signs
    p.setPen( whitePen );
    p.setBrush( Qt::NoBrush );
    p.drawEllipse( xm-rS1, ym-rS1, 2*rS1, 2*rS1 );
    p.drawEllipse( xm-rS2, ym-rS2, 2*rS2, 2*rS2 );
    draw_sign_belt( rS1, rS2, asc1 );
    
    // houses 1
    draw_houses_belt( rS1, rH1, asc1, &horoscope->houses );
    p.setPen( whitePen );
    p.drawEllipse( xm-rH1, ym-rH1, 2*rH1, 2*rH1 );
    
    // houses 2
    draw_houses_belt( rS2, rH2, asc1, &horoscope2->houses );
    p.setPen( whitePen );
    p.drawEllipse( xm-rH2, ym-rH2, 2*rH2, 2*rH2 );
    
    // degrees belt
    draw_degrees_belt( rH1, rD1, asc1 );
    draw_degrees_belt( rH2, rD2, asc1 );
    
    // planets
    draw_planets_belt( rD1, rP1, asc1, horoscope, PLANETBELT_DOUBLEENDED );
    draw_planets_belt( rD2, rP2, asc1, horoscope2, PLANETBELT_SINGLEENDED );
    
    // aspects
    draw_aspects_into_middle( rP1, asc1 );
}


/****************************************************************************
 *  Transits
 ****************************************************************************/
void
ScopeWidgetClass::paint_transits()
{
#define MAX_STEPS 200
    static double   curves[PLANET_MAX+POINT_MAX][MAX_STEPS+1];
    int             i=0, j=0, k=0, x1=0, y1=0, x2=0, y2=0, af=a/20,
                    maxSteps=100, labelSteps=10, daysOfMonth=0;
    TimeStepType    stepMode = TIMESTEP_DAY;
    char            labelVector[MAX_STEPS+1][12];
    double          ppd=(double)h/360.0; // pixel per degree
    double          ppt=(double)w/MAX_STEPS; // pixel per time
    double          asc=0, middle=0, pos=0, top=0, stepValue=1;
    PlanetClass     *planet;
    
    if (!horoscope || !horoscope2) return;
    
    asc = horoscope->houses.Asc;
    middle = asc;
    top = ROUND_DEG( middle - 180.0 );
    
    switch( transitMode )
    {
        default:
        case TRANSITMODE_MONTH:
            stepMode   = TIMESTEP_HOUR;
            stepValue  = 24.0 / 3.0;
            maxSteps   = 93;
            labelSteps = 31;
            if (horoscope2->observer.year%4 == 0)
            {
                daysOfMonth = SymbolClass::MonthInfoTable[ horoscope2->observer.month ].extraLength;
            }
            else
            {
                daysOfMonth = SymbolClass::MonthInfoTable[ horoscope2->observer.month ].length;
            }
            for (i=0; i<labelSteps; i++)
            {
                if ( i < daysOfMonth ) sprintf( labelVector[i], "%d", i+1 );
                                  else strcpy( labelVector[i], "" );;
            }
            break;
        
        case TRANSITMODE_YEAR:
            stepMode   = TIMESTEP_DAY;
            stepValue  = 3;
            maxSteps   = 122;
            labelSteps = 12;
            for (i=0; i<labelSteps; i++)
            {
                j = ((horoscope2->observer.month + i - 1) % 12) + 1;
                sprintf( labelVector[i], SymbolClass::MonthInfoTable[j].name );
                labelVector[i][3] = '1';
                labelVector[i][4] = '\0';
            }
            break;
        
        case TRANSITMODE_12YEAR:
            stepMode   = TIMESTEP_MONTH;
            stepValue  = 2;
            maxSteps   = 72;
            labelSteps = 12;
            for (i=0; i<labelSteps; i++)
                sprintf( labelVector[i], "%d", horoscope2->observer.year + i );
            break;
        
        case TRANSITMODE_100YEAR:
            stepMode   = TIMESTEP_YEAR;
            stepValue  = 1;
            maxSteps   = 100;
            labelSteps = 10;
            for (i=0; i<labelSteps; i++)
                sprintf( labelVector[i], "%d", horoscope2->observer.year + (10*i) );
            break;
    }
    
    // calculate pixel per time" value
    ppt = (double)w / maxSteps;
    
    // ----- put radix lines -----
    
    p.setBrush( Qt::NoBrush );
    
    // --- asc
    p.setPen( whitePen );
    pos = ROUND_DEG( top + asc );
    x1 = inMargin;
    y1 = (int)(inMargin + pos*ppd);
    x2 = inMargin + w;
    y2 = y1;
    p.drawLine( x1, y1, x2, y2 );
    
    // --- draw symbols of planets
    multiPen.setWidth( 1 );
    multiPen.setStyle( Qt::DashLine );
    p.setPen( multiPen );
    for (i=0; i<horoscope->solarSystem.numberOfPlanets; i++)
    {
        planet = horoscope->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        pos = ROUND_DEG( top + planet->Long );
        x1 = inMargin;
        y1 = (int)(inMargin + pos*ppd);
        x2 = inMargin + w;
        y2 = y1;
        multiColor.setRgb( (QRgb)Symbol->planetInfo[planet->index].color );
        multiPen.setColor( multiColor );
        p.setPen( multiPen );
        p.drawLine( x1, y1, x2, y2 );
        paint_planet( planet->index, x1, y1, af, af );
    }
    
    // ----- calculate progress curves -----
    static int year=-10000, month=-10000, day=0, mode=-1;
    static double UT=0;
    
    if (year!=horoscope2->observer.year ||
        month!=horoscope2->observer.month ||
        mode!=(int)transitMode)
    {
    	// get current time settings
        year  = horoscope2->observer.year;
        month = horoscope2->observer.month;
        day   = horoscope2->observer.day;
        UT    = horoscope2->observer.UT;
        mode  = transitMode;
        // go through the time-scale
//qDebug("tstep=%d, value=%f", stepMode, stepValue);
        for (i=0; i<maxSteps+2; i++)
        {
            horoscope2->shift_date( stepMode, stepValue );
/*
qDebug("[%i]:%04i-%02i-%02i %f",
		i,
		horoscope2->observer.year,
		horoscope2->observer.month,
		horoscope2->observer.day,
		horoscope2->observer.UT
		);
*/
            for (j=0; j<horoscope2->solarSystem.numberOfPlanets; j++)
            {
                planet = horoscope2->solarSystem.planetVector[j];
                curves[ planet->index ][ i ] = planet->Long;
            }
        }
        // restore original time settings
        horoscope2->observer.year = year;
        horoscope2->observer.month = month;
        horoscope2->observer.day = day;
        horoscope2->observer.UT = UT;
        horoscope2->observer.update();
        horoscope2->calculate_scope();
    }
    
    // ----- paint transit points ----
    int     radixPIndex=PLANET_NONE, transitPIndex=PLANET_NONE,
            transitWidth=0, transitHeight=0, transitStarts=0, transitEnds=0;
    double  radixPos=0, transitPos=0, orbit=0, diff;
    double  transitline[MAX_STEPS+1];
    
    // go through radix planets
    for (i=0; i<horoscope->solarSystem.numberOfPlanets; i++)
    {
        planet = horoscope->solarSystem.planetVector[i];
        radixPIndex = planet->index;
        if ( !Symbol->planetInfo[ radixPIndex ].enabled ) continue;
        radixPos = planet->Long;
        // go through transit planets
        for (j=0; j<horoscope2->solarSystem.numberOfPlanets; j++)
        {
            planet = horoscope2->solarSystem.planetVector[j];
            transitPIndex = planet->index;
            if ( !Symbol->planetInfo[ transitPIndex ].enabled ) continue;
            if ( !SolonConfig->transitPlanets[transitMode][ transitPIndex ] ) continue;
            orbit = Symbol->planetInfo[radixPIndex].orbit + Symbol->planetInfo[transitPIndex].orbit;
            // clear transit holding temporary vector
            for (k=0; k<maxSteps+1; k++) transitline[k] = -180;
            // go through the timeline
            for (k=0; k<maxSteps+1; k++)
            {
                transitPos = curves[transitPIndex][k];
                diff = ANGLE_SIGNED_DISTANCE( radixPos, transitPos );
                if ( ABSOLUTE(diff)<=orbit ) transitline[k] = orbit - ABSOLUTE(diff);
            }
            // draw transit ellipses / cyrcles
            transitStarts = transitEnds = 0;
            for (k=0; k<maxSteps; k++)
            {
                if ( transitline[k]<0  && transitline[k+1]>=0 ) transitStarts = k;
                if ( transitline[k]>=0 && (transitline[k+1]<0 || k+1==maxSteps) )
                {
                    transitEnds = k+1;
                    // calculate the transit length
                    transitWidth = (int)((transitEnds - transitStarts) * ppt);
                    transitHeight = (int)(orbit * ppd);
                    // calculate transit position
                    x1 = inMargin + (int)((transitStarts*ppt));
                    y1 = (int)(inMargin + ROUND_DEG( top + radixPos) * ppd);
                    // draw transit cyrcle
                    paint_transit( radixPIndex, transitPIndex,
                                   x1, y1-transitHeight/2,
                                   transitWidth, transitHeight );
                }
            }
        }
    }
    
    // ----- paint timelines -----
    for (i=0; i<labelSteps; i++)
    {
        x1 = inMargin + (int)((i*w)/(labelSteps));
        y1 = inMargin;
        x2 = x1;
        y2 = inMargin + h;
        p.setPen( housePen );
        p.drawLine( x1, y1, x2, y2 );
        p.setPen( whitePen );
        p.drawText( x2, y2-normalMetrics->height(), labelVector[i] );
    }
    
    // ----- paint progress curves -----
    multiPen.setWidth( 1 );
    multiPen.setStyle( Qt::DashLine );
    p.setPen( multiPen );
    for (i=0; i<horoscope2->solarSystem.numberOfPlanets; i++)
    {
        planet = horoscope2->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        if ( !SolonConfig->transitPlanets[transitMode][ planet->index ] ) continue;
        multiColor.setRgb( (QRgb)Symbol->planetInfo[planet->index].color );
        multiPen.setColor( multiColor );
        p.setPen( multiPen );
        
        for (j=0; j<maxSteps; j++)
        {
            pos = ROUND_DEG( top + curves[planet->index][j] );
            x1 = inMargin + (int)(j*ppt);
            y1 = (int)(inMargin + pos*ppd);
            pos = ROUND_DEG( top + curves[planet->index][j+1] );
            x2 = inMargin + (int)((j+1)*ppt);
            y2 = (int)(inMargin + pos*ppd);
            if ( !((top+curves[planet->index][j])<360 && (top+curves[planet->index][j+1])>360) )
                p.drawLine( x1, y1, x2, y2 );
        }
    }
}


/****************************************************************************
 *  Lifecyrcle
 ****************************************************************************/
void
ScopeWidgetClass::paint_lifecyrcle()
{
    const double        lifecyrcleHouseBelt = 0.06;
    const double        lifecyrcleSignBelt = 0.04;
    const double        lifecyrcleDegreeBelt = -0.005;
    const double        lifecyrclePlanetBelt = 0.09;
    int                 middleBeltRadius = (int)(a/3.2) - inMargin;
    //
    int                 rS=0, rH1=0, rH2=0, rD=0, rP=0;
    double              asc=0;
    
    asc = horoscope->houses.Asc;
    
    // radius of cyrcle of houses
    rH1 = middleBeltRadius;
    rH2 = middleBeltRadius + (int)(lifecyrcleHouseBelt*a);
    // radius of cyrcle of signs
    rS  = rH2 + (int)(lifecyrcleSignBelt*a);
    // radius of degree belts
    rD  = rS + (int)(lifecyrcleDegreeBelt*a);
    // radius of planets belts
    rP  = rD + (int)(lifecyrclePlanetBelt*a);
    
    p.setPen( whitePen );
    p.setBrush( Qt::NoBrush );
    
    // houses
    draw_houses_belt( rH1, rH2, asc, &horoscope->houses );
    p.setPen( whitePen );
    p.drawEllipse( xm-rH2, ym-rH2, 2*rH2, 2*rH2 );
    
    // signs
    draw_sign_belt( rH2, rS, asc );
    p.setPen( whitePen );
    p.drawEllipse( xm-rS, ym-rS, 2*rS, 2*rS );
    
    // degrees belt
    draw_degrees_belt( rS, rD, asc );
    
    // planets
    draw_planets_belt( rD, rP, asc, horoscope, PLANETBELT_LIFECYRCLE );
}


/****************************************************************************
 *  Basic Datas
 ****************************************************************************/
void
ScopeWidgetClass::paint_basic_datas()
{
    int                 i=0, x1=0, yBase=0;
    char                sbuf1[256]="";
    QString             qstr("");
    PlanetClass         *planet;
    
    p.setPen( whitePen );
    p.setFont( dataFont );
    
    x1 = inMargin;
    yBase = inMargin;
    
    // print date
    yBase += dataMetrics->height();
    qstr = "Date: " + QString::number( horoscope->observer.year ) + "." +
                      QString::number( horoscope->observer.month ) + "." +
                      QString::number( horoscope->observer.day ) + " " +
                      "UT=" + QString::number( horoscope->observer.UT );
    p.drawText( x1, yBase, qstr );
    // print julian day
    yBase += dataMetrics->height();
    qstr = "JD=" + QString::number( horoscope->observer.JD, 'f', 10 );
    p.drawText( x1, yBase, qstr );
    
    yBase += dataMetrics->height();
    
    // print house cusps
    for (i=0; i<12; i++)
    {
        qstr = QString::number(i+1) + " : " + QString::number( horoscope->houses.cusp[i+1] );
        x1 = inMargin;
        yBase += dataMetrics->height();
        p.drawText( x1, yBase, qstr );
    }
    
    yBase += dataMetrics->height();
    
    // print planet's text info
    for (i=0; i<horoscope->solarSystem.numberOfPlanets; i++)
    {
        planet = horoscope->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        qstr =     QString::fromUtf8(planet->name) + " : " +
                SolonMath::format_astro( planet->Long, sbuf1 );
        x1 = inMargin;
        yBase += dataMetrics->height();
        p.drawText( x1, yBase, qstr );
    }
    
}


/****************************************************************************
 *  Aspect Matrix
 ****************************************************************************/
void
ScopeWidgetClass::paint_aspect_matrix()
{
    int                 i=0, j=0, x1=0, y1=0, x2=0, y2=0, af=0, n=0,
                        index1=0, index2=0, asp=0, power=0, xBase=0, yBase=0;
    PlanetClass         *planet=NULL, *planet2=NULL;
    QString             qstr("");
    char                sbuf[64]="";
    HoroscopeClass      *hs = NULL;
    
    // create a little place for labels if aspectmatrix is a synatry/transit matrix
    if ( horoscope2 )
    {
        xBase = inMargin + dataMetrics->height() + 2;
        yBase = inMargin + dataMetrics->height() + 2;
        hs = horoscope2;
    }
    else
    {
        xBase = inMargin;
        yBase = inMargin;
        hs = horoscope;
    }
    
    // get number of enabled planets
    for (i=n=0; i<hs->solarSystem.numberOfPlanets; i++)
    {
        planet = hs->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        n++;
    }
    
    // af = size of symbol
    af = (int)((a-xBase+inMargin) / (1.2*(n+1)));
    
    p.setPen( Qt::blue );
    setFont( dataFont );
    if ( horoscope2 )
    {
        qstr = "--------" +
                QString::number( horoscope->observer.year ) + "." +
                QString::number( horoscope->observer.month ) + "." +
                QString::number( horoscope->observer.day ) + " " +
                SolonMath::format_hour( horoscope->observer.UT, sbuf ) +
                "--------";
        x1 = xBase + a/2 - dataMetrics->width(qstr)/2;
        y1 = inMargin + dataMetrics->height();
        p.drawText( x1, y1, qstr );
        //---
        qstr = "--------" +
                QString::number( horoscope2->observer.year ) + "." +
                QString::number( horoscope2->observer.month ) + "." +
                QString::number( horoscope2->observer.day ) + " " +
                SolonMath::format_hour( horoscope2->observer.UT, sbuf ) +
                "--------";
        x1 = inMargin + dataMetrics->height();
        y1 = yBase + a/2 + dataMetrics->width(qstr)/2;
        p.save();
        p.translate(x1, y1);
        p.rotate( -90 );
        p.drawText(0, 0, qstr);
        p.restore();
    }
    
    p.setPen( Qt::darkBlue );
    
    // draw cusp and left side planet lines
    for (i=0; i<hs->solarSystem.numberOfPlanets; i++)
    {
        planet = hs->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        // draw columns
        x1 = xBase + (int)((i+1)*1.2*af);
        y1 = yBase;
        paint_planet( planet->index, x1, y1, af, af, horoscope );
        // draw vertical line
        x1 -= 2;
        x2  = x1;
        y2  = yBase + (int)(1.2*(n+1)*af);
        p.drawLine( x1, y1, x2, y2 );
        // draw rows
        x1 = xBase;
        y1 = yBase + (int)((i+1)*1.2*af);
        paint_planet( planet->index, x1, y1, af, af, hs );
        // draw horizontal line
        y1 -= 2;
        x2  = xBase + (int)(1.2*(n+1)*af);
        y2  = y1;
        p.drawLine( x1, y1, x2, y2 );
    }
    
    // aspect table
    for (i=0; i<hs->solarSystem.numberOfPlanets; i++)
    {
        planet = hs->solarSystem.planetVector[i];
        for (j=0; j<hs->solarSystem.numberOfPlanets; j++)
        {
            if ( !horoscope2 && j<=i ) continue;
            planet2 = horoscope->solarSystem.planetVector[j];
            index1 = planet->index;
            index2 = planet2->index;
            if ( !Symbol->planetInfo[index1].enabled ) continue;
            if ( !Symbol->planetInfo[index2].enabled ) continue;
            if ( (asp=hs->aspects.matrix[index1][index2]) != ASPECT_NONE )
            {
                power = hs->aspects.powerMatrix[index1][index2];
                if ( !Symbol->aspectInfo[asp].enabled ) continue;
                x1 = xBase + (int)((j+1)*1.2*af);
                y1 = yBase + (int)((i+1)*1.2*af);
                paint_aspect( asp, x1, y1, af, af, power );
            }
        }
    }
    
}


/****************************************************************************
 *  Quality Matrixes
 ****************************************************************************/
void
ScopeWidgetClass::paint_quality_matrices()
{
    int                 i=0, j=0, sign=0, house=0,
                        x[6]={0,0,0,0,0,0}, y[7]={0,0,0,0,0,0,0}, yBase=0, rowHeight=0,
                        mx[5][4], // (quality) matrix
                        sx[13], // sign matrix
                        hx[13], // house matrix
                        negative, positive, spring, summer, autumn, winter,
                        north, east, south, west;
    PlanetClass         *planet;
    HoroscopeClass      *hs = NULL;
    QString             qstr("");
    
    if ( horoscope2 ) hs = horoscope2;
    else hs = horoscope;
    
    // ----- calculate ------
    for (i=0; i<=12; i++) sx[i] = hx[i] = 0;
    
    // planets in signs
    for (i=0; i<hs->solarSystem.numberOfPlanets; i++)
    {
        planet = hs->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        sign = hs->get_sign_where_planet( planet->index );
        house = hs->get_house_where_planet( planet->index );
        sx[sign]++;
        hx[house]++;
    }
    sign = hs->get_sign_where_house_cusp(1);
    sx[sign-1]++;
    
    // element/quality matrix
    mx[0][0] = sx[SIGN_ARIES] + hx[1];
    mx[1][1] = sx[SIGN_TAURUS] + hx[2];
    mx[2][2] = sx[SIGN_GEMINI] + hx[3];
    mx[3][0] = sx[SIGN_CANCER] + hx[4];
    mx[0][1] = sx[SIGN_LEO] + hx[5];
    mx[1][2] = sx[SIGN_VIRGO] + hx[6];
    mx[2][0] = sx[SIGN_LIBRA] + hx[7];
    mx[3][1] = sx[SIGN_SCORPION] + hx[8];
    mx[0][2] = sx[SIGN_SAGITTARIUS] + hx[9];
    mx[1][0] = sx[SIGN_CAPRICORN] + hx[10];
    mx[2][1] = sx[SIGN_AQUARIUS] + hx[11];
    mx[3][2] = sx[SIGN_PISCES] + hx[12];
    
    // elements TOTAL
    mx[0][3] = mx[0][0] + mx[0][1] + mx[0][2];
    mx[1][3] = mx[1][0] + mx[1][1] + mx[1][2];
    mx[2][3] = mx[2][0] + mx[2][1] + mx[2][2];
    mx[3][3] = mx[3][0] + mx[3][1] + mx[3][2];
    
    // qualities TOTAL
    mx[4][0] = mx[0][0] + mx[1][0] + mx[2][0] + mx[3][0];
    mx[4][1] = mx[0][1] + mx[1][1] + mx[2][1] + mx[3][1];
    mx[4][2] = mx[0][2] + mx[1][2] + mx[2][2] + mx[3][2];
    
    // TOTAL TOTAL
    mx[4][3] = mx[4][0] + mx[4][1] + mx[4][2];
    
    // (+) (-)
    negative = sx[1] + sx[3] + sx[5] + sx[7] + sx[9] + sx[11];
    positive = sx[0] + sx[2] + sx[4] + sx[6] + sx[8] + sx[10];
    
    //(Spring) (Summer) (Autumn) (Winter)
    spring = sx[SIGN_ARIES]     + sx[SIGN_TAURUS]   + sx[SIGN_GEMINI];
    summer = sx[SIGN_CANCER]    + sx[SIGN_LEO]      + sx[SIGN_VIRGO];
    autumn = sx[SIGN_LIBRA]     + sx[SIGN_SCORPION] + sx[SIGN_SAGITTARIUS];
    winter = sx[SIGN_CAPRICORN] + sx[SIGN_AQUARIUS] + sx[SIGN_PISCES];
    
    // North, East, South, West
    north = sx[SIGN_SAGITTARIUS] + sx[SIGN_CAPRICORN] + sx[SIGN_AQUARIUS];
    east  = sx[SIGN_PISCES]      + sx[SIGN_ARIES]     + sx[SIGN_TAURUS];
    south = sx[SIGN_GEMINI]      + sx[SIGN_CANCER]    + sx[SIGN_LEO];
    west  = sx[SIGN_VIRGO]       + sx[SIGN_LIBRA]     + sx[SIGN_SCORPION];
    
    // ------ draw ------
    p.setPen( whitePen );
    p.setFont( dataFont );
    
    rowHeight = dataMetrics->height() + 4;
    
    for (i=0; i<6; i++) x[i] = inMargin + (i*w)/5;
    for (i=0; i<7; i++) y[i] = inMargin + i*rowHeight;
    
    for (i=0; i<7; i++) p.drawLine( x[0], y[i], x[5], y[i] );
    for (i=0; i<6; i++) p.drawLine( x[i], y[0], x[i], y[6] );
    
    yBase = y[0] + dataMetrics->height();
    p.drawText( x[1], yBase, tr("Cardinal") );
    p.drawText( x[2], yBase, tr("Fixed") );
    p.drawText( x[3], yBase, tr("Mutable") );
    p.drawText( x[4], yBase, tr("TOTAL") );
    
    p.drawText( x[0], y[1] + dataMetrics->height(), tr("Fire") );
    p.drawText( x[0], y[2] + dataMetrics->height(), tr("Earth") );
    p.drawText( x[0], y[3] + dataMetrics->height(), tr("Air") );
    p.drawText( x[0], y[4] + dataMetrics->height(), tr("Water") );
    p.drawText( x[0], y[5] + dataMetrics->height(), tr("TOTAL") );
    
    for (i=0; i<5; i++)
        for (j=0; j<4; j++)
        {
            qstr = QString::number( mx[i][j] );
            p.drawText( x[j+1], y[i+1]+dataMetrics->height(), qstr );
        }
    
    yBase = y[5] + rowHeight*2;
    p.drawText( x[0], yBase, tr("Positive") + ":" + QString::number(positive) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("Negative") + ":" + QString::number(negative) );
    
    yBase += rowHeight*2;
    p.drawText( x[0], yBase, tr("Spring") + ":" + QString::number(spring) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("Summer") + ":" + QString::number(summer) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("Autumn") + ":" + QString::number(autumn) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("Winter") + ":" + QString::number(winter) );
    
    yBase += rowHeight*2;
    p.drawText( x[0], yBase, tr("North") + ":" + QString::number(north) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("East") + ":" + QString::number(east) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("South") + ":" + QString::number(south) );
    yBase += rowHeight;
    p.drawText( x[0], yBase, tr("West") + ":" + QString::number(west) );
}


/****************************************************************************
 *  Planet Info
 ****************************************************************************/
            
#define GET_ALTER_PLANET_SYMS( planet, planet1, planet2 ) \
{ \
    if ( (planet) == PLANET_MERCURY ) \
    { \
        planet1 = SIGN_GEMINI; \
        planet2 = SIGN_VIRGO; \
    } \
    if ( planet == PLANET_VENUS ) \
    { \
        planet1 = SIGN_TAURUS; \
        planet2 = SIGN_LIBRA; \
    } \
}

void
ScopeWidgetClass::paint_planet_info()
{
    int planet;
    
    if ( !m_printer )
    {
        if ( cursorSelectedInfoType != INFOTYPE_PLANET )
        {
            p.setFont( normalFont );
            p.drawText( inMargin, normalMetrics->height(), tr("Click on a planet!") );
            return;
        }
        
        planet = cursorSelectedIndex;
    }
    else
    {
        planet = analysedPlanet;
    }
    
    int sign = horoscope->get_sign_where_planet( planet );
    int house = horoscope->get_house_where_planet( planet );
    
    if ( planet==PLANET_MERCURY || planet==PLANET_VENUS )
    {
        int planetSym1=0, planetSym2=0;
        GET_ALTER_PLANET_SYMS( planet, planetSym1, planetSym2 );
        paint_three_planet_cards( planetSym1, house, sign, inMargin, inMargin, w, h/2 );
        paint_three_planet_cards( planetSym2, house, sign, inMargin, inMargin+h/2, w, h/2 );
    }
    else
    {
        int planetSym = Symbol->planet_to_symbolon( planet );    
        paint_three_planet_cards( planetSym, house, sign, inMargin, inMargin, w, h );
    }
}


//  Planet Info -- helper function
void
ScopeWidgetClass::paint_three_planet_cards( int planetSym, int house, int sign,
                                            int bx, int by, int bw, int bh,
                                            int transitSym, QString topLabel )
{
    int planetInHouseSym=0, planetInSingSym=0;
    
    if ( transitSym == 0 )
    {
        planetInHouseSym = Symbol->two_sign_to_symbolon( planetSym, house );
        planetInSingSym  = Symbol->two_sign_to_symbolon( planetSym, sign );
        paint_symbolon( planetSym, bx+0.02*bw, by+0.02*bh, 0.96*bw, 0.6*bh, topLabel );
    }
    else
    {
        int transitAndRadixSym = Symbol->two_sign_to_symbolon( planetSym, transitSym );
        planetInHouseSym = Symbol->two_sign_to_symbolon( transitSym, house );
        planetInSingSym  = Symbol->two_sign_to_symbolon( transitSym, sign );
        paint_symbolon( transitAndRadixSym, bx+0.02*bw, by+0.02*bh, 0.96*bw, 0.6*bh, topLabel );
    }
    
    paint_symbolon( planetInHouseSym, bx+0.02*bw,  by+0.6*bh, 0.48*bw, 0.4*bh,
                        tr("Where?"), ALIGN_RIGHT );
    paint_symbolon( planetInSingSym, bx+0.51*bw, by+0.6*bh, 0.48*bw, 0.4*bh,
                        tr("How works?"), ALIGN_LEFT );
}


/****************************************************************************
 *  Transit Info
 ****************************************************************************/

#define CALCULATE_TRANSIT_DRAW_POS() \
{ \
        if (found > 2) \
        { \
            x1 = inMargin + (j%2) * w/2; \
            y1 = inMargin + (((int)j/2)*h)/((found+1)/2); \
        } \
        else \
        { \
            y1 = inMargin + (j*h)/found; \
        } \
        j++; \
}


void
ScopeWidgetClass::paint_transit_info()
{

    int     i=0, j=0, found=0, planets=0, radixPlanet=0, transitPlanet=0, sign=0, house=0,
            radixPlanetSym=0, transitPlanetSym=0, radixPlanetSym1=0, radixPlanetSym2=0,
            transitPlanetSym1=0, transitPlanetSym2=0, x1=0, y1=0, fw=0, fh=0;
    
    for ( i=found=0; i<(int)cursorSelectedTooltips.size(); i++ )
    {
        if ( refToolTipList->at( cursorSelectedTooltips[i] )->infoType == INFOTYPE_TRANSIT )
        {
            planets = refToolTipList->at( cursorSelectedTooltips[i] )->index;
            radixPlanet = planets % PLANET_MAX;
            transitPlanet = planets / PLANET_MAX;
            found++;
            if ( radixPlanet==PLANET_MERCURY || radixPlanet==PLANET_VENUS ) found++;
            if ( transitPlanet==PLANET_MERCURY || transitPlanet==PLANET_VENUS ) found++;
            if ( (radixPlanet==PLANET_MERCURY || radixPlanet==PLANET_VENUS) &&
                 (transitPlanet==PLANET_MERCURY || transitPlanet==PLANET_VENUS) ) found++;
        }
    }
    
    if ( !found )
    {
        p.setFont( normalFont );
        p.setPen( whitePen );
        p.drawText( inMargin, normalMetrics->height(), tr("Click on transit!") );
        return;
    }
    
    if (found > 2)
    {
        fw = w / 2;
        fh = h / ((found+1)/2);
    }
    else
    {
        fw = w;
        fh = h / found;
    }
    
    for (i=j=0; i<(int)cursorSelectedTooltips.size(); i++)
    {
        if (refToolTipList->at( cursorSelectedTooltips[i] )->infoType != INFOTYPE_TRANSIT) continue;
        
        planets = refToolTipList->at( cursorSelectedTooltips[i] )->index;
        radixPlanet = planets % PLANET_MAX;
        transitPlanet = planets / PLANET_MAX;
        sign = horoscope->get_sign_where_planet( radixPlanet );
        house = horoscope->get_house_where_planet( radixPlanet );
        
        radixPlanetSym = Symbol->planet_to_symbolon( radixPlanet );
        transitPlanetSym = Symbol->planet_to_symbolon( transitPlanet );
        
        radixPlanetSym1 = radixPlanetSym2 = transitPlanetSym1 = transitPlanetSym2 = 0;
        
        GET_ALTER_PLANET_SYMS( radixPlanet, radixPlanetSym1, radixPlanetSym2 );
        GET_ALTER_PLANET_SYMS( transitPlanet, transitPlanetSym1, transitPlanetSym2 );
        
        if (!radixPlanetSym1 && !transitPlanetSym1)
        {
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym );
        }
        else if (!radixPlanetSym1 && transitPlanetSym1)
        {
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym1 );
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym2 );
        }
        else if (radixPlanetSym1 && !transitPlanetSym1)
        {
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym1, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym );
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym2, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym );
        }
        else
        {
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym1, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym1 );
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym1, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym2 );
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym2, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym1 );
            CALCULATE_TRANSIT_DRAW_POS();
            paint_three_planet_cards( radixPlanetSym2, house, sign,
                                      x1, y1, fw, fh, transitPlanetSym2 );
        }
    }

}


/****************************************************************************
 *  Lifecyrcle Info
 ****************************************************************************/
void
ScopeWidgetClass::paint_lifecyrcle_info()
{
    int                 i=0, infoType=0, index=0, planet=0, aspect=0, sign=0, house=0,
                        planetSym1=0, planetSym2=0, aspectPlanetSym=0, h2=0;
    double              data=0, tyear=0;
    QString             str;
    ObserverClass       observer;
    
    for ( i=0; i<(int)cursorSelectedTooltips.size(); i++ )
    {
        infoType = refToolTipList->at( cursorSelectedTooltips[i] )->infoType;
        if ( infoType==INFOTYPE_PLANET || infoType==INFOTYPE_PLANETASPECT )
        {
            index = refToolTipList->at( cursorSelectedTooltips[i] )->index;
            data  = refToolTipList->at( cursorSelectedTooltips[i] )->data;
            break;
        }
    }
    
    observer = horoscope->observer;
    h2 = h - 3 * normalMetrics->height();
    
    if ( infoType == INFOTYPE_PLANET ) // planet itself
    {
        planet = index;
        sign   = horoscope->get_sign_where_planet( planet );
        house  = horoscope->get_house_where_planet( planet );
        
        if ( planet==PLANET_MERCURY || planet==PLANET_VENUS )
        {
            GET_ALTER_PLANET_SYMS( planet, planetSym1, planetSym2 );
            paint_three_planet_cards( planetSym1, house, sign,
                                      inMargin, inMargin, w, h2/2 );
            paint_three_planet_cards( planetSym2, house, sign,
                                      inMargin, inMargin+h2/2, w, h2/2 );
        }
        else
        {
            int planetSym = Symbol->planet_to_symbolon( planet );    
            paint_three_planet_cards( planetSym, house, sign,
                                      inMargin, inMargin, w, h2 );
        }
        
        data  = horoscope->get_degree_of_planet( planet );
        tyear = horoscope->get_time_at_degree( data );
        p.setPen( whitePen );
        p.setFont( normalFont );
        p.drawLine( (int)(inMargin+0.1*w), inMargin+h2, (int)(inMargin+0.9*w), inMargin+h2 );
        str = QString(tr("Age")) + ": " + QString::number( tyear );
        p.drawText( inMargin, inMargin+h2 + normalMetrics->height(), str );
        observer.shift_date( TIMESTEP_YEAR, (int)tyear );
        observer.shift_date( TIMESTEP_DAY, (tyear - (int)tyear) * 365.25 );
        str = QString(tr("Date")) + ": " + QString::number( observer.year ) + " - " +
              QString::fromUtf8( SymbolClass::MonthInfoTable[ observer.month ].name );
        p.drawText( inMargin, inMargin + h2 + 2*normalMetrics->height(), str );
    }
    else if ( infoType == INFOTYPE_PLANETASPECT ) // planet aspect
    {
        // basic datas
        planet = index % PLANET_MAX;
        aspect = index / PLANET_MAX;
        sign   = ((int)data / 30) + 1;
        house  = horoscope->get_house_at_degree( data );
        
        // aspect energy info
        aspectPlanetSym = Symbol->planet_to_symbolon( Symbol->aspectInfo[aspect].planetEnergy );
        
        // top label
        str = QString::fromUtf8( Symbol->planetInfo[planet].name ) + " + " +
              QString::fromUtf8( Symbol->aspectInfo[aspect].name );
        
        if ( planet==PLANET_MERCURY || planet==PLANET_VENUS )
        {
            GET_ALTER_PLANET_SYMS( planet, planetSym1, planetSym2 );
            paint_three_planet_cards( planetSym1, house, sign,
                                      inMargin, inMargin, w, h2/2,
                                      aspectPlanetSym, str );
            paint_three_planet_cards( planetSym2, house, sign,
                                      inMargin, inMargin+h2/2, w, h2/2,
                                      aspectPlanetSym, str );
        }
        else
        {
            int planetSym = Symbol->planet_to_symbolon( planet );
            paint_three_planet_cards( planetSym, house, sign,
                                      inMargin, inMargin, w, h2,
                                      aspectPlanetSym, str );
        }
        
        tyear = horoscope->get_time_at_degree( data );
        p.setPen( whitePen );
        p.setFont( normalFont );
        p.drawLine( (int)(inMargin+0.1*w), inMargin+h2, (int)(inMargin+0.9*w), inMargin+h2 );
        str = QString(tr("Age")) + ": " + QString::number( tyear );
        p.drawText( inMargin, inMargin+h2 + normalMetrics->height(), str );
        observer.shift_date( TIMESTEP_YEAR, (int)tyear );
        observer.shift_date( TIMESTEP_DAY, (tyear - (int)tyear) * 365.25 );
        str = QString(tr("Date")) + ": " + QString::number( observer.year ) + " - " +
                tr(SymbolClass::MonthInfoTable[ observer.month ].name);
        p.drawText( inMargin, inMargin + h2 + 2*normalMetrics->height(), str );
    }
    else
    {
        p.setPen( whitePen );
        p.setFont( normalFont );
        p.drawText( inMargin, normalMetrics->height(), tr("Click on a planet!") );
        return;
    }
}


/****************************************************************************
 *  Synastry Info
 ****************************************************************************/
void
ScopeWidgetClass::paint_synastry_info()
{    
    if ( !horoscope || !horoscope2 ) return;
    p.setFont( normalFont );
    
    QString str;
    int yBase = inMargin;
    
    p.setPen( whitePen );
    p.setFont( bigFont );
    yBase += bigMetrics->height();
    str = QString( tr("Summary") );
    p.drawText( inMargin, yBase, str );
    
    // Mars-Venus
    int signOfVenus1     = horoscope->get_sign_where_planet( PLANET_VENUS );
    int houseOfVenus1    = horoscope->get_house_where_planet( PLANET_VENUS );
    int signOfVenus2     = horoscope2->get_sign_where_planet( PLANET_VENUS );
    int houseOfVenus2    = horoscope2->get_house_where_planet( PLANET_VENUS );
    int signOfMars1      = horoscope->get_sign_where_planet( PLANET_MARS );
    int houseOfMars1     = horoscope->get_house_where_planet( PLANET_MARS );
    int signOfMars2      = horoscope2->get_sign_where_planet( PLANET_MARS );
    int houseOfMars2     = horoscope2->get_house_where_planet( PLANET_MARS );
    double mvSignPoint1  = SolonTables->m_synastryTable[signOfVenus1][signOfMars2];
    double mvSignPoint2  = SolonTables->m_synastryTable[signOfMars1][signOfVenus2];
    double mvHousePoint1 = SolonTables->m_synastryTable[houseOfVenus1][houseOfMars2];
    double mvHousePoint2 = SolonTables->m_synastryTable[houseOfMars1][houseOfVenus2];
    
    // Sun-Sun
    int signOfSun1       = horoscope->get_sign_where_planet( PLANET_SUN );
    int houseOfSun1      = horoscope->get_house_where_planet( PLANET_SUN );
    int signOfSun2       = horoscope2->get_sign_where_planet( PLANET_SUN );
    int houseOfSun2      = horoscope2->get_house_where_planet( PLANET_SUN );
    double sunSignPoint  = SolonTables->m_synastryTable[signOfSun1][signOfSun2];
    double sunHousePoint = SolonTables->m_synastryTable[houseOfSun1][houseOfSun2];
    
    // Asc-Asc
    int asc1             = horoscope->get_sign_where_house_cusp( 1 );
    int asc2             = horoscope2->get_sign_where_house_cusp( 1 );
    double ascPoint      = SolonTables->m_synastryTable[asc1][asc2];
    
    // Pluto-Pluto
    int signOfPluto1       = horoscope->get_sign_where_planet( PLANET_PLUTO );
    int houseOfPluto1      = horoscope->get_house_where_planet( PLANET_PLUTO );
    int signOfPluto2       = horoscope2->get_sign_where_planet( PLANET_PLUTO );
    int houseOfPluto2      = horoscope2->get_house_where_planet( PLANET_PLUTO );
    double plutoSignPoint  = SolonTables->m_synastryTable[signOfPluto1][signOfPluto2];
    double plutoHousePoint = SolonTables->m_synastryTable[houseOfPluto1][houseOfPluto2];
    
    p.setPen( whitePen );
    p.setFont( normalFont );
    
    // Venus-Mars
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Venus") + "-" + tr("Mars") + " (" + tr("sign") + "):  " +
                   QString::number(mvSignPoint1) );
    p.drawText( inMargin, yBase, str );
    
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Venus") + "-" + tr("Mars") + " (" + tr("house") + "):  " +
                   QString::number(mvHousePoint1) );
    p.drawText( inMargin, yBase, str );
    
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Mars") + "-" + tr("Venus") + " (" + tr("sign") + "):  " +
                   QString::number(mvSignPoint2) );
    p.drawText( inMargin, yBase, str );
    
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Mars") + "-" + tr("Venus") + " (" + tr("house") + "):  " +
                   QString::number(mvHousePoint2) );
    p.drawText( inMargin, yBase, str );
    
    // Sun
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Sun") + "-" + tr("Sun") + " (" + tr("sign") + "):  " +
                   QString::number(sunSignPoint) );
    p.drawText( inMargin, yBase, str );
    
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Sun") + "-" + tr("Sun") + " (" + tr("house") + "):  " +
                   QString::number(sunHousePoint) );
    p.drawText( inMargin, yBase, str );
    
    // Asc
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Asc") + "-" + tr("Asc") + ":  " +
                   QString::number(ascPoint) );
    p.drawText( inMargin, yBase, str );
    
    // Pluto
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Pluto") + "-" + tr("Pluto") + " (" + tr("sign") + "):  " +
                   QString::number(plutoSignPoint) );
    p.drawText( inMargin, yBase, str );
    
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Pluto") + "-" + tr("Pluto") + " (" + tr("house") + "):  " +
                   QString::number(plutoHousePoint) );
    p.drawText( inMargin, yBase, str );
    
    // summary
    yBase += inMargin + normalMetrics->height();
    str = QString( "--------------------------------------------------" );
    p.drawText( inMargin, yBase, str );
    
    double sum = mvSignPoint1 + mvSignPoint2 + mvHousePoint1 + mvHousePoint2 + 
                 sunSignPoint + sunHousePoint + ascPoint +
                 plutoSignPoint + plutoHousePoint;
                 
    double average = sum / 9.0;
    
    yBase += inMargin + normalMetrics->height();
    str = QString( tr("Average") + ":  " + QString::number( average ) );
    p.drawText( inMargin, yBase, str );
}


/****************************************************************************
 *  Synastry Info of Venus-Mars situation
 ****************************************************************************/
void
ScopeWidgetClass::paint_synastry_venusmars_info()
{
    if ( !horoscope || !horoscope2 ) return;
    
    QString str;
    int yBase = inMargin;
    
    p.setPen( whitePen );
    p.setFont( bigFont );
    yBase += bigMetrics->height();
    str = QString( tr("Mars") + "+" + tr("Venus") );
    p.drawText( inMargin, yBase, str );
    
    // Mars-Venus
    int signOfVenus1     = horoscope->get_sign_where_planet( PLANET_VENUS );
    int houseOfVenus1    = horoscope->get_house_where_planet( PLANET_VENUS );
    int signOfVenus2     = horoscope2->get_sign_where_planet( PLANET_VENUS );
    int houseOfVenus2    = horoscope2->get_house_where_planet( PLANET_VENUS );
    int signOfMars1      = horoscope->get_sign_where_planet( PLANET_MARS );
    int houseOfMars1     = horoscope->get_house_where_planet( PLANET_MARS );
    int signOfMars2      = horoscope2->get_sign_where_planet( PLANET_MARS );
    int houseOfMars2     = horoscope2->get_house_where_planet( PLANET_MARS );
    
    double mvSignPoint1  = SolonTables->m_synastryTable[signOfVenus1][signOfMars2];
    int symOfSign1       = Symbol->two_sign_to_symbolon( signOfVenus1, signOfMars2 );
    double mvSignPoint2  = SolonTables->m_synastryTable[signOfMars1][signOfVenus2];
    int symOfSign2       = Symbol->two_sign_to_symbolon( signOfMars1, signOfVenus2 );
    
    double mvHousePoint1 = SolonTables->m_synastryTable[houseOfVenus1][houseOfMars2];
    int symOfHouse1      = Symbol->two_sign_to_symbolon( houseOfVenus1, houseOfMars2 );
    double mvHousePoint2 = SolonTables->m_synastryTable[houseOfMars1][houseOfVenus2];
    int symOfHouse2      = Symbol->two_sign_to_symbolon( houseOfMars1, houseOfVenus2 );
    
    // house combination
    p.setPen( whitePen );
    p.setFont( normalFont );
    yBase += 2 * normalMetrics->height();
    str = QString( tr("House combination:") );
    p.drawText( inMargin, yBase, str );
    
    yBase += normalMetrics->height();
    paint_symbolon( symOfHouse1, inMargin, yBase, w/2-inMargin/2, h/3,
                    QString::number(mvSignPoint1) );
    paint_symbolon( symOfHouse2, w/2+inMargin/2, yBase, w/2-inMargin/2, h/3,
                    QString::number(mvSignPoint2) );
    
    // sign combination
    p.setPen( whitePen );
    p.setFont( normalFont );
    yBase += h/3 + normalMetrics->height();
    str = QString( tr("Sign combination:") );
    p.drawText( inMargin, yBase, str );
    
    yBase += normalMetrics->height();
    paint_symbolon( symOfSign1, inMargin, yBase, w/2-inMargin/2, h/3,
                    QString::number(mvHousePoint1) );
    paint_symbolon( symOfSign2, w/2+inMargin/2, yBase, w/2-inMargin/2, h/3,
                    QString::number(mvHousePoint2) );
}


/****************************************************************************
 *  Synastry Info of Sun and Ascentant
 ****************************************************************************/
void
ScopeWidgetClass::paint_synastry_sunasc_info()
{
    if ( !horoscope || !horoscope2 ) return;
    
    QString str;
    int yBase = inMargin;
    
    p.setPen( whitePen );
    p.setFont( bigFont );
    yBase += bigMetrics->height();
    str = QString( tr("Sun") + " / " + tr("Asc") );
    p.drawText( inMargin, yBase, str );
    
    // Sun-Sun
    int signOfSun1       = horoscope->get_sign_where_planet( PLANET_SUN );
    int houseOfSun1      = horoscope->get_house_where_planet( PLANET_SUN );
    int signOfSun2       = horoscope2->get_sign_where_planet( PLANET_SUN );
    int houseOfSun2      = horoscope2->get_house_where_planet( PLANET_SUN );
    double sunSignPoint  = SolonTables->m_synastryTable[signOfSun1][signOfSun2];
    double sunHousePoint = SolonTables->m_synastryTable[houseOfSun1][houseOfSun2];
    int symOfSunHouses   = Symbol->two_sign_to_symbolon( signOfSun1, signOfSun2 );
    int symOfSunSigns    = Symbol->two_sign_to_symbolon( houseOfSun1, houseOfSun2 );
    
    // Asc-Asc
    int asc1             = horoscope->get_sign_where_house_cusp( 1 );
    int asc2             = horoscope2->get_sign_where_house_cusp( 1 );
    double ascPoint      = SolonTables->m_synastryTable[asc1][asc2];
    int symOfAsc         = Symbol->two_sign_to_symbolon( asc1, asc2 );
    
    // house and sign combination of the sun
    p.setPen( whitePen );
    p.setFont( normalFont );
    yBase += 2 * normalMetrics->height();
    str = QString( tr("House and Sign combination of Sun:") );
    p.drawText( inMargin, yBase, str );
    
    yBase += normalMetrics->height();
    paint_symbolon( symOfSunHouses, inMargin, yBase, w/2-inMargin/2, h/3,
                    QString::number(sunHousePoint) );
    paint_symbolon( symOfSunSigns, w/2+inMargin/2, yBase, w/2-inMargin/2, h/3,
                    QString::number(sunSignPoint) );
    
    // sign combination
    p.setPen( whitePen );
    p.setFont( normalFont );
    yBase += h/3 + normalMetrics->height();
    str = QString( tr("Ascentant combination:") );
    p.drawText( inMargin, yBase, str );
    
    yBase += normalMetrics->height();
    paint_symbolon( symOfAsc, inMargin, yBase, w-2*inMargin, h/3,
                    QString::number(ascPoint) );
}


/****************************************************************************
 *  Synastry Info of pluto
 ****************************************************************************/
void
ScopeWidgetClass::paint_synastry_pluto_info()
{
    if ( !horoscope || !horoscope2 ) return;
    
    QString str;
    int yBase = inMargin;
    
    p.setPen( whitePen );
    p.setFont( bigFont );
    yBase += bigMetrics->height();
    str = QString( tr("Pluto") );
    p.drawText( inMargin, yBase, str );
    
    // Pluto-Pluto
    int signOfPluto1       = horoscope->get_sign_where_planet( PLANET_PLUTO );
    int houseOfPluto1      = horoscope->get_house_where_planet( PLANET_PLUTO );
    int signOfPluto2       = horoscope2->get_sign_where_planet( PLANET_PLUTO );
    int houseOfPluto2      = horoscope2->get_house_where_planet( PLANET_PLUTO );
    double plutoSignPoint  = SolonTables->m_synastryTable[signOfPluto1][signOfPluto2];
    double plutoHousePoint = SolonTables->m_synastryTable[houseOfPluto1][houseOfPluto2];
    int symOfPlutoHouses   = Symbol->two_sign_to_symbolon( signOfPluto1, signOfPluto2 );
    int symOfPlutoSigns    = Symbol->two_sign_to_symbolon( houseOfPluto1, houseOfPluto2 );
    
    // house and sign combination of the pluto
    p.setPen( whitePen );
    p.setFont( normalFont );
    yBase += 2 * normalMetrics->height();
    str = QString( tr("House and Sign combination of Pluto:") );
    p.drawText( inMargin, yBase, str );
    
    yBase += normalMetrics->height();
    paint_symbolon( symOfPlutoHouses, inMargin, yBase, w/2-inMargin/2, h/3,
                    QString::number(plutoHousePoint) );
    paint_symbolon( symOfPlutoSigns, w/2+inMargin/2, yBase, w/2-inMargin/2, h/3,
                    QString::number(plutoSignPoint) );
    
}


/******************************************************************************************
*******************************************************************************************
**                                                                                       **
**                          Classic scope drawing helper functions                       **
**                                                                                       **
*******************************************************************************************
******************************************************************************************/

void
ScopeWidgetClass::draw_aspects_into_middle( int r1, double asc )
{
    int                 i=0, j=0, n=0, x1=0, x2=0, y1=0, y2=0,
                        index1=0, index2=0;
    double              angle=0, angle2=0;
    double              _2PI = 2 * M_PI;
    double              desc=0;
    PlanetClass         *planet=NULL, *planet2=NULL;
    AspectIndexType     asp=ASPECT_NONE;
    
    desc  = ROUND_DEG( asc+180 );
    asc  *= _2PI / 360;
    desc *= _2PI / 360;
    
    n = horoscope->solarSystem.numberOfPlanets;
    
    for (i=0; i<n; i++)
    {
        planet = horoscope->solarSystem.planetVector[i];
        for (j=0; j<n; j++)
        {
            if (horoscope2)
            {
                planet2 = horoscope2->solarSystem.planetVector[j];
            }
            else
            {
                if ( j<=i ) continue;
                planet2 = horoscope->solarSystem.planetVector[j];
            }
            index1 = planet->index;
            index2 = planet2->index;
            if ( !Symbol->planetInfo[index1].enabled ) continue;
            if ( !Symbol->planetInfo[index2].enabled ) continue;
            if (horoscope2)
            {
                asp = horoscope2->aspects.matrix[index1][index2];
            }
            else
            {
                asp = horoscope->aspects.matrix[index1][index2];
            }
            if ( asp != ASPECT_NONE )
            {
                if ( !Symbol->aspectInfo[asp].enabled ) continue;
                angle = -desc + planet->Long * _2PI / 360;
                angle2 = -desc + planet2->Long * _2PI / 360;
                x1 = (int)( xm + r1 * cos(angle) );
                y1 = (int)( ym - r1 * sin(angle) * beltDirection );
                x2 = (int)( xm + r1 * cos(angle2) );
                y2 = (int)( ym - r1 * sin(angle2) * beltDirection );
                multiColor.setRgb( (QRgb)Symbol->aspectInfo[asp].color );
                multiPen.setColor( multiColor );
                multiPen.setWidth( 2 );
                if ( asp == ASPECT_MIRROR )
                {
                    multiPen.setWidth( 1 );
                    multiPen.setStyle( Qt::DashLine );
                }
                p.setPen( multiPen );
                p.drawLine( x1, y1, x2, y2 );
                multiPen.setStyle( Qt::SolidLine );
            }
        }
    }
}


void
ScopeWidgetClass::draw_planets_belt( int _r1, int _r2, double asc, HoroscopeClass *hs,
                                     PlnaetBeltType beltType )
{
    static LifecyrcleAspectsType aspectingVector[] =
    {
        { 0,   ASPECT_CONJUCT },
        { 45,  ASPECT_SEMIQUADRAT },
        { 135, ASPECT_SEMIQUADRAT },
        { 225, ASPECT_SEMIQUADRAT },
        { 315, ASPECT_SEMIQUADRAT },
        { 60,  ASPECT_SEXTIL },
        { 300, ASPECT_SEXTIL },
        { 90,  ASPECT_QUADRAT },
        { 270, ASPECT_QUADRAT },
        { 120, ASPECT_TRIGON },
        { 240, ASPECT_TRIGON },
        { 180, ASPECT_OPPOSITE },
        { 720, ASPECT_MIRROR }
    };
    
    int                 i=0, j=0, k=0, n=0, x1=0, x2=0, y1=0, y2=0,
                        af=0, xf=0, yf=0, r0=0, r01=0, r1=0, r2=0, r3=0;
    double              angle=0, angle2=0;
    double              _2PI = 2 * M_PI;
    double              desc=0;
    double              planetPlacement=0; // minimal distance between planet figures
    PlanetFigureType    *planetFigures=NULL, planetFig;
    int                 isModified=0, doMove=0, direction=0;
    PlanetClass         *planet=NULL;
    
    desc  = ROUND_DEG( asc+180 );
    asc  *= _2PI / 360;
    desc *= _2PI / 360;
    
    // -- basic parameters
    n = hs->solarSystem.numberOfPlanets;
    af = (int)((ABSOLUTE(_r2 - _r1) / 2.1)); // size of planet glyphs
    r0  = _r1;                  // cyrcle of degrees
    r01 = _r1+(_r2-_r1)/4;      // planet glyph "outside" point
    r1  = _r1+2*(_r2-_r1)/4;    // planet glyph
    r2  = _r1+3*(_r2-_r1)/4;    // planet glyph "inside" point
    r3  = _r2;                  // planet pos. inside point
    
    // -- make distance between planets
    planetFigures = new PlanetFigureType[ n * DIM_OF(aspectingVector) ];
    // ---- put planets and it's positions to planetFigures vector
    for (i=j=0; i<n; i++)
    {
        planet = hs->solarSystem.planetVector[i];
        if ( !Symbol->planetInfo[ planet->index ].enabled ) continue;
        // planet itself
        planetFigures[j].planetIndex = planet->index;
        planetFigures[j].planetLong = planet->Long;
        planetFigures[j].anglePos = planet->Long;
        planetFigures[j].aspect = ASPECT_CONJUCT;
        j++;
        if ( beltType == PLANETBELT_LIFECYRCLE )
        {
            // planet aspects
            for (k=1; k<(int)DIM_OF(aspectingVector); k++)
            {
                if (aspectingVector[k].aspect == ASPECT_MIRROR)
                {
                    angle = ROUND_DEG( 360.0 - planet->Long );
                }
                else
                {
                    angle = ROUND_DEG( planet->Long + aspectingVector[k].angleShift );
                }
                planetFigures[j].planetIndex = planet->index;
                planetFigures[j].planetLong = angle;
                planetFigures[j].anglePos = angle;
                planetFigures[j].aspect = aspectingVector[k].aspect;
                j++;
            }
        }
    }
    n = j; // recalculated 'n' according to disabled planets and additional aspects
    // ---- sort planetFigures vector
    for (i=0; i<n; i++)
        for (j=0; j<n-1; j++)
        {
            if ( planetFigures[j].anglePos > planetFigures[j+1].anglePos )
            {
            planetFig = planetFigures[j];
            planetFigures[j] = planetFigures[j+1];
            planetFigures[j+1] = planetFig;
            }
        }
    // ---- calculate the distanced positions of planet figures
    // recalculate "af" if too much object is present
    if ( _2PI*r1 < n*af ) af = (int)(_2PI*r1/n);
    // calculate the place of a planet in degrees
    planetPlacement = (double)af / (_2PI*r1/360.0);
    // do rearrangement
    k = 0;
    do {
        isModified = 0;
        for (i=0; i<n; i++)
        {
            j = i+1;
            doMove = 0;            
            if ( j < n )
            {
                if ( planetFigures[j].anglePos - planetFigures[i].anglePos < planetPlacement )
                {
                    doMove = 1;
                }
            }
            else // end of zodiac cyrcle
            {
                j = 0;
                if ( (planetFigures[j].anglePos+360) - planetFigures[i].anglePos < planetPlacement )
                {
                    doMove = 1;
                }
            }
            if ( doMove )
            {
                planetFigures[j].anglePos += 0.1*planetPlacement;
                planetFigures[i].anglePos -= 0.1*planetPlacement;
                isModified++;
            }
        }
        k++;
    } while ( isModified && k<50 );
    // ---- normalize planet figures positions to 360deg  
    for (i=0; i<n; i++) planetFigures[i].anglePos = ROUND_DEG( planetFigures[i].anglePos );
    
    // -- paint planets
    for (i=0; i<n; i++)
    {
        p.setPen(Qt::darkGray);
        angle = -desc + planetFigures[i].anglePos * _2PI / 360;
        angle2 = -desc + planetFigures[i].planetLong * _2PI / 360;
        // draw small lines
        if (beltType == PLANETBELT_DOUBLEENDED)
        {
            // draw small line between planet and representator point of planet
            x1 = (int)( xm + r2 * cos(angle) );
            y1 = (int)( ym - r2 * sin(angle) * beltDirection );
            x2 = (int)( xm + r3 * cos(angle2) );
            y2 = (int)( ym - r3 * sin(angle2) * beltDirection );
            p.drawLine( x1, y1, x2, y2 );
        }
        // draw small line to begining direction
        x1 = (int)( xm + r01 * cos(angle) );
        y1 = (int)( ym - r01 * sin(angle) * beltDirection );
        x2 = (int)( xm + r0 * cos(angle2) );
        y2 = (int)( ym - r0 * sin(angle2) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
        // draw position and aspect information if needed
        if (beltType == PLANETBELT_LIFECYRCLE)
        {
            // draw aspect type and planet
            if (planetFigures[i].aspect == ASPECT_CONJUCT)
            {
                x1 = (int)( xm + r1 * cos(angle) ) - af/2;
                y1 = (int)( ym - r1 * sin(angle) * beltDirection ) - af/2;
                paint_planet( planetFigures[i].planetIndex, x1, y1, af, af, hs );
            }
            else
            {
                direction = ((r3 - r1) < 0) ? -1 : 1;
                x1 = (int)( xm + (r1 + direction * af) * cos(angle) ) - af/2;
                y1 = (int)( ym - (r1 + direction * af) * sin(angle) * beltDirection ) - af/2;
                x2 = (int)( xm + (r1 + direction * 2*af) * cos(angle) ) - af/2;
                y2 = (int)( ym - (r1 + direction * 2*af) * sin(angle) * beltDirection ) - af/2;
                paint_aspect( planetFigures[i].aspect, x1, y1, af, af );
                paint_planet( planetFigures[i].planetIndex, x2, y2, af, af,
                              hs, planetFigures[i].aspect, planetFigures[i].planetLong );
            }
        }
        else
        {
            // draw symbol of planet
            xf = (int)( xm + r1 * cos(angle) ) - af/2;
            yf = (int)( ym - r1 * sin(angle) * beltDirection ) - af/2;
            paint_planet( planetFigures[i].planetIndex, xf, yf, af, af, hs );
        }
    }
}


void
ScopeWidgetClass::draw_sign_belt( int r1, int r2, double asc )
{
    int       i=0, x1=0, x2=0, y1=0, y2=0, af=0, xf=0, yf=0;
    double    angle=0, angle2=0;
    double    _2PI = 2 * M_PI;
    double    desc=0;
    int       r12 = (r1 + r2) / 2;
    
    desc  = ROUND_DEG( asc+180 );
    asc  *= _2PI / 360;
    desc *= _2PI / 360;
    
    af = (int)(ABSOLUTE(r2-r1)/1.41);
    
    p.setPen( whitePen );
    
    for (i=0; i<12; i++)
    {
        // draw line between signs
        angle = -desc + (_2PI * i / 12.0);
        x1 = (int)( xm + r1 * cos(angle) );
        y1 = (int)( ym - r1 * sin(angle) * beltDirection );
        x2 = (int)( xm + r2 * cos(angle) );
        y2 = (int)( ym - r2 * sin(angle) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
        // draw sign figure
        angle2 = -desc + (_2PI * (i+0.5) / 12.0 );
        xf = (int)( xm + r12 * cos(angle2) ) - af/2;
        yf = (int)( ym - r12 * sin(angle2) * beltDirection ) - af/2;
        paint_sign( i+1, xf, yf, af, af );
    }
}


void
ScopeWidgetClass::draw_houses_belt( int r1, int r2, double asc, HouseClass *houses )
{
    int       i=0, x1=0, x2=0, y1=0, y2=0;
    double    angle=0, angle2=0;
    double    _2PI = 2 * M_PI;
    double    desc=0;
    int       r12 = (r1 + r2) / 2;
    
    desc  = ROUND_DEG( asc+180 );
    asc  *= _2PI / 360;
    desc *= _2PI / 360;
    
    p.setPen( whitePen );
    p.setFont( smallFont );
    
    for (i=0; i<12; i++)
    {
        // drawing angle of cusp of current house
        angle  = M_PI + ( houses->cusp[i+1] * _2PI / 360.0 ) - asc;
        // drawing angle of cusp of next house
        angle2 = M_PI + ( houses->cusp[ i+2<=12 ? i+2 : 1 ] * _2PI / 360.0 ) - asc;
        if (angle2 < angle) angle2 += _2PI;
        angle2 = (angle + angle2) / 2;
        // draw separator line
        x1 = (int)( xm + r1 * cos(angle) );
        y1 = (int)( ym - r1 * sin(angle) * beltDirection );
        x2 = (int)( xm + r2 * cos(angle) );
        y2 = (int)( ym - r2 * sin(angle) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
        // draw the number of cusp
        x1 = (int)( xm + r12 * cos(angle2) );
        y1 = (int)( ym - r12 * sin(angle2) * beltDirection );
        QString numStr = QString::number(i+1);
        p.drawText( x1-smallMetrics->width(numStr)/2, y1+smallMetrics->height()/2-2, numStr );
    }
}


void
ScopeWidgetClass::draw_degrees_belt( int r1, int r2, double asc )
{
    int        i=0, x1=0, x2=0, y1=0, y2=0;
    double    angle=0;
    double    _2PI = 2 * M_PI;
    double    desc;
    
    desc  = ROUND_DEG( asc+180 );
    asc  *= _2PI / 360;
    desc *= _2PI / 360;
    
    p.setPen(Qt::darkGray);
    for (i=0; i<360; i++)
    {
        angle = -desc + ( _2PI * i / 360.0 );
        x1 = (int)( xm + r1 * cos(angle) );
        y1 = (int)( ym - r1 * sin(angle) * beltDirection );
        x2 = (int)( xm + r2 * cos(angle) );
        y2 = (int)( ym - r2 * sin(angle) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
    }
    if (r2<r1) r2-=2;
    if (r2>r1) r2+=2;
    whitePen.setWidth(1);
    p.setPen(whitePen);
    for (i=0; i<72; i++)
    {
        angle = -desc + (_2PI * i / 72.0);
        x1 = (int)( xm + r1 * cos(angle) );
        y1 = (int)( ym - r1 * sin(angle) * beltDirection );
        x2 = (int)( xm + r2 * cos(angle) );
        y2 = (int)( ym - r2 * sin(angle) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
    }
    whitePen.setWidth(2);
    p.setPen(whitePen);
    for (i=0; i<12; i++)
    {
        angle = -desc + (_2PI * i / 12.0);
        x1 = (int)( xm + r1 * cos(angle) );
        y1 = (int)( ym - r1 * sin(angle) * beltDirection );
        x2 = (int)( xm + r2 * cos(angle) );
        y2 = (int)( ym - r2 * sin(angle) * beltDirection );
        p.drawLine( x1, y1, x2, y2 );
    }
    whitePen.setWidth(1);
}


/******************************************************************************************
*******************************************************************************************
**                                                                                       **
**                                Frontend for symbol paint                              **
**                                                                                       **
*******************************************************************************************
******************************************************************************************/

void
ScopeWidgetClass::clear_tooltip_list()
{
    while (!toolTipList.isEmpty())
        delete toolTipList.takeFirst();
}


QRect
ScopeWidgetClass::getTooltipRect( double x, double y, double w, double h )
{
    QRect rect( (int)((x + translateX) * scaleXY), (int)((y + translateY) * scaleXY),
                (int)(w * scaleXY), (int)(h * scaleXY) );
    return rect;
}


void
ScopeWidgetClass::paint_sign( int sign, double x, double y, double w, double h )
{
    ToolTipControl        *tip = new ToolTipControl;
    
    tip->rect = getTooltipRect( x, y, w, h );
    tip->str = tr("SIGN:") + QString::fromUtf8(Symbol->signInfo[sign].name);
    tip->infoType = INFOTYPE_SIGN;
    tip->index = sign;
    toolTipList << tip;
    
    if ( m_printer )
    {
        QBrush bru = p.brush();
        p.setBrush( Qt::SolidPattern );
        p.fillRect( x, y, w, h, QColor( SolonConfig->backgroundColor ) );
        p.setBrush( bru );
    }
    
    Symbol->paint_sign( p, sign, x, y, w, h );
}


void
ScopeWidgetClass::paint_planet( int planetIndex, double x, double y, double w, double h,
                                HoroscopeClass *hs, int aspect, double longitude )
{
    char                sbuf1[64]="", sbuf2[64]="";
    PlanetClass         *planet = NULL;
    ToolTipControl      *tip = new ToolTipControl;
    
    if ( hs==NULL ) hs = horoscope;
    if ( hs==NULL ) return;
    
    for (int i=0; i<hs->solarSystem.numberOfPlanets; i++)
        if (hs->solarSystem.planetVector[i]->index == planetIndex)
        {
            planet = hs->solarSystem.planetVector[i];
            break;
        }
    
    if (planet == NULL) return;
    
    tip->rect = getTooltipRect( x, y, w, h );
    
    if ( aspect == ASPECT_NONE )
    {
        tip->str = QString( tr("PLANET") + ": " +
            QString::fromUtf8(planet->name) + "\n" +
            "*" + tr("Longitude") + ": " +
            SolonMath::format_deg( planet->Long, sbuf1 ) + "\n" +
            "*" + tr("Latitude") + ": " +
            SolonMath::format_deg( planet->Lat, sbuf2 ) + "\n" +
            "*" + tr("Sign") + ": " +
            QString::fromUtf8(
                Symbol->signInfo[ hs->get_sign_where_planet( planet->index ) ].name ) +
            "\n" +
            "*" + tr("House") + ": " +
            QString::number( hs->get_house_where_planet( planet->index ) )
            );
        tip->infoType = INFOTYPE_PLANET;
        tip->index = planetIndex;
    }
    else // planet aspect
    {
        tip->str = QString( tr("PLANET-ASPECT") + ": " +
            QString::fromUtf8( planet->name ) + " - " +
            QString::fromUtf8( Symbol->aspectInfo[aspect].name ) + "\n" +
            "*" + tr("Longitude") + ": " +
            SolonMath::format_deg( longitude, sbuf1 ) + "\n" +
            "*" + tr("Sign") + ": " +
            QString::fromUtf8(
                Symbol->signInfo[ ((int)ROUND_DEG(longitude)/30) + 1 ].name ) +
            "\n" +
            "*" + tr("House") + ": " +
            QString::number( hs->get_house_at_degree( longitude ) )
            );
        tip->infoType = INFOTYPE_PLANETASPECT;
        tip->index = planetIndex + (PLANET_MAX * aspect);
        tip->data = longitude;
    }
    
    toolTipList << tip;
    
    Symbol->paint_planet( p, planetIndex, x, y, w, h );
}


void
ScopeWidgetClass::paint_aspect( int aspectIndex, double x, double y, double w, double h,
                                int power )
{
    ToolTipControl        *tip = new ToolTipControl;
    
    if (aspectIndex<=ASPECT_NONE || aspectIndex>=ASPECT_MAX) return;
    
    tip->rect = getTooltipRect( x, y, w, h );
    tip->str = QString( tr("ASPECT") + ": " +
                QString::fromUtf8( Symbol->aspectInfo[aspectIndex].name ) + " (" +
                ((aspectIndex == ASPECT_MIRROR) ? "mir" :
                    ( QString::number( Symbol->aspectInfo[aspectIndex].angle ) ) ) + ")\n" );
    if (power <= 100) tip->str += "*" + tr("Power") + ": " + QString::number( power ) + "%";
    tip->infoType = INFOTYPE_ASPECT;
    tip->index = aspectIndex;
    toolTipList << tip;
    
    if ( power <= 100 )
    {
        // draw power measurement bar
        p.setPen( Qt::blue );
        p.setBrush( Qt::blue );
        //p.setBrush( Qt::SolidPattern );
        p.drawRect( (int)x, (int)(y+h-2), (int)((w*power)/100), 2 );
    }
    
    if ( m_printer )
    {
        QBrush bru = p.brush();
        p.setBrush( Qt::SolidPattern );
        p.fillRect( x+1, y, w-2, h-2, QColor( SolonConfig->backgroundColor ) );
        p.setBrush( bru );
    }
    
    // draw symbol
    Symbol->paint_aspect( p, aspectIndex, x+1, y, w-2, h-2 );
}


void
ScopeWidgetClass::paint_symbolon( int symbolon, double x, double y, double w, double h,
                QString topLabel, AlignType align, VAlignType valign )
{
    paint_symbolon( symbolon, x, y, w, h, topLabel, "", align, valign );
}


void
ScopeWidgetClass::paint_symbolon( int symbolon, double x, double y, double w, double h,
                QString topLabel, QString topLabel2, AlignType align, VAlignType valign )
{
    ToolTipControl        *tip = new ToolTipControl;
    
    tip->rect = getTooltipRect( x, y, w, h );
    tip->str = QString("SYMBOLON") + ": " + QString::fromUtf8(Symbol->symbolonInfo[symbolon].name) +
                + "\n" + Symbol->symbolonInfo[symbolon].description.summary;
    tip->strDetailed =
        Symbol->symbolonInfo[symbolon].description.general + "\n" +
        Symbol->symbolonInfo[symbolon].description.problem + "\n" +
        Symbol->symbolonInfo[symbolon].description.way + "\n" +
        Symbol->symbolonInfo[symbolon].description.outcome;
    tip->infoType = INFOTYPE_SYMBOLON;
    tip->index = symbolon;
    toolTipList << tip;
    
    Symbol->paint_symbolon( p, symbolon, x, y, w, h, topLabel, topLabel2, align, valign );
}


void
ScopeWidgetClass::paint_transit( int radixPlanet, int transitPlanet,
                                 double x, double y, double w, double h,
                                 QString label )
{
    ToolTipControl      *tip = new ToolTipControl;
    QColor              mixedColor;
    unsigned int        mixedUColor;
    
    tip->rect = getTooltipRect( x, y, w, h );
    tip->str = tr("TRANSIT") + ": " +
                QString::fromUtf8(Symbol->planetInfo[radixPlanet].name) + " + " +
                QString::fromUtf8(Symbol->planetInfo[transitPlanet].name) + label;
    tip->infoType = INFOTYPE_TRANSIT;
    tip->index = radixPlanet + transitPlanet * (int)PLANET_MAX;
    toolTipList << tip;
    
    mixedUColor = UINT_COLOR_MIX( Symbol->planetInfo[radixPlanet].color,
                                  Symbol->planetInfo[transitPlanet].color );
    mixedColor.setRgb( UINT_GET_RED(mixedUColor),
                       UINT_GET_GREEN(mixedUColor),
                       UINT_GET_BLUE(mixedUColor),
                       0x80 );
    
    p.setPen( Qt::NoPen );
    p.setBrush( Qt::SolidPattern );
    p.setBrush( mixedColor );
    p.drawEllipse( (int)x, (int)y, (int)w, (int)h );
}
