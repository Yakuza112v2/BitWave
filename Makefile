BITWAVE_APP_NAME = "BitWave"
BITWAVE_VERSION=`grep -m 1 '__version__' bitwave/bitwave_ui/__init__.py | tr -d ' "' | cut -d'=' -f2`

.PHONY: install check test gui-bitwave gui-bitwave-windows build-windows help
install:
	@poetry install --all-extras --with dev
	@poetry run pre-commit install

check:
	@poetry check --lock
	@poetry run pre-commit run -a
	@poetry run deptry .

test:
	@poetry run pytest --doctest-modules

gui-bitwave:
	@poetry run python -c "import sys; sys.exit(0 if sys.platform == 'win32' else 'BitWave wird ausschließlich für Windows gebaut.')"
	@poetry run python tools/prune_static_qml_plugins.py
	@poetry run python -m nuitka \
		--file-version=$(BITWAVE_VERSION) \
		--product-version=$(BITWAVE_VERSION) \
		--output-filename=$(BITWAVE_APP_NAME) \
		--product-name=$(BITWAVE_APP_NAME) \
		bitwave.py
	@bash tools/trim_qt_bundle.sh "dist/bitwave.dist"

gui-bitwave-windows: gui-bitwave
build-windows: gui-bitwave-windows

help:
	@echo "make build-windows — BitWave für Windows erstellen"
