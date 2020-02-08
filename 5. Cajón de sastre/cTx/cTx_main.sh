#!/bin/bash
population=20 # number of sperm cells per generation
iterations=1000	#number of movement steps per cell
podium=5	#number of selected cells for heritage MUST BE EQUAL OR LOWER THAN POPULATION
generations=1000	#number of generations
performance="n" #if "y", the output will contain only summary data (storage saving purposes)
oox=0	#oocyte position x
ooy=0	#oocyte position y


echo "     _______  ________  __  __ "
echo "    / _____/ /__  ___/ / /_/ / "
echo "   / /         / /     > _ <   "
echo "  / /____     / /    / / / /   "
echo " /______/    /_/    /_/ /_/    "
echo 
echo "cTx - Chemotaxis Evolution Simulator v 1.0"
echo "2019 Created by Miguel Roman"
echo 

for (( genNum = 1; genNum <= $generations; genNum++ )); do
	echo "__ GENERATION "$genNum" __________________"
	mkdir -p gen\_$genNum
	cd gen\_$genNum
	mkdir -p params
	mkdir -p walks
	for (( i = 1; i <= $population; i++ )); do
		echo "outputting results for sperm cell ""$i in generation ""$genNum"
	#	python3 /home/mroman/projects/chemTx/chemTx.py 500 $i > /home/mroman/projects/chemTx/walks/walk_coords\_$i.tsv
		python3 /home/mroman/projects/chemTx/chemTx.py $iterations $i $podium $genNum $oox $ooy
	done
	echo

	mv params_* params/
	mv walk_* walks/

	cd params/
	echo "generating summary tables for generation ""$genNum"
	perl /home/mroman/projects/chemTx/chTxFormatter.pl $population $podium $genNum $iterations $oox $ooy
	mv summary_gen* ../
	mv podium* ../
	cd ..

	if [[ performance == "y" ]]; then
		cd walks/
		rm walk_*
		cd ..
	fi
	
	cd ..
	echo 
	echo 
done



















#      _______  ________  __  __ 
#     / _____/ /__  ___/ / /_/ / 
#    / /         / /     >__ <   
#   / /____     / /    / / / /   
#  /______/    /_/    /_/ /_/    