dir_gen() {
    echo ${SCRIPTDIR}/${GENERATOR}
}

cp_input() {
    cp $(dir_gen)/$1 .
}

run_in_env() {
    /cvmfs/alice.cern.ch/bin/alienv setenv ${PACKAGES} -c "$*"
}
