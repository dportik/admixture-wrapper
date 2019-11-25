# admixture-wrapper

-----

A tool to automate analyses in admixture, a program used for detecting population structure with SNP data.
 
 
### Overview

The `admixture-wrapper.py` Python script is a tool for automating analyses with the program admixture. It can be run using Python 2 or 3. A directory containing one or more ped files (with file extension `.ped`) should be specified using the `-i` flag. The minimum and maximum K values, the number of replicates per K, and the cross-validation procedure folds value are set by the user. The number of threads can also be specified. Outputs from each replicate are written to a unique directory created for each ped file. Two main summary files are produced per ped file, one which contains the cross-validation scores for every replicate, and one which contains the average cross-validation score per K value. This second file can be used to plot the CV scores with the associated R script (`cross_validation_plotting.R`). A log file is also produced, which contains the analysis settings and the commands used to execute admixture for all K value replicates. 


### Script Usage 

The `admixture-wrapper.py` script is a command-line Python script that has five mandatory flags and one optional flag:

**Mandatory Arguments:**

+ `-i <path-to-directory>`: The full path to the directory which contains at least one ped file (in '12' recoded format).

+ `--kmin <integer>`: The minimum K-value to start with.

+ `--kmax <integer>`: The maximum K-value to end with.

+ `--reps <integer>`: The number of replicates to perform for each K-value.

+ `--cv <integer>`: Select the fold number for the cross-validation procedure. For example, setting 10 would invoke the `--cv=10` flag in admixture.

**Optional Arguments**:

+ `-t <integer>`: Specifies number of threads to use. Default = 1.

```
admixture-analysis
│
├── populations_r50_m70_randomSNP_recoded.ped
├── ppopulations_r60_m50_randomSNP_recoded.ped
├── populations_r70_m50_randomSNP_recoded.ped
│
```



```
admixture-analysis
│
├── Outputs-populations_r50_m70_randomSNP_recoded
│	└── output files...
├── Outputs-populations_r60_m50_randomSNP_recoded
│	└── output files...
├── Outputs-populations_r70_m50_randomSNP_recoded
│	└── output files...
├── admixture_wrapper.log
├── populations_r50_m70_randomSNP_recoded.CV_All.txt
├── populations_r50_m70_randomSNP_recoded.CV_Avg.txt
├── populations_r50_m70_randomSNP_recoded.ped
├── populations_r60_m50_randomSNP_recoded.CV_All.txt
├── populations_r60_m50_randomSNP_recoded.CV_Avg.txt
├── populations_r60_m50_randomSNP_recoded.ped
├── populations_r70_m50_randomSNP_recoded.CV_All.txt
├── populations_r70_m50_randomSNP_recoded.CV_Avg.txt
├── populations_r70_m50_randomSNP_recoded.ped
```


## Outputs 




### License

GNU Lesser General Public License v3.0

### Contact

The admixture-wrapper scripts were written by Daniel Portik (daniel.portik@gmail.com)
