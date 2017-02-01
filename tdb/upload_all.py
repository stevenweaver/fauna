'''
Use this script to reconstruct titer database from archived files containing titer tables
Assumed directory structure is:
.
+-- data
|   +-- cdc
|       +-- subtype1
|           +-- flat_file_1.tsv
|           +-- flat_file_2.tsv
|           +-- ...
|       +-- subtype2
|       +-- ...
|   +-- elife
|       +-- subtype1
|           +-- flat_file_1.tsv
|           +-- flat_file_2.tsv
|           +-- ...
|       +-- subtype2
|       +-- ...
|   +-- nimr
|       +-- subtype1
|           +-- tabular_file_1.csv
|           +-- tabular_file_2.csv
|           +-- ...
|       +-- subtype2
|       +-- ...
+-- tdb
|   +-- upload_all.py
'''
import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument('--db', '--database', default='test_tdb_2', help="database to upload to")
parser.add_argument('--subtype', default='h3n2', help="subtype to upload")
parser.add_argument('--nimr_path', default='data/nimr/', help="directory containing NIMR titers")
parser.add_argument('--cdc_path', default='data/cdc/', help="directory containing CDC titers")
parser.add_argument('--elife_path', default='data/elife/', help="directory containing eLife titers")

def upload_nimr(database, nimr_path, subtype):
    '''
    Makes calls to tdb/upload.py for every file in an NIMR titer directory (default data/nimr/).
    All files in the directory should be tabular titer tables in CSV format for only one subtype
    of virus (H3N2, H1N1pdm, etc.).
    '''
    print "Beginning upload of NIMR documents to", database + "."
    path = nimr_path + subtype + "/"
    print "Uploading NIMR reports for subtype", subtype, "contained in directory", path + "."

    for fname in os.listdir(path):
        if fname[0] != '.':
            fpath = path + fname
            fstem = fname[:-4]
            command = "python tdb/nimr_upload.py -db " + database + " --subtype " + subtype + " --ftype tables --path " + path + " --fstem " + fstem
            subprocess.call(command, shell=True)
            print "Done with", fname + "."

    print "Done uploading NIMR documents."

def upload_cdc(database, cdc_path, subtype):
    '''
    Makes calls to tdb/upload.py for every flat file in an CDC titer directory (default data/cdc/).
    All files in the directory should be flat titer files in TSV format for only one subtype
    of virus (H3N2, H1N1pdm, etc.).
    '''
    print "Beginning upload of CDC documents to", database + "."
    path = cdc_path + subtype + "/"
    print "Uploading CDC reports for subtype", subtype, "contained in directory", path + "."

    for fname in os.listdir(path):
        if fname[0] != '.':
            fpath = path + fname
            fstem = fname[:-4]
            command = "python tdb/cdc_upload.py -db " + database + " --subtype " + subtype + " --path " + path + " --fstem " + fstem
            subprocess.call(command, shell=True)
            print "Done with", fname + "."

    print "Done uploading CDC documents."

def upload_elife(database, elife_path, subtype):
    '''
    Makes calls to tdb/upload.py for every flat file in an eLife titer directory (default data/elife/).
    All files in the directory should be flat titer files in TSV format for only one subtype
    of virus (H3N2, H1N1pdm, etc.).
    '''
    print "Beginning upload of stored NIMR documents to", database + "."
    path = elife_path + subtype + "/"
    print "Uploading CDC reports for subtype", subtype, "contained in directory", path + "."

    for fname in os.listdir(path):
        if fname[0] != '.':
            fpath = path + fname
            fstem = fname[:-4]
            command = "python tdb/elife_upload.py -db " + database + " --subtype " + subtype + " --path " + path + " --fstem " + fstem
            subprocess.call(command, shell=True)
            print "Done with", fname + "."

    print "Done uploading stored eLife documents."

if __name__=="__main__":
    args = parser.parse_args()
    db = args.db
    print "Beginning construction of", db + "."
    nd = args.nimr_path
    cd = args.cdc_path
    ed = args.elife_path
    upload_nimr(db, nd, "h3n2")
    upload_nimr(db, nd, "h1n1pdm")
    upload_nimr(db, nd, "vic")
    upload_nimr(db, nd, "yam")
    upload_cdc(db, cd, "h3n2")
    upload_elife(db, ed, "h3n2")
    upload_elife(db, ed, "vic")
    upload_elife(db, ed, "yam")
    print "Done with all uploads."
