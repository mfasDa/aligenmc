gen_pythia6() {
    case $1 in
	run)
	    PACKAGES="AGILe/v1.4.1-alice1-1,pythia6/428-1"

	    run_in_env "agile-runmc Pythia6:HEAD --beams=LHC:${ENERGY} -n ${NEV} ${TUNE:+-p PYTUNE=${TUNE}} --out=${HEPMCFILENAME}"

	    ;;

	*)
	    help "Pythia 6"
	    ;;
    esac
}
