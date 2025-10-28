/*
 * SqadView
 * (C) MEDISO Ltd., HUNGARY
 */

#include "framepainter.h"


void
FramePainterClass::paintEvent(QPaintEvent *e)
{
	emit paintFrame( this, e );
}


bool
FramePainterClass::event( QEvent *event )
{
	emit frameEvent( event );
	return QWidget::event( event );
}

