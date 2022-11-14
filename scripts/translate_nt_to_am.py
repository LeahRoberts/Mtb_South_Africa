"""
script that takes a fasta, extracts a sequence based on [start] and [end]
and translates the sequence from nucleotides to amino acids
"""

import sys
from Bio.Seq import Seq
from Bio import SeqIO

blast_output = sys.argv[1]

with open(blast_output, "r") as blast_in:
    for line in blast_in:
        fasta_file = line.split("\t")[0].rstrip()
        strand = line.split("\t")[5].rstrip()
        start = int(line.split("\t")[3].rstrip()) - 1
        end = int(line.split("\t")[4].rstrip())
        for seq_record in SeqIO.parse(fasta_file, "fasta"):
            rv0678_seq = str(seq_record.seq[start:end])
            rv0678_seq = Seq(rv0678_seq)
            if strand == 'minus':
                rv0678_seq = rv0678_seq.reverse_complement()
            # translate from nucleotide to amino acid
            rv0678_protein = str(rv0678_seq.translate(table=11, to_stop=True))
            with open("mmpL5_aa.msa", "a") as f:
                f.write(">%s\n%s\n" % (fasta_file, rv0678_protein))
