# References: https://cran.r-project.org/web/packages/GGIR/vignettes/GGIR.html
g.shell.GGIR(
  mode=c(1,2,3,4,5),
  datadir= "put the directory of your input file",
  outputdir= "put the directory of your output file",
  do.report=c(2,4,5),
  overwrite = FALSE,
  #storefolderstructure =TRUE,
  #=====================
  
  # Part 2
  #=====================
  strategy = 1,
  idloc = 2,
  do.parallel = TRUE,
  do.call = TRUE,
  do.enmo = TRUE,
  do.anglez = TRUE,
  hrs.del.start = 0,          hrs.del.end = 0,
  maxdur = 9,                 includedaycrit = 16,
  qwindow=c(0,24),
  mvpathreshold =c(70), #it can be multiple
  bout.metric = 1, # it could be 1, 2, 3, 4
  excludefirstlast = FALSE,
  includenightcrit = 16,
  #=====================
  # Part 3 + 4
  #=====================
  def.noc.sleep = 1,
  outliers.only = TRUE,
  criterror = 4,
  do.visual = TRUE,
  #=====================
  # Part 5
  #=====================
  
  threshold.lig = c(30), threshold.mod = c(100),  threshold.vig = c(400),
  boutcriter = 0.8,      boutcriter.in = 0.9,     boutcriter.lig = 0.8,
  boutcriter.mvpa = 0.8, boutdur.in = c(1,10,30), boutdur.lig = c(1,10),
  boutdur.mvpa = c(1),
  includedaycrit.part5 = 2/3,
  
  #=====================
  # Visual report
  #=====================
  timewindow = c("MM"),
  visualreport=TRUE,
  dofirstpage = TRUE,
  viewingwindow = 2)

