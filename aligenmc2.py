#! /usr/bin/env python3

""" aligenmc python port

author:: Markus Fasel <markus.fasel@cern.ch>, ORNL
author:: Raymond Ehlers <raymond.ehlers@cern.ch>, ORNL
"""

import argparse
import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import Dict, Union

import generator


logger = logging.getLogger(__name__)


def discover_generators(base_generator_dir: Union[Path, str] = Path("gen"), generator_file_name: str = "gen.py") -> Dict[str, generator.Generator]:
    """ Discover generators based on the specified directory structure and filename.

    Finds the generators, loads the modules, and retrieves the generator classes

    Args:
        base_generator_dir: Base generator directory. Default: "gen"
        generator_file_name: Filename of the generator. Default: "gen.py"
    Returns:
        Dict containing each generator class defined by the modules. Keys are the generator names.
    """
    # Validation
    base_generator_dir = Path(base_generator_dir)
    generators = {}
    for generator_directory in base_generator_dir.glob("*"):
        # Validation
        # Require it to be a non-hidden directory.
        if not generator_directory.is_dir() or generator_directory.name.startswith("_"):
            continue

        # Extract generator name based on the directory.
        generator_name = generator_directory.name

        # Import it, and load all Generator classes.
        try:
            # Convert the path into a module name.
            module_path = str(generator_directory / generator_file_name).replace(".py", "").replace("/", ".")
            generator_module = importlib.import_module(module_path)
            classes = {
                name: cls for name, cls in inspect.getmembers(generator_module, inspect.isclass)
                # Only provide classes of interest.
                if issubclass(cls, generator.Generator)
            }
            if len(classes) == 1:
                generators[generator_directory.name] = next(iter(classes.values()))
            else:
                # Handle multiple generators.
                for generator_class_name, cls in classes:
                    generators[f"{generator_name}_{generator_class_name}"] = cls
        except ImportError as e:
            logger.warning(f"Unable to load generator for '{generator_name}'")

    return generators



def availble_generators(plugins):
    helptext = "Available generators:\n"
    for genname, generator in plugins.items():
        helptext += f"  {genname}: {generator.description()}"
    return helptext


if __name__ == "__main__":
    # Setup
    logging.basicConfig(format="%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s")
    logger.setLevel(logging.INFO)

    # Setup
    plugins = discover_generators()
    generators_string = availble_generators(plugins)
    logger.info(f"\ngenerators: {generators_string}")

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
    gen_runner.run(**argmap)
