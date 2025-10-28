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
#ifndef SCOPEWIDGET_H
#define SCOPEWIDGET_H

#include "solon_global.h"
#include "solonmath.h"
#include "studiowindow.h"
#include "symsolon.h"
#include "horoscope.h"

#include <QtGui/QPainter>
#include <QtGui/QPalette>
#include <QtGui/QBrush>
#include <QtGui/QColor>
#include <QtSvg/QSvgRenderer>
#include <QRect>
#include <QtGui/QFont>
#include <QtGui/QFontMetrics>
#include <QPrinter>


class ScopeWidgetClass : public QWidget
{
    Q_OBJECT

typedef struct ToolTipControl
{
    QRect           rect;
    QString         str;
    QString         strDetailed;
    int             infoType;
    int             index;
    double          data;
} ToolTipControl;

public:

    HoroscopeClass          *horoscope;
    HoroscopeClass          *horoscope2;
    ScopeStyleType          style;
    PlanetIndexType         analysedPlanet;
    int                     analysedSymbolon;
    TransitModeType         transitMode;
    ScopeWidgetClass        *neighbourWidget;
    
    ScopeWidgetClass( QWidget *parent=0 );
    ~ScopeWidgetClass();
    
    void setHoroscope( HoroscopeClass *h1, HoroscopeClass *h2=NULL );
    HoroscopeClass *getHoroscope();
    HoroscopeClass *getHoroscope2();
    void setStyle( ScopeStyleType s );
    void setAnalysedPlanet( PlanetIndexType p );
    void setAnalysedSymbolon( int sym );
    void refresh_horoscope();
    void set_neighbour( ScopeWidgetClass* );
    void print_begin( QPrinter* );
    void print_end();
    void call_paint_handler();
    void set_header_info( QString, QString );

signals:

    void on_object_clicked( InfoType, int );

protected:
    
    void paintEvent(QPaintEvent *event);
    bool event(QEvent *event);

private:
    // main aspects
    double                  marginRatio;
    double                  inMarginRatio;
    double                  belt1Ratio;
    double                  belt2Ratio;
    double                  belt3Ratio;
    int                     beltDirection; // +1/-1
    // length & positions
    int                     ww; // widget width
    int                     wh; // widget height
    int                     a0; // size of smaller side of original wdget
    int                     inMargin; // margin to zodiac belt 
    int                     xm; // horizontal middle
    int                     ym; // vertical middle
    int                     w; // active width
    int                     h; // active height
    int                     a; // size of smaller side of active area
    // scale & translate
    double                  scaleXY;
    int                     translateX;
    int                     translateY;
    // other graphical tools
    QPainter                p;
    QFont                   bigFont;
    QFontMetrics            *bigMetrics;
    QFont                   normalFont;
    QFontMetrics            *normalMetrics;
    QFont                   smallFont;
    QFontMetrics            *smallMetrics;
    QFont                   dataFont;
    QFontMetrics            *dataMetrics;
    QFont                   printingFont;
    QFontMetrics            *printingMetrics;
    QPen                    whitePen;
    QPen                    darkPen;
    QPen                    housePen;
    QPen                    multiPen;
    QColor                  multiColor;
    QPen                    aspectArrowPen;
    QBrush                  aspectArrowBrush;
    QList<ToolTipControl*>  toolTipList;
    QList<ToolTipControl*>  *refToolTipList;
    std::vector<int>        cursorOverTooltips;
    int                     cursorOverInfoType;
    int                     cursorOverIndex;
    std::vector<int>        cursorSelectedTooltips;
    int                     cursorSelectedInfoType;
    int                     cursorSelectedIndex;
    quint32                 m_bgColor;
    quint32                 m_fgColor;
    
    // printing
    QPrinter                *m_printer;
    QString                 m_printigLeftHeaderText;
    QString                 m_printigRightHeaderText;
    
    // classic scope paint functions
    void paint_circle_scope();
    void paint_rectangle_scope();
    void paint_box_scope();
    void paint_synastry();
    void paint_transits();
    void paint_lifecyrcle();
    
    // symbolon scope paint functions
    void paint_symbolon_asc_and_sun();
    void paint_symbolon_dialectic();
    void paint_symbolon_asc_influence();
    void paint_symbolon_sun_influence();
    void paint_symbolon_mc_influence();
    void paint_symbolon_planet_analysis( int planet );
    void paint_symbolon_planet_aspects( int basePlanet, int baseSign=SIGN_NONE, int enforceAspectPower=false );
    int planet2sign_according_to_constellation( int planet, int withPlanet=PLANET_NONE );
    void paint_symbolon_house_mandal();
    void paint_symbolon_planet_mandal( InfoType type );
    void paint_symbolon_explore();
    
    // datascope paint functions
    void paint_basic_datas();
    void paint_aspect_matrix();
    void paint_quality_matrices();
    void paint_planet_info();
    void paint_transit_info();
    void paint_synastry_info();
    void paint_lifecyrcle_info();
    void paint_synastry_venusmars_info();
    void paint_synastry_sunasc_info();
    void paint_synastry_pluto_info();

    // frontend for SymbolClass paint functions
    void paint_sign( int sign, double x, double y, double w, double h );
    void paint_planet( int planet, double x, double y, double w, double h,
                        HoroscopeClass *hs=NULL, int aspect=ASPECT_NONE, double longitude=0 );
    void paint_aspect( int aspectIndex, double x, double y, double w, double h, int power = 101 );
    void paint_symbolon( int symbolon, double x, double y, double w, double h,
                                QString topLabel = "",
                                AlignType align=ALIGN_CENTER, VAlignType valign=ALIGN_MIDDLE );
    void paint_symbolon( int symbolon, double x, double y, double w, double h,
                QString topLabel, QString topLabel2,
                AlignType align=ALIGN_CENTER, VAlignType valign=ALIGN_MIDDLE );
    void paint_transit( int radixPlanet, int transitPlanet,
                        double x, double y, double w, double h,
                        QString label = "" );
    void clear_tooltip_list();
    QRect getTooltipRect( double x, double y, double w, double h );
    void paint_three_planet_cards( int planetSym, int house, int sign,
                                   int bx, int by, int bw, int bh,
                                   int transitSym = 0, QString topLabel = "" );

    // classic horoscope drawing helper functions
    void draw_degrees_belt( int r1, int r2, double asc );
    void draw_houses_belt( int r1, int r2, double asc, HouseClass *houses );
    void draw_sign_belt( int r1, int r2, double asc );
    void draw_planets_belt( int _r1, int _r2, double asc, HoroscopeClass *hs,
                            PlnaetBeltType beltType = PLANETBELT_DOUBLEENDED );
    void draw_aspects_into_middle( int r1, double asc );
    void get_object_under_mouse( int x, int y );
    
    typedef struct _PlanetFigureType
    {
        int                 planetIndex;
        double              planetLong;
        double              anglePos;
        int                 aspect;
    } PlanetFigureType;
    
    typedef struct _LifecyrcleAspectsType
    {
        int                 angleShift;
        int                 aspect;
    } LifecyrcleAspectsType;
};

#endif
