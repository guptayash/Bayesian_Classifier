import os
import time
import nltk, string, math
from string import digits
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from itertools import islice
stop_words=set(stopwords.words('english'))
def make_Dictionary(Email_Data):
    emails = [os.path.join(Email_Data,f) for f in os.listdir(Email_Data)]    
    all_words = []       
    for mail in emails:    
        with open(mail) as m:
            data=m.read()
        translator = data.maketrans('', '', string.punctuation) #PunctuationFilter
        remove_digits = data.maketrans('', '', digits) #DigitFilter
        data_filtered_with_numbers=data.translate(translator)
        data_filtered=data_filtered_with_numbers.translate(remove_digits)
        data_token=word_tokenize(data_filtered)
        #print (data_token)
        filtered_sentence=[]
        filtered_lemmatize=[]
        for w in data_token:
            if w not in stop_words:
                filtered_sentence.append(w)
        lmtzr=WordNetLemmatizer()
        for i in filtered_sentence:
            v=lmtzr.lemmatize(i)
            filtered_lemmatize.append(v)
        #print (filtered_sentence)
        
        all_words += filtered_lemmatize
    
    dictionary = Counter(all_words)
    #print(len(dictionary))
    
    return (dictionary)
Email_Ham_Dic=make_Dictionary('Email_Ham')
Email_Spam_Dic=make_Dictionary('Email_Spam')
#print(Email_Ham_Dic)
shared_items = dict(set(Email_Ham_Dic.items()) & set(Email_Spam_Dic.items()))

#print(shared_items)
##print (shared_items)
shared_sorted=(sorted(shared_items.items(), key=lambda kv: kv[1], reverse=True))
shared_sorted_sliced=list(islice(shared_sorted,20))

##print(len(shared_items))
##print("Most Common Ham",Email_Ham_Dic.most_common(30))
##print("Most Common Spam",Email_Spam_Dic.most_common(30))
##print("Most Common Common",shared_sorted_sliced )
#print(Email_Ham_Dic.items())
terms=['online','plant','also','reference','needed','currently','proposal','pleased',
       'department','still','way','file','family','receive','mean','made','web',
       'news','simple','information','order','money','claim','bank','question'
       ,'sap','pipeline','account','email','winning']
term_vector_Ham={}
for i in terms:
    if i in Email_Ham_Dic.keys():
        term_vector_Ham[i]=(Email_Ham_Dic[i])
    else:
        term_vector_Ham[i]=0
term_vector_Spam={}
for i in terms:
    if i in Email_Spam_Dic.keys():
        term_vector_Spam[i]=(Email_Spam_Dic[i])
    else:
        term_vector_Spam[i]=0
term_vector_total =[x + y for x, y in zip(term_vector_Spam, term_vector_Ham)]
#print(term_vector_Ham,term_vector_Spam)
sum_Spam=0
sum_Ham=0
for i in term_vector_Spam:
    sum_Spam+=term_vector_Spam[i]
for i in term_vector_Ham:
    sum_Ham+=term_vector_Ham[i]
#print(sum_Ham,sum_Spam)
def prob(term,Sum):
    prob_term= (term+1)/(Sum+2)
    return prob_term

array_prob_ham=[]
array_prob_spam=[]
for i in terms:
    array_prob_ham.append(prob(term_vector_Spam[i],sum_Spam))
    array_prob_spam.append(prob(term_vector_Ham[i],sum_Ham))
#print(array_prob_ham,"\n",array_prob_spam)
##print(prob(term_vector_Spam['online'],sum_Spam))
test_dict=make_Dictionary('Test')
#print(test_dict)
test_vector={}
for i in terms:
    if i in test_dict.keys():
        test_vector[i]=test_dict[i]
    else:
        test_vector[i]=0
test_vector_strip={}
for i in test_vector.keys():
    if test_vector[i]!=0:
        test_vector_strip[i]=test_vector[i]
sum_test_vector=0
for i in test_vector:
    sum_test_vector+=test_vector[i]
prob_test= 1
for i in test_vector_strip.keys():
    #print(i)
    a=array_prob_ham[terms.index(i)]
    prob_test*= (a**test_vector_strip[i])/test_vector_strip[i]
prob_test=prob_test*math.factorial(sum_test_vector)
#print(prob_test)
#print(sum_test_vector)
prob_test1=1
for i in test_vector_strip.keys():
    #print(i)
    a=array_prob_spam[terms.index(i)]
    prob_test1*= (a**test_vector_strip[i])/test_vector_strip[i]
#print(sum_test_vector)
prob_test1=prob_test1*math.factorial(sum_test_vector)
#print(prob_test1)
if(prob_test>prob_test1):
    print('Mail is a Spam')
else:
    print('Mail is not Spam')
