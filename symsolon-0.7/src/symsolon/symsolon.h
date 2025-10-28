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


#ifndef SYMSOLON_H
#define SYMSOLON_H

#include <QtGui/QWorkspace>
#include <QProcess>
#include <QtGui/QMainWindow>
#include <QtGui/QLineEdit>
#include <QtGui/QComboBox>

#include "solon_global.h"
#include "ui_symsolon.h"

class SymSolonClass : public QMainWindow
{
    Q_OBJECT

public:
    QMainWindow         *win;
    Ui::SymSolon        *ui;
    QWorkspace          *workspace;
    QList<QProcess*>    processList;
    QList<void*>        clientList;
    void                *actualClient;
    QComboBox           *nameWidget;     // name of actual client
    QLineEdit           *birthWidget;    // birth of actual client
    void                *preferencesWindow;
    void                *aboutSymSolonWindow;
    void                *aboutSymbolonWindow;
    void                *solonExplorerWindow;
    
    SymSolonClass();
    ~SymSolonClass();
    
    void new_process( QString &prog, QStringList &args, int aLocalProg=true );
    void close_all_process();
    void repaint_all_windows();

public slots:
    
    virtual void refresh_header();
    virtual void header_name_changed();
    virtual void new_client();
    virtual void open_client();
    virtual void modify_client();
    virtual void close_client();
    virtual void save_client();
    virtual void print_client();
    virtual void preferences();
    virtual void close_preferences();
    virtual void new_classic_scope();
    virtual void new_symbolon_table();
    virtual void new_transits_scope();
    virtual void new_life_cyrcle_scope();
    virtual void new_synastry_scope();
    virtual void about_symsolon();
    virtual void about_symbolon();
    virtual void window_activated(QWidget*);
    virtual void client_selector_changed();
    virtual void close_about_symbolon();
    virtual void close_about_symsolon();
    virtual void regenerate_windows_menu();
    virtual void explorer( InfoType t, int index );
    virtual void close_explorer();

protected:
    void closeEvent( QCloseEvent *ce );

};

extern SymSolonClass        *SymSolon;


#endif
