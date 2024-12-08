import xml.etree.ElementTree as ET


class AppPageElement:

    def __init__(self, element: ET.Element | None):
        self.element = element
        self.exists: bool = self.element is not None
        self.attributes = self.element.attrib if self.exists else {}
        self.text: str = self.attributes.get('text')
        self.children: list['AppPageElement'] = self.__get_children()
        self.width, self.height = self.__get_size()
        self.x, self.y = self.__get_xy()
        self.xml: str = str(self)

    def get(self, key: str, value: str) -> "AppPageElement":
        element = None
        if self.exists:
            element = self.element.find(f'.//node[@{key}="{value}"]')
        return AppPageElement(element)

    def get_all(self, key: str, value: str) -> list["AppPageElement"]:
        if self.exists:
            elements = self.element.findall(f'.//node[@{key}="{value}"]')
            return [AppPageElement(element) for element in elements]
        return []

    def __get_children(self) -> list["AppPageElement"]:
        if self.exists:
            return [AppPageElement(child) for child in list(self.element)]
        return []

    def __get_xy(self) -> tuple[int, int] | tuple[None, None]:
        if bounds := self.attributes.get('bounds'):
            (coord_one_x, coord_one_y), *_ = self.__str_to_coords_list(bounds)
            return coord_one_x, coord_one_y
        return None, None

    def __get_size(self) -> tuple[int, int] | tuple[None, None]:
        if bounds := self.attributes.get('bounds'):
            (coord_one_x, coord_one_y), (coord_two_x, coord_two_y), *_ = self.__str_to_coords_list(bounds)
            return coord_two_x - coord_one_x, coord_two_y - coord_one_y
        return None, None

    def __str_to_coords_list(self, string: str) -> list[int, int] | list[list[int, int]]:
        coords_list = []
        for el in string.replace('][', '|').replace('[', '').replace(']', '').split('|'):
            coords_list.append([int(coords) for coords in el.split(',')])
        return coords_list

    def __str__(self) -> str:
        if self.element:
            return str(ET.tostring(self.element, encoding='utf-8'))
        return ''


class AppPageFabric:

    @classmethod
    def str_to_element(cls, xml_str: str) -> "AppPageElement":
        return AppPageElement(ET.fromstring(xml_str))

    @classmethod
    def file_to_element(cls, xml_file: str) -> "AppPageElement":
        with open(xml_file) as file:
            return cls.str_to_element(file.read())
