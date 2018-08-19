import modules.util as util
import numpy as np

'''
    Action Templates

    1. 'any preference on a type of cuisine',
    2. 'api_call <party_size> <rest_type>',
    3. 'great let me do the reservation',
    4. 'hello what can i help you with today',
    5. 'here it is <info_address>',
    6. 'here it is <info_phone>',
    7. 'how many people would be in your party',
    8. "i'm on it",
    9. 'is there anything i can help you with',
    10. 'ok let me look into some options for you',
    11. 'sure is there anything else to update',
    12. 'sure let me find an other option for you',
    13. 'what do you think of this option: ',
    14. 'where should it be',
    15. 'which price range are looking for',
    16. "you're welcome",

    [1] : cuisine
    [2] : location
    [3] : party_size
    [4] : rest_type

'''
class ActionTracker():

    def __init__(self, ent_tracker):
        # maintain an instance of EntityTracker
        self.et = ent_tracker
        # get a list of action templates
        self.action_templates = self.get_action_templates()
        self.action_size = len(self.action_templates)
        # action mask
        self.am = np.zeros([self.action_size], dtype=np.float32)
        # action mask lookup, built on intuition
        '''self.am_dict = {
                '000' : [3,5,6,7,9,11,12,13],
                '001' : [1,2,4,10],
                '011' : [1,2,4,10],
                '010' : [3,5,6,7,9,11,12],
                '100' : [3,5,6,7,9,11,12],
                '101' : [1,2,4,10],
                '110' : [5,6,9,11,12],
                '111' : [1,2,4,10]
                }'''
        self.am_dict = {
                '000' : [5,11,13,7,17,9,15,1,8,14,16,12,10,18],
                '001' : [3,4,1,2,6,12,13,17],
                '011' : [3,4,1,2,6,12,13,17],
                '010' : [5,11,13,7,17,9,15,1,8,14,16,12,10,18],
                '100' : [5,11,13,7,17,9,15,1,8,14,16,12,10,18],
                '101' : [3,4,1,2,6,12,13,17],
                '110' : [5,11,13,7,17,9,15,1,8,14,16,12,10,18],
                '111' : [3,4,1,2,6,12,13,17]
                }

        '''self.am_dict = {
                '0' : [3,5,6,7,9,11,12],
                '1' : [1,2,4,10]
                }'''

    def action_mask(self):
        # get context features as string of ints (0/1)
        ctxt_f = ''.join([ str(flag) for flag in self.et.context_features().astype(np.int32) ])

        def construct_mask(ctxt_f):
            indices = self.am_dict[ctxt_f]
            for index in indices:
                self.am[index-1] = 1.
            return self.am
    
        return construct_mask(ctxt_f)

    def get_action_templates(self):
        responses = list(set([ self.et.extract_entities(response, update=False) 
            for response in util.get_responses() ]))

        def extract_(response):
            template = []
            for word in response.split(' '):
                if 'resto_' in word: 
                    if 'phone' in word:
                        template.append('<info_phone>')
                    elif 'address' in word:
                        template.append('<info_address>')
                    else:
                        template.append('<restaurant>')
                else:
                    template.append(word)
            return ' '.join(template)

        # extract restaurant entities
        return sorted(set([ extract_(response) for response in responses ]))
