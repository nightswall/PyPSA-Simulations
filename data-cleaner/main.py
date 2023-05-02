import pandas as pd
from sys import argv

ignored_fields = []
time_series_field = -1
actual_data_field = -1
label_fields = []

if __name__ == "__main__":
    if len(argv) < 2:
        print('Usage: python3 main.py /path/to/example.cvs')

    # cvs = pd.read_csv(argv[1], encoding='utf-16', sep='\t') # reading may be perform with generator functions
    cvs = pd.read_csv(argv[1], encoding='utf-8')
    for i, col in enumerate((cvs.columns)):
        print(i, col)

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

    x = list(cvs.groupby(label_fields))
    print(x)
    print(len(x))

    # ask for export and create exporting tool