init:
	sudo pip install -r requirements.txt

test:
	nosetests

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

.PHONY: init test cleans
