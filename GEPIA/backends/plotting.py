import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pymongo
from backends.database import DatabaseAPI


class GenePlot(object):
    def __init__(self,gene_name):
        self.api = DatabaseAPI(db_name='tcga',collection_name='gene_by_var_table')
        self.collection_name = "gene_by_var_table"
        self.gene_name = gene_name

    def stripplot(self) -> plt.figure:
        fig, ax = plt.subplots(figsize=(10, 8))
        arr = np.array(self.api.read_table_gene_by_var(self.gene_name))
        arr = 2**arr - 1
        print(np.min(arr))
        self.collection_name = "sample_info"
        df = pd.DataFrame(self.api.get_metadata(self.collection_name))
        df[self.gene_name] = arr
        y_max, y_min = np.max(df[self.gene_name]), np.min(df[self.gene_name])
        grouped = df.groupby(["Disease", "Type"])
        for i, (group_name, group_data) in enumerate(grouped):
            sorted_values = group_data[self.gene_name].sort_values()
            x_values = np.array(i + np.linspace(0, 1, len(sorted_values)))
            ax.scatter(x_values, sorted_values, s=2)
            if i % 2 == 0:
                plt.fill_betweenx([y_min, y_max], i, i + 1, color='grey', alpha=0.2)
        ax.set_xticks(np.arange(len(grouped)) + 0.5)
        ax.set_xticklabels(
            [f"{disease}-{Type}({group_data.shape[0]})" for (disease, Type), group_data in grouped.groups.items()],
            rotation=45, ha='right', fontsize=8)
        offset_x = 5e-3 * (len(grouped))
        offset_y = 5e-3 * (y_max - y_min)
        ax.set_xlim(-offset_x, len(grouped) + offset_x)
        ax.set_ylim(-offset_y, y_max + offset_y)
        plt.tight_layout()
        return fig

