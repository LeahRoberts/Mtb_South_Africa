import glob

cov_data = glob.glob("./*tsv")

outfile = open("coverage_summary.tsv", "a")
outfile.write("samples\toverall_cov\tRv0678_cov\tmmpS5_cov\tmmpL5_cov\n")

for f in cov_data:
    name = f.split(".")[0]
    covs = {}
    with open(f, "r") as fin:
        for line in fin:
            position = line.split("\t")[0].rstrip()
            depth = line.split("\t")[1].rstrip()
            if position == 'H37Rv':
                ref_cov = depth
            else:
                prop_cov = float(depth) / float(ref_cov)
                prop_cov_rounded = round(prop_cov, 2)
                covs[position] = prop_cov_rounded
        outfile.write("%s\t%s\t%s\t%s\t%s\n" % (name, ref_cov, covs['Rv0678'], covs['mmpS5'], covs['mmpL5']))



