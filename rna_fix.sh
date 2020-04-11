#!/bin/bash
cat - | sed \$d |sed \$d |sed  '1d'|sed 's/ -/-/g'|sed 's/  */ /g' |tr " " "\t"
