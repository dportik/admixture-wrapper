import os
import subprocess as sp
import shutil
from datetime import datetime
import numpy as np
import argparse

def get_args():
    """
    Get arguments from command line.
    """
    parser = argparse.ArgumentParser(
            description="""---------------------------------------------------------------------------
    admixture-wrapper - A tool for automating analyses with the program admixture. A directory of 
    ped files should be specified using the -i flag. The minimum and maximum K values, the 
    number of replicates per K, and the cross-validation procedure folds value are set by the user. 
    The number of threads can also be specified. Outputs from each replicate are written to a unique 
    directory created for each ped file. Two main output files are produced per ped file, one which 
    contains the cross-validation scores for every replicate, and one which contains the average 
    cross-validation score per K value. The second file can be used to plot the CV scores with the 
    associated R script. A log file is also produced, which contains the analysis settings and the 
    commands used to execute admixture for all K value replicates. 
    
 
    DEPENDENCIES: admixture (in path).
    ---------------------------------------------------------------------------""")
    
    parser.add_argument("-i", "--indir",
                            required=True,
                            help="REQUIRED: The full path to the directory which contains "
                            "at least one ped file (in '12' coded format).")
    
    parser.add_argument("--kmin",
                            required=True,
                            type=int,
                            help="REQUIRED: The minimum K-value to start with.")
    
    parser.add_argument("--kmax",
                            required=True,
                            type=int,
                            help="REQUIRED: The maximum K-value to end with.")
    
    parser.add_argument("--reps",
                            required=True,
                            type=int,
                            help="REQUIRED: The number of replicates to perform for "
                            "each K-value.")
        
    parser.add_argument("--cv",
                            required=True,
                            type=int,
                            help="REQUIRED: Select the fold number for the cross-validation "
                            "procedure. For example, setting 10 would invoke the "
                            "--cv=10 flag in admixture.")
    
    parser.add_argument("-t", "--threads",
                            required=False,
                            type=int,
                            default=1,
                            help="OPTIONAL: Specifies number of threads to use. Default = 1.")
        
    return parser.parse_args()

def write_log(argd, text, indir):
    os.chdir(indir)
    if argd:
        with open("admixture_wrapper.log", 'a') as fh:
            fh.write("Run executed: {}\n\nadmixture_wrapper settings:\n-i:\t\t{}\n--kmin:\t{}\n--kmax:\t{}\n--reps:\t{}\n--cv:\t{}\n-t:\t\t{}\n\n"
                .format(datetime.now(), argd["indir"], argd["kmin"], argd["kmax"], argd["reps"], argd["cv"], argd["threads"]))
    else:
        with open("admixture_wrapper.log", 'a') as fh:
            fh.write("{}".format(text))

def get_peds(indir):
    os.chdir(indir)
    peds = [f for f in os.listdir('.') if f.endswith('.ped')]
    if not peds:
        raise ValueError("\n\n\nERROR: No ped files (X.ped) were "
                             "located in input directory.\n\n\n")
    else:
        print("\n\nFound {} ped files to run:".format(len(peds)))
        for p in peds:
            print("\t{}".format(p))
        return peds

def make_outdir(indir, prefix):
    outdir = os.path.join(indir, "Outputs-{}".format(prefix))
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    else:
        raise ValueError("\n\n\nERROR: Output directory already exists: "
                             "{}\nPlease remove before running.\n\n\n".format(outdir))
    return outdir

