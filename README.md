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


To run an analysis, you'll want to put the ped file(s) in a single directory. For example:

```
admixture-analysis
│
├── populations_r50_m70_randomSNP_recoded.ped
├── ppopulations_r60_m50_randomSNP_recoded.ped
├── populations_r70_m50_randomSNP_recoded.ped
│
```

In the above example, let's say the full path to `admixture-analysis` directory is `Research/project/admixture-analysis`. If we wanted to test K values from 1-12, using 10 replicates each, with 10-fold cross validation, we could use the following command:

```
python admixture-wrapper.py -i Research/project/admixture-analysis --kmin 1 --kmax 12 --reps 10 --cv 10 
```

We could also use the `-t` flag to specify how many threads to use:

```
python admixture-wrapper.py -i Research/project/admixture-analysis --kmin 1 --kmax 12 --reps 10 --cv 10 -t 4
```

These settings will be applied to each ped file present. 


## Outputs 


Output files will be written for every ped file included in the input directory. Based on the example above, this is what would be written after the analysis is completed:

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

For each ped file, the following outputs are written:

+ Directory `Output-[ped name]`: Contains the `.P`, `.Q`, and log files for every replicate for every K value tested. 

+ File `[ped name].CV_All.txt`: The cross-validation scores for every replicate for every K value tested for this ped file. Example contents:

```
K	Rep	CV
1	1	0.45393
1	2	0.45393
1	3	0.45393
1	4	0.45393
1	5	0.45393
2	1	0.37103
2	2	0.37103
2	3	0.37103
2	4	0.37103
2	5	0.37103
3	1	0.3384
3	2	0.3384
3	3	0.3384
3	4	0.3384
3	5	0.3384
```

+ File `[ped name].CV_Avg.txt`: The **average** cross-validation scores (and standard deviation) for every replicate for every K value tested for this ped file. This file can be used to plot the scores using the associated `cross_validation_plotting.R` R script. Example contents:

```
K	CV_Avg	CV_Stdev
1	0.4539	0.0
2	0.371	0.0
3	0.3384	0.0
4	0.3665	0.0
5	0.3384	0.0
6	0.3536	0.0
7	0.3551	0.0
8	0.3626	0.0
9	0.3766	0.0
10	0.39	0.0001
11	0.4069	0.0
12	0.4203	0.0
```

In addition, a main log file is written in the input directory that is called `admixture_wrapper.log`. This file contains information about the settings used to run `admixture-wrapper.py`, as well as each specific command used to execute admixture (all ped files, all K values, all replicates). Example contents:

```
Run executed: 2019-11-22 12:42:18.382613

admixture_wrapper settings:
-i:		/Volumes/West_Africa/West_Africa/Hyperolius-Merged/5-analyses-ocellatus/admixture
--kmin:	1
--kmax:	12
--reps:	5
--cv:	20
-t:		4



================================================================================
Running admixture for: populations_r50_m70_randomSNP_recoded.ped
================================================================================

2019-11-22 12:42:18.383124: K1 replicate 1: admixture populations_r50_m70_randomSNP_recoded.ped 1 -j4 --cv=20 | tee populations_r50_m70_randomSNP_recoded.1.log.out
2019-11-22 12:42:21.324944: K1 replicate 1: Finished. Elapsed time: 0:00:02.941766

2019-11-22 12:42:21.325129: K1 replicate 2: admixture populations_r50_m70_randomSNP_recoded.ped 1 -j4 --cv=20 | tee populations_r50_m70_randomSNP_recoded.1.log.out
2019-11-22 12:42:24.248489: K1 replicate 2: Finished. Elapsed time: 0:00:02.923321

2019-11-22 12:42:24.248672: K1 replicate 3: admixture populations_r50_m70_randomSNP_recoded.ped 1 -j4 --cv=20 | tee populations_r50_m70_randomSNP_recoded.1.log.out
2019-11-22 12:42:27.117978: K1 replicate 3: Finished. Elapsed time: 0:00:02.869267

...............
```



### License

GNU Lesser General Public License v3.0

### Contact

The admixture-wrapper scripts were written by Daniel Portik (daniel.portik@gmail.com)
