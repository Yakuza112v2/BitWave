BITWAVE_APP_NAME = "BitWave"
BITWAVE_VERSION=`grep -m 1 '__version__' bitwave/bitwave_ui/__init__.py | tr -d ' "' | cut -d'=' -f2 | cut -d'-' -f1`

.PHONY: install gui-bitwave gui-bitwave-windows build-windows help
install:
	@poetry install --all-extras --with dev

gui-bitwave:
	@poetry run python -c "import sys; sys.exit(0 if sys.platform == 'win32' else 'BitWave wird ausschließlich für Windows gebaut.')"
	@poetry run python .github/build/prune_static_qml_plugins.py
	@poetry run python -m nuitka \
		--file-version=$(BITWAVE_VERSION) \
		--product-version=$(BITWAVE_VERSION) \
		--output-filename=$(BITWAVE_APP_NAME) \
		--product-name=$(BITWAVE_APP_NAME) \
		bitwave.py
	@bash .github/build/trim_qt_bundle.sh "dist/bitwave.dist"

gui-bitwave-windows: gui-bitwave
build-windows: gui-bitwave-windows

help:
	@echo "make build-windows — BitWave für Windows erstellen"
