gen_herwig(){
    case $1 in
    run)
        PACKAGES="Herwig::v7.1.2-alice1-3"

        python3 $(dir_gen)/generate_hwgin.py --herwigfile herwig.in --hepmcfile ${HEPMCFILENAME} --tune ${TUNE} --energy ${ENERGY} --numevents ${NEV}
        cp_input PPCollider.in .
        cp_input SoftModel.in .
        cp_input SoftTune.in .
        if [ "x${TUNE}" == "xmb" ]; then cp_input MB.in .; fi

        run_in_env 'Herwig --repo=${HERWIG_ROOT}/share/Herwig/HerwigDefaults.rpo read herwig.in' > setup.log
        run_in_env 'Herwig --repo=${HERWIG_ROOT}/share/Herwig/HerwigDefaults.rpo run -N ${NEV} --seed ${SEED}' > sim.log
        ;;
    *)
        help "Herwig 7"
        ;;
    esac
}