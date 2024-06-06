import json

def get_empty_relation_instance(input_data):
    # if relationMentions exists and is not empty return all relations in the entry
    for rel in input_data.get('relationMentions', []):
        if rel['label'] == '':
            return True 
    return False

with open('train_1.json', 'r') as f_in:
    for line in f_in:
        input_data = json.loads(line)
        if get_empty_relation_instance(input_data):
            print("Found a example with empty relation: ", json.dumps(input_data, ensure_ascii=False))
            break
