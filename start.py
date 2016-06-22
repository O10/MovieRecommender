import sys
import os
import time

datafile = sys.argv[1]

os.system("python create_rating_table.py " + datafile)
os.system("python create_eval_data_v2.py ")
os.system("python create_movie_table.py " + datafile)
os.system("python create_sim_table_rating.py ")
os.system("python create_sim_table_content.py ")
os.system("python create_matrix_feature.py ")
os.system("python create_user_rec.py ")
