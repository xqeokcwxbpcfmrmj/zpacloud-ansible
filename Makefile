# Taken from: https://github.com/sensu/sensu-go-ansible/blob/master/Makefile

# Make sure we have ansible_collections/willguibr/zpacloud_enhanced
# as a prefix. This is ugly as heck, but it works. I suggest all future
# developer to treat next few lines as an opportunity to learn a thing or two
# about GNU make ;)
collection := $(notdir $(realpath $(CURDIR)      ))
namespace  := $(notdir $(realpath $(CURDIR)/..   ))
toplevel   := $(notdir $(realpath $(CURDIR)/../..))

err_msg := Place collection at <WHATEVER>/ansible_collections/willguibr/zpacloud
ifneq (zpacloud,$(collection))
  $(error $(err_msg))
else ifneq (willguibr,$(namespace))
  $(error $(err_msg))
else ifneq (ansible_collections,$(toplevel))
  $(error $(err_msg))
endif

install:
	rm -f willguibr*
	ansible-galaxy collection build . --force
	ansible-galaxy collection install willguibr* --force
	rm -f willguibr*

doctest:
	for i in $$(ls -1 plugins/modules | grep -v init); do \
		echo "Checking $$i..." ; \
		ansible-doc -M plugins/modules $$i > /dev/null ; \
	done

.PHONY: install doctest
