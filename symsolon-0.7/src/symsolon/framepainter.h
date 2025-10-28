/*
 * SqadView
 * (C) MEDISO Ltd., HUNGARY
 */

#ifndef _FRAMEPAINTER_H
#define _FRAMEPAINTER_H

#include <QWidget>
#include <QPainter>
#include <QEvent>

class FramePainterClass : public QWidget
{
	Q_OBJECT;
	
public:
	FramePainterClass() {};
	~FramePainterClass() {};
	
	void paintEvent(QPaintEvent *e);
	bool event( QEvent *event );
	
signals:

	void paintFrame( QWidget*, QPaintEvent* );
	void frameEvent( QEvent* );

};

#endif
