#!/usr/bin/env perl
#	generates a summary chart for a given generation

#cd /projects/chemTx/params
# perl ../chTxFormatter.pl 100 10
use strict;
use warnings;


my $population = $ARGV[0];
my $podium_size = $ARGV[1];
my $generation = $ARGV[2];
my $iterations = $ARGV[3];
my $oox = $ARGV[4];
my $ooy = $ARGV[5];

my (%sperm, @podium, $ct);
my $oo_x = 5;
my $oo_y = 10;

open(OUTPUT, ">summary_gen_".$generation.".tsv");
close(OUTPUT);

open(OUTPUT, ">>summary_gen_".$generation.".tsv");
print OUTPUT ("SpermID\tFinalD\tClosest\tAvgD\tMaxAv\tsteepAv\tthresAv\tbaseAv\tsteepIv\tthresIv\tbaseIv\tMaxAr\tsteepAr\tthresAr\tbaseAr\tsteepIr\tthresIr\tbaseIr\tparent\n");



for (my $spermID = 1; $spermID <= $population; $spermID++) {
	open(FILE, "<params_".$spermID.".tsv");
	my @par = <FILE>;
	close(FILE);

	chomp @par;
	my $x = $par[0];
	my $y = $par[1];
	my $dist = (sqrt(($x - $oo_x)**2 + ($y - $oo_y)**2));
	my $closest;
	my $avgD; #average distance to the oocyte

	#finds the closest distance in the walk:
	open(WALKCOORDS, "</home/mroman/projects/chemTx/gen_".$generation."/walks/walk_coords_".$spermID.".tsv");
	while (<WALKCOORDS>) {
		my ($x, $y) = split("\t", $_);
		my $eucD = (sqrt(($x - $oo_x)**2 + ($y - $oo_y)**2));
		$avgD += $eucD; #cuidao
		if (!defined($closest) || $eucD < $closest || $closest == 0) {
			$closest = $eucD;
		}
	}
	$avgD = $avgD/$iterations;


	close(WALKCOORDS);
	
	#here is where the evolution objective is set. Next, we build a hash that relates sperm IDs and their respective value of the parameter under selection.
	#$sperm{$spermID} = $dist;
	#$sperm{$spermID} = $closest;
	$sperm{$spermID} = $avgD;


	#print($spermID." ".$sperm{$spermID}."\n");
	#print($sperm{$spermID});
	print OUTPUT ($spermID."\t".$dist."\t".$closest."\t".$avgD."\t$par[4]\t$par[5]\t$par[6]\t$par[7]\t$par[8]\t$par[9]\t$par[10]\t$par[11]\t$par[12]\t$par[13]\t$par[14]\t$par[15]\t$par[16]\t$par[17]\t$par[18]\n");
}
close(OUTPUT);

#
foreach my $key (sort { $sperm{$a} <=> $sperm{$b} } keys %sperm) {
	#printf ($key." ".$sperm{$key}."\n");
	#print(""."\n")
	push(@podium, $key);
	$ct++;
	if ($ct >= $podium_size) {
		last;
	}
}

#print("\n\n\n");
open(LIST, "<summary_gen_".$generation.".tsv");
open(PODIUM, ">podium_gen_".$generation.".tsv");
print PODIUM ("SpermID\tFinalD\tClosest\tAvgD\tMaxAv\tsteepAv\tthresAv\tbaseAv\tsteepIv\tthresIv\tbaseIv\tMaxAr\tsteepAr\tthresAr\tbaseAr\tsteepIr\tthresIr\tbaseIr\tparent\n");
#print ("SpermID\tDistance\tMaxAv\tsteepAv\tthresAv\tbaseAv\tsteepIv\tthresIv\tbaseIv\tMaxAr\tsteepAr\tthresAr\tbaseAr\tsteepIr\tthresIr\tbaseIr\n");

while(<LIST>) {
	my $line = $_;
	chomp $line;
	my @par = split("\t", $line);
	foreach my $id (@podium){
		if ($id eq $par[0]) {
			print PODIUM ($line."\n");
#			print($line."\n");
		}
	}
}


