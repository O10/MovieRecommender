import sys
import os

datafile = sys.argv[1]

os.system("python create_rating_table.py " + datafile)
os.system("python create_movie_table.py " + datafile)
os.system("python create_sim_table_rating.py " + datafile)
os.system("python create_sim_table_content.py " + datafile)
os.system("python create_matrix_feature.py "+datafile)
os.system("python create_user_rec.py " + datafile)
