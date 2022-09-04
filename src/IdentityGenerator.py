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
import pickle
import bz2
import json
import os
import sys

# --- version
version = '0.1.0'

class Utilities:

    def __init__(self):

        self.file_path_config = './data/config.json'
        self.file_path_last_names = './data/LastName/last_names.pbz2'
        self.file_path_first_names = './data/FirstName/first_names_decades.pbz2'

        # -- load config
        config = json.load( open(self.file_path_config, 'r') )
        self.female_ratio = config['female_ratio']
        self.decades_start = config['decades_start']
        self.decades_end = config['decades_end']
        self.last_names_range_start = config['last_names_range_start']
        self.last_names_range_end = config['last_names_range_end']
        self.first_names_range_start = config['first_names_range_start']
        self.first_names_range_end = config['first_names_range_end']
        self.random_seed = config['random_seed']
        self.weighted_samples = config['weighted_sampling']

        # --- validate input parameters
        if self.validate_input_parameters() == False:
            sys.exit("error in input parameter(s)")  

        # --- define range of decades
        self.decades = list(range(self.decades_start, self.decades_end + 1, 10))

        # --- load first names including preprocess
        self.dict_first_names = self.preprocess_first_names()

    def validate_input_parameters(self):
        """
        decade range, file_paths, last_name_range, first_name_range
        """
        pass_validation = False

        # --- out of range
        if (1880 > self.decades_start) or (2020 < self.decades_end):
            print(1)
            return pass_validation

        # --- inverted range (start > end)
        if (self.decades_end - self.decades_start) < 0:
            print(2)
            return pass_validation

        # --- file paths
        if os.path.isfile(self.file_path_last_names) == False:
            print(3)
            return pass_validation

        if os.path.isfile(self.file_path_first_names) == False:
            print(4)
            return pass_validation

        # --- last names
        if (self.last_names_range_end - self.last_names_range_start) < 0:
            print(5)
            return pass_validation

        if (self.last_names_range_end - self.last_names_range_start) > 1000:
            print(6)
            return pass_validation

        # --- first names
        if (self.first_names_range_end - self.first_names_range_start) < 0:
            print(7)
            return pass_validation

        # --- number of names are depending on decades

        # --- passed all validation
        pass_validation = True

        return pass_validation

    def preprocess_first_names(self):
        """
        load pbz2 file and split data by years and genders
        """
        # --- initialization
        res = dict()

        # --- load data
        df_raw = self.load_pickled_bz2_file(self.file_path_first_names)

        # --- slice data by decades
        df = df_raw[
            (df_raw.year >= self.decades_start) &
            (df_raw.year <= self.decades_end)
        ]

        # --- 
        for year in df.year.unique():

            # --- slice year
            _df = df[df.year == year].copy()

            # --- slice by gender
            _df_m = _df[_df.gender == 'M'].sort_values(by = 'count', ascending = False)
            _df_f = _df[_df.gender == 'F'].sort_values(by = 'count', ascending = False)

            # --- slice by range
            start = self.first_names_range_start
            end   = self.first_names_range_end

            # --- update "end" if it is needed
            if end >= min( len(_df_m), len(_df_f) ):
                end = min( len(_df_m), len(_df_f) )

            # --- slice by specified range (ranking)
            _df_m = _df_m[start-1:end]
            _df_f = _df_f[start-1:end]

            # --- store sliced dataframe
            res[year] = {
                'male': _df_m[['name', 'count']],
                'female': _df_f[['name', 'count']]
            }

        return res

    def preprocess_last_names(self):
        """
        load pbz2 file and split data
        """
        # --- initialization
        res = dict()

        # --- load data
        df_raw = self.load_pickled_bz2_file(self.file_path_last_names)

        # --- slice by range
        start = self.last_names_range_start
        end   = self.last_names_range_end

        # --- update "end" if it is needed
        if end >= len(df_raw):
            end = len(df_raw)

        # --- slice data by decades
        df = df_raw[start-1:end].copy()

        return df[['name', 'count']]

    def get_num_samples_per_decade(self, num_samples:int, decades:list):
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

    def sample_last_names(self, num_samples:int):
        """
        """
        # --- get names and weights
        df = self.preprocess_last_names()

        # --- sampling 
        if self.weighted_samples:
            res = df.sample(
                n = num_samples,
                weights = 'count',                
                random_state = self.random_seed,
                replace = True
            )['name']
        else:
            res = df['name'].sample(
                n = num_samples, 
                random_state = self.random_seed,
                replace = True
            )            
        return res.tolist()

    def sample_first_names(self, num_samples:int):
        """
        """
        # --- initialization
        res = []
        source = self.preprocess_first_names()

        # --- number of samples per year
        num_names_per_year = self.get_num_samples_per_decade(
            num_samples = num_samples,
            decades = self.decades
        )

        # --- pick names with female_ratio
        for year, num in zip(self.decades, num_names_per_year):
            
            # --- number of names per gender
            num_male = int( num * self.female_ratio )
            num_female = num - num_male

            # --- sampling male names
            _df_m = source[year]['male'] 
            if self.weighted_samples:
                first_names_male = _df_m.sample(
                    n = num_male, 
                    random_state = self.random_seed,
                    weights = 'count',
                    replace = True
                )['name'].tolist()
            else:
                first_names_male = _df_m['name'].sample(
                    n = num_male, 
                    random_state = self.random_seed,
                    replace = True
                ).tolist()

            # -- sampling female names
            _df_f = source[year]['female'] 
            if self.weighted_samples:
                first_names_female = _df_f.sample(
                    n = num_female, 
                    random_state = self.random_seed,
                    weights = 'count',
                    replace = True
                )['name'].tolist()
            else:
                first_names_female = _df_f['name'].sample(
                    n = num_female, 
                    random_state = self.random_seed,
                    replace = True
                ).tolist()                      
                
            res.extend(first_names_male)
            res.extend(first_names_female)

        return res

    def load_pickled_bz2_file(self, file_path:str):
        """
        """
        if file_path.lower().endswith('.pbz2') == False:
            file_path = f'{file_path}.pbz2'
        return pickle.load( bz2.BZ2File(file_path, 'rb') )

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

    print('--- first 5 generated sample names')
    for name in res[:5]:
        print(name)


