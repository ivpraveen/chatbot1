from enum import Enum
import numpy as np


class EntityTracker():

    def __init__(self):
        self.entities = {
                '<amount>' : None,
                '<paydate>' : None,
                '<loan>' : None,
                }
        self.num_features = 3 # tracking 4 entities
        self.rating = None

        # constants
        #self.party_sizes = ['1', '2', '3', '4', '5', '6', '7', '8', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
        #self.locations = ['bangkok', 'beijing', 'bombay', 'hanoi', 'paris', 'rome', 'london', 'madrid', 'seoul', 'tokyo'] 
        #self.cuisines = ['british', 'cantonese', 'french', 'indian', 'italian', 'japanese', 'korean', 'spanish', 'thai', 'vietnamese']
        #self.rest_types = ['cheap', 'expensive', 'moderate']
        self.amount = ['$1000', '$1200', '$600']
        self.paydate = ['10thjuly','15thjuly','16thjuly','05thjuly','05thaugust']
        self.loan = ['educationloan','homeloan','creditcard']
        self.EntType = Enum('Entity Type', '<amount> <paydate> <loan>')


    def ent_type(self, ent):
        if ent in self.amount:
            return self.EntType['<amount>'].name
        elif ent in self.paydate:
            return self.EntType['<paydate>'].name
        elif ent in self.loan:
            return self.EntType['<loan>'].name
        else:
            return ent


    def extract_entities(self, utterance, update=True):
        tokenized = []
        for word in utterance.split(' '):
            entity = self.ent_type(word)
            if word != entity and update:
                self.entities[entity] = word

            tokenized.append(entity)

        return ' '.join(tokenized)


    def context_features(self):
       keys = list(set(self.entities.keys()))
       self.ctxt_features = np.array( [bool(self.entities[key]) for key in keys], 
                                   dtype=np.float32 )
       return self.ctxt_features


    def action_mask(self):
        print('Not yet implemented. Need a list of action templates!')
