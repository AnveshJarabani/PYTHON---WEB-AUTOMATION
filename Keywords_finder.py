import json,re
import pandas as pd
from collections import Counter
import nltk,os
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
cur_dir=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
data_dict=json.load(open(os.path.join(cur_dir,'job_data.json'),'r'))
# df_lst=[pd.DataFrame(i,index=[0]) for i in data_dict]
del data_dict['Form Data']
data_dict['Salary Detail'].extend(['\n\n']*(len(data_dict['Company Detail'])-len(data_dict['Salary Detail'])))
df=pd.DataFrame(data_dict)
print(df.columns)
df['Salary'] = df['Salary Detail'].apply(
    lambda x: [i for i in x.split('\n') if '$' in i])
df['Company'] = df['Company Detail'].apply(lambda x: x.split('\n')[1]
                                           if len(x.split('\n'))>1 else '')
df['Position'] = df['Details'].apply(lambda x: x.split('\n')[0])
patrn=re.compile(r"\b\w+\b")
nltk.download('stopwords')
stop_words=set(stopwords.words('english'))
filterd_phrases=[]
for i in df['Desc']:
    words=patrn.findall(i.lower())
    filterd_words=[wrd for wrd in words if wrd not in stop_words]
    phrases=list(ngrams(filterd_words,2)) # generate 2 word phrases
    filterd_phrases.extend(phrases)
phrase_frequencies=Counter(filterd_phrases)
keywords={'word':[i for i,_ in phrase_frequencies.items()],
          'freq':[i for _,i in phrase_frequencies.items()]}
lst=[]
for i in keywords['word']:
    v=''
    for j in i:
        v+=j+' '
    lst.append(v.strip())
keywords['word']=lst
df_phrases=pd.DataFrame(keywords)
df_phrases=df_phrases.sort_values(by='freq',ascending=False,ignore_index=True)
print(df_phrases.head(100))
# df_phrases.to_csv(path.format('key_phrases.csv'),index=False)
"""
1. FIND THE TOP 25 KEYWORDS WITH THE FREQUENCY FROM Desc
2. EXTRACT COMPANY NAMES, LOCATION, SALARY RANGE. 
3. DOES IT HAVE EASY APPLY ON THEM. 
"""
