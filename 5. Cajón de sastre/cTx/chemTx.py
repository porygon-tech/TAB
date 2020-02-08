#!/usr/bin/python
import sys
import math
import random
#https://stackoverflow.com/questions/25342072/computing-and-drawing-vector-fields
#https://www.youtube.com/watch?time_continue=89&v=ksW59gYEl6Q
#import sys # https://www.quora.com/What-does-import-sys-mean-in-Python
#
spawn_radius = 10

class oocyte(object):
	"""docstring for oocyte"""
	def __init__(self, x, y, secretion_level, substance_diffusibility):
		#super(oocyte, self).__init__()
		self.x = x
		self.y = y
		self.secretion_level = secretion_level
		self.substance_diffusibility = substance_diffusibility

class sperm(object):
	"""
	xy: cell position
	o: cell orientation angle in degrees, starting from positive y axis
	v_response: movement speed of this cell, depending on the signal intensity
	dc_response: direction change variance of this cell, depending on the signal intensity

	behavior logistic function parameters:
		maxActivation: max level of activation
		steepness_A: steepness of activation curve
		threshold_A: midpoint of activation curve
		base_A: basal state of activation when not activated
		steepness_I: steepness of inhibition curve
		threshold_I: midpoint of inhibition curve
		base_I: basal state of activation when inhibited

	"""
	def __init__(self, 
		x, 
		y, 
		v=1, 
		r=0, 

		maxActivation_v=1,
		steepness_vA=1,
		threshold_vA=1,
		base_vA=0,
		steepness_vI=-1,
		threshold_vI=1,
		base_vI=1,

		maxActivation_r=45,
		steepness_rA=1,
		threshold_rA=1,
		base_rA=0,
		steepness_rI=-1,
		threshold_rI=1,
		base_rI=1,

		parent=0
		):
		#super(sperm, self).__init__()
		self.x = x
		self.y = y
		self.v = v
		self.r = r
	#velocity response params
		self.maxActivation_v = maxActivation_v
		self.steepness_vA = steepness_vA
		self.threshold_vA = threshold_vA
		self.base_vA = base_vA
		self.steepness_vI = steepness_vI
		self.threshold_vI = threshold_vI
		self.base_vI = base_vI
	#angle variance response params
		self.maxActivation_r = maxActivation_r
		self.steepness_rA = steepness_rA
		self.threshold_rA = threshold_rA
		self.base_rA = base_rA
		self.steepness_rI = steepness_rI
		self.threshold_rI = threshold_rI
		self.base_rI = base_rI

		self.parent = parent



	def signalfrom(self, oo):
		#the intensity of signal substance this sperm is receiving from an oocyte
		intensity = oo.secretion_level / (1 + (eucdist(self,oo) / oo.substance_diffusibility)**2)
		return intensity

	def response_r(self, oo):
		resp = ((self.maxActivation_r - self.base_rA) / (1 + math.e ** (-self.steepness_rA * (self.signalfrom(oo) - self.threshold_rA))) + self.base_rA) * ((1 - self.base_rI) / (1 + math.e ** (-self.steepness_rI * (self.signalfrom(oo) - self.threshold_rI))) + self.base_rI)
		return resp
		
	def response_v(self, oo):
		resp = ((self.maxActivation_v - self.base_vA) / (1 + math.e ** (-self.steepness_vA * (self.signalfrom(oo) - self.threshold_vA))) + self.base_vA) * ((1 - self.base_vI) / (1 + math.e ** (-self.steepness_vI * (self.signalfrom(oo) - self.threshold_vI))) + self.base_vI)
		return resp

	def move(self, oo):
		self.r = rnorm(self.r,self.response_r(oo))
		self.v = self.response_v(oo)
		dx = math.sin(math.radians(self.r))*self.v
		dy = math.cos(math.radians(self.r))*self.v
		self.x += dx
		self.y += dy

		
def eucdist(cell_a, cell_b):
#	returns euclidean distance between two cells
	dist = math.sqrt((cell_a.x - cell_b.x)**2 + (cell_a.y - cell_b.y)**2)
	return dist

def rnorm(mu = 0, sigma = 1):
#	implements Box-Muller transform
	u1 = random.uniform(0,1)
	u2 = random.uniform(0,1)
	theta = 2 * math.pi * u2
	R = math.sqrt(-2 * math.log(u1))
	z = R * math.cos(theta)
	x = z*sigma+mu
	return x

def mutate(sp):
#	alters the parameters of reponse functions of a target cell using a stdev of 1
		varMut = 0.1
#probar a aislar parámetros uno a uno
		sp.maxActivation_v = round(rnorm(mu = sp.maxActivation_v, sigma = varMut), 3)
		sp.steepness_vA = round(rnorm(mu = sp.steepness_vA, sigma = varMut), 3)
		sp.threshold_vA = round(rnorm(mu = sp.threshold_vA, sigma = varMut), 3)
		sp.base_vA = round(rnorm(mu = sp.base_vA, sigma = varMut), 3)
		sp.steepness_vI = round(rnorm(mu = sp.steepness_vI, sigma = varMut), 3)
		sp.threshold_vI = round(rnorm(mu = sp.threshold_vI, sigma = varMut), 3)
		sp.base_vI = round(rnorm(mu = sp.base_vI, sigma = varMut), 3)

		sp.maxActivation_r = round(rnorm(mu = sp.maxActivation_r, sigma = varMut), 3)
		sp.steepness_rA = round(rnorm(mu = sp.steepness_rA, sigma = varMut), 3)
		sp.threshold_rA = round(rnorm(mu = sp.threshold_rA, sigma = varMut), 3)
		sp.base_rA = round(rnorm(mu = sp.base_rA, sigma = varMut), 3)
		sp.steepness_rI = round(rnorm(mu = sp.steepness_rI, sigma = varMut), 3)
		sp.threshold_rI = round(rnorm(mu = sp.threshold_rI, sigma = varMut), 3)
		sp.base_rI = round(rnorm(mu = sp.base_rI, sigma = varMut), 3)

