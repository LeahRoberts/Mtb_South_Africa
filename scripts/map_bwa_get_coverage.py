import sys
import subprocess
from subprocess import Popen
from os.path import exists
import os
import pandas as pd

reference = "../H37Rv.fasta"
sample_name = sys.argv[1]


def bwa_index(reference):
    command = ['bwa', 'index', reference]
    subprocess.run(command)


def run_bwa_mem(reference, read_1, read_2, bam_out):
    p1 = subprocess.Popen(['bwa', 'mem', reference, read_1, read_2],
            stdout=subprocess.PIPE)
    p2 = subprocess.run(['samtools', 'sort', '-o', bam_out], stdin=p1.stdout)


def pysamstats_coverage(bam_file, start, end, outfile):
    command = ['pysamstats', '-t', 'coverage', '--chromosome', 'NC_000962.3', '--start', start, '--end', end, bam_file]
    fout = open(outfile, "a")
    subprocess.run(command, stdout=fout)


def get_avg_cov(coverage_file, location):
    data = pd.read_csv(coverage_file, sep='\t')
    df = pd.DataFrame(data)
    avg_cov = df['reads_all'].mean()
    print("%s\t%s" % (location, avg_cov))
    os.remove(coverage_file)


# create index for reference if doesn't exist:
if not exists("../H37Rv.fasta.bwt"):
    bwa_index(reference)

# run bwa mem
read_1 = '../reads/' + sample_name + "_1.fastq.gz"
read_2 = '../reads/' + sample_name + "_2.fastq.gz"
bam_out = sample_name + ".bam"

if not exists(bam_out):
    run_bwa_mem(reference, read_1, read_2, bam_out)
    subprocess.run(['samtools', 'index', bam_out])

# get average coverage with pysamstats:
coverage_out = sample_name + ".cov.tsv"
sys.stdout = open(coverage_out, "a")

pysamstats_coverage(bam_out, '1', '4411532', 'H37Rv.out')
get_avg_cov('H37Rv.out', 'H37Rv')

# get coverage at Rv0678:
pysamstats_coverage(bam_out, '778990', '779487', 'Rv0678.out')
get_avg_cov('Rv0678.out', 'Rv0678')

# get coverage at mmpS5:
pysamstats_coverage(bam_out, '778477', '778905', 'mmpS5.out')
get_avg_cov('mmpS5.out', 'mmpS5')

# get coverage at mmpL5:
pysamstats_coverage(bam_out, '775586', '778480', 'mmpL5.out')
get_avg_cov('mmpL5.out', 'mmpL5')

sys.stdout.close()