# use as
# run vdb/flu_download_complete.py --virus flu --select lineage:seasonal_h3n2  --fstem h3n2

import os,datetime
from download import download
from download import get_parser

class flu_download(download):
    def __init__(self, **kwargs):
        download.__init__(self, **kwargs)

if __name__=="__main__":
    parser = get_parser()
    args = parser.parse_args()
    fasta_fields = ['strain', 'virus', 'accession', 'collection_date', 'region', 'country',
                    'division', 'location', 'passage_category', 'submitting_lab', 'age', 'gender']
    args.fasta_fields = fasta_fields
    current_date = str(datetime.datetime.strftime(datetime.datetime.now(),'%Y_%m_%d'))
    if args.fstem is None:
        args.fstem = args.virus + '_' + current_date
    if not os.path.isdir(args.path):
        os.makedirs(args.path)
    connfluVDB = flu_download(**args.__dict__)
    args.select.append("locus")
    vir = args.fstem
    for seg in ["pb1", "pb2", "ha", "na", "np", "mp", "pa", "ns"]:
        args.select[-1]="locus:%s"%seg
        args.fstem = vir+'_'+seg
        connfluVDB.download(**args.__dict__)
