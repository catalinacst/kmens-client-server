#!/bin/bash

. ./utils.sh

declare -a datasets=("dataParse-01" "dataParse-02" "dataParse-03" "dataParse-04")

utils.printer "██╗  ██╗ █████╗ ██╗     ██╗  ██╗ ██████╗     ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗"
utils.printer "██║ ██╔╝██╔══██╗██║     ██║  ██║██╔═══██╗    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝"
utils.printer "█████╔╝ ███████║██║     ███████║██║   ██║    ███████╗██║     ██████╔╝██║██████╔╝   ██║   "
utils.printer "██╔═██╗ ██╔══██║██║     ██╔══██║██║   ██║    ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   "
utils.printer "██║  ██╗██║  ██║███████╗██║  ██║╚██████╔╝    ███████║╚██████╗██║  ██║██║██║        ██║   "
utils.printer "_________________________________________________________________________________________"
for dataset in "${datasets[@]}"; do
	echo "File $dataset"
	utils.printer "Generate graph"
	python3 stats.py "$dataset.txt" >> "$dataset-stats.txt"
	# utils.printer "Moving file"
	# mv "$dataset-stats.txt" "./stats/"
	utils.printer "Finish process"
done