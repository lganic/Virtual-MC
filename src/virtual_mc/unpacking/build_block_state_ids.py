import json
import os

BLOCKS_RELPATH = 'generated/reports/blocks.json'

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../../data')
BLOCKS_PATH = os.path.join(os.path.dirname(__file__), BLOCKS_RELPATH)

def build_id_lookup():

    # Load raw blocks json

    with open(BLOCKS_PATH, 'r') as blocks_json:

        block_data = json.load(blocks_json)
    
    block_data: dict

    output_data = {}

    basic_block_ids = {}

    print('Building ID lookup table...')

    for block_name in block_data:
        
        for block_state in block_data[block_name].get('states', []):

            properties = block_state.get('properties', {})
            properties['name'] = block_name
            state_id = block_state['id']
            output_data[state_id] = properties

            if len(properties) == 1:

                if block_name in basic_block_ids:
                    raise IndexError('Attempting to re-add block to basic block ID table. Something must have changed in the minecraft format!')
                
                basic_block_ids[block_name] = state_id
    
    print('Writing to id_to_block.json...')
    with open(os.path.join(DATA_PATH, 'id_to_block.json'), 'w') as output_file:
        json.dump(output_data, output_file)

    print('Writing to basic_block_to_id.json...')
    with open(os.path.join(DATA_PATH, 'basic_block_to_id.json'), 'w') as output_file:
        json.dump(basic_block_ids, output_file)

if __name__ == '__main__':
    build_id_lookup()



    #     "states": [
    #   {
    #     "id": 9482,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "north",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "id": 9483,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "north",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9484,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "south",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "id": 9485,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "south",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9486,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "west",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "id": 9487,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "west",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9488,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "east",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "id": 9489,
    #     "properties": {
    #       "face": "floor",
    #       "facing": "east",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9490,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "north",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "default": true,
    #     "id": 9491,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "north",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9492,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "south",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "id": 9493,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "south",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9494,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "west",
    #       "powered": "true"
    #     }
    #   },
    #   {
    #     "id": 9495,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "west",
    #       "powered": "false"
    #     }
    #   },
    #   {
    #     "id": 9496,
    #     "properties": {
    #       "face": "wall",
    #       "facing": "east",
    #       "powered": "true"
    #     }
    #   },