gen_pythia8() {
    case $1 in
	run)
	    PACKAGES="Sacrifice/v1.0.0-1,pythia/v8211pre-7"

            run_in_env run-pythia --collision-energy ${ENERGY} -i ${SCRIPTDIR}/gen/pythia8/params.txt -c "Tune:pp=${TUNE:-5}" -n ${NEV} -o ${HEPMCFILENAME}
	    ;;

	*)
	    help "Pythia 8"
	    ;;
    esac
}
