#
# To help clean-up and zip up everything
#

NOADD  := db.sqlite3 $(wildcard *.tar)
FILES  := $(filter-out $(NOADD), $(wildcard *))
OUTPUT := $(notdir $(abspath .))

all: zip

.PHONY: clean zip
clean:
	rm -rf */__pycache__/ */*/__pycache__/ */migrations/0*.py $(NOADD)
	
zip: clean
	tar cvf $(OUTPUT).tar $(FILES)
