#! /usr/bin/env python3

import argparse

def GenerateHerwigInput(outputfile, tune, cmsenegy, events, hepmcfile, ktmin, ktmax):
    # See (minimum-bias): http://mcplots.cern.ch/dat/pp/jets/pt/atlas3-akt4/7000/herwig++/2.7.1/default.params
    # See (jet): http://mcplots.cern.ch/dat/pp/jets/pt/cms2011-y0.5/7000/herwig++/2.7.1/default.params
    # See also for minimum-bias: Chapter B.2 https://arxiv.org/abs/0803.0883
    with open(outputfile, "w") as myfile:
        myfile.write("read PPCollider.in\n")
        myfile.write("set /Herwig/Generators/EventGenerator:EventHandler:LuminosityFunction:Energy {}.0\n".format(cmsenegy))
        if tune == "beauty":
            myfile.write("set /Herwig/MatrixElements/MEHeavyQuark:QuarkType 5\n")
            myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEHeavyQuark\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT 0.0*GeV\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT {}.0*GeV\n".format(cmsenegy))
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE -1\n")
        elif tune == "charm":
            myfile.write("set /Herwig/MatrixElements/MEHeavyQuark:QuarkType 4\n")
            myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEHeavyQuark\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT 0.0*GeV\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT {}.0*GeV\n".format(cmsenegy))
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE -1\n")
        elif tune == "dijet":
            myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEQCD2to2\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT 5.0*GeV\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT {}.0*GeV\n".format(cmsenegy))
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE -1\n")
        elif tune == "mb":
            myfile.write("read MB.in\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT 0.0*GeV\n")
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT {}.0*GeV\n".format(cmsenegy))
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE 0\n")
        elif tune == "kthard":
            myfile.write("insert /Herwig/MatrixElements/SubProcess:MatrixElements[0] /Herwig/MatrixElements/MEQCD2to2\n")
            localktmin = ktmin
            localktmax = ktmax
            if localktmin < 0:
                localktmin > 0
            if localktmax < 0 or localktmax > cmsenegy:
                localktmax = cmsenegy
            myfile.write("set /Herwig/Cuts/JetKtCut:MinKT %f*GeV\n" %(localktmin))
            myfile.write("set /Herwig/Cuts/JetKtCut:MaxKT %f*GeV\n" %(localktmax))
            myfile.write("set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE -1\n")
        else:
            print("Process '{}' not implemented for HERWIG!".format(tune))
            exit(1)
        myfile.write("set /Herwig/Cuts/Cuts:MHatMax {}.0*GeV\n".format(cmsenegy))
        myfile.write("set /Herwig/Cuts/Cuts:MHatMin 0.0*GeV\n")
        myfile.write("read SoftTune.in\n")

        # PDF selection
        myfile.write("create ThePEG::LHAPDF /Herwig/Partons/PDFSet ThePEGLHAPDF.so\n")
        myfile.write("set /Herwig/Partons/PDFSet:PDFName CT10nlo\n")
        myfile.write("set /Herwig/Partons/PDFSet:RemnantHandler /Herwig/Partons/HadronRemnants\n")
        myfile.write("set /Herwig/Particles/p+:PDF /Herwig/Partons/PDFSet\n")

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