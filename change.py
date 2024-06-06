import json
import random
from collections import defaultdict

def transform_data(input_data, relation_count):
    output_data = {'token': [], 'h': {}, 't': {}, 'relation': ''}
    sent = input_data['sentText']
    output_data['token'] = sent.split()

    if input_data.get('relationMentions'):
        relations = sorted(input_data['relationMentions'], key=lambda x: relation_count.get(x['label'], 0))
        # choose the relation which has minimum count
        rel = relations[0] if relations else None
        if rel:
            output_data['h'] = {'name': rel['em1Text'], 'pos': [rel['e1start'], rel['e1start'] + len(rel['em1Text'])]}
            output_data['t'] = {'name': rel['em2Text'], 'pos': [rel['e21start'], rel['e21start'] + len(rel['em2Text'])]}
            output_data['relation'] = rel['label']

    return output_data, output_data['relation']

relation_count = defaultdict(int)
with open('train_1.json', 'r') as f_in, open('change2.txt', 'w', encoding='utf-8') as f_out:
    for line in f_in:
        input_data = json.loads(line)
        transformed_data, relation = transform_data(input_data, relation_count)
        if relation:  
            f_out.write(json.dumps(transformed_data, ensure_ascii=False))
            f_out.write('\n')
            relation_count[relation] += 1

print("Transform completed and data saved to change2.txt")
print("Distribution of relations: ", dict(relation_count))
