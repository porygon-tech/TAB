cTx is a chemotaxis simulator developed by Miguel Román-Sánchez in August 2019. 
cTx attempts to emulate and explore sperm cell movement towards a chemical signal through implementing a natural algorithm designed by Miguel Román-Sánchez. The movement is defined by the following parameters:
  the variance of the normal distribution for the angles of random direction change.
  the parameters of a combined sigmoidal function for the response to the signal in form of movement speed.
  
The pipeline repeats a given number of offspring generations, where generated sperm cells inherit parameters from the best ones in the last generation (the ones who spent more time closer to the oocyte). Inherited parameters may experiment slight variations, adjusted by a mutation rate.

for more information, contact miguelroman98@gmail.com
