# Repeated evolution of bedaquiline resistance in Mycobacterium tuberculosis is driven by truncation of mmpR5

## Project folder

Repository of all scripts used in project for reproducibility.

Scripts
=======

* `run_blastn.sh` and `translate_nt_to_am.py`: collate predicted protein sequences from _de novo_ assemblies
* `map_bwa_get_coverage.py` and `summarize_coverage_data.py`: map reads and summarise coverage using pysamstats
* `make_VCF_consensus.py`: script to make consensus fasta from VCF for input into iqtree 
* `MIC_comparisons.py`: script to combine distance matrix, Ariba variant information and isolate MICs



Plots
=======

* `figure_6_plot.R`: R code to make Figure 6 plot
* `Figure_7_plot.R`: R code to make Figure 7 plot


Mask files
===========

* `R00000039_repregions.bed`: conventional mask file
* `R00000039_repregions_wAMR.bed`: conventional mask file with the following AMR genes masked:

```
gene	start	end	start-100 bp	end+100bp	bp masked
ahpC	2726193	2726780	2726093	2726880	787
eis 	2714124	2715332	2714024	2715432	1408
embA	4243233	4246517	4243133	4246617	3484
embB	4246514	4249810	4246414	4249910	3496
fabG1	1673440	1674183	1673340	1674283	943
gid	4407528	4408202	4407428	4408302	874
gyrA	7302	9818	7202	9918	2716
inhA	1674202	1675011	1674102	1675111	1009
katG	2153889	2156111	2153789	2156211	2422
pncA	2288681	2289241	2288581	2289341	760
rpoB	759807	763325	759707	763425	3718
rpsL	781560	781934	781460	782034	574
rrs	1471846	1473382	1471746	1473482	1736
rv0678	778990	779487	778890	779587	697
mmpl5	775586	778480	775486	778580	3094
```