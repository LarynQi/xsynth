OUT = ./out
ifneq ("$(wildcard $(OUT))","")
    CLEAN-OUT = @rm -r $(OUT)
else
    CLEAN-OUT = @:
endif

PYCACHE = ./__pycache__
ifneq ("$(wildcard $(PYCACHE))","")
    CLEAN-CACHE= @rm -r $(PYCACHE)
else
    CLEAN-CACHE = @:
endif

clean:
	$(CLEAN-OUT)
	$(CLEAN-CACHE)