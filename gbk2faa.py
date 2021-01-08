#!/usr/bin/env python

# Copyright (C) 2020 Sur Herrera Paredes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Bio import SeqIO
import argparse


def process_arguments():
    # Read arguments
    parser_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=parser_format)
    required = parser.add_argument_group("Required arguments")

    # Define description
    parser.description = ("Convert antiSMASH5 gbk output into FAA file")

    # Define required arguments
    required.add_argument("--infile",
                          help=("Input GBK file"),
                          required=True, type=str)

    # Define other arguments
    parser.add_argument("--outfile",
                        help=("Name of output FAA file."),
                        type=str,
                        default="genome.faa")

    # Read arguments
    print("Reading arguments")
    args = parser.parse_args()

    # Processing goes here if needed

    return args


def gbk2faa(infile, outfile):
    gb = SeqIO.parse(infile, 'genbank')
    with open(outfile, 'w') as oh:
        for record in gb:
            rec_id = record.id
            print(rec_id)
            for feat in record.features:
                if feat.type == 'CDS':
                    locus_tag = feat.qualifiers['locus_tag'][0]
                    translation = feat.qualifiers['translation'][0]
                    oh.write(">" + locus_tag + "\t" + rec_id + "\n")
                    oh.write(translation + "\n")
    oh.close

    return


if __name__ == "__main__":
    args = process_arguments()

    print("Processing {}".format(args.infile))
    gbk2faa(args.infile, args.outfile)
