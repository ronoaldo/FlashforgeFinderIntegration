#!/bin/bash
set -e

rootdir="$(readlink -f "$(dirname $0)/../..")"
pkg="FlashforgeFinderIntegration"
version="${version:-latest-$(git rev-parse HEAD)}"
outdir="${rootdir}/${pkg}/build"
outfile="${pkg}-${version}.zip"

echo "Package: $pkg"
echo "Root dir: $rootdir"
echo "Version: $version"

cd $rootdir
mkdir -p ${outdir}
zip ${outdir}/${outfile} \
	-x "*testdata*" -q -r \
	${pkg}/plugin.json \
	${pkg}/plugins/ \
	${pkg}/scripts/

echo "Package file created at ${outdir}/${outfile}"
unzip -l "${outdir}/${outfile}"
