library(vegan)
library(ape)

get.clusters <- function(infile) {
    sscurr <- read.table(infile,header=F)
    for (i in 1:nrow(sscurr)) {
        currmat <- as.matrix(read.table(as.character(sscurr[i,]),sep=',',row.names=1,header=T))
        currmat[lower.tri(currmat)]  <- t(currmat)[lower.tri(currmat)]
        currclust <- hclust(as.dist(currmat))
        curr.tree <- unroot(as.phylo(currclust))
        write.tree(curr.tree,file=paste(as.character(sscurr[i,]),'nwk',sep='.'))
        }
    }
