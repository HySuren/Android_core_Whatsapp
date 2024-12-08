import os
import subprocess
import uiautomator2 as u2


class WaAnalyzer:
    """ Сравнивает две файлы .db sqlite3 в указанных директориях.
        Директории указывать с "/" на конце
    """
    def __init__(self, first_path=None, second_path=None):
        self.first_path = first_path
        self.second_path = second_path
        self.separator = "-" * 50

    def show_diff(self, out_in_file=False):
        data = ""
        files = self.get_db_files()

        for file in files:
            data += f'{self.separator}\nINFO FOR {file}\n'
            answer = subprocess.run(f"sqldiff {self.first_path + file} {self.second_path + file}", shell=True, capture_output=True, text=True).stdout
            data += f"{answer if answer else 'NONE DIFF'}\n{self.separator}\n"

        data += "END ANALYZE\n"

        if out_in_file:
            with open(f'analyzer_output_{self.first_path[:-1]}_{self.second_path[:-1]}.txt', 'w') as f:
                f.write(data)
        else:
            return data

    def get_db_files(self):
        data = []
        for filename in os.listdir(self.first_path):
            if filename.endswith('.db'):
                data.append(filename)
        return data

    def generate_output_by_device(self):
        d = u2.connect()
        folder_path = f"{d.serial}"
        file_list = os.listdir(folder_path)
        if not file_list:
            raise Exception("Нет баз для анализа")
        count_files = len(file_list)
        for num in sorted([int(i) for i in file_list]):
            if num < count_files:
                self.first_path, self.second_path = f'{folder_path}/{num}/', f'{folder_path}/{num + 1}/'
                data = self.show_diff()
                with open(f'{folder_path}/{num}_to_{num + 1}', 'w') as f:
                    f.write(data)


if __name__ == "__main__":
    analyzer = WaAnalyzer()
    analyzer.generate_output_by_device()

