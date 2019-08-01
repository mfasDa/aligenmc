gen_thepeg() {
    case $1 in
	run)
	    PACKAGES="ThePEG::v2015-08-11-4"

	    sed -e "s#^\([[:space:]]*set HepMCFile:Filename\) .*\$#\1 ${HEPMCFILENAME}#" $(dir_gen)/Rope.in > thepeg.in
        cp_input LHCpp.in
	    cp_input Tune31.in .

        run_in_env 'setupThePEG -r ${THEPEG_ROOT}/lib/ThePEG/ThePEGDefaults.rpo -I ${THEPEG_ROOT}/share/Ariadne thepeg.in' > setup.log
	    run_in_env runThePEG Rope.run -N ${NEV} --seed ${SEED} > sim.log
	    ;;

	*)
	    help "ThePEG"
	    ;;
    esac
}
