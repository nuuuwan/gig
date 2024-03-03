from gig import Ent, EntType
from utils import File, JSONFile, Log
import json
log = Log('example-8')

CHILD_TYPE = EntType.GND
PARENT_TYPE = EntType.DSD
PARENT_ID_LAMBDA = lambda ent: ent.dsd_id

def main():
    child_ents = Ent.list_from_type(CHILD_TYPE)
    parent_ent_idx = Ent.idx_from_type(PARENT_TYPE)
    idx = {}
    for child_ent in child_ents:
        parent_id= PARENT_ID_LAMBDA(child_ent)
        parent = parent_ent_idx.get(parent_id)
        parent_name = parent.name
        child_name = child_ent.name
        if parent_name not in idx:
            idx[parent_name] = []
        idx[parent_name].append(child_name)

    idx = dict(sorted([[item[0], sorted(item[1])] for item in idx.items()], key=lambda item: item[0]))
    
    content = f'''// Auto Generated
const PLACE_IDX = {json.dumps(idx, indent=4)};    
export default PLACE_IDX;
'''
    js_path = __file__[:-3] + '.PLACE_IDX.js'
    File(js_path).write(content)
    log.info(f'Wrote {js_path}')
if __name__ == "__main__":
    main()