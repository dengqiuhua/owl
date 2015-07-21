# coding=utf-8
import re
import math
import os,sys
import bisect

def get_model(file_dict):
	prob_cv = {}
	prob_v = {}
	word_all = []
	for line in open(file_dict,"rb"):
		word, freq = line.split(" ")
		freq = int(freq)
		word = unicode(word,"utf-8")
		length = len(word)
		if not (length in prob_v):
			prob_v[length] = 0
		prob_v[length] += 1
		word_all.append(word)
		for i,char in enumerate(word):
			if not (char in prob_cv):
				prob_cv[char] = {}
			if not (i in prob_cv[char]):
				prob_cv[char][i] = 0
			prob_cv[char][i] += freq

	total_freq = sum(prob_v.values())

	for k,v in prob_v.iteritems():
		prob_v[k] = float(v) / total_freq

	for k,v in prob_cv.iteritems():
		subtaotal_freq = sum(v.values())
		new_v = {}
		for kk,vv in v.iteritems():
			new_v[kk] = float(vv) / subtaotal_freq
		prob_cv[k] = new_v

	word_all.sort()
	return prob_v,prob_cv,word_all

_localDir=os.path.dirname(__file__)
_curpath=os.path.normpath(os.path.join(os.getcwd(),_localDir))
print "loading dictionary..."
prob_v, prob_cv,word_all = get_model(os.path.join(_curpath,"dict.txt"))
print "done."

def has_prefix(word):
	idx = bisect.bisect_right(word_all,word)
	if idx< len(word_all):
		if word_all[idx].startswith(word) or word_all[idx-1]==word :
			return True
	return False

def in_dict(word):
	idx = bisect.bisect_right(word_all,word)
	if idx< len(word_all):
		if word_all[idx-1]==word :
			return True
	return False

def __cut(sentence):
	length = len(sentence)
	if length<2:
		return [sentence]
	i ,j = 0, 1
	result = []

	while j< length:
		char = sentence[j]
		if not (char in prob_cv):
			prob_cv[char]={}
		p_1 = prob_v[j-i] *  prob_cv[char].get(0,0)# probility of seg
		p_2 = prob_v[j-i+1] * prob_cv[char].get(j-i,0)#probility of not seg
		part = sentence[i:j]
		if (p_1 > p_2) and in_dict(part):
			result.append(part)
			i = j
		else:
			if not has_prefix(sentence[i:j+1]):
				result.append(part)
				i = j
		j+=1
		if j == length:
			result.append(sentence[i:])

	return result

def cut(sentence):
	if not ( type(sentence) is unicode):
		try:
			sentence = sentence.decode('utf-8')
		except:
			sentence = sentence.decode('gbk')
	blocks = re.split(ur"([^\u4E00-\u9FA5]+)",sentence)
	result = []
	for blk in blocks:
		if re.match(ur"[\u4E00-\u9FA5]+",blk):
			result.extend(__cut(blk))
		else:
			tmp = re.split(ur"[^a-zA-Z0-9+#]",blk)
			result.extend([x for x in tmp if x.strip()!=""])
	return result