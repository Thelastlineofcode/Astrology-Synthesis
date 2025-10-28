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
#include "synastrychooser.h"

#include "client.h"

SynastryChooserClass::SynastryChooserClass(QWidget *parent) : StudioWindowClass(parent)
{
    int                i=0;
    ClientClass        *client=NULL;
    QString            qstr("");
    
    UI_TO_WORKSPACE( new Ui::SynastryChooserForm() );
    set_user_info("SynastryChooserClass");
    
    StudioWindowClass *swin = (StudioWindowClass*)parent;
    if (!swin || swin->userInfo!="ClientClass") return;
    ClientClass *pClient = (ClientClass*)swin;
    m_ui->label->setText( pClient->get_name() + " @ " + pClient->get_birth() );
    
    // fill up partner combo box
    for (i=0; i<SymSolon->clientList.count(); i++)
    {
        client = (ClientClass*)SymSolon->clientList.at(i);
        if (client == NULL) continue;
        qstr = client->get_name() + " @ " + client->get_birth();
        m_ui->partner_combo->addItem( qstr, qVariantFromValue((void*)client) );
    }
    
    // --- connect button signals ---
    connect( m_ui->ok_button, SIGNAL( clicked(void) ),
             this, SLOT( ok_button() ) );
}


SynastryChooserClass::~SynastryChooserClass()
{
}


void
SynastryChooserClass::ok_button()
{
    // get selected client
    int index = m_ui->partner_combo->currentIndex();
    QVariant v = m_ui->partner_combo->itemData( index );
    ClientClass *otherClient = (ClientClass*)v.value<void*>();
    
    // shoot synastry scope
    StudioWindowClass *swin = (ClientClass*)m_creatorWin;
    if (swin && swin->userInfo == "ClientClass")
    {
        ClientClass *client = (ClientClass*)swin;
        client->shoot_synastry_scope( otherClient );
    }
    
    close();
}

