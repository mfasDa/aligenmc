gen_pythia8() {
    case $1 in
	run)
	    PACKAGES="Sacrifice/latest"

            run_in_env run-pythia --collision-energy 8000 -i AU2-CTEQ6L1 -c "SoftQCD:all=on" -n ${NEV} -o ${HEPMCFILENAME}
	    ;;

	*)
	    help "Pythia 8"
	    ;;
    esac
}
