library(ape)
library(vegan)

get.tree.dists.factors <- function(infile,reftree) {
    sscurr <- read.table(infile,header=F)
    dvec <- 1:nrow(sscurr)
    for (i in 1:nrow(sscurr)) {
        currmat <- as.matrix(read.table(as.character(sscurr[i,]),sep=',',row.names=1,header=T))
        currmat[lower.tri(currmat)]  <- t(currmat)[lower.tri(currmat)]
        currclust <- hclust(as.dist(currmat))
        curr.tree <- unroot(as.phylo(currclust))
        dvec[i] <- dist.topo(reftree,curr.tree,method = 'PH85')[1]
        }
    return(cbind(dvec,rep(infile,nrow(sscurr))))
    }
