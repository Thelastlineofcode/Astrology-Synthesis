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
#ifndef LOCATIONFINDER_H
#define LOCATIONFINDER_H

#include "solon_global.h"
#include "studiowindow.h"
#include "ui_locationfinder.h"

#include "stdio.h"    /* for stdout, stderr, perror */
#include "string.h"    /* for strcpy */
#include "sys/types.h"    /* for time_t */
//#include "time.h"    /* for struct tm */
#include "stdlib.h"    /* for exit, malloc, atoi */
#include "float.h"    /* for FLT_MAX and DBL_MAX */
#include "ctype.h"    /* for isalpha et al. */
#include "math.h"

class LocationFinderClass : public StudioWindowClass
{
    Q_OBJECT

public:
    Ui::LocationFinder                    *m_ui;

    LocationFinderClass();
    ~LocationFinderClass();

    static void print_tm( struct tm *tmp );
    static void get_zone_and_dst(
                    char *tzDir, char *country, double longitude, double latitude,
                    int year, int month, int day, double localTime,
                    double *zoneShift, int *dst );

public slots:

    virtual void search();
    virtual void ok();

private:
    QString                cityArchiveFileName;

};

#endif
