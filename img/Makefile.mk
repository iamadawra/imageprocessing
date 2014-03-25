DIR = img
IMAGES = $(shell cut -d' ' -f1 $(DIR)/sources | sed -e 's/^/$(DIR)\//g')

all:

include $(DIR)/images.mk

$(DIR)/images.mk: $(DIR)/Makefile.mk
	@rm -f $@
	@echo "all: $(IMAGES)\n" > $@
	@awk '{ \
		print "$(DIR)/"$$1 ":\n\
\t@echo Downloading "$$1"\n\
\t@wget -q \"" $$2 "\" -O $(DIR)/"$$1 "\n\
\t@touch $(DIR)/"$$1">/dev/null \n" \
		}' $(DIR)/sources >> $@
