# =================================================================================
#                      Identity Generator (full names)
# =================================================================================
#
#  source data: 
#    https://www.ssa.gov/oact/babynames/limits.html (first names)
#    https://www.census.gov/topics/population/genealogy/data/2010_surnames.html (last names)
#               
import numpy as np
import pandas as pd
import argparse
import copy

# --- version
version = '0.0.1'

class Utilities:

    def __init__(self):

        self.female_ratio = 0.5 # female/(male + female)
        self.decades_start = 1940
        self.decades_end = 2000
        self.decades = list(range(self.decades_start, self.decades_end + 1, 10))
        self.file_path_last_names = './data/LastName/last_name.csv'
        self.file_path_first_names_template = './data/FirstName/first_names_||||year||||s_||||gender||||.csv'
        self.threshold_last_name = 400
        self.threshold_first_name = 400

    def get_num_samples_per_year(self, num_samples:int, decades:list):
        """
        """
        reminder = num_samples%len(decades)

        if reminder != 0:
            tmp = (num_samples - reminder) / len(decades)
            num_names_per_year = [tmp] * len(decades)
            num_names_per_year[-1] += reminder
        else:
            tmp = num_samples / len(decades)
            num_names_per_year = [tmp] * len(decades)
            
        return [int(v) for v in num_names_per_year]

    def sample_names_weighted(self, file_path:str, threshold:int, num_samples:int, seed:int=5963):
        """
        """
        # --- load file
        tmp = []
        with open(file_path, 'r') as f:
            for line in f:
                name,count = line.split(',')
                tmp.append((name.strip(), int(count.strip())))
                
        # --- names and counts
        _tmp = tmp[:threshold]
        names, counts = zip(*_tmp)
        
        # --- weigths
        weights = np.array(counts)/sum(counts)
        
        # --- seed
        np.random.seed(seed)
        
        return [np.random.choice(names, p = weights) for _ in range(num_samples)]

    def sample_last_names(self, num_samples:int):
        """
        """
        res = self.sample_names_weighted(
            file_path = self.file_path_last_names,
            threshold = self.threshold_last_name,
            num_samples = num_samples
        )
        return res

    def sample_first_names(self, num_samples:int):
        """
        """
        # --- initialization
        res = []

        # --- number of samples per year
        num_names_per_year = self.get_num_samples_per_year(
            num_samples = num_samples,
            decades = self.decades
        )

        # --- pick names with female_ratio
        for year, num in zip(self.decades, num_names_per_year):
            
            # --- number of names per gender
            num_male = int( num * self.female_ratio )
            num_female = num - num_male
                
            # --- file_paths
            file_path_male = copy.deepcopy(self.file_path_first_names_template)
            file_path_male = file_path_male.replace('||||year||||', str(year)).replace('||||gender||||', 'male')
     
            file_path_female = copy.deepcopy(self.file_path_first_names_template)
            file_path_female = file_path_male.replace('||||year||||', str(year)).replace('||||gender||||', 'female')
            
            # --- first names per year
            first_names_male = self.sample_names_weighted(
                file_path = file_path_male, 
                threshold = self.threshold_first_name,
                num_samples = num_male
            )

            first_names_female = self.sample_names_weighted(
                file_path = file_path_female, 
                threshold = self.threshold_first_name,
                num_samples = num_female
            )
            
            res.extend(first_names_male)
            res.extend(first_names_female)

        return res

def generate_full_names(num_samples:int, output_path:str):
    """
    """
    # ---
    res = []
    utils = Utilities()

    # --- last names
    last_names = utils.sample_last_names(num_samples)

    # --- first names
    first_names = utils.sample_first_names(num_samples)

    # --- concatenate first and last names (full name)
    for fn, ln in zip(first_names, last_names):
        res.append(f'{fn} {ln}')

    # --- save output (optional)
    if output_path != None:
        with open(output_path, 'w') as f:
            for name in res:
                f.write(name + '\n')

    return res


if __name__ == '__main__':

    # --- initialization
    arg_parser = argparse.ArgumentParser()

    # --- load parameters
    arg_parser.add_argument('--num_samples', type=int, default = 1000)
    arg_parser.add_argument('--output_path', type=str)

    # --- parser arguments
    options = arg_parser.parse_args()

    # --- single query
    res = generate_full_names(
        num_samples = options.num_samples,
        output_path = options.output_path
    )

    print('sample names')
    for name in res[:5]:
        print(name)


