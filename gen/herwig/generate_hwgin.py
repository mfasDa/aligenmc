#! /usr/bin/env python3

import argparse

def setupMatchBox(configwriter, process, loopprovider):
    ''' Setup MatchBox for NLO process generation

        Based on LHC-Matchbox.in
    '''
    configwriter.write("read snippets/Matchbox.in\n")
    configwriter.write("read Matchbox/StandardModelLike.in\n")
    configwriter.write("read Matchbox/DiagonalCKM.in\n")
    ## Set the order of the couplings
    configwriter.write("cd /Herwig/MatrixElements/Matchbox\n")
    configwriter.write("set Factory:OrderInAlphaS 0\n")
    configwriter.write("set Factory:OrderInAlphaEW 2\n")
    ## Select the process
    ## You may use identifiers such as p, pbar, j, l, mu+, h0 etc.
    configwriter.write("do Factory:Process {}\n".format(process))
    configwriter.write("set Factory:ScaleChoice Scales/MaxJetPtScale\n")
    ## Select a generic tree/loop combination or a
    ## specialized NLO package
    ## Currently ALICE has only openloops support, MadGraph to be added soon 
    ## All other ME providers irrelevant for ALICE
    # read Matchbox/MadGraph-MadGraph.in
    configwriter.write("read Matchbox/{}.in\n".format(loopprovider))
    configwriter.write("read Matchbox/CT14.in\n")
    configwriter.write("do /Herwig/MatrixElements/Matchbox/Factory:ProductionMode\n")

