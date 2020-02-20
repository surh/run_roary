# Run roary

Simple wrapper pipeline to process a set of genomes in genbank format through roary to
identify orthologues and perform pangenome analysis.

The pipeline has been tested with genbank files produced by antiSMASH 5 where CDSs were
predicted by prodigal. In theory, any set of genbank files should work as long as CDS
files are marked as CDS features and they have a `locus_tag` qualifier.

# Requirements

The pipeline script is nextflow, and it requires python3 with biopython for parsing the
genbank files and roary. It was tested with roary version 1.3.

Processes that require python 3 and biopython are labelled 'py3', and those that
require roary alre labelled 'roary'. Use the withLabel directive in your nextflow.config
file to point those processes to the appropriate installation locations. See an example
at the end of the nf file.


# Running roary

After setting your `nextflow.config` file, there are only three paramters that you
need to specify in the nextflow call:

* **indir**: Directory with input genbank files. Each genome must correspond to a single
file with extension `.gbk` (no compressed files).
* **outdir**: Directory for output.
* **roary_threads**: Indicate how many threads to use for roary.`

Memory/time requrirements can be set in the `nextflow.config` file.
