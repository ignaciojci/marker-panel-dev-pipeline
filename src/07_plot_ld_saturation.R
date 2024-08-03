library(gaston)

vcffile<-$1
vcf <- read.vcf(vcffile)

dir.create("tmp", recursive=T)
ldfile <- ("tmp/vcf_ld")

write.bed.matrix(vcf,ldfile)

plink <- "lib/plink/plink"

nmarkers <- rep(NA, 20)
for(i in 1:20){
    system(paste(plink,"--bfile",ldfile,"--allow-extra-chr","--indep-pairwise 250 10",i/20,"--out",ldfile))
    ldfilt <- read.table(paste0(ldfile,".prune.in"))
    nmarkers[i] <- nrow(ldfilt)
}