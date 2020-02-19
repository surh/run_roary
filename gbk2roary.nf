// Params
params.indir = 'genomes/'
params.outdir = 'output'
params.roary_threads = 8


GBKS = Channel.fromPath("${params.indir}/*.gbk"}.
  .map{gbk_file -> tuple(gbk_file.name.replaceAll(/\.gbk/, ""),
  file(gbk_file))}

process gbk2gff3{
  label 'bioperl'
  tag "$acc"
  publishDir "${params.outdir}/gff3/", mode: 'rellink'

  input:
  tupple acc, file(gbk_file) from GBKS

  output:
  tuple file("${acc}.gff3") into GFF3S

  """
  bp_genbank2gff3 $gbk_file --outdir - > ${acc}.gff3
  """
}

mode run_roary{
  label 'roary'
  cpus params.roary_threads
  publishDir "params.outdir/", mode: 'rellink'
  
  input:
  file '*.gff3' from GFF3S.collect()
  
  output:
  file "roary"
  
  """
  roary -p ${params.roary_threads} \
    -f roary/ \
    -v \
    *.gff3
  """
}

