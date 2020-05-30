#!/bin/bash
set -e
[ -n "$DEBUG" ] && set -x

# Globals
rootdir="$(readlink -f "$(dirname $0)/..")"
pkg="FlashforgeFinderIntegration"
version="${version:-latest-$(git rev-parse HEAD)}"
outdir="${rootdir}/build"
outfile="${pkg}-${version}.curapackage"

# Use a temporary folder to bundle the extension
work="$(mktemp -d)"
trap 'rm -r "$work"' EXIT

# Create .curapackage skeleton
mkdir -p "$work/files"
cp LICENSE icon.png package.json "$work"
cp -r plugins/ "$work/files"

# Package the output
mkdir -p "${outdir}"
rm -f "${outdir}/${outfile}"
cd "$work"
zip ${outdir}/${outfile} -q \
	-x "*testdata*" \
	-x "*__pycache__*" \
	-x "*pyc" \
	-r .

echo "Package file created at ${outdir}/${outfile}"
unzip -l "${outdir}/${outfile}"