def stdAngle(r):
	return(r-360*math.floor(sp1.r/360))

def spawn(n = 1, x = 0, y = 0):
	sons = []
	for i in range(1,n):
		sons.append(sperm(x = x, y = y, r = random.uniform(0,360)))
	return(sons)

def offspring(generation):

	angle = random.uniform(0,360)
	pos_x = math.cos(math.radians(angle - 180)) * spawn_radius + int(sys.argv[5])
	pos_y = math.sin(math.radians(angle - 180)) * spawn_radius + int(sys.argv[6])

	if generation == 1:
		sp = sperm(x = pos_x, y = pos_y, r = angle)
		mutate(sp)
		return(sp)
	else:
		podiumSize = int(sys.argv[3])
		

		podium_filename = ("/home/mroman/projects/chemTx/gen_" + str(generation - 1) + "/podium_gen_" + str(generation - 1) + ".tsv")
		podiumFH=open(podium_filename,"r")
		pRL = podiumFH.readlines()

		parent_ID = (pRL[random.randint(1,podiumSize)].split("\t"))[0]	#parent will be selected at random from the parent's podium

		for line in pRL:	#now we look in each line in parent's podium to find the selected parent
			pars = line.split("\t")
			if pars[0] == str(parent_ID): #here we're checking if the current readline corresponds to the selected parent
				sp = sperm(x = pos_x, y = pos_y, r = angle, maxActivation_v = float(pars[4]), steepness_vA = float(pars[5]), threshold_vA = float(pars[6]), base_vA = float(pars[7]), steepness_vI = float(pars[8]), threshold_vI = float(pars[9]), base_vI = float(pars[10]), maxActivation_r = float(pars[11]), steepness_rA = float(pars[12]), threshold_rA = float(pars[13]), base_rA = float(pars[14]), steepness_rI = float(pars[15]), threshold_rI = float(pars[16]), base_rI = float(pars[17]), parent = int(pars[0]))
				mutate(sp)
				return(sp)
				break

		#sp = sperm(x = 0, y = 0, r = 0) #this is made for the supposedly impossible case that we cannot find the selected parent
		#return(sp)






#------------------------------------------------------------

total_iterations = int(sys.argv[1])
sperm_ID = int(sys.argv[2])
podium = int(sys.argv[3])
generation = int(sys.argv[4])
oox = int(sys.argv[5])
ooy = int(sys.argv[6])

oo1 = oocyte(x=oox, y=ooy, secretion_level=10, substance_diffusibility=10)
#sp1 = sperm(x = 0, y = 0, r = 0) #r = random.uniform(0,360)


angle = random.uniform(0,360)
pos_x = math.cos(math.radians(angle - 180)) * spawn_radius + int(sys.argv[5])
pos_y = math.sin(math.radians(angle - 180)) * spawn_radius + int(sys.argv[6])



sp1 = offspring(generation)
#mutate(sp1)





#print("x\ty\tAngle")


#===================================================================|
#	walk coordinates output
coords_filename = ("walk_coords_" + str(sperm_ID) + ".tsv")
coords=open(coords_filename,"w+")
for x in range(0,total_iterations):
	coords.write(str(round(sp1.x, 2)) + "\t" + str(round(sp1.y, 2)) + "\n")
	sp1.move(oo1)
	#print(eucdist(oo1, sp1))
	#print(sp1.signalfrom(oo1))
	#print(str(round(sp1.x, 2)) + "\t" + str(round(sp1.y, 2)) + "\t" + str(round(stdAngle(sp1.r), 1)) + "º")
coords.write(str(round(sp1.x, 2)) + "\t" + str(round(sp1.y, 2)))
coords.close()
#===================================================================|

#=======================|
#	parameter output
showparams = str("p")
if showparams == "p":
	params_filename = ("params_" + str(sperm_ID) + ".tsv")
	params=open(params_filename,"w+")
	params.write(str(sp1.x) + "\n")
	params.write(str(sp1.y) + "\n")
	params.write(str(sp1.v) + "\n")
	params.write(str(sp1.r) + "\n")

	params.write(str(sp1.maxActivation_v) + "\n")
	params.write(str(sp1.steepness_vA) + "\n")
	params.write(str(sp1.threshold_vA) + "\n")
	params.write(str(sp1.base_vA) + "\n")
	params.write(str(sp1.steepness_vI) + "\n")
	params.write(str(sp1.threshold_vI) + "\n")
	params.write(str(sp1.base_vI) + "\n")
	
	params.write(str(sp1.maxActivation_r) + "\n")
	params.write(str(sp1.steepness_rA) + "\n")
	params.write(str(sp1.threshold_rA) + "\n")
	params.write(str(sp1.base_rA) + "\n")
	params.write(str(sp1.steepness_rI) + "\n")
	params.write(str(sp1.threshold_rI) + "\n")
	params.write(str(sp1.base_rI) + "\n")
	params.write(str(sp1.parent))
	params.close()
#=======================|




#for x in range(0,100):
#	v = rnorm()
#	print (v)

#for x in range(0,100):
#	print (str(round(rnorm(0,45), 1)) + "º")

#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    mainWin = HelloWindow()
#    mainWin.show()
#    sys.exit( app.exec_() )


#-ln(1-x^2)