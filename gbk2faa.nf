#!/usr/bin/env nextflow
// Copyright (C) 2020 Sur Herrera Paredes

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// Params
params.indir = 'genomes/'
params.outdir = 'output'
// params.eggnog_threads = 8


GBKS = Channel.fromPath("${params.indir}/*.gbk")
  .map{gbk_file -> tuple(gbk_file.name.replaceAll(/\.gbk/, ""),
  file(gbk_file))}

process gbk2faa{
  label 'py3'
  tag "$genome"
  publishDir params.outdir, mode: 'rellink'

  input:
  tuple genome, gbk_file from GBKS

  output:
  tuple genome, file("${genome}.faa") into FAAS

  """
  ${workflow.projectDir}/gbk2faa.py \
    --infile $gbk_file \
    --outfile ${genome}.faa
  """
}

// Example nextflow.config
/*
process{
  queue = 'hbfraser,hns'
  maxForks = 20
  errorStrategy = 'finish'
  stageInMode = 'rellink'
  withLabel: 'py3'{
    module = 'anaconda'
    conda = '/opt/modules/pkgs/anaconda/3.6/envs/fraserconda'
  }
}

executor{
  name = 'slurm'
  queueSize = 500
  submitRateLitmit = '1 sec'
}
*/
