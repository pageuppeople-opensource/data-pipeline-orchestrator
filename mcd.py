from modules.ModelChangeDetector import ModelChangeDetector

if __name__ == "__main__":
    result = ModelChangeDetector().main()
    # TODO don't know if we should print from here or within the ModelChangeDetector module,
    # felt that the module should be left alone returning a result and the caller here 
    # can decide what to do with the result. :S
    print(result)
