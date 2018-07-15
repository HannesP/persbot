# -*- coding: utf-8 -*-

#import urllib2
#python pwb.py pagefromfile -notitle -file:../dict.txt

import sys, unidecode, codecs, pickle

def add_form(person, number, ta, mood, tr, form, verb, verbtr):
	params = [(u'\u200f%s\u200e' % verb, verbtr), str(person), number, '', '', ta, mood]
	tinvoc = u'{{inflection of|'+verb+'||lang=fa|'+str(person)+'||'+number+'|'+ta+'|'+mood+'|tr='+verbtr+'}}'
	content = u'''==Persian==
===Verb===
{{head|fa|verb form|sc=fa-Arab|tr=%s}}
# %s''' % (tr, tinvoc)

	return """{{-start-}}
'''%s'''
%s
{{-stop-}}""" % (form, content)

def stress(s):
	repl_tbl = {}
	repl_tbl[u'a'] = u'á'
	repl_tbl[u'â'] = u'ấ'
	repl_tbl[u'e'] = u'é'
	repl_tbl[u'i'] = u'í'
	repl_tbl[u'u'] = u'ú'
	repl_tbl[u'o'] = u'ó'
	highest_ind = max([i for i,c in enumerate(s) if c in repl_tbl.keys()])
	return s[:highest_ind] + repl_tbl[s[highest_ind]] + s[highest_ind+1:]

try:
	history = pickle.load(open('history.bin','r'))
except:
	history = set()

def generate_forms(past_fa, past_tr, pres_fa=None, pres_tr=None, be=None):
	if be is None:
		be = u'bé'
	
	if not pres_fa and past_fa[-2:] == u'ید':
		pres_fa = past_fa[:-2]
		pres_tr = past_tr[:-2]
	
	verb = past_fa + u'ن'
	past_tr_str = stress(past_tr)
	verbtr = past_tr + 'an'
	
	if pres_tr[0] in ('i', 'y'):
		print 'Error!'
		return
	
	history.add((past_fa, past_tr, pres_fa, pres_tr, be))
	
	forms = []
	forms.append(add_form(1, 's', 'pres', 'ind', u'mí-{}am'.format(pres_tr), u'می‌{}م'.format(pres_fa), verb, verbtr))
	forms.append(add_form(2, 's', 'pres', 'ind', u'mí-{}i'.format(pres_tr), u'می‌{}ی'.format(pres_fa), verb, verbtr))
	forms.append(add_form(3, 's', 'pres', 'ind', u'mí-{}ad'.format(pres_tr), u'می‌{}د'.format(pres_fa), verb, verbtr))
	forms.append(add_form(1, 'p', 'pres', 'ind', u'mí-{}im'.format(pres_tr), u'می‌{}یم'.format(pres_fa), verb, verbtr))
	forms.append(add_form(2, 'p', 'pres', 'ind', u'mí-{}id'.format(pres_tr), u'می‌{}ید'.format(pres_fa), verb, verbtr))
	forms.append(add_form(3, 'p', 'pres', 'ind', u'mí-{}and'.format(pres_tr), u'می‌{}ند'.format(pres_fa), verb, verbtr))
	
	forms.append(add_form(1, 's', 'imperfect', 'ind', u'mí-{}am'.format(past_tr), u'می‌{}م'.format(past_fa), verb, verbtr))
	forms.append(add_form(2, 's', 'imperfect', 'ind', u'mí-{}i'.format(past_tr), u'می‌{}ی'.format(past_fa), verb, verbtr))
	forms.append(add_form(3, 's', 'imperfect', 'ind', u'mí-{}'.format(past_tr), u'می‌{}'.format(past_fa), verb, verbtr))
	forms.append(add_form(1, 'p', 'imperfect', 'ind', u'mí-{}im'.format(past_tr), u'می‌{}یم'.format(past_fa), verb, verbtr))
	forms.append(add_form(2, 'p', 'imperfect', 'ind', u'mí-{}id'.format(past_tr), u'می‌{}ید'.format(past_fa), verb, verbtr))
	forms.append(add_form(3, 'p', 'imperfect', 'ind', u'mí-{}and'.format(past_tr), u'می‌{}ند'.format(past_fa), verb, verbtr))
	
	forms.append(add_form(1, 's', 'pret', 'ind', u'{}am'.format(past_tr_str), u'{}م'.format(past_fa), verb, verbtr))
	forms.append(add_form(2, 's', 'pret', 'ind', u'{}i'.format(past_tr_str), u'{}ی'.format(past_fa), verb, verbtr))
	forms.append(add_form(3, 's', 'pret', 'ind', past_tr, past_fa, verb, verbtr))
	forms.append(add_form(1, 'p', 'pret', 'ind', u'{}im'.format(past_tr_str), u'{}یم'.format(past_fa), verb, verbtr))
	forms.append(add_form(2, 'p', 'pret', 'ind', u'{}id'.format(past_tr_str), u'{}ید'.format(past_fa), verb, verbtr))
	forms.append(add_form(3, 'p', 'pret', 'ind', u'{}and'.format(past_tr_str), u'{}ند'.format(past_fa), verb, verbtr))
	
	forms.append(add_form(1, 's', 'pres', 'sub', u'{}{}am'.format(be, pres_tr), u'ب{}م'.format(pres_fa), verb, verbtr))
	forms.append(add_form(2, 's', 'pres', 'sub', u'{}{}i'.format(be, pres_tr), u'ب{}ی'.format(pres_fa), verb, verbtr))
	forms.append(add_form(3, 's', 'pres', 'sub', u'{}{}ad'.format(be, pres_tr), u'ب{}د'.format(pres_fa), verb, verbtr))
	forms.append(add_form(1, 'p', 'pres', 'sub', u'{}{}im'.format(be, pres_tr), u'ب{}یم'.format(pres_fa), verb, verbtr))
	forms.append(add_form(2, 'p', 'pres', 'sub', u'{}{}id'.format(be, pres_tr), u'ب{}ید'.format(pres_fa), verb, verbtr))
	forms.append(add_form(3, 'p', 'pres', 'sub', u'{}{}and'.format(be, pres_tr), u'ب{}ند'.format(pres_fa), verb, verbtr))
	
	output = '\n'.join(forms)
	return output

verbs = [
#	(u'نوشید',	u'nušid')
#	(u'آموخت', u'āmuxt', u'آموز', u'āmuz'), hur blir det med be-?
#	(u'آمیخت', u'āmixt', u'آمیز', u'āmiz'),
#	(u'آویخت', u'āvixt', u'آویز', u'āviz'),
#	(u'', u'', u'', u''),
]

txts = []
for verb in verbs:
	if len(verb[0]) == 0: continue
	if verb in history: continue
	
	txt = generate_forms(*verb)
	txts.append(txt)

txt = '\n'.join(txts)
codecs.open('dict.txt', 'w', encoding='utf-8').write(txt)
print txt
pickle.dump(history, open('history.bin','w'))