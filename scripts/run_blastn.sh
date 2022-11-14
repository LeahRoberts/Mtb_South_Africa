fasta=$1

blastn -query ${fasta} -db ../../../blast/mmpl5 -outfmt "6 pident length qstart qend sstrand" > tmp.out

sort -k3 -n tmp.out > tmp.sorted.out

cat tmp.sorted.out | while read line; do
  pident=$(echo $line | cut -f1 -d' ');
  length=$(echo $line | cut -f2 -d' ');
  qstart=$(echo $line | cut -f3 -d' ');
  qend=$(echo $line | cut -f4 -d' ');
  strand=$(echo $line | cut -f5 -d' ');
  echo -e ${fasta}'\t'${pident}'\t'${length}'\t'${qstart}'\t'${qend}'\t'${strand};
done

rm tmp.out
rm tmp.sorted.out


