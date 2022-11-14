"""
Script to filter VCF for PASS SNPs and use to build consensus sequence
"""

# from cyvcf2 import VCF, Writer
import sys
from subprocess import Popen
from os.path import exists
import re
import os


def tabix_index(filename, preset="vcf"):
    """Call tabix to create an index for a bgzip-compressed file."""
    command = ['tabix', '-p', preset, filename]
    p = Popen(command)
    p.communicate()

def bcftools_consensus(reference, mask_file, sample_name, outfile, VCF_file):
    """Call bcftools to create consensus sequence."""
    command = ['bcftools', 'consensus', '-f', reference, '-m', mask_file, '-s', sample_name,
               '-o', outfile, VCF_file]
    p = Popen(command)
    p.communicate()

def gunzip(file):
    command = ['gunzip', file]
    p = Popen(command)
    p.communicate()

def bgzip(file):
    outfilename = file + ".gz"
    with open(outfilename, "w") as f:
        command = ['bgzip', '-c', file]
        p = Popen(command, stdout=f)
        p.communicate()


## For some reason, cyvcf2 doesn't recognise the PASS filter
# VCF_file = sys.argv[1]
# sample_name = VCF_file.split(".")[0].rstrip()
# vcf = VCF(VCF_file)
# fname = 'out.vcf'
# w = Writer(fname, vcf)
#
# for variant in vcf:
#     print(str(variant.ID))
#     if variant.FILTER == "PASS":
#         var = variant.gt_types
#         if var[0] == 3: # only want HOM_ALT variants
#             w.write_record(variant)
#
# w.close(); vcf.close()

vcf = sys.argv[1]
sample_name = vcf.split(".")[0].rstrip()

if vcf.split(".")[-1] == "gz":
    gunzip(vcf)
    vcf = re.sub(r"\.\w+$", r"", vcf)

outfile = "out.vcf"
with open(vcf, "r") as fin:
    for line in fin:
        with open(outfile, "a") as fout:
            if line[0] == "#":
                fout.write(line)
            else:
                var_filter = line.split("\t")[6]
                if var_filter == "PASS":
                    info = line.split("\t")[9]
                    gt = info.split(":")[0]
                    if gt != "0/0": # if not REF allele
                        REF = line.split("\t")[3]
                        ALT = line.split("\t")[4]
                        if "," in ALT: # more than one ALT allele
                            alt_var_1, alt_var_2 = gt.split("/")
                            if alt_var_1 == alt_var_2: # homozygous
                                alt_split = int(alt_var_1) - 1
                                alt_var = ALT.split(",")[alt_split]
                                if len(REF) == len(alt_var):
                                    fout.write(line)
                        else:
                            if len(REF) == len(ALT):
                                fout.write(line)

bgzip(vcf)
os.remove(vcf)
bgzip('out.vcf')

if not exists("out.vcf.gz.tbi"):
    tabix_index('out.vcf.gz')

outfilename = sample_name + ".consensus.fasta"
bcftools_consensus('../refs/H37Rv.fasta', '../mask_files/R00000039_repregions_wAMR.bed', sample_name, outfilename, 'out.vcf.gz')

os.remove("out.vcf")
os.remove("out.vcf.gz")
os.remove("out.vcf.gz.tbi")