def GenerateHerwigInput(outputfile, tune, cmsenegy, events, hepmcfile, ktmin, ktmax):
    # See (minimum-bias): http://mcplots.cern.ch/dat/pp/jets/pt/atlas3-akt4/7000/herwig++/2.7.1/default.params
    # See (jet): http://mcplots.cern.ch/dat/pp/jets/pt/cms2011-y0.5/7000/herwig++/2.7.1/default.params
    # See also for minimum-bias: Chapter B.2 https://arxiv.org/abs/0803.0883
    with open(outputfile, "w") as myfile:
        myfile.write("read snippets/PPCollider.in\n") # Markus: Take PPCollider.in from Herwig repositiory instead of custom version
        myfile.write("set /Herwig/Generators/EventGenerator:EventHandler:LuminosityFunction:Energy {}.0\n".format(cmsenegy))
        # reduce verbosity in log file,
        # print only the first event (for whatever reason Herwig uses N+1 here)
        myfile.write("set /Herwig/Generators/EventGenerator:PrintEvent 2\n") 
        if tune == "mb":
            # MB tune from Herwig repo
            myfile.write("set /Herwig/Shower/ShowerHandler:IntrinsicPtGaussian 2.2*GeV\n")
            myfile.write("read snippets/MB.in\n")
            myfile.write("read snippets/Diffraction.in\n")
        else:
            # Use SoftTune as UE tune for Herwig7 (>= 7.1) based on https://herwig.hepforge.org/tutorials/mpi/tunes.html
            myfile.write("read SoftTune.in\n")
            isLeadingOrder = False
            kthardmin = 0.
            kthardmax = 0.
            if "beauty" in tune or "charm" in tune:
                quarktye = 4 if tune == "charm" else 5
                myfile.write("set /Herwig/MatrixElements/MEHeavyQuark:QuarkType {}\n".format(quarktye))
                myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEHeavyQuark\n")
                if "kthard" in tune:
                    kthardmin = ktmin
                    kthardmax = ktmax
                    if kthardmin < 0:
                        kthardmin = 0
                    if kthardmax < 0 or kthardmax > cmsenegy:
                        kthardmax = cmsenegy
                else:
                    kthardmin = 0.
                    kthardmax = float(cmsenegy)
                isLeadingOrder = True
            elif tune == "dijet_lo":
                myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEQCD2to2\n")
                kthardmin = 5.
                kthardmax = float(cmsenegy)
                isLeadingOrder = True
            elif tune == "kthard_lo":
                isLeadingOrder = True
                myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEQCD2to2\n")
                kthardmin = ktmin
                kthardmax = ktmax
                if kthardmin < 0:
                    kthardmin = 0
                if kthardmax < 0 or kthardmax > cmsenegy:
                    kthardmax = cmsenegy
            elif tune == "dijet_nlo_ol":
                setupMatchBox(myfile, "p p -> j j", "OpenLoops-OpenLoops")
                kthardmin = 5.
                kthardmax = float(cmsenegy)
            elif tune == "dijet_nlo_mg":
                setupMatchBox(myfile, "p p -> j j", "MadGraph-MadGraph")
                kthardmin = 5.
                kthardmax = float(cmsenegy)
            else:
                print("Process '{}' not implemented for HERWIG!".format(tune))
                exit(1)
            if isLeadingOrder:
                # Set PDF (LO)
                # do not set in case of NLO, there Hard processes need to be simulated
                # with NLO PDF sets while shower and MPI need to be simulated with LO
                # PDF set
                myfile.write("set /Herwig/Partons/HardLOPDF:PDFName CT14lo\n")
                myfile.write("set /Herwig/Partons/ShowerLOPDF:PDFName CT14lo\n")
                myfile.write("set /Herwig/Partons/MPIPDF:PDFName CT14lo\n")
                myfile.write("set /Herwig/Partons/RemnantPDF:PDFName CT14lo\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT %f*GeV\n" %(kthardmin))
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT %f*GeV\n" %(kthardmax))
            myfile.write("set /Herwig/Cuts/Cuts:MHatMax {}.0*GeV\n".format(cmsenegy))
            myfile.write("set /Herwig/Cuts/Cuts:MHatMin 0.0*GeV\n")
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE -1\n")

        # Setting particles stable by hand (based on the definition in AliPythia8):
        # Those particles are not decayed by Herwig but must be decayed by an external
        # decayer (i.e. pythia or EVGEN). This is important i.e. for full simulations
        # where the particles can still interact with the material
        # - K0l (130)
        # - K0s (310)
        # - Lambda (3122)
        # - Sigma (+ -> 3222, 0 -> 3212, - -> 3112)
        # - Xi (0 -> 3322, - -> 3312)
        # - Omega (3334)
        # Also set corresponding antiparticles to stable
        stableparticles = ["K0", "Kbar0", "Lambda0", "Lambdabar0", "Sigma0", "Sigmabar0", 
                           "Sigma+", "Sigmabar-", "Sigma-", "Sigmabar+", "Xi0", "Xibar0", 
                           "Xi-", "Xibar+", "Omega-", "Omegabar+"]
        for particle in stableparticles:
            myfile.write("set /Herwig/Particles/{}:Stable Stable\n".format(particle))

        # In addition: stable particles with a lifetime > 10 mm (decay externally)
        myfile.write("set /Herwig/Decays/DecayHandler:MaxLifeTime 10*mm\n")
        myfile.write("set /Herwig/Decays/DecayHandler:LifeTimeOption Average\n")

        #HEP MC writer
        myfile.write("read snippets/HepMC.in\n")
        myfile.write("set /Herwig/Analysis/HepMC:Filename {}\n".format(hepmcfile))
        myfile.write("set /Herwig/Analysis/HepMC:PrintEvent {}\n".format(events))
        myfile.write('saverun herwig /Herwig/Generators/EventGenerator\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate HERWIG input file.')
    parser.add_argument('--numevents', metavar='NEVT',
                        default=50000, type=int)
    parser.add_argument('--energy', metavar='ENERGY',
                        default=13000, type=int)
    parser.add_argument('--tune', metavar="TUNE",
                        default='mb')
    parser.add_argument('--herwigfile', metavar='HERWIGFILE',
                        default='herwig.in')
    parser.add_argument('--hepmcfile', metavar='HEPMCFILE', 
                        default='events.hepmc')
    parser.add_argument('--ktmin', metavar='KTMIN',
                        default=-1., type=float)
    parser.add_argument('--ktmax', metavar='KTMAX',
                        default=-1., type=float)
    args = parser.parse_args()

    GenerateHerwigInput(args.herwigfile, args.tune, args.energy, args.numevents, args.hepmcfile, args.ktmin, args.ktmax)
