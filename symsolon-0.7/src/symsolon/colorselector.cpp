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

#include "colorselector.h"
#include "framepainter.h"

static quint32 Pixels[256][256];
QImage *Image = new QImage( (uchar*)Pixels, 256, 256, QImage::Format_RGB32  );

ColorSelectorClass::ColorSelectorClass()
{
    UI_TO_WORKSPACE( new Ui::ColorSelectorForm() );
    
    m_color = NULL;
    m_widget = NULL;
    m_localWidget = NULL;
    
    // big frame
    FramePainterClass *fpainter = new FramePainterClass();
    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget( fpainter );
    layout->setMargin( 0 );
    layout->setSpacing( 0 );
    m_ui->frame->setLayout( layout );
    
    // small frame
    FramePainterClass *fpainter2 = new FramePainterClass();
    QVBoxLayout *layout2 = new QVBoxLayout;
    layout2->addWidget( fpainter2 );
    layout2->setMargin( 0 );
    layout2->setSpacing( 0 );
    m_ui->selected_color_frame->setLayout( layout2 );
    
    // connect signals
    connect( fpainter, SIGNAL( paintFrame(QWidget*, QPaintEvent*) ),
                this, SLOT( paint_frame( QWidget*, QPaintEvent* ) ) );
    
    connect( fpainter, SIGNAL( frameEvent(QEvent*) ),
                this, SLOT( frame_event( QEvent* ) ) );
    
    connect( fpainter2, SIGNAL( paintFrame(QWidget*, QPaintEvent*) ),
                this, SLOT( paint_selectedcolor_frame( QWidget*, QPaintEvent* ) ) );
    
    connect( m_ui->ok_button, SIGNAL( clicked() ),
             this, SLOT( color_selected() ) );
    
    // fill up image with content
    quint32 x=0, y=0, c=0;
    static quint32 rainbowColors[7] =
        { 0xff0000, 0xffff00, 0x00ff00, 0x00ffff, 0x0000ff, 0xff00ff, 0xffffff };
    for ( y=0; y<256; y++ )
        for ( x=0; x<256; x++ )
        {
			c = interpolate( rainbowColors[ (6*x)/252 ],
			                 rainbowColors[ (6*x)/252 + 1 ], (x%(252/6))/(252.0/6) );
			c = lightness( c, y/256.0 );
			Pixels[y][x] = c;
        }
}


ColorSelectorClass::~ColorSelectorClass()
{
}


quint32
ColorSelectorClass::lightness( quint32 c0, float lightness )
{
    quint32 a0 = (c0 & 0xff000000) >> 24;
    quint32 r0 = (c0 & 0x00ff0000) >> 16;
    quint32 g0 = (c0 & 0x0000ff00) >> 8;
    quint32 b0 = (c0 & 0x000000ff) >> 0;
    
    r0 *= lightness;
    g0 *= lightness;
    b0 *= lightness;
    
    if ( r0 > 0xff ) r0 = 0xff;
    if ( g0 > 0xff ) g0 = 0xff;
    if ( b0 > 0xff ) b0 = 0xff;
    
    return ( (a0<<24) | (r0<<16) | (g0<<8) | (b0) );
}


quint32
ColorSelectorClass::interpolate( quint32 c0, quint32 c1, float rate )
{
    quint32 a0 = (c0 & 0xff000000) >> 24;
    quint32 r0 = (c0 & 0x00ff0000) >> 16;
    quint32 g0 = (c0 & 0x0000ff00) >> 8;
    quint32 b0 = (c0 & 0x000000ff) >> 0;
    
    quint32 a1 = (c1 & 0xff000000) >> 24;
    quint32 r1 = (c1 & 0x00ff0000) >> 16;
    quint32 g1 = (c1 & 0x0000ff00) >> 8;
    quint32 b1 = (c1 & 0x000000ff) >> 0;
    
    a0 = a0*(1.0-rate) + a1*rate;
    r0 = r0*(1.0-rate) + r1*rate;
    g0 = g0*(1.0-rate) + g1*rate;
    b0 = b0*(1.0-rate) + b1*rate;
    
    return ( (a0<<24) | (r0<<16) | (g0<<8) | (b0) );
}


void
ColorSelectorClass::paint_frame( QWidget *widget, QPaintEvent* )
{
    if ( !widget ) return;
    
    m_localWidget = widget;
    
    QPainter p( widget );
    QSize size( widget->width(), widget->height() );
    
    p.drawImage( 0, 0, Image->scaled( size ) );
}


void
ColorSelectorClass::frame_event( QEvent *event )
{
    if ( !event ) return;
    if ( !m_color ) return;
    
    int x=0, y=0;
    
    if ( event->type() == QEvent::MouseButtonPress )
    {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent *>(event);
        Qt::MouseButtons buttons = mouseEvent->buttons();
        
        if ( buttons.testFlag( Qt::LeftButton ) || buttons.testFlag( Qt::RightButton ) )
        {
            x = 0xff * mouseEvent->x() / m_localWidget->width();
            y = 0xff * mouseEvent->y() / m_localWidget->height();
            *m_color = Pixels[y][x];
            if (m_localWidget) m_ui->selected_color_frame->repaint();
        }
    }
    else if ( event->type() == QEvent::MouseMove )
    {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent *>(event);
        Qt::MouseButtons buttons = mouseEvent->buttons();
        
        if ( buttons.testFlag( Qt::LeftButton ) || buttons.testFlag( Qt::RightButton ) )
        {
            x = 0xff * mouseEvent->x() / m_localWidget->width();
            y = 0xff * mouseEvent->y() / m_localWidget->height();
            *m_color = Pixels[y][x];
            if (m_localWidget) m_ui->selected_color_frame->repaint();
        }
    }

}


void
ColorSelectorClass::paint_selectedcolor_frame( QWidget *widget, QPaintEvent* )
{
    if ( !widget ) return;
    
    static QColor whiteColor( Qt::white );
    QPainter p( widget );
    QColor *color;
    
    if (m_color)
    {
        color = new QColor( *m_color );
    }
    else
    {
        color = &whiteColor;
    }
    
    p.setBrush( Qt::SolidPattern );
    p.setPen( *color );
    p.fillRect( 0, 0, widget->width(), widget->height(), *color );
}


void
ColorSelectorClass::color_selected()
{
    if ( m_widget ) m_widget->repaint();
    m_widget = NULL;
    m_color = NULL;
    hide();
}

