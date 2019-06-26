clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

virtualenv:
	virtualenv -ppython3.6 venv
setup-develop:
	cd src && python setup.py develop &&\
		pip install -r requirements_dev.txt
build-lambda:
	deploy/package.sh

docs:
	$(MAKE) -C src docs

docker-test:
	$(MAKE) -C ./src docker-test

coverhtml:
	$(MAKE) -C ./src coverhtml

deploy-ci-infra:
	cd infra/codebuild && nimbi deploy
deploy-ci-lambda:
	cd infra/codebuild && deploy/package.sh 
