gen_pythia6() {
    case $1 in
	run)
	    PACKAGES="pythia6/latest,AGILe/latest"

	    run_in_env "agile-runmc Pythia6:HEAD --beams=LHC:13000 -n ${NEV} --out=${HEPMCFILENAME}"

	    ;;

	*)
	    help "Pythia 6"
	    ;;
    esac
}
