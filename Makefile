VERSION=master

all: build/GXWriter-$(VERSION).curapackage build/FlashforgeFinderIntegration-$(VERSION).curapackage

clean:
	rm -rf build

build/GXWriter-$(VERSION).curapackage: plugins/GXWriter/* LICENSE icon.png
	mkdir -p build/GXWriter/files/plugins
	cp LICENSE icon.png build/GXWriter
	cp -r plugins/GXWriter/ build/GXWriter/files/plugins/
	mv build/GXWriter/files/plugins/GXWriter/package.json build/GXWriter/
	cd build/GXWriter && \
		zip ../GXWriter-$(VERSION).curapackage -q \
		-x "*testdata*" \
		-x "*__pycache__*" \
		-x "*pyc" \
		-r .

build/FlashforgeFinderIntegration-$(VERSION).curapackage: plugins/FlashforgeFinderIntegration/* LICENSE icon.png
	mkdir -p build/FlashforgeFinderIntegration/files/plugins
	cp LICENSE icon.png build/FlashforgeFinderIntegration
	cp -r plugins/FlashforgeFinderIntegration/ build/FlashforgeFinderIntegration/files/plugins/
	mv build/FlashforgeFinderIntegration/files/plugins/FlashforgeFinderIntegration/package.json build/FlashforgeFinderIntegration/
	cd build/FlashforgeFinderIntegration && \
		zip ../FlashforgeFinderIntegration-$(VERSION).curapackage -q \
		-x "*testdata*" \
		-x "*__pycache__*" \
		-x "*pyc" \
		-r .
