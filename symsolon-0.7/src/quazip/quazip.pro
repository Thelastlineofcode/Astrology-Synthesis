TEMPLATE = lib

CONFIG += staticlib \
release \
warn_on
HEADERS += crypt.h \
ioapi.h \
quazipfile.h \
quazipfileinfo.h \
quazip.h \
quazipnewinfo.h \
unzip.h \
zip.h
SOURCES += ioapi.c \
quazip.cpp \
quazipfile.cpp \
quazipnewinfo.cpp \
unzip.c \
zip.c
QMAKE_CFLAGS_STATIC_LIB =
DESTDIR = output

