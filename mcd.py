from modules.ModelChangeDetector import ModelChangeDetector
"""
TODO
1. fix logging levels in different modules
2. fix argument sharing
"""
if __name__ == "__main__":
    result = ModelChangeDetector().main()
    # don't know if we should print from here or within the ModelChangeDetector module,
    # felt that the module should be left alone returning a result and the caller here 
    # can decide what to do with the result.
    print(result)
