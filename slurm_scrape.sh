#!/bin/bash

#SBATCH --job-name=webscraping%j
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

gnome-terminal -- python3 scrape.py $1 $2

