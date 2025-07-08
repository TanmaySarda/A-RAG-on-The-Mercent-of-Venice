import os
import re 
import pandas as pd
import time

with open('Shakespeare.txt', 'r') as file:
    content = file.read()

content = re.sub(r'\b(enter|exit|exeunt|scene)\b', r'\n\1', content, flags=re.IGNORECASE)

content = content.split('\n')

content = [line.strip() for line in content if line.strip()]

dialogue_list = []

i = 0
while i < len(content):
    if(content[i].lower().startswith('enter') or content[i].lower().startswith('exit') or content[i].lower().startswith('exeunt')):
        content.pop(i)
        continue

    if(content[i].startswith('<<')):
        while(not content[i].endswith('>>')):
            content.pop(i)
        content.pop(i)
        continue

    i += 1


i = 0
if content[i].isdigit():
    current_play_name = content[i+1]
    i += 4



while(i < len(content)):
    if i < len(content) and content[i][:3] == 'ACT':
        parts = content[i].split(" ")  
        current_act = parts[1].removesuffix('.')
        i += 1
        continue

    
    if i < len(content) and content[i][:5] == 'SCENE':
        parts = content[i].split(" ")
        current_scene = parts[1].removesuffix('.')
        current_place = content[i+1]
        i += 1
        continue

    
    if content[i].split(" ")[0].endswith(".") and content[i].split(" ")[0].isupper():
        dialogue = content[i] + ' '
        flag = False
        i += 1
        while(i < len(content)):
            if(content[i].split(" ")[0].endswith(".") and content[i].split(" ")[0].isupper()):
                break
            if(content[i].startswith('SCENE')):
                parts = content[i].split(" ")
                current_scene = parts[1].removesuffix('.')
                current_place = content[i+1]
                i += 1
                continue
            if(content[i].startswith('ACT')):
                current_act = content[i].split(" ")[1].removesuffix('.')
                i += 1
                continue
            
            dialogue += content[i] + ' '
            i += 1

        speaker = dialogue.split(" ")[0][:-1]
        dialogue = dialogue.split(" ")[1:]
        dialogue = ' '.join(dialogue)
        dialogue.strip()
        
        if not dialogue.startswith('"'):
            dialogue = f'"{dialogue}'

        if dialogue.endswith(' '):
            dialogue = dialogue[:-1]
        
        if not dialogue.endswith('"'):
            dialogue = f'{dialogue}"'
        

        dialogue_list.append([current_act, current_scene, current_place, speaker, dialogue])
        continue


    i += 1


i = 1
while(i < len(dialogue_list)):
    pattern = r'([a-z0-9,.?!;-])([A-Z])'
    substitution = r'\1 \2'
    dialogue_list[i][4] = re.sub(pattern, substitution, dialogue_list[i][4])


    if dialogue_list[i][1] != dialogue_list[i-1][1]:
        dialogue_list[i][0:3] = dialogue_list[i-1][0:3]
        i += 1

    i += 1


df = pd.DataFrame(dialogue_list, columns=['Act', 'Scene', 'Place', 'Speaker', 'Dialogue'])
df.to_csv('dialogue.csv', index=False)