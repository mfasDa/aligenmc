dir_gen() {
    echo ${SCRIPTDIR}/gen/${GENERATOR}
}

cp_input() {
    cp $(dir_gen)/$1 .
}

run_in_env() {
    if [[ -n ${GEN_PACKAGES} ]]; then
#	/cvmfs/alice.cern.ch/bin/alienv setenv ${GEN_PACKAGES} -c "$*"
	(eval $(alienv --no-refresh printenv ${GEN_PACKAGES}) && eval $*)
#	alienv setenv ${GEN_PACKAGES} -c "$*"
    else
	/bin/bash -c "$*"
    fi
}
