""" Solution to assignment "Statistics", BSA """

# author:   Thomas Haslwanter
# date:     Dec-2024


# Import the standard packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import pingouin as pg
import seaborn as sns


def get_and_analyze_data() -> pd.DataFrame:
    """ Exercise 1: Analyze data

    Returns
    -------
    df : the columns ['tirol', 'vienna'] contain the corresponding data
    """

    # Generate the data
    rng = np.random.default_rng(12345)
    num_subjects = 100
    tirol = rng.normal(loc=60, scale=8, size=num_subjects)
    vienna = rng.normal(loc=55, scale=10, size=num_subjects)
    vienna_after = vienna + rng.normal(loc=0.25, scale=1.0, size=num_subjects)

    # I like to store the data in pandas DataFrames, since it a) groups them,
    # and b) it gives me sensible names for the variables.
    # Alternatively, one could put all the data into a numpy array.
    df = pd.DataFrame({'tirol': tirol,
                      'vienna': vienna,
                      'vienna_after': vienna_after})

    # Analyze the data: calculate mean, std, and sem
    # First for all data, and then for a small subset
    analysis = []   # Start with an empty list, and gradually append new values
    for data in [df.tirol, df.tirol[:10]]:
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        sem = stats.sem(data)
        # This would be equivalent to
        # sem = np.std(data, ddof=1) / np.sqrt(len(data))
        analysis.append([mean, std, sem])

    # Put them in a pandas DataFrame, so that it is simpler to understand
    results = np.array(analysis).T
    data_stats = pd.DataFrame(data=results, columns=['tirol', 'tirol_10'],
                              index=['mean', 'std', 'sem'])

    # Show the data - readily formatted!
    print(data_stats)

    return df


def plot_data(df: pd.DataFrame) -> None:
    """ Exercise 2: Plot data, with errorbars

    Parameters
    ----------
    df : data for ['tirol', 'vienna', 'vienna_after']
    """

    # Find the required parameters
    mean_tirol = np.mean(df.tirol)
    std_tirol = np.std(df.tirol, ddof=1)
    sem_tirol = stats.sem(df.tirol)

    mean_vienna = np.mean(df.vienna)
    std_vienna = np.std(df.vienna, ddof=1)
    sem_vienna = stats.sem(df.vienna)

    # Show errorbars, first for the SD ...
    fig, axs = plt.subplots(1,2)

    axs[0].errorbar([1, 2], [mean_tirol, mean_vienna],
                    yerr=[std_tirol, std_vienna],
                   lw=0, elinewidth=2, capsize=5, marker='o')

    # Format the plot
    axs[0].set_xlim([0.5, 2.5])
    axs[0].set_ylim([40, 70])
    axs[0].set_xticks([1, 2])
    axs[0].set_xticklabels(['Tirol', 'Vienna'])
    axs[0].set_title('Errorbars: SD')
    axs[0].set_ylabel('Weight [kg]')

    # ... and then for the SEM
    axs[1].errorbar([1,2], [mean_tirol, mean_vienna],
                    yerr=[sem_tirol, sem_vienna],
                    lw=0, elinewidth=2, capsize=5, marker='o')

    axs[1].set_xlim([0.5, 2.5])
    axs[1].set_ylim([40, 70])
    axs[1].set_xticks([1, 2])
    axs[1].set_xticklabels(['Tirol', 'Vienna'])
    axs[1].set_title('Errorbars: SEM')
    axs[1].set_ylabel('Weight [kg]')

    plt.tight_layout()  # Helps to get nicely positioned labels
    plt.show()


def boxplots(df: pd.DataFrame) -> None:
    """ Exercise 3: Boxplots

    Parameters
    ----------
    df : data for ['tirol', 'vienna', 'vienna_after']

    Getting the data in shape with seaborn is a bit tricky, but seaborn gives
    you more formatting options.
    """


    fig, axs = plt.subplots(1, 2)

    use_seaborn = True

    if use_seaborn:
        # Using seaborn.boxplot

        # First, reshape the data into the format required by seaborn
        df2 = df.transpose().stack().reset_index()
        df2 = df2.drop('level_1', axis=1)
        df2.columns = ['type', 'value']
        # That returns data in the following format:
        #     type      value
        # 0  tirol  48.609400
        # 1  tirol  70.109828
        # 2  tirol  53.034706
        # 3  tirol  57.926614
        # 4  tirol  59.397254
        sns.boxplot(data=df2, x='type', y='value', ax=axs[0])
        axs[0].grid(True)

    else:
        # Tirol & Vienna
        # The using the "boxplot" method of pandas DataFrames has the advantage
        # that the labels are automatically added on the x-axis
        df[['tirol', 'vienna']].boxplot(ax=axs[0])
        axs[0].set_ylabel('Weight [kg]')
            
        
    # 1000 random points, here with matplotlib
    data = np.random.randn(1000)*12+85
    axs[1].boxplot(data, sym='*')
    axs[1].set_title('Random Data')

    plt.show()


def compare_groups(df: pd.DataFrame) -> None:
    """ Exercise 4: Compare groups

     Parameters
     ----------
    df : data for ['tirol', 'vienna', 'vienna_after']
    """

    print('Comparing Groups -----------------------')

    # Comparison of independent groups
    # Statistical tests can be taken from either 'scipy.stats', or from the
    # package 'pengouin'. The latter provides a nicer layout, and more
    # comfortable data management.
    result = pg.ttest(df.tirol, df.vienna)
    p = result['p-val']['T-test']
    significant = 0.05
    if p < significant:
        print('There is a significant difference between Tirol and Vienna, ' +
                f'with p = {p:4.2e}.')
    else:
        print('No significant difference between Tirol and Vienna')

    # Pre/post comparisons
    result = pg.ttest(df.vienna, df.vienna_after, paired=True)
    p = result['p-val']['T-test']
    if p < significant:
        print('The Viennese chocolate diet causes significant weight change, ' +
                f'with p = {p:4.2e} .')
    else:
        print('The Viennese chocolate diet causes NO significant weight change')


if __name__ == '__main__':
    data = get_and_analyze_data()   # Exercise 1
    # plot_data(data)                 # Exercise 2
    boxplots(data)                  # Exercise 3
    # compare_groups(data)            # Exercise 4
