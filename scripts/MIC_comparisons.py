"""
script to automatically find a closely related isolate that differs
only in the variant of interest, and record change in MIC
"""

import pandas as pd

####################################################################
####################################################################
####################################################################
# IMPORTING FILES
####################################################################
####################################################################
####################################################################

# list of samples with variants of interest
# one sample per line
# currently looking only at Rv0678 mutations
variant_list = "mutations_all_final.txt"

# distance matrix between all samples
distance_matrix = "distance_matrix.out.distance_matrix.txt"

# MICs for BDQ
# removed all non-integer symbols (e.g. >=<, NA)
sample_MICs = "mic_comparison_v2/ZA_BDQ_MIC.txt"

# truncations list
# only looking at mmpL5, mmpS5, Rv0678
sample_truncations = "truncations_mmpLS5_Rv0678.txt"

####################################################################
####################################################################
####################################################################
# PROCESSING FILES
####################################################################
####################################################################
####################################################################

# list of variants
samples_with_variants_dic = {}
with open(variant_list, "r") as var_in:
    for var in var_in:
        sam = var.split("\t")[1]
        variant = var.split("\t")[2].rstrip()
        if sam in samples_with_variants_dic.keys():
            print("%s already in dictionary, skipping %s\n" % (sam, variant))
        else:
            samples_with_variants_dic[sam] = variant

# save distance matrix as dataframe
dist_matrix_DF = pd.read_csv(distance_matrix, sep='\t', header=None,
                             index_col=0)
all_samples_list = dist_matrix_DF.index.to_list()

# save sample BDQ MICs as dictionary
sample_MICs_dic = {}
with open(sample_MICs, "r") as sam_MICs_in:
    for line in sam_MICs_in:
        sample = line.split("\t")[1].rstrip()
        MIC = line.split("\t")[0]
        sample_MICs_dic[sample] = MIC

# convert sample_truncation to binary:
sample_trunc_binary_dic = {}
with open(sample_truncations, "r") as samples_trunc_in:
    next(samples_trunc_in)  # skip header
    for line in samples_trunc_in:
        line = line.rstrip()
        sample_name = line.split(",")[0]
        trunc_genes_all = line.split(",")[1:]
        trunc_genes_all = ["1" if item == "yes" else item for item in trunc_genes_all]
        trunc_genes_all = ["0" if item == "no" else item for item in trunc_genes_all]
        binary_encoding = "".join(trunc_genes_all)
        sample_trunc_binary_dic[sample_name] = binary_encoding


####################################################################
####################################################################
####################################################################
# FUNCTIONS
####################################################################
####################################################################
####################################################################


def check_has_MIC(sample):
    if sample in sample_MICs_dic.keys():
        return True
    else:
        return False


def find_closest_samples(isolate_name):
    threshold = 20
    sample_position = int(all_samples_list.index(isolate_name))
    sample_position_adjusted = sample_position + 1
    temp_df = dist_matrix_DF.iloc[:, sample_position:sample_position_adjusted].copy()
    temp_df.sort_values(sample_position_adjusted, inplace=True)
    index_ordered = temp_df.index.to_list()
    closest_samples_dic = {}
    distance = 0
    counter = 0
    while distance < threshold:
        close_sample_name = index_ordered[counter]
        distance = temp_df.iloc[counter, 0]
        if distance > threshold:
            break
        else:
            closest_samples_dic[close_sample_name] = distance
            counter += 1
    return closest_samples_dic


def check_sample_variants(sample):
    if sample in samples_with_variants_dic.keys():
        return True
    else:
        return False

MIC_dictionary_scale = {"0.008": "0", "0.015": "1", "0.03": "2", "0.06": "3", 
						"0.12": "4", "0.25": "5", "0.5": "6", "1": "7", "2": "8"}

def check_MIC_change(sample1, sample2):
    sam1_MIC = sample_MICs_dic[sample1]
    sam2_MIC = sample_MICs_dic[sample2]
    MIC_change = float(MIC_dictionary_scale[sam1_MIC]) - float(MIC_dictionary_scale[sam2_MIC])
    return sam1_MIC, sam2_MIC, MIC_change

####################################################################
####################################################################
####################################################################
# SCRIPT START
####################################################################
####################################################################
####################################################################


samples_to_check = samples_with_variants_dic.keys()
sample_printed_to_results = []

for sam in samples_to_check:
    # check that the sample has no truncated genes:
    # check that the sample has an MIC:
    has_MIC = check_has_MIC(sam)
    if has_MIC:
        dictionary_of_close_samples = find_closest_samples(sam)
        if len(dictionary_of_close_samples.keys()) == 0:
            print("%s has no samples within 50 SNVs, skipping\n" % sam)
        else:
            # loop through and see if any match the conditions required
            for possible_sample in dictionary_of_close_samples.keys():
                # check it's not the same sample:
                if possible_sample != sam:
                    # check this sample has an MIC:
                    has_MIC_second_sample = check_has_MIC(possible_sample)
                    if has_MIC_second_sample:
                        # condition 1: does not have the same variant of interest or any other non-syn snp
                        has_variants = check_sample_variants(possible_sample)
                        if not has_variants:
                            # get change in MIC
                            sam1_mic, sam2_mic, MIC_change = check_MIC_change(sam, possible_sample)
                            with open("MIC_change_results.tsv", "a") as results_out:
                                sample_printed_to_results.append(sam)
                                results_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                                sam, possible_sample, sam1_mic, sam2_mic, MIC_change, 
                                dictionary_of_close_samples[possible_sample], samples_with_variants_dic[sam],
                                sample_trunc_binary_dic[sam], sample_trunc_binary_dic[possible_sample]))
                            break

    else:
        with open("no_MIC_data.txt", "a") as no_MIC_out:
            no_MIC_out.write("%s has no MIC, skipping variant %s\n" % (sam, samples_with_variants_dic[sam]))

for sam in samples_to_check:
    if sam not in sample_printed_to_results:
        with open("no_results.tsv", "a") as no_results_out:
            variant = samples_with_variants_dic[sam]
            no_results_out.write("%s\t%s\n" % (sam, variant))
            


