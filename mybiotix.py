import sys
import matplotlib
import pandas
import matplotlib_venn as vplt
from matplotlib import pyplot as plt


class Parameters:
    def __init__(self):
        """Initializes with default path value like below (change the path to the one needed).

        Args:
            None.

        """
        self.first_org_name = None
        self.second_org_name = None
        self.file_path = r"C:\Users\Daniel\Desktop\mybiotix submmission\NJS16.txt"

    def read_info_from_file(self) -> None:
        """Finds the needed bacterias information.

         Args:
             None.

         Returns:
             None.
         """
        f = open(self.file_path, "rt")

        # list of first organism
        first_attr_lis = []

        # list of second organism
        second_attr_lis = []

        self.get_export_materials(f, first_attr_lis, self.first_org_name)
        f.seek(0)
        self.get_export_materials(f, second_attr_lis, self.second_org_name)
        f.close()
        self.venn_creator(first_attr_lis, second_attr_lis)

    def get_export_materials(self, f, attributes_lis: list, org_name):
        """Finds the substances the wanted bacteria products.

        Args:
         f: file, the file where the bacteria info is held.
         attributes_lis: list, holds the substances that each bacteria export.
         org_name: str, the name of the organism.


        Returns:
             None.
        """

        for line in f:

            if org_name in line and ("Production" in line or "production" in line):
                line_of_bac1 = line
                export_material = line_of_bac1.split()[0]

                # takes the string at the first place
                attributes_lis.append(export_material)
        f.seek(0)
        if org_name not in f.read():
            print(org_name)
            print("Organism not found")

    def venn_creator(self, first_lis: list, second_lis: list) -> None:
        """Creates a venn diagram that shows what substances each organism produce
            and which substances are mutual.

        Args:
            first_lis: list, all substances of the first germ.
            second_lis: list, all substances of the second germ.

        Returns:
                None.
        """
        first_set = set(first_lis)
        second_set = set(second_lis)
        v = vplt.venn2(
            subsets=(first_set, second_set),
            set_labels=(self.first_org_name, self.second_org_name),
            set_colors=("green", "blue"),
        )
        # changing the labels
        v.get_label_by_id("100").set_text(str(len(first_lis)))
        v.get_label_by_id("010").set_text(str(len(second_lis)))
        plt.title("Produced substances comparison")
        matplotlib.pyplot.savefig("Bacterias.png")
        plt.show()

    # loops through the excel file and finds the matching bacteria
    def find_germs(self, germ_id: int) -> str:
        """ Find the germs name from the excel file using the id.

        Args:
         germ_id: int, id of the germ in the excel file.


        Returns:
              org_name: str, name of the organism.
        """
        list_of_bacterias = pandas.read_excel(r"organisms.xlsx")
        return list_of_bacterias["Organism"][germ_id]

    def main(self):

        # first num from user
        first_str = sys.argv[1]

        # conversion of str to int
        first_num = int(first_str, 10)

        # second num from user
        second_str = sys.argv[2]

        # conversion of str to int
        second_num = int(second_str, 10)
        self.first_org_name = self.find_germs(first_num - 1)
        self.second_org_name = self.find_germs(second_num - 1)
        self.read_info_from_file()


if __name__ == "__main__":
    obj = Parameters()
    obj.main()
