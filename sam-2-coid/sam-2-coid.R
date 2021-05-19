coid <- read.table('prueba.coid.tsv', sep='\t', header=T)


for (i in 1:length(levels(coid$ref))) {
 current <- levels(coid$ref)[i]
 print(current)
 ndf <- coid[coid$ref == current,]
 pdf(current)
 plot(id~pos, data=ndf, ylim = c(0.5,1),  main=current)
 dev.off()
}

