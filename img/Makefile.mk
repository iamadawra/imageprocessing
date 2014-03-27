DIR = img

# There are a list of image entries in the $(DIR)/sources file of the format
# <img-name> <img-url>
# on each line. The $(DIR)/images.mk target creates an images.mk files with
# targets for each image entry.

# A list of all image names from the sources files
IMAGES = $(shell cut -d' ' -f1 $(DIR)/sources | sed -e 's/^/$(DIR)\//g')

all:

include $(DIR)/images.mk

# Create an images.mk file with targets of the following format:
# ---
# $(DIR)/<img-name>:
# 	@echo Downloading <img-name>
# 	@wget -q "<img-url>" -O $(DIR)/<img-name>
# 	@touch $(DIR)/<img-name> >/dev/null
# ---
#
# Note that the URL needs to be quoted before passing into wget, to avoid
# various issues with the terminal.

$(DIR)/images.mk: $(DIR)/Makefile.mk
	@rm -f $@
	@echo "all: $(IMAGES)" > $@ # target `all`
	@echo >> $@                 # separating line
	@awk '{ \
		print "$(DIR)/"$$1 ":\n\
\t@echo Downloading "$$1"\n\
\t@wget -q \"" $$2 "\" -O $(DIR)/"$$1 "\n\
\t@touch $(DIR)/"$$1" >/dev/null \n" \
		}' $(DIR)/sources >> $@
