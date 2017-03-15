gen_eposlhc() {
    case $1 in
	run)
	    PACKAGES="CRMC::v1.5.4-3"

	    case $TUNE in
		pbpb)
		    run_in_env "sed -e s#__CRMC_BASEDIR__#\$CRMC_ROOT# $(dir_gen)/crmc_template.param > crmc.param"
		    run_in_env crmc -o hepmc -p $((ENERGY / 2)) -P-$((ENERGY / 2)) -i 822080 -I 822080 -n ${NEV} -m 0 -f ${HEPMCFILENAME} > sim.log
		    ;;

		*)
		    run_in_env "sed -e s#__CRMC_BASEDIR__#\$CRMC_ROOT# $(dir_gen)/crmc_template.param > crmc.param"
		    run_in_env crmc -o hepmc -p 6500 -P-6500 -n ${NEV} -m 0 -f ${HEPMCFILENAME} > sim.log
		    ;;
	    esac
	    ;;

	*)
	    help "EPOS-LHC"
	    ;;
    esac
}
