#!/bin/bash

#SBATCH --job-name=webscarping%j
#SBATCH --output=webscraping%j.out
#SBATCH --error=webscraping%j.err
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

arg1 = $1
arg2 = $2

python3 scrape.py $arg1 $arg2
