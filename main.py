import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


class SalesDataAnalyzer:
    def __init__(self):
        self.data = None
        self.last_fig = None   
 
    def get_choice(self, prompt="Enter your choice: "):
        """Safely read an integer. Returns None if the user types a non-number."""
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number only.")
            return None

    def column_exists(self, col):
        if col in self.data.columns:
            return True
        print(f"Column '{col}' not found. Available columns: {list(self.data.columns)}")
        return False

    def numeric_ok(self, col):
        """Check that a column holds numbers (needed for average, line, scatter, histogram, stack plot)."""
        if pd.api.types.is_numeric_dtype(self.data[col]):
            return True
        numeric_cols = list(self.data.select_dtypes(include="number").columns)
        print(f"'{col}' is a text column, so it cannot be used here. Please choose a numeric column.")
        print(f"Numeric columns: {numeric_cols}")
        return False

    
    def load_data(self):
        print("Load data")
        input_path = input("Enter the path of the csv file: ").strip().strip('"')
        try:
            self.data = pd.read_csv(input_path)
            print("Data loaded successfully!")
        except FileNotFoundError:
            print("File not found. Please check the path and try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

   
    def explore(self):
        if self.data is None:
            print("No data available!")
            return
        print("1. Display first 5 rows")
        print("2. Display last 5 rows")
        print("3. Display column names")
        print("4. Display data types")
        print("5. Display basic info")
        choice = self.get_choice()
        if choice == 1:
            print(self.data.head())
        elif choice == 2:
            print(self.data.tail())
        elif choice == 3:
            print(self.data.columns)        
        elif choice == 4:
            print(self.data.dtypes)           
        elif choice == 5:
            self.data.info()                  
        else:
            print("Invalid choice. Please try again.")

  
    def data_frame_operations(self):
        if self.data is None:
            print("No data available!")
            return
        print("1. Select specific columns")
        print("2. Filter rows based on conditions")
        print("3. Sort data by column")
        print("4. Group data and perform aggregations")
        choice = self.get_choice()
        try:
            if choice == 1:
                columns = [c.strip() for c in input("Enter column names separated by commas: ").split(",")]
                print(self.data[columns])
            elif choice == 2:
                condition = input("Enter the condition (e.g., Sales > 500 or Region == 'East'): ")
                print(self.data.query(condition))
            elif choice == 3:
                column_name = input("Enter the column name to sort by: ").strip()
                if self.column_exists(column_name):
                    print(self.data.sort_values(by=column_name))
            elif choice == 4:
                group_column = input("Enter the column name to group by: ").strip()
                agg_column = input("Enter the numeric column to aggregate: ").strip()
                if self.column_exists(group_column) and self.column_exists(agg_column):
                    print(self.data.groupby(group_column)[agg_column].mean())
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:              
            print(f"Error: {e}")

   
    def handle_missing_data(self):
        if self.data is None:
            print("No data available!")
            return
        print("Handle Missing Data")
        print("1. Display rows with missing values")
        print("2. Fill missing values with mean")
        print("3. Drop rows with missing values")
        print("4. Replace missing values with a specific value")
        choice = self.get_choice()

        if choice == 1:
            print("Rows with missing values:")
            print(self.data[self.data.isnull().any(axis=1)])
        elif choice == 2:
            self.data = self.data.fillna(self.data.mean(numeric_only=True))
            print("Missing values filled with mean.")
        elif choice == 3:
            self.data = self.data.dropna()
            print("Rows with missing values dropped.")
        elif choice == 4:
            value = input("Enter the value to replace missing data: ")
            try:
                value = float(value)         
            except ValueError:
                pass
            self.data = self.data.fillna(value)
            print("Missing values replaced successfully.")
        else:
            print("Invalid choice!")

    
    def data_descriptive_statics(self):      
        if self.data is None:
            print("No data available!")
            return
        print("Descriptive Statistics")
        print("1. Summary Statistics")
        print("2. Correlation Matrix")
        print("3. Value Counts for a Column")
        print("4. Unique Values for a Column")
        print("5. Frequency Table")
        choice = self.get_choice()

        if choice == 1:
            print(self.data.describe(include="all"))
        elif choice == 2:
            print(self.data.corr(numeric_only=True))   
        elif choice in (3, 4, 5):
            col = input("Enter column name: ").strip()
            if self.column_exists(col):
                if choice == 3:
                    print(self.data[col].value_counts())
                elif choice == 4:
                    print(self.data[col].unique())
                else:
                    print(self.data[col].value_counts().rename("Frequency"))
        else:
            print("Invalid choice!")

  
    def data_visualization(self):
        if self.data is None:
            print("No data available!")
            return
        print("1. Bar Plot")
        print("2. Line Plot")
        print("3. Scatter Plot")
        print("4. Pie Chart")
        print("5. Histogram")
        print("6. Stack Plot")
        choice = self.get_choice()
        if choice not in range(1, 7):
            print("Invalid choice!")
            return

        try:
            fig = plt.figure(figsize=(9, 5))
            if choice in (1, 2, 3):
                x = input("Enter X-axis column name: ").strip()
                y = input("Enter Y-axis column name: ").strip()
                if not (self.column_exists(x) and self.column_exists(y)):
                    plt.close(fig)
                    return
               
                text_bar = choice == 1 and not pd.api.types.is_numeric_dtype(self.data[y])
                if not text_bar and not self.numeric_ok(y):
                    plt.close(fig)
                    return
                if choice == 3 and not self.numeric_ok(x):
                    plt.close(fig)
                    return
                if choice == 1:
                   
                    if text_bar:
                        pd.crosstab(self.data[x], self.data[y]).plot(kind="bar", stacked=True, ax=plt.gca())
                        plt.ylabel("Number of orders")
                        plt.legend(title=y)
                        plt.xticks(rotation=60, ha="right")
                    else:
                        self.data.groupby(x)[y].mean().plot(kind="bar", ax=plt.gca())
                        plt.ylabel(f"Average {y}")
                    plt.title("Bar Plot")
                elif choice == 2:
                    self.data.plot(kind="line", x=x, y=y, ax=plt.gca())
                    plt.title("Line Plot")
                else:
                    plt.scatter(self.data[x], self.data[y])
                    plt.xlabel(x)
                    plt.ylabel(y)
                    plt.title("Scatter Plot")
            elif choice == 4:
                col = input("Enter column name: ").strip()
                if not self.column_exists(col):
                    plt.close(fig)
                    return
                self.data[col].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=plt.gca())
                plt.title("Pie Chart")
                plt.ylabel("")
            elif choice == 5:
                col = input("Enter column name: ").strip()
                if not self.column_exists(col):
                    plt.close(fig)
                    return
                if not self.numeric_ok(col):
                    plt.close(fig)
                    return
                plt.hist(self.data[col].dropna(), bins=10)
                plt.xlabel(col)
                plt.ylabel("Frequency")
                plt.title("Histogram")
            elif choice == 6:
                col1 = input("Enter first column name: ").strip()
                col2 = input("Enter second column name: ").strip()
                if not (self.column_exists(col1) and self.column_exists(col2)):
                    plt.close(fig)
                    return
                if not (self.numeric_ok(col1) and self.numeric_ok(col2)):
                    plt.close(fig)
                    return
                plt.stackplot(
                    range(len(self.data)),
                    self.data[col1].fillna(0),  
                    self.data[col2].fillna(0),
                    labels=[col1, col2],
                )
                plt.legend()
                plt.title("Stack Plot")

            plt.tight_layout()
            self.last_fig = fig               
            plt.show()
        except Exception as e:
            plt.close("all")
            print(f"Could not draw the plot: {e}")

    
    def save_visualization(self):
        if self.last_fig is None:               
            print("No visualization to save. Create a plot first (option 6).")
            return
        print("Save Visualization")
        print("1. Save as PNG")
        print("2. Save as JPG")
        print("3. Save as PDF")
        choice = self.get_choice()
        formats = {1: "png", 2: "jpg", 3: "pdf"}
        if choice in formats:
            filename = input("Enter file name: ").strip()
            ext = formats[choice]
            try:
                self.last_fig.savefig(f"{filename}.{ext}", bbox_inches="tight")
                print(f"Visualization saved as {filename}.{ext} successfully!")
            except Exception as e:
                print(f"Could not save: {e}")
        else:
            print("Invalid choice!")

    def main_menu(self):
        while True:
            print()
            print(" Data Analysis & Visualization Program ")
            print("1. Load Dataset")
            print("2. Explore Data")
            print("3. Perform DataFrame Operations")
            print("4. Handle Missing Data")
            print("5. Generate Descriptive Statistics")
            print("6. Data Visualization")
            print("7. Save Visualization")
            print("8. Exit")
            choice = self.get_choice("Enter Your Choice: ")
            if choice is None:
                continue
            if choice == 1:
                self.load_data()
            elif choice == 2:
                self.explore()
            elif choice == 3:
                self.data_frame_operations()
            elif choice == 4:
                self.handle_missing_data()
            elif choice == 5:
                self.data_descriptive_statics()
            elif choice == 6:
                self.data_visualization()
            elif choice == 7:
                self.save_visualization()
            elif choice == 8:
                print("Exiting the program")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    obj = SalesDataAnalyzer()
    obj.main_menu()