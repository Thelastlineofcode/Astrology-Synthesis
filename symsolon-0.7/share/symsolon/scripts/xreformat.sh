#!/bin/sh

# Reformat symsonon worfile to card-description file

LANGCHAR=en

INFILE=symbolon_${LANGCHAR}.txt
OUTFILE=symbolon_text_${LANGCHAR}.pre.xml
FINAL_OUT=symbolon_text_${LANGCHAR}.xml

echo "<!DOCTYPE SymSolonXML>" >$OUTFILE
echo "<SymSolonCardDescription>" >>$OUTFILE

CARDNUM=0



beginparagraph() {
	case "$CARDPARAGRAPH" in
		0)
			echo "    <summary>" >>$OUTFILE
			;;
		z)
			echo "    <general>" >>$OUTFILE
			;;
		a)
			echo "    <problem>" >>$OUTFILE
			;;
		b)
			echo "    <way>" >>$OUTFILE
			;;
		c)
			echo "    <outcome>" >>$OUTFILE
			;;
	esac
}

closeparagraph() {
	case "$CARDPARAGRAPH" in
		0)
			echo "    </summary>" >>$OUTFILE
			;;
		z)
			echo "    </general>" >>$OUTFILE
			;;
		a)
			echo "    </problem>" >>$OUTFILE
			;;
		b)
			echo "    </way>" >>$OUTFILE
			;;
		c)
			echo "    </outcome>" >>$OUTFILE
			;;
	esac
}

while read -r xx
do
	BEGIN2=`echo $xx |grep ^@@`
	BEGIN1=`echo $xx |grep ^@`

	[ ! "$BEGIN2" = "" ] && BEGIN1=""

	if [ ! "$BEGIN1" = "" ]
	then
		if [ ! "$CARDNUM" = "0" ]
		then
			closeparagraph;
			echo "  </card>" >>$OUTFILE
		fi
		CARDNUM=`echo $xx |cut -c 2-`
		CARDPARAGRAPH=0
		echo "CARDNUM=$CARDNUM"
		echo "  <card>" >>$OUTFILE
		echo "    <number>$CARDNUM</number>" >>$OUTFILE
		beginparagraph;
		continue;
	fi

	if [ ! "$BEGIN2" = "" ]
	then
		closeparagraph;
		CARDPARAGRAPH=`echo $xx |cut -c 3-3`
		echo "CARDPARAGRAPH=$CARDPARAGRAPH"
		beginparagraph;
		continue;
	fi

	echo "$xx" >>$OUTFILE

done <$INFILE

closeparagraph;
echo "  </card>" >>$OUTFILE

echo "</SymSolonCardDescription>" >>$OUTFILE

## wrap the file:
cat $OUTFILE |fold -w 60 -s >$FINAL_OUT


