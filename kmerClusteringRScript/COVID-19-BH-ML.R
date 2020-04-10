# load package
library(pheatmap)

# load data and subset
kmer_metadata_file <- "data/kmer_analysis_and_meta_data__fixed_merged.csv"
data <- read.delim(kmer_metadata_file, sep=",", header=T, row.names="Accession")

headers <- colnames(data)
headerTrimmed <- c(headers[1:8], c(paste0("Kmer", seq(1:(2432-8)))))

colnames(data) <- headerTrimmed

annotationRowDate = data.frame(
  strainDate = data$Collection_Date,
  strainGeo = data$Geo_Location 
)
rownames(annotationRowDate) = rownames(data)


png("clusteringKmers.png",   # create PNG for the heat map        
    width  = 6000,
    height = 6000,
    res    = 300,                               # 300 pixels per inch
    pointsize = 15);                             # smaller font size


# create heatmap using pheatmap
pheatmap(
  data[,9:2432],
  cluster_row = TRUE,
  cluster_col = TRUE,
  fontsize_row = 5,
  fontsize_col = 5,
  # "euclidean", "maximum", "manhattan", "canberra", "binary" or "minkowski"
  clustering_distance_rows = "binary", 
  clustering_distance_col = "binary",
  # "ward.D", "ward.D2", "single", "complete", "average" (= UPGMA), "mcquitty" (= WPGMA), "median" (= WPGMC) or "centroid" (= UPGMC).
  clustering_method = "ward.D2",
  annotation_row = annotationRowDate,
  show_rownames = TRUE,
  show_colnames = FALSE,
  cutree_rows = 10,
  cutree_cols = 10
  )

dev.off()
