# Makefile build script to bundle the source
# code as .curapackage and -src.zip for distribution.

VERSION=master

all: build

clean:
	rm -rf build

build: build-gxwriter build-ffintegration

build-gxwriter: build/GXWriter-$(VERSION).curapackage

build/GXWriter-$(VERSION).curapackage: plugins/GXWriter/* LICENSE icon.png
	mkdir -p build/GXWriter/files/plugins
	cp LICENSE icon.png build/GXWriter
	cp -r plugins/GXWriter/ build/GXWriter/files/plugins/
	mv build/GXWriter/files/plugins/GXWriter/package.json build/GXWriter/
	sed -i -e 's/"version":.*/"version": "$(VERSION)",/g' build/GXWriter/files/plugins/GXWriter/plugin.json
	sed -i -e 's/"package_version":.*/"package_version": "$(VERSION)",/g' build/GXWriter/package.json
	cd build/GXWriter && \
		zip ../GXWriter-$(VERSION).curapackage -q \
		-x "*testdata*" \
		-x "*__pycache__*" \
		-x "*pyc" \
		-r .
	cd build/GXWriter/files/plugins && \
		zip ../../../GXWriter-$(VERSION)-src.zip -q \
		-x "*testdata*" \
		-x "*__pycache__*" \
		-x "*pyc" \
		-r .

build-ffintegration: build/FlashforgeFinderIntegration-$(VERSION).curapackage plugins/FlashforgeFinderIntegration/printer/defs/finder.def.json

build/FlashforgeFinderIntegration-$(VERSION).curapackage: plugins/FlashforgeFinderIntegration/* LICENSE icon.png
	mkdir -p build/FlashforgeFinderIntegration/files/plugins
	cp LICENSE icon.png build/FlashforgeFinderIntegration
	cp -r plugins/FlashforgeFinderIntegration/ build/FlashforgeFinderIntegration/files/plugins/
	mv build/FlashforgeFinderIntegration/files/plugins/FlashforgeFinderIntegration/package.json build/FlashforgeFinderIntegration/
	sed -i -e 's/"version":.*/"version": "$(VERSION)",/g' build/FlashforgeFinderIntegration/files/plugins/FlashforgeFinderIntegration/plugin.json
	sed -i -e 's/"package_version":.*/"package_version": "$(VERSION)",/g' build/FlashforgeFinderIntegration/package.json
	cd build/FlashforgeFinderIntegration && \
		zip ../FlashforgeFinderIntegration-$(VERSION).curapackage -q \
		-x "*testdata*" \
		-x "*__pycache__*" \
		-x "*pyc" \
		-r .
	cd build/FlashforgeFinderIntegration/files/plugins && \
		zip ../../../FlashforgeFinderIntegration-$(VERSION)-src.zip -q \
		-x "*testdata*" \
		-x "*__pycache__*" \
		-x "*pyc" \
		-r FlashforgeFinderIntegration

plugins/FlashforgeFinderIntegration/printer/defs/finder.def.json:
	git submodule init
	git submodule update

test:
	find plugins -type f -iname '*_test.py' | xargs -I{} python3 {}

release: build test
	if [ x"$(VERSION)" = x"master" ] ; then echo "Unable to release from master. Use make VERSION=X.Y.Z" ; exit 1; fi
	git tag v$(VERSION)
	git push --tags
