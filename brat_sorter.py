'''Sort entities in a brat stand-off file.

Editing annotations in brat simply amends the annotation file. New and changed
entities can be added at the end fo teh existing entities. 
For some of our tasks, it is easier if the entities are listed in offset order.
This script has two functions: one to read and sort on start offset the
entities in a brat file returning a list of tuples, and one to write the list
of tuples to a file inserting new IDs in acending order.

David King <David.King@open.ac.uk>
for ViBRANT <http://vbrant.eu//>
March 2013

License: GPLv2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt>
'''

from collections import namedtuple
import re

Entity = namedtuple('Entity',
                    'brat_ID, brat_type, start_offset, end_offset, brat_text')

def sort_entities(filename):
    entities = []
    extract_stand_off = re.compile(
        '(?P<brat_ID>\S+)\t'
        '(?P<brat_type>\S+)\W'
        '(?P<start_offset>\d+)\W'
        '(?P<end_offset>\d+)\t'
        '(?P<brat_text>\S+)')
    with open(filename, 'r', encoding='utf-8') as annotation_file:
        for line in annotation_file:
            stand_off = extract_stand_off.search(line)
            entities.append(
                Entity(
                brat_ID=stand_off.group('brat_ID'),
                brat_type=stand_off.group('brat_type'),
                start_offset=int(stand_off.group('start_offset')),
                end_offset=int(stand_off.group('end_offset')),
                brat_text=stand_off.group('brat_text')))
    entities.sort(key=lambda t: t.start_offset)
    return entities

def write_entities(entities, filename):
    with open(filename, 'w', encoding='utf-8', newline='\n') \
        as brat_file:
        for idx, entity in enumerate(entities, 1):
            brat_file.write(
                'T' + str(idx) + '\t' +
                entity.brat_type + ' ' +
                str(entity.start_offset) + ' ' +
                str(entity.end_offset) + '\t' +
                entity.brat_text + '\n')

if __name__ == '__main__':

    # sample uses

    # for a one off file sort
    entity_list = sort_entities('bca_03_aves_v4_ocr/bca_03_aves_v4_ocr_p003.ann')
    print(repr(entity_list)) # see what is returned
    write_entities(entity_list, 'bca_03_aves_v4_ocr/bca_03_aves_v4_ocr_p003_sorted.ann')

    # for a complete directory
    import os
    directory = 'bca_03_aves_v4_ocr'
    ann_list = [entry for entry in os.listdir(directory) if entry.endswith('ann')]
    for ann_file in ann_list:
        sorted_entities = sort_entities(directory + '/' + ann_file)
        write_entities(sorted_entities, directory + '/' + ann_file)
            