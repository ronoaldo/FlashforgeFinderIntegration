#!/bin/bash
set -e

echo "Installing for all Cura versions... "

srcdir="$(readlink -f "`dirname $0`/..")"
destdir=$HOME/.local/share/cura
VERSIONS="$(ls -d $destdir/*/)"

cd $srcdir
for version in $VERSIONS ; do
	echo "Installing via symbolic link to $version"

	for plugin in plugins/* ; do
		if ! [ -e "${version}${plugin}" ] ; then
			echo "Installing $plugin -> ${version}${plugin}"
			ln -s "${srcdir}/${plugin}" "${version}${plugin}"
		else
			echo "$plugin already installed."
		fi
	done
	
	for script in scripts/* ; do
		if ! [ -e "${version}${script}" ] ; then
			echo "Installing $script -> ${version}${script}"
			ln -s "${srcdir}/${script}" "${version}${script}"
		else
			echo "$script already installed."
		fi
	done

	if ! [ -e "${version}/definitions/finder.def.json" ] ; then
		echo "Installing printer definition ..."
		ln -s "${srcdir}/printer/definitions/finder.def.json" "${version}/definitions/finder.def.json"
	else
		echo "finder.def.json already installed."
	fi
	if ! [ -e "${version}/extruders/FF_finder_extruder_0.def.json" ] ; then
		echo "Installing extruder definition ..."
		ln -s "${srcdir}/printer/extruders/FF_finder_extruder_0.def.json" "${version}/extruders/FF_finder_extruder_0.def.json"
	else
		echo "FF_finder_extruder_0.def.json already installed."
	fi
	if ! [ -e "${version}/meshes/FlashforgeFinderBed.stl" ] ; then
		echo "Installing printer definition ..."
		mkdir -p "${version}/meshes/"
		ln -s "${srcdir}/printer/meshes/FlashforgeFinderBed.stl" "${version}/meshes/FlashforgeFinderBed.stl"
	else
		echo "FlashForgeFinderBed.stl already installed."
	fi
done
