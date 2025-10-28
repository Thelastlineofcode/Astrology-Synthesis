#!/bin/sh

DATE=`date +"%Y%m%d"`
NAME=symsolon-$DATE

echo $NAME

tar -c `pwd`/.. |gzip -c >../../$NAME.tgz

