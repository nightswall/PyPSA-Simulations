import os, json
import pandas as pd
from sys import argv

ignored_fields = []
time_series_field = -1
actual_data_field = -1
label_fields = []

meta_fields={}

if __name__ == "__main__":
    if len(argv) < 2:
        print('Usage: python3 main.py /path/to/folder/of/cvses/')
        exit(1)

    dir_name = os.path.basename(argv[1])
    try:
        with open(f'{os.path.dirname(__file__)}/meta/{dir_name}.json', 'r') as f:
            meta_fields=json.load(f)

    except FileNotFoundError:
        pass

    finally:
        for cvs_file in os.listdir(argv[1]):
            cvs = pd.read_csv(f'{argv[1]}/{cvs_file}', encoding='utf-16', sep='\t') # reading may be perform with generator functions
            for i, col in enumerate((cvs.columns)):
                print(i, col)

            if meta_fields:
                first_cvs = next(iter(meta_fields))

                for pre_determined_fields in meta_fields[first_cvs]:
                    print(pre_determined_fields, meta_fields[first_cvs][pre_determined_fields])
                
                if (set(cvs.columns)-set(meta_fields[first_cvs].values())) == 0\
                      or input('Continue with pre determined fields?[y/N]: ') == 'y':
                    meta_fields[cvs_file] = meta_fields[first_cvs]
                    continue
            else:
                ignored_fields.extend(
                    map(
                        lambda x: cvs.columns[int(x)],
                        input("Give ignored fields with seperator ',': ")
                            .split(',')
                    )
                )

                time_series_field = cvs.columns[  
                    int(
                        input("Give exactly one time-series field: ")
                    )
                ]

                actual_data_field = cvs.columns[
                    int(
                        input("Give exactly one actual data field: ")
                    )
                ]

                label_fields = list(
                    set(cvs.columns) - set(ignored_fields+[time_series_field]+[actual_data_field])
                )

                print("Ignored Fields:", ignored_fields)
                print("Label Fields:", label_fields)
                print("Time Series Field:", time_series_field)
                print("Actual Data Field:", actual_data_field)

                meta_fields[cvs_file] = {
                    'ignored_fields': ignored_fields,
                    'label_fields': label_fields,
                    'time_series_field': time_series_field,
                    'actual_data_field': actual_data_field
                }

        with open(f'{os.path.dirname(__file__)}/meta/{dir_name}.json', 'w') as f:
            json.dump(meta_fields, f)



    # 
    # # cvs = pd.read_csv(argv[1], encoding='utf-8')
    # for i, col in enumerate((cvs.columns)):
    #     print(i, col)

    # print(list(
    #     cvs.groupby(label_fields)
    # ))