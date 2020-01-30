'''
We randomly select a third and a color; each third has 6 red and 6 black, so when we
select third and a color, numbers are automatically known:
For 0 sum game we:
- bet 1 (#betNum) coins on each of the 6 number
- bet 12 (#betThird) coins on the selected third
- bet 18 (#betColor) coins on the selected color
i.e. bet = 36 coins

Winnings
- when number falls, we get 36*betNum + 3*betThird + 2*betColor coins back (=108 coins)
- when number on the same third falls, but of different color, we get 3*betThird back (=36 coins)
- when number of the same color falls, but on the different third, we get 2*betColor back (=36coins)
'''

import random

# global variables

french = (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8,
          23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)
american = (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13,
            1, '00', 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2)
red = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
black = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)

session = 50 #bets per session
iterations = 10000 #number of sessions

#betting values
betNum = 1
betThird = 20
betColor = 30
bet = (betNum*6 + betThird + betColor)
tot = 0

#mode: 0 - bet randomly; 1 - bet same if loss (need 'lost' variable); 2 - always bet the same
mode = 0
lost = 'false'

#max up/downswing
maxDownSwing = 0
maxUpSwing = 0
currUpSwing = 0
currDownSwing = 0
cntFullWin = 0
cntSemiWin = 0
swing = 'neutral'

#min/max win in session
minWin = 99999999999999
maxWin = 0

#min/max total
maxSessTotal = 0
maxTotal = 0
minSessTotal = 9999999999999
minTotal = 9999999999999
winsTotal = 0
lossesTotal = 0

#total session wins/loss
winCnt = 0
lossCnt = 0
allTotal = 0

#print debug option
debug = 0

#create (number, color, third) tuple
def addColors(numbers):
    global red, black

    out = []
    for number in numbers:
        color = 'red' if number in red else 'black' if number in black else 'green'
        out.append((number, color, -1 if number == 0 else int((number-1)/12)+1))

    return out

#pick a winning number
def play(type_ = 'french'):
	global withColors

	withColors = addColors(french if type_ == 'french' else american)

	pick = random.randint(1,len(withColors))

	return(withColors[pick-1])

for j in range(0, iterations):
	tot = 0
	mod2 = 0
	for i in range(0, session):
		
		tmpTot = -bet
		
		#choose third and color
		if mode == 2 and mod2 == 0:
			third = random.randint(1,3)
			color = 'red' if random.randint(1,2) == 1 else 'black'
			mod2 = 1
		elif mode == 0 or lost == 'false':
			third = random.randint(1,3)
			color = 'red' if random.randint(1,2) == 1 else 'black'

		if debug > 2:
			print('third chosen:', third, ' color chosen:', 'red' if color == 1 else 'black')
			print('numbers in', third, 'st' if third == 1 else 'nd' if third == 2 else 'th', 'third', (third)*12, '-', (third+1)*12)
		if debug > 0:
			print('third:', third, '(',((third-1)*12)+1, '-', third*12, ')')
			print('color:', color)
		
		#betting numbers
		b = [x for x in red if x >= (third-1)*12 and x <= third*12] if color == 'red' else [x for x in black if x >= (third-1)*12 and x <= third*12]

		if debug > 2:
			print(b)

		if debug > 0:
			print('BET:', bet)
		
		#get winning number
		ret = play(type_ = 'french')
		winNum, winColor, winThird = ret
		
		if debug > 0:
			print('Winning number:',ret)

		#calculate current total winnings/loss
		tmpTot += 36 * betNum if winNum in b else 0
		tmpTot += 3 * betThird if winThird == third else 0
		tmpTot += 2 * betColor if winColor == color else 0

		cntFullWin += 1 if winNum in b else 0
		cntSemiWin += 1 if winNum not in b and tmpTot > 0 else 0

		#calculate maximum upswing/downswing for the session
		if tmpTot > 0:
			#increase winning count
			winCnt += 1
			lost = 'false'

			#calculate upswing record
			if swing == 'up':
				currUpSwing += 1
				if currUpSwing > maxUpSwing:
					maxUpSwing = currUpSwing
			else:
				swing = 'up'
				currUpSwing = 1
		else:
			#increase loss count
			lossCnt += 1
			lost = 'true'

			#calculate downswing record
			if swing == 'down':
				currDownSwing += 1
				if currDownSwing > maxDownSwing:
					maxDownSwing = currDownSwing
			else:
				swing = 'down'
				currDownSwing = 1

		#this session total
		tot += tmpTot

		if tot < 0 and debug > 3:
			print('NEGATIVE TOTAL', tot, 'at run', j, 'and', i, 'th iteration')
		
		if debug > 0:
			print('Current win:', tmpTot)
			print('Total win:', tot, '\n')

		if tot < minSessTotal:
			minSessTotal = tot

		if tot > maxSessTotal:
			maxSessTotal = tot


	
	if debug > -1:
		print('Session', j, 'stats:')
		print('Max UP swing:', maxUpSwing)
		print('Max DOWN swing:', maxDownSwing)
		print('Biggest Session positive:',maxSessTotal)
		print('Biggest Session negative:', minSessTotal)
		print('Nr. full wins:', cntFullWin)
		print('Nr. semi wins:', cntSemiWin)
		print('wins:', winCnt)
		print('losses:', lossCnt)
		print('win percentage', (winCnt/(winCnt+lossCnt)*100), '%')
		print('Total win:', tot, '\n')
	
	#best and worst sessions
	if tot >= maxWin:
		maxWin = tot
	elif tot < minWin:
		minWin = tot

	if minSessTotal < minTotal:
		minTotal = minSessTotal

	if maxSessTotal > maxTotal:
		maxTotal = maxSessTotal

	if tot > 0:
		winsTotal += 1
	else:
		lossesTotal += 1

	allTotal += tot

	#reset values
	currUpSwing = 0
	currDownSwing = 0
	maxUpSwing = 0
	maxDownSwing = 0
	swing = 'neutral'
	minSessTotal = 9999999999999
	maxSessTotal = 0
	winCnt = 0
	lossCnt = 0
	lost = 'false'
	cntSemiWin = 0
	cntFullWin = 0

print('MODE:','bet random thirds and colors' if mode == 0 else 'bet same numbers until win' if mode == 1 else 'bet always same numbers')
print('Total sessions:', iterations)
print('Bets per session:', session)
print('MAX session:', maxWin)
print('MIN session:', minWin)
print('Average session win in', iterations, 'iterations of', session, ' bets per session:',allTotal/iterations)
print('Winning sessions:', winsTotal)
print('Losing sessions:', lossesTotal)
print('Min starting money needed in WORST session:', minTotal)