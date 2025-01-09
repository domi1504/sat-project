import matplotlib.pyplot as plt
import numpy as np
from sat.instance.instance import Instance


def visualize_formula(instance: Instance):
    plt.figure(figsize=(8, 8))
    plt.imshow(instance.bit_matrix, cmap='binary', interpolation='nearest')
    plt.xticks(np.arange(0.5, instance.bit_matrix.shape[1], 1), [])
    plt.yticks(np.arange(0.5, instance.bit_matrix.shape[0], 1), [])

    plt.grid(color='gray', linestyle='--', linewidth=1)

    # Draw vertical gridlines with alternating linestyle
    for i in range(instance.bit_matrix.shape[1]):
        linestyle = '-' if i % 2 == 0 else '--'
        plt.axvline(x=i - 0.5, color='gray', linestyle=linestyle, linewidth=1)

    # Add column labels
    column_labels = ['x{}'.format(i // 2 + 1) for i in range(instance.bit_matrix.shape[1])]
    for i in range(0, len(column_labels), 2):
        column_label = column_labels[i]
        plt.text(i, instance.bit_matrix.shape[0], column_label, ha='center')

    plt.show()


def visualize_two_formulas(instance_1: Instance, instance_2: Instance):

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 10))
    axes[0].imshow(instance_1.bit_matrix, cmap='binary', interpolation='nearest')
    axes[0].set_xticks(np.arange(0.5, instance_1.bit_matrix.shape[1], 1), [])
    axes[0].set_yticks(np.arange(0.5, instance_1.bit_matrix.shape[0], 1), [])
    axes[0].grid(color='gray', linestyle='--', linewidth=1)

    # Draw vertical gridlines with alternating linestyle
    for i in range(instance_1.bit_matrix.shape[1]):
        linestyle = '-' if i % 2 == 0 else '--'
        axes[0].axvline(x=i - 0.5, color='gray', linestyle=linestyle, linewidth=1)

    # Add column labels
    column_labels = ['x{}'.format(i // 2 + 1) for i in range(instance_1.bit_matrix.shape[1])]
    for i in range(0, len(column_labels), 2):
        column_label = column_labels[i]
        axes[0].text(i, instance_1.bit_matrix.shape[0], column_label, ha='center')

    # F2
    axes[1].imshow(instance_2.bit_matrix, cmap='binary', interpolation='nearest')
    axes[1].set_xticks(np.arange(0.5, instance_2.bit_matrix.shape[1], 1), [])
    axes[1].set_yticks(np.arange(0.5, instance_2.bit_matrix.shape[0], 1), [])
    axes[1].grid(color='gray', linestyle='--', linewidth=1)

    # Draw vertical gridlines with alternating linestyle
    for i in range(instance_2.bit_matrix.shape[1]):
        linestyle = '-' if i % 2 == 0 else '--'
        axes[1].axvline(x=i - 0.5, color='gray', linestyle=linestyle, linewidth=1)

    # Add column labels
    column_labels = ['x{}'.format(i // 2 + 1) for i in range(f2.shape[1])]
    for i in range(0, len(column_labels), 2):
        column_label = column_labels[i]
        axes[1].text(i, instance_2.bit_matrix.shape[0], column_label, ha='center')

    plt.show()

