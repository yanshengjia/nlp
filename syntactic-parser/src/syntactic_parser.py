# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-04 Monday
# @email: i@yanshengjia.com


from __future__ import unicode_literals, print_function
import spacy

def main():
    model='en_core_web_sm'
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)

    doc = nlp("When I was and the @NUM1 grade and I had to put a mible set up, and then I went to put the mible set up and it bruck and then we went to the park and I had to wate for the shag, and after that went to the ice making and I had to hart in a line of people in then when we got ther we pard them are munem and axyer that we went ice starting. and then that was all we did which that day in then he went back to the house to build are mible mirne and art of that way went to the house in plade outside in inside the house")
    
    # pos tagging
    for token in doc:
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_stop)
        print(token.text, token.pos_)
    print('-----------------------')

    # principal component analysis
    for word in doc:
        if word.dep_ in ('xcomp', 'ccomp'):
            print(''.join(w.text_with_ws for w in word.subtree))
    print('-----------------------')
    
    for word in doc:
        if word.dep_ in ('xcomp', 'ccomp'):
            subtree_span = doc[word.left_edge.i : word.right_edge.i + 1]
            print(subtree_span.text, '|', subtree_span.root.text)

if __name__ == '__main__':
    main()