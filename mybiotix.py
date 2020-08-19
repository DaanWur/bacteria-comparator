import sys
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
        for line in f:
            if self.first_org_name in line and (
                    "Production" in line or "production" in line
            ):
                line_of_bac1 = line
                export_material_1 = line_of_bac1.split()[0]

                # takes the string at the first place
                first_attr_lis.append(
                    export_material_1
                )  # appending the found export materials to a list
            if self.second_org_name in line and (
                    "Production" in line or "production" in line
            ):
                line_of_bac2 = line
                export_material_2 = line_of_bac2.split()[0]
                second_attr_lis.append(export_material_2)
        f.close()
        self.venn_creator(first_attr_lis, second_attr_lis)

    def venn_creator(self, first_lis: list, second_lis: list) -> None:
        """Creates the venn diagram.

        Args:
            first_lis: list, all substances of the first germ.
            second_lis: list, all substances of the second germ.

        Returns:
                None.
        """

        v = vplt.venn2(
            subsets=(set(first_lis), set(second_lis)),
            set_labels=(self.first_org_name, self.second_org_name),
            set_colors=("green", "blue"),
        )
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
        for key in list_of_bacterias.index:
            if key == germ_id:
                org_name = list_of_bacterias["Organism"][key]
                return org_name

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
