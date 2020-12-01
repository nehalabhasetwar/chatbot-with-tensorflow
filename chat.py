import json #to import the json file
import numpy as np
import nltk
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from  tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

try:
    with open("data1.pickle", "rb") as f:
        bag, labels, trainX, trainY = pickle.load(f)
    print("Loading exsisting data")
    
except:    
    bag=[]#to collect the bag of words
    labels=[]#to store all of the tags
    x=[]#all of the phrases stemmed into words
    y=[]#store the labels related to the phrases


    #loading the json file
    #change the location accordingly. Thanks :)
    with open('intents.json') as file:
        data=json.load(file)#converting json to python dictionary

    #going through data to extract the words and  the tags
    for intent in data['intents']:
        labels.append(intent['tag'])
        for pattern in intent['patterns']:
            tokens=nltk.word_tokenize(pattern)
            bag.extend(tokens)#making a dic of words
            x.append(tokens)#this pattern phrases split into words is used as input
            y.append(intent['tag'])#setting the labels w.r.t 'x'


    bag=[stemmer.stem(token) for token in bag if token != '?']
    bag=sorted(list(set(bag)))

    #print(bag)
    #print(x)
    #print(labels)
    #print(y)

    ''' 
        From this part we start the training procedure.
            Now I will perform one hot encoding on this data to
            make it machine readable.

            I will take a numpy array(say training) of zeros same as the length of the bag. 

            Then, I will grab every token's list from 'x' and put a '1' 
            in the index corresponding to the token's originial position in the bag
    '''

    trainX=[]
    trainY=[]


    for ref,tokens in enumerate(x) :


        #print(ref,tokens)
        oheb=[]
        for word in bag:

            stem_tokens=[stemmer.stem(token) for token in tokens]

            if word in stem_tokens:
                oheb.append(1)	
            else :
                oheb.append(0)

        out=[0 for _ in range(len(labels))]
        out[labels.index(y[ref])]=1

        trainX.append(oheb)
        trainY.append(out)


    trainX=np.array(trainX)
    trainY=np.array(trainY)	
    with open("data.pickle", "wb") as f:
        pickle.dump((bag, labels, trainX, trainY), f)	

#print(trainX.shape)
#print(trainY.shape)

try:
    model=tf.keras.models.load_model('chatbot')
    print(model)
    print("Exsisting model loaded")
except:
    model=Sequential()
    model.add(Dense(64,input_shape=(len(trainX[0]),),activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32,activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(16,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(len(trainY[0]),activation='softmax'))

    model.summary()


    sgd=SGD(lr=0.01,decay=1e-5,momentum=0.9,nesterov=True)
    model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])
    
    model.fit(trainX,trainY, epochs=500, batch_size=8, verbose=1)
    
    model.save('chatbot')

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    out=[]
    for w in words:
        if w in s_words:
            out.append(1)
        else:
            out.append(0)
    return np.array([out])


def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp,bag)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                print('< tag: ',tag,'>',max(results))


chat()  

