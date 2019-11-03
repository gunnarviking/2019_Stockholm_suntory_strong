from common import filter_service_data_collection
from common import filter_service_filter
from common import filter_service_save
def main():
    print("main")
    filelist = filter_service_data_collection.init()
    counter = 0
    if filelist is not None:
        for file in filelist:
            counter+=1
            print("counter:",counter)

            print("for file", file)
            newfile = filter_service_filter.init(file)
            if newfile is not None:
                filter_service_save.init(newfile, counter)
            newfile = None


if __name__ == '__main__':
    main()
