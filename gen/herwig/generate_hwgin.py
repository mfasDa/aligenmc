#! /usr/bin/env python3

import argparse

def GenerateHerwigInput(outputfile, tune, cmsenegy, events, hepmcfile, ktmin, ktmax):
    # See (minimum-bias): http://mcplots.cern.ch/dat/pp/jets/pt/atlas3-akt4/7000/herwig++/2.7.1/default.params
    # See (jet): http://mcplots.cern.ch/dat/pp/jets/pt/cms2011-y0.5/7000/herwig++/2.7.1/default.params
    # See also for minimum-bias: Chapter B.2 https://arxiv.org/abs/0803.0883
    with open(outputfile, "w") as myfile:
        myfile.write("read snippets/PPCollider.in\n") # Markus: Take PPCollider.in from Herwig repositiory instead of custom version
        myfile.write("set /Herwig/Generators/EventGenerator:EventHandler:LuminosityFunction:Energy {}.0\n".format(cmsenegy))
        if tune == "mb":
            # MB tune from Herwig repo
            myfile.write("set /Herwig/Shower/ShowerHandler:IntrinsicPtGaussian 2.2*GeV\n")
            myfile.write("read snippets/MB.in\n")
            myfile.write("read snippets/Diffraction.in\n")
        else:
            # Use SoftTune as UE tune for Herwig7 (>= 7.1) based on https://herwig.hepforge.org/tutorials/mpi/tunes.html
            myfile.write("read SoftTune.in\n")
            # Set PDF (LO)
            myfile.write("set /Herwig/Partons/HardLOPDF:PDFName CT14lo\n")
            myfile.write("set /Herwig/Partons/ShowerLOPDF:PDFName CT14lo\n")
            myfile.write("set /Herwig/Partons/MPIPDF:PDFName CT14lo\n")
            myfile.write("set /Herwig/Partons/RemnantPDF:PDFName CT14lo\n")
            kthardmin = 0.
            kthardmax = 0.
            if tune == "beauty" or tune == "charm":
                quarktye = 4 if tune == "charm" else 5
                myfile.write("set /Herwig/MatrixElements/MEHeavyQuark:QuarkType {}\n".format(quarktye))
                myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEHeavyQuark\n")
                kthardmin = 0.
                kthardmax = float(cmsenegy)
            elif tune == "dijet_lo":
                myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEQCD2to2\n")
                kthardmin = 5.
                kthardmax = float(cmsenegy)
            elif tune == "kthard":
                myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEQCD2to2\n")
                kthardmin = ktmin
                kthardmax = ktmax
                if kthardmin < 0:
                    kthardmin = 0
                if kthardmax < 0 or kthardmax > cmsenegy:
                    kthardmax = cmsenegy
            else:
                print("Process '{}' not implemented for HERWIG!".format(tune))
                exit(1)
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT %f*GeV\n" %(kthardmin))
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT %f*GeV\n" %(kthardmax))
            myfile.write("set /Herwig/Cuts/Cuts:MHatMax {}.0*GeV\n".format(cmsenegy))
            myfile.write("set /Herwig/Cuts/Cuts:MHatMin 0.0*GeV\n")
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE -1\n")

        # Stable particles with a lifetime > 10 mm (decay externally)
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
