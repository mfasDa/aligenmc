gen_herwig(){
    case $1 in
    run)
        PACKAGES="Herwig::v7.1.2-alice1-3"

        cmd=$(printf "python3 %s/generate_hwgin.py --herwigfile herwig.in" $(dir_gen))
        if [ "x${HEPMCFILENAME}" != "x" ]; then cmd=$(printf "%s --hepmcfile %s" "$cmd" ${HEPMCFILENAME}); fi
        if [ "x${TUNE}" != "x" ]; then cmd=$(printf "%s --tune %s" "$cmd" ${TUNE}); fi
        if [ "x${ENERGY}" != "x" ]; then cmd=$(printf "%s --energy %s" "$cmd" ${ENERGY}); fi
        if [ "x${NEV}" != "x" ]; then cmd=$(printf "%s --numevents %s" "$cmd" ${NEV}); fi
        eval $cmd
        cp_input PPCollider.in .
        cp_input SoftModel.in .
        cp_input SoftTune.in .
        if [ "x${TUNE}" == "xmb" ]; then cp_input MB.in .; fi

        run_in_env 'Herwig --repo=${HERWIG_ROOT}/share/Herwig/HerwigDefaults.rpo read herwig.in' > setup.log
        run_in_env 'Herwig --repo=${HERWIG_ROOT}/share/Herwig/HerwigDefaults.rpo run herwig.run -N ${NEV} --seed ${SEED}' > sim.log
        ;;
    *)
        help "Herwig 7"
        ;;
    esac
}