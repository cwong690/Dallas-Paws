#Plotting helper functions
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def autolabel(bar_graph, ax):
    for bar in bar_graph:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

def bar_count(ax, cat_col, dog_col, width=0.35):
    axes_labels = cat_col.index
    x = np.arange(len(axes_labels))
    cat = ax.bar(x - width/2, cat_col, width, label='Cats', color='tomato')
    dog = ax.bar(x + width/2, dog_col, width, label='Dogs', color='lightseagreen')
    ax.set_ylabel('Counts')
    ax.set_title(f'Count of {cat_col.name}: Cats vs Dogs')
    ax.set_xticks(x)
    ax.set_xticklabels(axes_labels, rotation=45)
    ax.legend(loc='upper center')
    autolabel(cat, ax)
    autolabel(dog, ax)
    
def bar_percent(ax, cat_col, dog_col, width=0.35):
    cats_data = cat_col.values
    cats_percent = ((cats_data / cats_data.sum()) * 100).round()
    dogs_data = dog_col.values
    dogs_percent = ((dogs_data / dogs_data.sum()) * 100).round()
    
    axes_labels = cat_col.index
    x = np.arange(len(axes_labels))
    cat = ax.bar(x - width/2, cats_percent, width, label='Cats', color='tomato')
    dog = ax.bar(x + width/2, dogs_percent, width, label='Dogs', color='lightseagreen')
    ax.set_ylabel('Percentage')
    ax.set_title(f'Percentage of {cat_col.name}: Cats vs Dogs')
    ax.set_xticks(x)
    ax.set_xticklabels(axes_labels, rotation=45)
    ax.legend(loc='upper center')
    autolabel(cat, ax)
    autolabel(dog, ax)