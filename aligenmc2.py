#! /usr/bin/env python3

import argparse
import os
import sys

def find_plugins(inputdir):
    plugins = []
    for root, dirs, files in os.walk(os.getcwd()):
        for fl in files:
            if fl.endswith("gen.py"):
                print("found %s" %fl)
                plugins.append(os.path.join(root, fl))
    return plugins

def extract_generator(pluginpath):
    tags = pluginpath.split("/")
    return tags[len(tags) - 2]

def availble_generators(plugins):
    helptext = "Available generators:\n"
    for genname, generator in plugins.items():
        helptext += "  %s: %s" %(genname, generator.description())
    return helptext

if __name__ == "__main__":
    sourcedir = os.path.dirname(os.path.abspath(sys.argv[0]))
    plugins = {}
    for pl in find_plugins(sourcedir):
        plugin = __import__(pl)
        plugins[extract_generator(plugin)] = plugin.gen() 

    generators_string = availble_generators(plugins)
    print("generators: %s" %generators_string)

    parser = argparse.ArgumentParser(prog="aligenmc2", description="Tool to run Monte Carlo generators in ALICE", epilog=generators_string)
    parser.add_argument("-g", "--generator", metavar="GENERATOR", type=str, required=True, help="Generator type (see below)")
    #parser.add_argument("-h", "--help", metavar="HELP", action="store_true", help="Show help")
    parser.add_argument("-E", "--energy", metavar="ENERGY", type=float, default = 13000., help="Centre-of-mass energy (default: 13000.)")
    parser.add_argument("-N", "--nevents", metavar="NEVENTS", type=int, default=100, help="Number of events (default: 100)")
    parser.add_argument("-o", "--outputfile", metavar="OUTPUTFILE", type=str, default="gen.hepmc", help="Output file (default: gen.hepmc)")
    parser.add_argument("-p", "--packages", metavar="PACKAGES", type=str, default="", help="Packages to be loaded for job execution")
    parser.add_argument("-S", "--seed", metavar="SEED", type=int, default=0, help="Generator seed (default: 0)")
    parser.add_argument("-t", "--tune", metavar="TUNE", type=str, default="", help="Generator tune")
    parser.add_argument("--ktmin", metavar="KTMIN", type = float, default = -1., help="min. kt hard (default: -1)")
    parser.add_argument("--ktmax", metavar="KTMAX", type = float, default = -1., help="max. kt hard (default: -1)")

    args = parser.parse_args()
    if args.help:
        parser.print_help()
        sys.exit(1)
    if not args.generator in plugins.keys():
        print("Generator %s not supported" %args.generator)
        parser.print_help()
        sys.exit(1)

    argmap = {"energy": args.energy, "nevents": args.nevents, "seed": args.seed, "outputfile": args.outputfile, "tune": args.tune, 
              "packages": args.packages, "kthardmin": args.ktmin, "kthardmax": args.ktmax}
    gen_runner = plugins[args.generator]
    gen_runner.run(argmap)