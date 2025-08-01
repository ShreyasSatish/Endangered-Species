import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def replace_na(species, desired_value):
    """Replace rows with NaN values with desired value, but only for ones that are key to our analysis"""
    
    cleaned_species = species.fillna(desired_value, inplace=False)
    return cleaned_species

def analyse_data(species):
    """Analyse the uncleaned data to see key information"""

    print()
    print(species.head())
    print(species.columns)
    column_names = species.columns
    print()
    for column in column_names:
        print(f"{column} Unique Values: {species[column].unique()}")
        print()
    print(species.dtypes)

def plot_data(species):
    """Plot desired variables and insights"""

    def plot_conservation_category(species):
        conservation_category_summary = species[species["conservation_status"] != "No Intervention"].groupby(["conservation_status", "category"])["scientific_name"].count().unstack()

        ax = conservation_category_summary.plot(kind="bar", figsize=(8, 6), stacked=True)
        ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(["Endangered", "In Recovery", "Species of Concern", "Threatened"], rotation=0)
        ax.set_xlabel("Conservation Status")
        ax.set_ylabel("Number of Species")
        ax.legend(frameon=True, title="Categories", draggable=True)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.set_title("Categories and their Conservation Status")
        manager = plt.get_current_fig_manager()
        manager.window.state("zoomed")
        plt.show()

    def plot_category_protection(species):
        species["is_protected"] = species.conservation_status != "No Intervention"
        category_counts = species.groupby(["category", "is_protected"]).scientific_name.nunique().reset_index().pivot(columns="is_protected", index="category", values="scientific_name").reset_index()
        category_counts.rename(columns={"category": "Category", False: "not_protected", True: "protected"}, inplace=True)
        
        ax = category_counts.plot(kind="bar", figsize=(8, 6), stacked=True)
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.set_xticklabels(["Amphibian", "Bird", "Fish", "Mammal", "Nonvascular Plant", "Reptile", "Vascular Plant"], rotation=0)
        ax.set_xlabel("Category")
        ax.set_ylabel("Number of Observations")
        ax.legend(frameon=True, draggable=True, title="Protection Status")
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.set_title("Animal Categories and their Protection Status")
        manager = plt.get_current_fig_manager()
        manager.window.state("zoomed")
        plt.show()
    
    plot_conservation_category(species)
    plot_category_protection(species)
    
    
def main():
    species = pd.read_csv("species_info.csv", encoding="utf-8")
    
    # analyse_data(species)
    # analyse_data(observations)

    species = replace_na(species, "No Intervention")
    
    plot_data(species)
    
    
if __name__ == "__main__":
    main()