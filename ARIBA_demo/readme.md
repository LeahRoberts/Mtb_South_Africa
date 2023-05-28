ARIBA Demo
==========

[ARIBA](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5695208/): Antimicrobial Resistance Identification By Assembly

This short demonstration explains how ARIBA was used to detect gene truncations in _M. tuberculosis_.

# Contents: 

1. [Install ARIBA](#install-ariba)
2. [Adding a new database](#adding-a-new-database)
3. [Querying fastq files](#querying-fastq-files)
4. [What's in the output files](#whats-in-the-output-files)
5. [Summarising results](#summarising-results)
6. [Compare to an assembly](#compare-to-an-assembly)


## Install ARIBA

Various installation methods are provided in the [ARIBA github](https://github.com/sanger-pathogens/ariba). 

ARIBA (v2.14.6) can be installed via Conda:

`conda install -c bioconda ariba`

To check installation, try:

`ariba --help`

To get the usage menu.

### Troubleshooting:

If conda gets stuck resolving the environment, you may want to try [Mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html).

If you have a problem with Mummer/Nucmer and perl ("bad interpreter"), you may need to downgrade Mummer: 
`mamba install -c bioconda mummer=3.23=h6de7cb9_11`

If you have problems running ARIBA (in section 3) you may need to follow the help on this [issue](https://github.com/sanger-pathogens/ariba/issues/327).


## Adding a new database

ARIBA has a range of pre-built, commonly used [databases](https://github.com/sanger-pathogens/ariba/wiki/Task:-getref) available for download via the `getref` and `prepareref` command:

`ariba getref reference_name output_prefix`


To add a [new database](https://github.com/sanger-pathogens/ariba/wiki/Task:-prepareref), you first need to provide a multifasta of the sequences you want to query (see `bedaquiline.fasta` file):

`ariba prepareref --all_coding yes -f bedaquiline.fasta bedaquiline_out`

Note: `all_coding` means that all the sequences provided are genes. To provide sequences that are non\_coding, use `--all_coding no`. If you have a mix, you must use a metadata spreadsheet, as explained [here](https://github.com/sanger-pathogens/ariba/wiki/Task:-prepareref).


Running `prepareref` will create a new folder for the ARIBA database called `bedaquiline_out`. As the `prepareref` step QC's the input, you should check the log to make sure no genes have been removed: 

```
01.filter.check_genes.log <-- should list all genes as KEEP
01.filter.check_metadata.log <-- blank as didn't provide metadata
01.filter.check_noncoding.log <-- blank as didn't provide non-coding sequences
```


## Querying fastq files

Note: ARIBA doesn't do any QC of reads!

To query reads, use the following command:

`ariba run bedaquiline_out reads_1.fq reads_2.fq output_dir`

Examples from the manuscript:

* good examples:
	* (mmpR5 p48fs) ERS14298681
	* (mmpR5 insertion sequence) ERS14298680
* poor quality example:
	* SAMEA23770168


See below ("compare to assembly") for what some of these examples look like.

## What's in the output files

There are pretty comprehensive descriptions for the output files [here](https://github.com/sanger-pathogens/ariba/wiki/Task:-run). The most important file is the `report.tsv`:

```
assembled_genes.fa.gz
assembled_seqs.fa.gz
assemblies.fa.gz
debug.report.tsv
log.clusters.gz
report.tsv
version_info.txt
```

## Summarising results

To summarise a number of isolates, you can use the summarise command: 

`ariba summary out ERS14298680_out/report.tsv ERS14298681_out/report.tsv SAMEA23770168_out/report.tsv --cluster_cols assembled,match,ref_seq`

Note: You can select a number of different columns to output various information (see [here](https://github.com/sanger-pathogens/ariba/wiki/Task:-summary)).

This will make three summary files: 

```
out.csv
out.phandango.csv
out.phandango.tre
```

The `phandango` outfiles are for if you want to visualise the output:


![alt text](ARIBA_demo/images/phandango_example.png)

Because of the columns we have selected in the summary, the phandango output isn't particularly informative here (e.g. the purple columns are just the gene name)

Looking at the `rv0678` column in `out.csv`, you can see the gene is "interrupted" in two samples and "no" (i.e. not able to be assembled) from the third sample.


## Compare to an assembly

Let's use [ACT](http://sanger-pathogens.github.io/Artemis/ACT/) to visualise what some of these interrupted genes look like.

Note: if you're still using ACT, these wrappers might interest you!
* Bwast.py: https://github.com/bawee/bwast
* Easy\_bwast: https://github.com/leoisl/easy_bwast


Frameshift mutation:
* (mmpR5 p48fs) ERS14298681 

![alt text](https://github.com/LeahRoberts/Mtb_South_Africa/blob/main/ARIBA_demo/images/frameshift_example.png)

Insertion sequence: 
* (mmpR5 insertion sequence) ERS14298680 

![alt text](https://github.com/LeahRoberts/Mtb_South_Africa/blob/main/ARIBA_demo/images/IS_example.png)

Poor quality example: 
* SAMEA23770168

The gene has assembled with Shovill, despite being absent in the ARIBA assembly. While it is likely the gene is present, it is difficult to confirm anything from this data and as such it should be excluded from the analysis. 

![alt text](https://github.com/LeahRoberts/Mtb_South_Africa/blob/main/ARIBA_demo/images/sam_perfect_match.png)





