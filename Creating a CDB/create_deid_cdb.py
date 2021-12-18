from medcat.cdb_maker import CDBMaker
from medcat.config import Config
import pandas as pd

csv_path = '../Creating_a_de-identification_terminology/20211218_cat_anon_cdb.csv'  # DEID terminology path
output_cdb = '20211218_basic_deid_cdb.dat'  # Name of CDB output

csv = pd.read_csv(csv_path)

# Create CDB
config = Config()  # default config is fine
maker = CDBMaker(config)
cdb = maker.prepare_csvs([csv_path], full_build=True)

cdb.save(output_cdb)
