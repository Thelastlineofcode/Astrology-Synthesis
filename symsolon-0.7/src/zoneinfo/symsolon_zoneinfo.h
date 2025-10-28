#ifndef _SYMSOLON_ZONEINFO_H
#define _SYMSOLON_ZONEINFO_H

#include "time.h"

#ifdef __cplusplus
extern "C" {
#endif

extern time_t symsolon_mktime( struct tm * const tmp);
extern struct tm *symsolon_localtime(const time_t * const timep);
extern struct tm *symsolon_gmtime(const time_t * const timep);
extern double symsolon_difftime(const time_t time1, const time_t time0);

extern char symsolon_tzdir[256];
extern char symsolon_tzname[256];

extern char *tzname[2];

#ifdef __cplusplus
}
#endif

#endif