def run_admixture(p, indir, kmin, kmax, reps, cv, threads):
    os.chdir(indir)
    outdir = make_outdir(indir, p.split('.ped')[0])
    
    kreps = []
    for i in range(kmin, kmax +1):
        kreps.append([[i, x] for x in list(range(1, reps+1))])

    for i in kreps:
        for j in i:
            tb = datetime.now()
            print("\n\n{}".format("-"*50))
            print("Running: K{0} replicate {1}".format(j[0], j[1]))
            print("{}\n".format("-"*50))
            
            call_str = "admixture {0} {1} -j{2} --cv={3} | tee {4}.{1}.log.out".format(p, j[0], threads, cv, p.split('.ped')[0])
            write_log(None, "{0}: K{1} replicate {2}: {3}\n".format(datetime.now(), j[0], j[1], call_str), indir)
            print("{}\n".format(call_str))
            proc = sp.call(call_str, shell=True)
            
            outs = [f for f in os.listdir('.') if f.endswith(('.P', '.Q', '.out'))]
            for o in outs:
                shutil.move(o, os.path.join(outdir, "{}.{}.{}.{}".format(o.split('.')[0], o.split('.')[1], j[1], o.split('.')[-1])))
                
            tf = datetime.now()
            print("\n{}".format("-"*50))
            print("Finished: K{0} replicate {1}".format(j[0], j[1]))
            print("Elapsed time: {} (H:M:S)".format(tf - tb))
            write_log(None, "{0}: K{1} replicate {2}: Finished. Elapsed time: {3}\n\n".format(datetime.now(), j[0], j[1], tf - tb), indir)
            print("{}\n".format("-"*50))

    return outdir

def summarize_outputs(outdir, indir, kmin, kmax, prefix):
    os.chdir(outdir)
    outs = [f for f in os.listdir('.') if f.endswith('.out')]
    
    if outs:
        tb = datetime.now()
        print("\n\n{}".format("-"*50))
        print("\nSummarizing output files...")

        outall = "Cross_Validation_All_Replicates.txt"
        with open(outall, 'a') as fh:
            fh.write("{}\t{}\t{}\n".format("K", "Rep", "CV"))
            
        outavg = "Cross_Validation_Averages.txt"
        with open(outavg, 'a') as fh:
            fh.write("{}\t{}\t{}\n".format("K", "CV_Avg", "CV_Stdev"))
        
        for i in range(kmin, kmax +1):
            kouts = sorted([f for f in outs if int(f.split('.')[1]) == i])
            cv_vals = []
            for f in kouts:
                with open(f, 'r') as fh:
                    cv = [float(l.strip().split()[-1]) for l in fh if l.startswith('CV error')]
                    cv_vals.append(cv[0])
                    with open(outall, 'a') as fh:
                        fh.write("{}\t{}\t{}\n".format(i, f.split('.')[2], cv[0]))
                        
            with open(outavg, 'a') as fh:
                fh.write("{}\t{}\t{}\n".format(i, np.round(np.mean(cv_vals), 4), np.round(np.std(cv_vals), 4)))
                
        tf = datetime.now()
        print("\tFinished.\n\tElapsed time: {} (H:M:S)".format(tf - tb))
        print("{}\n".format("-"*50))

        shutil.move(outall, os.path.join(indir, "{}.CV_All.txt".format(prefix)))
        shutil.move(outavg, os.path.join(indir, "{}.CV_Avg.txt".format(prefix)))
        
    else:
        raise ValueError("\n\n\nERROR: No output log files found in directory: {}\n\n\n".format(outdir))
    
    
def main():
    args = get_args()
    tb = datetime.now()
    
    argd = vars(args)
    print("\n\n\nadmixture_wrapper settings:\n-i: {}\n--kmin: {}\n--kmax: {}\n--reps: {}\n--cv {}\n-t {}\n\n"
              .format(argd["indir"], argd["kmin"], argd["kmax"], argd["reps"], argd["cv"], argd["threads"]))    
    write_log(argd, None, args.indir)
    
    peds = get_peds(args.indir)
    
    for p in peds:
        print("\n\n{}".format("="*80))
        print("Running admixture for: {}".format(p))
        print("{}\n\n".format("="*80))
        write_log(None, "\n\n{0}\nRunning admixture for: {1}\n{0}\n\n".format("="*80, p), args.indir)
        
        outdir = run_admixture(p, args.indir, args.kmin, args.kmax, args.reps, args.cv, args.threads)
        
        summarize_outputs(outdir, args.indir, args.kmin, args.kmax, p.split('.ped')[0])
        
    tf = datetime.now()
    write_log(None, "\n\n{0}\n\nTotal elapsed time: {1} (H:M:S)\n\n{0}\n\n".format("="*80, tf - tb), args.indir)
    print("\n\n{}".format("="*80))
    print("\nTotal elapsed time: {} (H:M:S)\n".format(tf - tb))
    print("{}\n\n".format("="*80))
    


if __name__ == '__main__':
    main()
