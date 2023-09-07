#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 13:09:26 2023

@author: nickarrivo
"""

import pandas as pd

data_2021 = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Composite Score Final 2021.csv')
data_2022 = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Composite Score Final 2022.csv')
data_2023 = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Composite Score Final 2023.csv')

data_2021['year_x'] = 2021
data_2022['year_x'] = 2022
data_2023['year_x'] = 2023
# Concatenate the original datasets vertically
vertical_merged_all_columns = pd.concat([data_2021, data_2022, data_2023], ignore_index=True)

# Display the first few rows of the vertically merged dataset with all columns
#vertical_merged_all_columns.head()


vertical_merged_all_columns.to_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Improved Vertical Merge Composite Score w stats.csv')
