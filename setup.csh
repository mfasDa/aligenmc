#!/bin/tcsh -f

set called=($_)
set scriptpath=`readlink -f $called[2]`
alias aligenmc `dirname $scriptpath`/aligenmc
