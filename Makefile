BITWAVE_APP_NAME = "BitWave"
BITWAVE_VERSION=`grep -m 1 '__version__' waves/waves_ui/__init__.py | tr -d ' "' | cut -d'=' -f2`

.PHONY: install check test gui-waves gui-waves-windows build-windows help
install:
	@poetry install --all-extras --with dev
	@poetry run pre-commit install

check:
	@poetry check --lock
	@poetry run pre-commit run -a
	@poetry run deptry .

test:
	@poetry run pytest --doctest-modules

gui-waves:
	@poetry run python -c "import sys; sys.exit(0 if sys.platform == 'win32' else 'BitWave wird ausschließlich für Windows gebaut.')"
	@poetry run python tools/prune_static_qml_plugins.py
	@poetry run python -m nuitka \
		--file-version=$(BITWAVE_VERSION) \
		--product-version=$(BITWAVE_VERSION) \
		--output-filename=$(BITWAVE_APP_NAME) \
		--product-name=$(BITWAVE_APP_NAME) \
		waves.py
	@bash tools/trim_qt_bundle.sh "dist/waves.dist"

gui-waves-windows: gui-waves
build-windows: gui-waves-windows

help:
	@echo "make build-windows — BitWave für Windows erstellen"
