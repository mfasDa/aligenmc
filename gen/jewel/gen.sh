gen_jewel() {
    case $1 in
	run)
	    PACKAGES="JEWEL::v2.0.2-3"

	    sed -e "s,^\([[:space:]]*NEVENT\) .*$,\1 ${NEV}," \
		-e "s,^\([[:space:]]*HEPMCFILE\) .*$,\1 ${HEPMCFILENAME}," \
		$(dir_gen)/params-simple.dat > params.dat

	    run_in_env jewel-2.2.0-vac params.dat > sim.log
	    ;;

	*)
	    help "JEWEL"
	    ;;
    esac
}
