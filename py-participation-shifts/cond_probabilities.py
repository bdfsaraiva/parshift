import pandas as pd
from annotation import pshift_annotation


def frequency_table(file_name):

    df = pshift_annotation(file_name)

    pshift_codes = ['AB-BA', 'AB-B0', 'AB-BY', 'A0-X0', 'A0-XA', 'A0-XY', 'AB-X0', 'AB-XA', 'AB-XB', 'AB-XY', 'A0-AY', 'AB-A0', 'AB-AY', 'A0-A0']

    dict_prob_empirical_count = {}
    count_start_A0_total = 0
    count_start_AB_total = 0
    count_not_turn_continuing_A0 = 0
    count_not_turn_continuing_AB = 0

    for code in pshift_codes:
        count = 0
        for index, row in df.iterrows():
            # print(users_data[line[1]]['gender'])
            # users_data[line[1]]['gender'] == 'FEMALE' and
            if row['label_code'] == code :
                count += 1
        
        dict_prob_empirical_count[code] = count
        
        if code.split('-')[0] == 'A0':
            count_start_A0_total += count
            if code not in ['A0-AY','AB-A0','AB-AY','A0-A0']:
                count_not_turn_continuing_A0 += count
        else:
            count_start_AB_total +=count
            if code not in ['A0-AY','AB-A0','AB-AY','A0-A0']:
                count_not_turn_continuing_AB += count

    # print(dict_prob_empirical_count)
    # print(count_start_A0_total)
    # print(count_start_AB_total )
    # print(count_not_turn_continuing_A0)
    # print(count_not_turn_continuing_AB)    
    return [dict_prob_empirical_count, count_start_A0_total, count_start_AB_total, count_not_turn_continuing_A0, count_not_turn_continuing_AB]



def conditional_probabilities(file_name):
    frequency_table_and_counts = frequency_table(file_name)
    freq_table = frequency_table_and_counts[0]

    cond_prob = {}
    for key in freq_table:
        if key.split('-')[0] == 'A0':
            if key not in ['A0-AY','AB-A0','AB-AY','A0-A0']:
                cond_prob[key] = {
                    'CP General': round(freq_table[key] / frequency_table_and_counts[1], 2),
                    'CP excludes turn continuing': round(freq_table[key] / frequency_table_and_counts[3],2)
                }
            else:
                cond_prob[key] = {
                    'CP General': round(freq_table[key] / frequency_table_and_counts[1], 2),
                    'CP excludes turn continuing': ''
                }
        else:
            if key not in ['A0-AY','AB-A0','AB-AY','A0-A0']:
                cond_prob[key] = { 
                    'CP General': round(freq_table[key] / frequency_table_and_counts[2], 2),
                    'CP excludes turn continuing': round(freq_table[key] / frequency_table_and_counts[4],2)
                }
            else:
                cond_prob[key] = {
                    'CP General': round(freq_table[key] / frequency_table_and_counts[2], 2),
                    'CP excludes turn continuing': ''
                }

    cond_prob = pd.DataFrame.from_dict(cond_prob, orient='index')
    freq = pd.DataFrame.from_dict(freq_table, orient='index', columns=['Frequency'])
    result = pd.concat([freq, cond_prob], axis=1)
    custom_dict={
        'AB-BA': 5, 'AB-B0': 6,
        'AB-BY': 11, 'A0-X0': 1,
        'A0-XA': 0, 'A0-XY': 2,
        'AB-X0': 7, 'AB-XA': 8,
        'AB-XB': 9, 'AB-XY': 12,
        'A0-AY': 3, 'AB-A0': 10,
        'AB-AY': 12, 'A0-A0': 4
    }
    result = result.sort_index(key = lambda x: x.map(custom_dict))
    return result


print(conditional_probabilities('./py-Participation-Shifts/py-participation-shifts/a.csv'))