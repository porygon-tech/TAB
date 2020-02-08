#!/usr/bin/env R
#load and print all walk paths in /home/mroman/projects/chemTx/walks
#possibility of path color heat map
#analysis during generations




pdir = 'C:/Users/Miki/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc/LocalState/rootfs/home/mroman/projects/chemTx/'
filename = paste(c(pdir, 'gen_', genNum, '/summary_gen_', genNum, '.tsv'), collapse = '')
parm <- read.table(filename, header = TRUE)


avgtable <- data.frame(matrix(ncol = 18, nrow = 0))
vartable <- data.frame(matrix(ncol = 18, nrow = 0))
colnames(avgtable) <- c("generation", names(parm)[2:18])
colnames(vartable) <- c("generation", names(parm)[2:18])



for (genNum in 1:1000) {
  filename = paste(c(pdir, 'gen_', genNum, '/summary_gen_', genNum, '.tsv'), collapse = '')
  parm <- read.table(filename, header = TRUE)
  
  avgtable[genNum, "generation"] <- genNum
  vartable[genNum, "generation"] <- genNum
#  var(parm[["thresAv"]])
#  names(parm)
  for (pID in 2:18) { #pID means 'parameter ID'
    #print(names(parm)[pID]); print(mean(parm[,pID]))

    avgtable[genNum, pID] = mean(parm[,pID])
    vartable[genNum, pID] = var(parm[,pID])
    
  }
}


plot(avgtable[["generation"]], avgtable[["steepIr"]], type = 'n', ylim = c(-7, 7));for (ploo in names(parm)[2:18]) {
  lines(avgtable[["generation"]], avgtable[[ploo]], col = paste0('#',paste0(sample(c(0:9, LETTERS[1:6]), 6, T), collapse = '')))
}

set.seed(123)
paste0(sample(c(0:9, LETTERS[1:6]), 6, T), collapse = '')

paste0('#',paste0(sample(c(0:9, LETTERS[1:6]), 6, T), collapse = ''))

