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


#ifndef SOLONTABLES_H
#define SOLONTABLES_H

#include <QObject>
#include <QString>

#include "solon_global.h"


class SolonTablesClass : public QObject
{
    Q_OBJECT;

public:

    double		m_synastryTable[SIGN_MAX][SIGN_MAX];

    SolonTablesClass( QString aSharePath );
    ~SolonTablesClass();
    
    void load_synastry_table();

private:

	QString		m_sharePath;

};

extern SolonTablesClass        *SolonTables;

#endif
