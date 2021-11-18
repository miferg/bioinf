NW.matrix <- function(a, b, gap=-2, match=1, mismatch=-2) {
  asplit <- strsplit(a, split="")[[1]]
  bsplit <- strsplit(b, split="")[[1]]
  x <- matrix(0, length(bsplit)+1, length(asplit)+1)
  x[1,] <- seq(0, gap*(length(asplit)), gap)
  x[,1] <- seq(0, gap*(length(bsplit)), gap)
  for (i in 1:length(bsplit)+1) {
    for (j in 1:length(asplit)+1) {
      anterior <- max(x[i-1,j], x[i-1,j-1], x[i,j-1])
      if (bsplit[i-1] == asplit[j-1]) {
      actual <- match} else {
      actual <- mismatch
      }
      x[i,j] <- anterior + actual
    }
  }
  return(x)
  }
