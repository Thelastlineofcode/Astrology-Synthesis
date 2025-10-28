/***************************************************************************
 *   Copyright (C) 2007 by Bela MIHALIK,,,                                 *
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


#include "symsolon.h"
#include "preferences.h"
#include "classicscope.h"
#include "symbolonscope.h"
#include "lifecyrclescope.h"
#include "transitscope.h"
#include "synastryscope.h"
#include "client.h"
#include "aboutsymsolon.h"
#include "aboutsymbolon.h"
#include "colorselector.h"
#include "solonexplorer.h"


SymSolonClass        *SymSolon = NULL;


SymSolonClass::SymSolonClass()
{
    unsigned int    t;
    
    // ralize main window
    ui = new Ui::SymSolon();
    ui->setupUi( this );
    
    // creating workspace in main window
    workspace = new QWorkspace;
    setCentralWidget( workspace );
    
    // --- add buttons / widgets to toolbar ---
    nameWidget = new QComboBox(ui->toolBar);
    nameWidget->setEditable(false);
    nameWidget->setMinimumWidth( 250 );
    nameWidget->setMaximumWidth( 250 );
    nameWidget->setBackgroundRole( QPalette::AlternateBase );
    nameWidget->clear();
    ui->toolBar->addWidget( nameWidget );
    //-
    birthWidget = new QLineEdit(ui->toolBar);
    birthWidget->setReadOnly(true);
    birthWidget->setMaximumWidth( 250 );
    birthWidget->setBackgroundRole( QPalette::AlternateBase );
    ui->toolBar->addWidget( birthWidget );
    //-
    QAction    *actionEdit  = ui->toolBar->addAction( tr("Display") );
    QAction    *actionSave  = ui->toolBar->addAction( tr("Save") );
    QAction    *actionClose = ui->toolBar->addAction( tr("Close") );
    
    // --- connect signals of menu ---
    connect( ui->actionNew, SIGNAL( triggered() ),
             this, SLOT( new_client() ) );
    
    connect( ui->actionOpen, SIGNAL( triggered() ),
             this, SLOT( open_client() ) );
    
    connect( ui->actionModify, SIGNAL( triggered() ),
             this, SLOT( modify_client() ) );
    
    connect( ui->actionClose, SIGNAL( triggered() ),
             this, SLOT( close_client() ) );
    
    connect( ui->actionSave, SIGNAL( triggered() ),
             this, SLOT( save_client() ) );
    
    connect( ui->actionPrint, SIGNAL( triggered() ),
             this, SLOT( print_client() ) );
    
    connect( ui->actionQuit, SIGNAL( triggered() ),
             this, SLOT( close() ) );
    
    connect( ui->actionClassic_Scope, SIGNAL( triggered() ),
             this, SLOT( new_classic_scope() ) );
    
    connect( ui->actionSymbolon_Table, SIGNAL( triggered() ),
             this, SLOT( new_symbolon_table() ) );
    
    connect( ui->actionAbout_SymSolon, SIGNAL( triggered() ),
             this, SLOT( about_symsolon() ) );
    
    connect( ui->actionAbout_Symbolon, SIGNAL( triggered() ),
             this, SLOT( about_symbolon() ) );
    
    connect( ui->actionPreferences, SIGNAL( triggered() ),
             this, SLOT( preferences() ) );
    
    connect( ui->actionTransits, SIGNAL( triggered() ),
             this, SLOT( new_transits_scope() ) );
    
    connect( ui->actionLife_Cyrcle, SIGNAL( triggered() ),
             this, SLOT( new_life_cyrcle_scope() ) );
    
    connect( ui->actionSynastry, SIGNAL( triggered() ),
             this, SLOT( new_synastry_scope() ) );
    
    connect( ui->menuWindow, SIGNAL( aboutToShow() ),
             this, SLOT( regenerate_windows_menu() ) );
    
    // --- connect signal of toolbar ---
    connect( nameWidget, SIGNAL( currentIndexChanged(int) ),
             this, SLOT( client_selector_changed() ) );
    
    connect( actionEdit, SIGNAL( triggered() ),
             this, SLOT( modify_client() ) );
    
    connect( actionSave, SIGNAL( triggered() ),
             this, SLOT( save_client() ) );
             
    connect( actionClose, SIGNAL( triggered() ),
             this, SLOT( close_client() ) );
    
    // --- connect signal of workspace ---
    connect( workspace, SIGNAL( windowActivated(QWidget*) ),
             this, SLOT( window_activated(QWidget*) ) );
    
    // general stuff
    t = time( NULL );
    srand( t );
    preferencesWindow = NULL;
    aboutSymSolonWindow = NULL;
    aboutSymbolonWindow = NULL;
    actualClient = NULL;
    solonExplorerWindow = NULL;
}


void
SymSolonClass::window_activated( QWidget *w )
{
    if (w==NULL) return;
    QWidget *creator = ((StudioWindowClass*)w)->getCreator();
    if (creator == NULL) return;
    ClientClass *client = (ClientClass*)creator;
    if (client == NULL) return;
    actualClient = (void*)client;
    refresh_header();
}


SymSolonClass::~SymSolonClass()
{
    if (solonExplorerWindow) ((QWidget*)solonExplorerWindow)->close();
}


void
SymSolonClass::new_client()
{
    ClientClass  *client = new ClientClass();
    clientList << (void*)client;
    actualClient = (void*)client;
    client->setCreator( client );
    client->create();
    client->show();
    nameWidget->addItem( QT_TR_NOOP("<new-client>"), QVariant::fromValue(actualClient) );
    refresh_header();
}


void
SymSolonClass::open_client()
{
    QString fileName = QFileDialog::getOpenFileName(
                    this, "Choose a file...", SolonConfig->clientDataPath,
                    "SymSolon File (*.sol)");
    
    if ( fileName.size() <= 0 ) return;
    SolonConfig->clientDataPath = fileName.section('/', 0, -2);
    
    ClientClass  *client = new ClientClass();
    clientList << (void*)client;
    actualClient = (void*)client;
    client->setCreator( client );
    nameWidget->addItem( "", QVariant::fromValue(actualClient) );
    refresh_header();
    
    if ( client->open( fileName ) )
    {
        client->show();
    }
    else
    {
        close_client();
    }
    
    refresh_header();
}


void
SymSolonClass::modify_client()
{
    if ( nameWidget->count()<=0 || clientList.size()<=0 ) return;
    
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    
    client->show();
    workspace->setActiveWindow( client );
    
    refresh_header();
}


void
SymSolonClass::save_client()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->save();
}


void
SymSolonClass::print_client()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->print();
}


void
SymSolonClass::close_client()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    
    // close client window & it's childrens
    client->remove_all_child_windows();
    delete client;
    
    // remove client from the clientList
    clientList.removeAll( client );
    
    // remove the actual client widget from nameWidget header element
    for (int i=0; i<nameWidget->count(); i++)
        if (nameWidget->itemData(i).value<void*>() == client)
            nameWidget->removeItem( i );
    
    // slecet a different actualWidget
    if ( nameWidget->count() > 0 )
    {
        actualClient = nameWidget->itemData(0).value<void*>();
    }
    else
    {
        actualClient = NULL;
    }
    
    // refresh header info
    refresh_header();
}


void
SymSolonClass::client_selector_changed()
{
    if ( nameWidget->count()>0 && clientList.size()>0 )
    {
        int index = nameWidget->currentIndex();
        if (index >= 0)
        {
            void *selectedClient = nameWidget->itemData(index).value<void*>();
            if (actualClient != selectedClient)
            {
                actualClient = selectedClient;
                refresh_header();
                modify_client();
            }
        }
    }
}


void
SymSolonClass::preferences()
{
    if (preferencesWindow == NULL)
    {
        PreferencesClass  *preferences = new PreferencesClass();
        preferences->setCreator( NULL );
        preferences->show();
        preferencesWindow = (void*)preferences;
    }
}


void
SymSolonClass::close_preferences()
{
    preferencesWindow = (void*)NULL;
}


void
SymSolonClass::explorer( InfoType t, int index )
{
    if ( t != INFOTYPE_SYMBOLON ) return;
    
    SolonExplorerClass  *solonExplorer = NULL;
    
    if (solonExplorerWindow == NULL)
    {
        solonExplorer = new SolonExplorerClass(this);
        solonExplorer->setCreator( NULL );
        solonExplorer->scope->setHoroscope( NULL );
        solonExplorerWindow = (void*)solonExplorer;
    }
    else
    {
        solonExplorer = (SolonExplorerClass*)solonExplorerWindow;
    }
    
    if ( index >= 0 ) solonExplorer->set_card( index );
    solonExplorer->show();
}


void
SymSolonClass::close_explorer()
{
    ((SolonExplorerClass*)solonExplorerWindow)->hide();
    //solonExplorerWindow = (void*)NULL;
}


void
SymSolonClass::new_classic_scope()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->shoot_classic_scope();
}


void
SymSolonClass::new_symbolon_table()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->shoot_symbolon_table();
}


void
SymSolonClass::new_transits_scope()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->shoot_transit_scope();
}


void
SymSolonClass::new_life_cyrcle_scope()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->shoot_life_cyrcle_scope();
}


void
SymSolonClass::new_synastry_scope()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    client->shoot_synastry_chooser();
}


void
SymSolonClass::header_name_changed()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL) return;
    
    int index = nameWidget->currentIndex();
    
    nameWidget->setItemText( index, client->get_name() );
}


void
SymSolonClass::refresh_header()
{
    ClientClass  *client = (ClientClass*)actualClient;
    if (client == NULL)
    {
        nameWidget->setEditText( "" );
        nameWidget->setItemText( 0, "" );
        birthWidget->setText( "" );
        return;
    }
    
    int index = nameWidget->currentIndex();
    
    if ( actualClient != nameWidget->itemData(index).value<void*>() )
    {
        for (int i=0; i<nameWidget->count(); i++)
        {
            if (nameWidget->itemData(i).value<void*>() == actualClient)
            {
                index = i;
                break;
            }
        }
        nameWidget->setCurrentIndex( index );
    }
    
    birthWidget->setText( client->get_birth() );
}


void
SymSolonClass::about_symsolon()
{
    if (aboutSymSolonWindow == NULL)
    {
        AboutSymSolonClass  *about = new AboutSymSolonClass(this);
        about->show();
        aboutSymSolonWindow = (void*)about;
    }
}


void
SymSolonClass::about_symbolon()
{
    if (aboutSymbolonWindow == NULL)
    {
        AboutSymbolonClass  *about = new AboutSymbolonClass(this);
        about->show();
        aboutSymbolonWindow = (void*)about;
    }
}


void
SymSolonClass::close_about_symsolon()
{
    if (aboutSymSolonWindow)
    {
        ((AboutSymSolonClass*)aboutSymSolonWindow)->close();
        aboutSymSolonWindow = NULL;
    }
}


void
SymSolonClass::close_about_symbolon()
{
    if (aboutSymbolonWindow)
    {
        ((AboutSymbolonClass*)aboutSymbolonWindow)->close();
        aboutSymbolonWindow = NULL;
    }
}


void
SymSolonClass::closeEvent( QCloseEvent* )
{
    close_all_process();
}


void
SymSolonClass::new_process( QString &prog, QStringList &args, int /*aLocalProg*/ )
{
    QProcess        *proc = new QProcess();
    
    //if (aLocalProg) prog.prepend( m_programDirectory + "/" );
    //proc->setWorkingDirectory( m_projectDirectory );
    proc->start( prog, args );
    processList << proc;
}


