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

#include "solontables.h"
#include "symbol.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

SolonTablesClass        *SolonTables = NULL;


SolonTablesClass::SolonTablesClass( QString aSharePath )
{
    m_sharePath = aSharePath;
    load_synastry_table();
}


SolonTablesClass::~SolonTablesClass()
{
}


void
SolonTablesClass::load_synastry_table()
{
    QString fileName = m_sharePath + "/tables/synastry.txt";
    QFile f( fileName );	
    
    if ( !f.open(QIODevice::ReadOnly | QIODevice::Text) )
    {
        QMessageBox::critical(NULL, "SymSolon", tr("Couldn't open synastry file:") +
                            "(" + fileName + ")" );
        return;
    }
    
    QString line, sign1name, sign2name;
    double point;
    int sign1, sign2;
    QRegExp exp("[+=]");
    
    QTextStream in( &f );
    
    while ( !in.atEnd() )
    {
        line = in.readLine().trimmed();
        if ( line.isEmpty() || line[0]==';' || line[0]=='#' ) continue;
        sign1name = line.section( exp, 0, 0, QString::SectionSkipEmpty ).trimmed();
        sign2name = line.section( exp, 1, 1, QString::SectionSkipEmpty ).trimmed();
        point = line.section( exp, 2, 2, QString::SectionSkipEmpty ).toDouble();
        sign1 = Symbol->english_name_to_index( INFOTYPE_SIGN, sign1name );
        sign2 = Symbol->english_name_to_index( INFOTYPE_SIGN, sign2name );
        m_synastryTable[sign1][sign2] = point;
    }
    
    f.close();
}

