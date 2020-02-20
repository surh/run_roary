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

import argparse
from Bio import SeqIO


def process_arguments():
    # Read arguments
    parser_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=parser_format)
    required = parser.add_argument_group("Required arguments")

    # Define description
    parser.description = ("Convert antiSMASH5 gbk to GFF3 format")

    # Define required arguments
    required.add_argument("--input", help=("Input gbk file."),
                          required=True, type=str)
    required.add_argument("--output", help=("Output filename"),
                          required=True, type=str)

    # Read arguments
    print("Reading arguments")
    args = parser.parse_args()

    # Processing goes here if needed

    return args


if __name__ == "__main__":
    args = process_arguments()
    # print("Arguments read...")

    with open(args.output, 'w') as gff:
        gb = SeqIO.parse(args.input, 'genbank')
        seqs = []
        for record in gb:
            rec_id = record.id
            seqs.append(record)
            for feat in record.features:
                if feat.strand == 1:
                    strand = '+'
                elif feat.strand == -1:
                    strand = '-'
                else:
                    raise ValueError("feat.strand value not recognized ({})".format(str(feat.strand)))

                # Get ID numbers
                if feat.type == 'CDS':
                    feat_id = feat.qualifiers['locus_tag'][0]
                elif feat.type == 'region':
                    feat_id = 'region_' + feat.qualifiers['region_number'][0]
                elif feat.type == 'cand_cluster':
                    feat_id = 'cand_cluster_' + feat.qualifiers['candidate_cluster_number'][0]
                elif feat.type == 'proto_core':
                    feat_id = 'proto_core.' + str(feat.location.start + 1) + '_' + str(feat.location.end)
                elif feat.type == 'protocluster':
                    feat_id = 'protocluster_' + feat.qualifiers['protocluster_number'][0]
                elif feat.type == 'aSDomain':
                    feat_id = feat.qualifiers['locus_tag'][0] + '.' + str(feat.location.start + 1) + '_' + str(feat.location.end)
                elif feat.type == 'aSModule':
                    feat_id = feat.qualifiers['locus_tags'][0] + '.' + str(feat.location.start + 1) + '_' + str(feat.location.end)
                elif feat.type == 'CDS_motif':
                    feat_id = feat.qualifiers['locus_tag'][0] + '.' + str(feat.location.start + 1) + '_' + str(feat.location.end)
                elif feat.type == 'misc_feature':
                    feat_id = 'misc_feature.' + str(feat.location.start + 1) + '_' + str(feat.location.end)
                else:
                    raise ValueError("Feature type({}) not recognized.".format(feat.type))

                feat_id = 'ID=' + feat_id

                gff_line = [rec_id,
                            'antiSMASH5',
                            feat.type,
                            str(feat.location.start + 1),
                            str(feat.location.end),
                            '.',
                            strand,
                            '.',
                            feat_id]
                gff_line = "\t".join(gff_line) + "\n"
                gff.write(gff_line)
        gff.write("##FASTA\n")
        print("Writing sequences")
        for seq in seqs:
            SeqIO.write(seq, gff, 'fasta')
