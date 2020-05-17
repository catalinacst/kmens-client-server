#!/bin/bash

. ./utils.sh

declare -a datasets=("dataParse-01" "dataParse-02" "dataParse-03" "dataParse-04")

utils.info "███╗   ██╗███████╗████████╗███████╗██╗     ██╗██╗  ██╗    ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗"
utils.info "████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║     ██║╚██╗██╔╝    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝"
utils.info "██╔██╗ ██║█████╗     ██║   █████╗  ██║     ██║ ╚███╔╝     ███████╗██║     ██████╔╝██║██████╔╝   ██║   "
utils.info "██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██║     ██║ ██╔██╗     ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   "
utils.info "██║ ╚████║███████╗   ██║   ██║     ███████╗██║██╔╝ ██╗    ███████║╚██████╗██║  ██║██║██║        ██║   "
utils.info "╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   "
utils.alert "┌─┐┌┬┐┬┬  ┬┌─┐┌┐┌  ┌─┐┌─┐┬─┐┌┬┐┌─┐┌┐┌┌─┐"
utils.alert "└─┐ │ │└┐┌┘├┤ │││  │  ├─┤├┬┘ │││ ││││├─┤"
utils.alert "└─┘ ┴ ┴ └┘ └─┘┘└┘  └─┘┴ ┴┴└──┴┘└─┘┘└┘┴ ┴"
utils.alert "┌─┐┌─┐┌┬┐┌─┐┬  ┬┌┐┌┌─┐  ┌─┐┌─┐┌─┐┌┬┐┬─┐┌─┐"
utils.alert "│  ├─┤ │ ├─┤│  ││││├─┤  │  ├─┤└─┐ │ ├┬┘│ │"
utils.alert "└─┘┴ ┴ ┴ ┴ ┴┴─┘┴┘└┘┴ ┴  └─┘┴ ┴└─┘ ┴ ┴└─└─┘"
utils.info  "_____________________________________________________________________________________________________"
for dataset in "${datasets[@]}"; do
	echo "File $dataset"
	utils.info "Generate graph"
	python3 stats.py "$dataset.txt" "create" >> stats.txt
	utils.info "Moving file"
	mv stats.txt "./stats/$dataset.txt"
	# utils.info "Moving file"
	# mv "$dataset-stats.txt" "./stats/"
	utils.info "Finish process"
done