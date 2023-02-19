import os
import time
from Dialogue import Dialogue


DIALOGUES_PATH = './Dialogues'
with open(os.path.join(DIALOGUES_PATH, 'test.csv'), 'r', encoding='utf-8') as f:
    all = f.read()

dial = Dialogue(all)
dialIter = dial.__iter__()

for i in dialIter :
    print(i)
    print(i[0])
    time.sleep(2)

