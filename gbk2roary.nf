// Params
params.indir = 'genomes/'
params.outdir = 'output'
params.roary_threads = 8
params.identity = 90


GBKS = Channel.fromPath("${params.indir}/*.gbk")
  .map{gbk_file -> tuple(gbk_file.name.replaceAll(/\.gbk/, ""),
  file(gbk_file))}

//GBKS.subscribe{println it}


process gbk2gff3{
  label 'py3'
  tag "$acc"
  publishDir "${params.outdir}/gff3/", mode: 'rellink'

  input:
  tuple acc, file(gbk_file) from GBKS

  output:
  file "${acc}.gff3" into GFF3S

  """
  ${workflow.projectDir}/gbk2gff3.py --input $gbk_file --output ${acc}.gff3 --type CDS
  """
}

process run_roary{
  label 'roary'
  cpus params.roary_threads
  publishDir "${params.outdir}/", mode: 'rellink'
  
  input:
  file '*.gff3' from GFF3S.collect()
  val identity from params.identity
  
  output:
  file "roary/"
  
  """
  roary -p ${params.roary_threads} \
    -i $identity \
    -f roary/ \
    -v \
    *.gff3
  """
}


// Example nextflow.config
/*
process{
  queue = 'hbfraser,hns'
  maxFors = 300
  errorStrategy = 'finish'
  stageInMode = 'rellink'
  withLabel: 'py3'{
    module = 'anaconda'
    conda = '/opt/modules/pkgs/anaconda/3.6/envs/fraserconda'
  }
  withLabel: 'roary'{
    module = 'anaconda'
    conda = '/home/sur/.conda/envs/sur/'
  }
}

executor{
  name = 'slurm'
  queueSize = 500
  submitRateLitmit = '1 sec'
}
*/
