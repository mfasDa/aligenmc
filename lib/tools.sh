dir_gen() {
    echo ${SCRIPTDIR}/gen/${GENERATOR}
}

cp_input() {
    cp $(dir_gen)/$1 .
}

run_in_env() {
    if [[ -n ${GEN_PACKAGES} ]]; then
#	    /cvmfs/alice.cern.ch/bin/alienv setenv ${GEN_PACKAGES} -c "$*"
        # Distinction needed for local builds cvmfs builds:
        # ---------------------------------------------------------------
        # In case of local builds aligenmc should not refresh the modules 
        # as this can lead to conflicts when two processes are refreshing
        # modules at the same time (local batch jobs). In case of cvmfs
        # packages alienv from cvmfs is not aware of the option --no-refresh,
        # consequently it must not be called. In order to distinguish between
        # local and cvmfs pacakges one can make use of the "::" in the name
        # of cmvfs packages
        if [ "x$(echo ${GEN_PACKAGES} | grep :: )" != "x" ]; then
            # cvmfs package
	        (eval $(alienv  printenv ${GEN_PACKAGES}) && eval $*)
        else
            # package from local build
	        (eval $(alienv --no-refresh printenv ${GEN_PACKAGES}) && eval $*)
        fi
#	    alienv setenv ${GEN_PACKAGES} -c "$*"
    else
	    /bin/bash -c "$*"
    fi
}
