"""Sort entities in a brat stand-off file.

Editing annotations in brat simply amends the annotation file. New and changed
entities can be added at the end of the existing entities.

For some of our tasks, it is easier if the entities are listed in offset order.

This script has two functions:
- sort_entities() to read and sort on start offset the entities in a brat file
returning a list of tuples.
- write_entities() to write the list of tuples to a file inserting new IDs
in an ascending order.

The script can be run on an individual file, or on all .ann files in a folder.

David King <David.King@open.ac.uk>
for ViBRANT <http://vbrant.eu//>
April 2014

License: GPLv2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt>
"""

from collections import namedtuple
import os
import re

Entity = namedtuple(
    'Entity',
    'brat_ID, brat_type, start_offset, other_offsets, brat_text')

extract_stand_off = re.compile(
    '(?P<brat_ID>\S+)\t'
    '(?P<brat_type>\S+)\W'
    '(?P<start_offset>\d+)\W'
    '(?P<other_offsets>[\d; ]+)\t'
    '(?P<brat_text>.*$)').search


def sort_entities(filename):
    """Return list of sorted entities from specified .ann file."""
    entities = []
    with open(filename, 'r', encoding='utf-8') as annotation_file:
        for line in annotation_file:
            stand_off = extract_stand_off(line)
            entities.append(Entity(
                brat_ID=stand_off.group('brat_ID'),
                brat_type=stand_off.group('brat_type'),
                start_offset=int(stand_off.group('start_offset')),
                other_offsets=stand_off.group('other_offsets'),
                brat_text=stand_off.group('brat_text')))
    entities.sort(key=lambda t: t.start_offset)
    return entities


def write_entities(entities, file_name):
    """Print formatted list of entities to specified .ann file."""
    with open(file_name, 'w', encoding='utf-8', newline='\n') as brat_file:
        for idx, entity in enumerate(entities, 1):
            brat_file.write(
                'T{:d}\t{entity.brat_type} '
                '{entity.start_offset} '
                '{entity.other_offsets}\t{entity.brat_text}\n'
                .format(idx, entity=entity))


def sort_file(file_name):
    """Sample routine to process one file."""
    sorted_entities = sort_entities(file_name)
    write_entities(sorted_entities, file_name)


def sort_folder(folder_name):
    """Sample routine to process one folder."""
    ann_files = (os.path.join(folder_name, filename)
                 for filename in os.listdir(folder_name)
                 if filename.endswith('ann'))
    for ann_file in ann_files:
        sorted_entities = sort_entities(ann_file)
        write_entities(sorted_entities, ann_file)


if __name__ == '__main__':

    # sort_file('aves_v1/d149.ann')

    # sort_folder('aves_v1')
    # sort_folder('mamm_v1')
    sort_folder('bot_v1')
