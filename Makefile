all:
	mkdir -p ${HOME}/.sams/messages
	touch ${HOME}/.sams/addressbook.csv
	python generate_keys.py

keygen:
	python generate_keys.py
