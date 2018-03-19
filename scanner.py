"""
Sample script to test ad-hoc scanning by table drive.
This accepts "term","test" and "long" words.
"""
import re

def getchar(words,pos):
	""" returns char at pos of words, or None if out of bounds """
	rexp = re.compile(r'\d\d[.|:]\d\d');
	m = rexp.search('[0:1]?[0:9][:|.][0:5]?[0:9]|2[0:3][:|.][0:5]?[0:9]|[3:9][:|.][0:9]')
	if pos<0 or pos>=len(words): return None

	return words[pos]
	

def scan(text,transition_table,accept_states):
	""" Scans `text` while transitions exist in 'transition_table'.
	After that, if in a state belonging to `accept_states`,
	returns the corresponding token, else ERROR_TOKEN.
	"""
	
	# initial state
	pos = 0
	state = 'q0'
	
	while True:
		
		c = getchar(text,pos)	# get next char
		
		if state in transition_table and c in transition_table[state]:
		
			state = transition_table[state][c]	# set new state
			pos += 1	# advance to next char
			
		else:	# no transition found

			# check if current state is accepting
			if state in accept_states:
				return accept_states[state],pos

			# current state is not accepting
			return 'ERROR_TOKEN',pos
			
	
# the transition table, as a dictionary
td = { 'q0':{'0:1':'q1', '2':'q2', '3:9':'q3' },
       'q1':{'0:9':'q4' },
       'q2':{'0:3':'q4' },
       'q3':{'.':'q5' },
       'q4':{':':'q5' },
       'q5':{'0:5':'q6' },
       'q6':{'0:9':'q7' }
     } 

# the dictionary of accepting states and their
# corresponding token
ad = { 'q7':'TIME_TOKEN'
     }


# get a string from input
text = input('give some input>')

# scan text until no more input
while text:	# that is, while len(text)>0
	
	# get next token and position after last char recognized
	token,position = scan(text,td,ad)
	
	if token=='ERROR_TOKEN':
		print('unrecognized input at pos',position+1,'of',text)
		break
	
	print("token:",token,"string:",text[:position])
	
	# remaining text for next scan
	text = text[position:]