void
SymSolonClass::close_all_process()
{
     while (!processList.isEmpty())
         delete processList.takeFirst();
}


void
SymSolonClass::regenerate_windows_menu()
{
    QWidget *widget = NULL;
    QString actionText;
    
    // get the list of workspace
    QWidgetList winList = workspace->windowList( QWorkspace::StackingOrder );
    
    // clear the current window-menu
    ui->menuWindow->clear();
    
    // create window list menu and connect signals
    for ( int i=0; i<winList.size(); i++)
    {
        widget = winList.at(i);
        actionText = QString::number(i) + "-" + widget->windowTitle();
        ui->menuWindow->addAction( actionText, widget, SLOT( setFocus() ) );
    }
}


void
SymSolonClass::repaint_all_windows()
{
    QWidgetList winList = workspace->windowList( QWorkspace::StackingOrder );
    
    for ( int i=0; i<clientList.size(); i++)
    {
        StudioWindowClass *swin = (StudioWindowClass*)clientList.at(i);
        for ( int j=0; j<STUDIOWINDOW_CHILD_MAX; j++)
        {
            StudioWindowClass *swin2 = swin->m_childWinArray[ j ];
            if (swin2 == NULL) continue;
            QString info = swin2->get_user_info();
            if ( info == "ClassicScopeClass" )
            {
                ((ClassicScopeClass*)swin2)->refresh_horoscope();
            }
            if ( info == "SymbolonScopeClass" )
            {
                ((SymbolonScopeClass*)swin2)->refresh_horoscope();
            }
            if ( info == "LifeCyrcleScopeClass" )
            {
                ((LifeCyrcleScopeClass*)swin2)->refresh_horoscope();
            }
            if ( info == "TransitScopeClass" )
            {
                ((TransitScopeClass*)swin2)->refresh_horoscope();
            }
            if ( info == "SynastryScopeClass" )
            {
                ((SynastryScopeClass*)swin2)->refresh_horoscope();
            }
        }
    }
    
    SymSolon->update();
    ui->menubar->update();
    for ( int i=0; i<winList.size(); i++)
    {
        winList.at(i)->setUpdatesEnabled(true);
        winList.at(i)->update();
        QList<QWidget*> widgets = qFindChildren<QWidget*>( winList.at(i), QString() );
        for (int i = 0; i < widgets.size(); i++)
            widgets.at(i)->update();
    }
}

