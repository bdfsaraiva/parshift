import csv
import pandas as pd

def read_conversation(filename, delimiter=','):
    """_summary_

    Args:
        filename (csv): _description_
        delimiter (str, optional): _description_. Defaults to ','.

    Returns:
        list: _description_
    """

    conversation = []
    with open(filename, 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file, delimiter = delimiter)
        
        turn = 0 
        for idx, csv_line in enumerate(csv_reader):
            
            if idx != 0 and conversation[turn-1]['user_id'] == csv_line[1] and conversation[turn-1]['reply_id'] == csv_line[3]:
                msg_join = f"{conversation[turn-1]['message_text']}. {csv_line[2]}"
                list_id = conversation[turn-1]['id'] + [csv_line[0]]
                conversation[turn-1]['id'] = list_id
                conversation[turn-1]['message_text'] = msg_join

            else:
                id = csv_line[0]
                user_id = csv_line[1]
                message_text = csv_line[2]
                reply_id = csv_line[3]
                turn +=1

                conversation.append({
                    'id': [id],
                    'user_id': user_id,
                    'message_text': message_text,
                    'reply_id': reply_id
                })


    return conversation

def pshift_annotation(filename, delimiter=','):

    conversation = read_conversation(filename)

    df = pd.DataFrame({'id': [],
                        'user_id': [],
                        'message_text': [],
                        'reply_id': [],
                        'label_desc': [],
                        'label_code': [],
                        'label_value': []})

    part_1 = ''
    part_2 = ''
    p1p2 = ''
    label_code_v = ''
    label_type_v = ''

    for idx,msg in enumerate(conversation):

        if msg['reply_id'] == None or msg['reply_id'] == 'None':
            part_2 = ' ' + str(msg['user_id']) + ' to group'
        else:
            for msgPrev in conversation:
                if msg['reply_id'] in msgPrev['id']:
                    if msgPrev['reply_id'] == None or msgPrev['reply_id'] == 'None':
                        part_1 = str(msgPrev['user_id']) + ' to group,'
                    else:  # SE O REPLY TIVER TAMBÉM REPLY
                        for msgPrev2 in conversation:
                            if msgPrev['reply_id'] in msgPrev2['id']:  # ENCONTRAR REPLY-REPLY
                                part_1 = str(msgPrev['user_id']) + ' to ' + str(msgPrev2['user_id']) + ','

                    part_2 = ' ' + str(msg['user_id']) +' to ' + str(msgPrev['user_id'])

        p1p2 = part_1 + part_2
        # print(part_1 + part_2)
        part_1 = part_2[1:] + ','

        #############! CRIAÇÃO DE CODIGOS ##########
        def label_code(label):
            # divisão por partes
            a = label.split(',')[0].split('to')[0].replace(' ', '')
            b = label.split(',')[0].split('to')[1].replace(' ', '')
            c = label.split(',')[1].split('to')[0].replace(' ', '')
            d = label.split(',')[1].split('to')[1].replace(' ', '')

            # 1
            result = 'A'

            # 2
            result += '0-' if b == 'group' else 'B-'

            # 3
            if c == a:
                result += 'A'
            elif c == b:
                result += 'B'
            else:
                result += 'X'

            # 4
            if d == 'group':
                result += '0'
            elif d == a:
                result += 'A'
            elif d == b:
                result += 'B'
            else:
                result += 'Y'

            return result
        #######!#####################################

        
        if idx != 0:
            msg['label'] = p1p2
            label_code_v = label_code(p1p2)
            msg['label_code'] = label_code_v
            label_type_v = label_type(label_code_v)
            msg['label_type'] = label_type_v

        
        df.loc[len(df.index)] = [str(msg['id']), str(msg['user_id']), msg['message_text'], str(msg['reply_id']),
            (p1p2), (label_code_v), (label_type_v)]
        # print('-'*20)
    return df

def label_type(label_code):
    """Returns the Participation Shift type, based in Gibson's paper

    Args:
        label_code (str): Participation Shift Code (e.g A0-XA) 

    Returns:
        str: Participation Shift type - one of [Turn Receiving, Turn Claiming, Turn Usurping, Turn Continuing] 
    """
    p_shift = {
        'AB-BA': 'Turn Receiving',
        'AB-B0': 'Turn Receiving',
        'AB-BY': 'Turn Receiving',
        'A0-X0': 'Turn Claiming',
        'A0-XA': 'Turn Claiming',
        'A0-XY': 'Turn Claiming',
        'AB-X0': 'Turn Usurping',
        'AB-XA': 'Turn Usurping',
        'AB-XB': 'Turn Usurping',
        'AB-XY': 'Turn Usurping',
        'A0-AY': 'Turn Continuing',
        'AB-A0': 'Turn Continuing',
        'AB-AY': 'Turn Continuing',
        'A0-A0': 'Turn Continuing',
    }
    return p_shift[label_code]

# print(pshift_annotation('./py-Participation-Shifts/py-participation-shifts/a.csv'))



