gen_herwig(){
    case $1 in
    run)
        PACKAGES="Herwig::v7.2.0-4"

        cmd=$(printf "python3 %s/generate_hwgin.py --herwigfile herwig.in" $(dir_gen))
        if [ "x${HEPMCFILENAME}" != "x" ]; then cmd=$(printf "%s --hepmcfile %s" "$cmd" ${HEPMCFILENAME}); fi
        if [ "x${TUNE}" != "x" ]; then cmd=$(printf "%s --tune %s" "$cmd" ${TUNE}); fi
        if [ "x${ENERGY}" != "x" ]; then cmd=$(printf "%s --energy %s" "$cmd" ${ENERGY}); fi
        if [ "x${NEV}" != "x" ]; then cmd=$(printf "%s --numevents %s" "$cmd" ${NEV}); fi
        if [ "x${KTMIN}" != "x" ]; then cmd=$(printf "%s --ktmin %s" "$cmd" ${KTMIN}); fi
        if [ "x${KTMAX}" != "x" ]; then cmd=$(printf "%s --ktmax %s" "$cmd" ${KTMAX}); fi
        eval $cmd
        if [ "x${TUNE}" != "xmb" ]; then
            cp_input DefaultTune.in .
            cp_input SoftTune.in .
        fi


        run_in_env 'Herwig --repo=${HERWIG_ROOT}/share/Herwig/HerwigDefaults.rpo read herwig.in' > setup.log
        run_in_env 'Herwig --repo=${HERWIG_ROOT}/share/Herwig/HerwigDefaults.rpo run herwig.run -N ${NEV} --seed ${SEED}' > hwgen.log
        ;;
    *)
        help "Herwig 7"
        ;;
    esac
}
