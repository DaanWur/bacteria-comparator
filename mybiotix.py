import ctypes
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
        self.venn_creator(first_attr_lis, second_attr_lis)

        f.close()

    def get_export_materials(self, f, attributes_lis: list, org_name):
        """Finds the substances the wanted bacteria products.
        in case the organism doesn't exist or doesn't produce a message pops and shut down.

        Args:
         f: file, the file where the bacteria info is held.
         attributes_lis: list, holds the substances that each bacteria export.
         org_name: str, the name of the organism.


        Returns:
             None.
        """
        appeared_counter = 0

        for line in f:
            # finds the line where the name is within the line
            if org_name in line and ("Production" in line or "production" in line):

                # split and check if the exact string exists
                substances = line.split("\t")
                if substances[2] == org_name:
                    line_of_bac1 = line
                    export_material = line_of_bac1.split()[0]
                    appeared_counter += 1
                    # takes the string at the first place
                    attributes_lis.append(export_material)
        if appeared_counter == 0:
            self.Mbox(
                "Organism not found",
                org_name + " does not exist in NJS16.txt or does not produce , sorry for the inconvenience.",
                1,
            )
            sys.exit()

    def Mbox(self, title: str, text: str, style: int):
        """Creates a message if the bacteria does not exits in the file.
        Args:
         title: str, title of the window.
         text: str, text of the window.
         style: int, number which sets the window style.


        Returns:
                Int.

        """
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

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
