import os, json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sys import argv

ignored_fields = []
time_series_field = -1
actual_data_field = -1
label_fields = []

list_of_cvses = []


if __name__ == "__main__":
    if len(argv) < 2:
        print('Usage: python3 main.py /path/to/folder/of/cvses/')
        exit(1)
    
    csv_files = [f'{argv[1]}/{csv_file}' for csv_file in os.listdir(argv[1])]
    csv_file = csv_files[0]
    # csv = pd.read_csv(csv_file, encoding='utf-16', sep='\t') # reading may be perform with generator functions
    csv = pd.read_csv(argv[1], encoding='utf-8')

    for i, col in enumerate((csv.columns)):
        print(i, col)

    ignored_fields.extend(
        map(
            lambda x: csv.columns[int(x)],
            input("Give ignored fields with seperator ',': ")
                .split(',')
        )
    )

    time_series_field = csv.columns[  
        int(
            input("Give exactly one time-series field: ")
        )
    ]

    actual_data_field = csv.columns[
        int(
            input("Give exactly one actual data field: ")
        )
    ]

    label_fields = list(
        set(csv.columns) - set(ignored_fields+[time_series_field]+[actual_data_field])
    )

    print("Ignored Fields:", ignored_fields)
    print("Label Fields:", label_fields)
    print("Time Series Field:", time_series_field)
    print("Actual Data Field:", actual_data_field)

    print("Merging csvs")

    df_cluster = pd.concat(
        map(lambda x: pd.read_csv(x, encoding='utf-16', sep='\t'), csv_files)
    )

    print("Merging end...")
    
    for k, df in df_cluster.groupby(label_fields):
        df.plot(x=time_series_field, y=actual_data_field)
        plt.xticks(rotation=90)
        plt.legend([' '.join(k)])
        plt.savefig(''.join(k)+'.png', dpi=600, format='png', bbox_inches='tight')

    # fig, ax = plt.subplots(figsize=(10,4))
    # for k, df in df_cluster.groupby(label_fields):
    #     ax.plot(df[time_series_field], df[actual_data_field], label=k)

    # ax.legend()
    # plt.show()


        