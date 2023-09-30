import csv
from datetime import datetime


class Create_CSV_File():
    def __init__(self, all: dict):
        self.all = all

    def create_csv(self):
        vremya = datetime.now()
        with open(f"Output_file_{vremya.strftime('%H-%M-%S')}.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for key, value in self.all.items():
                row = []
                if len(value) == 1:
                    row = [key] if key[-1] != " " else [key[:-1:]]
                    for inner_list in value[0]:
                        if isinstance(inner_list, datetime):
                            tt = inner_list.strftime('%d.%m.%Y')
                            row.append(tt)
                        else:
                            row.append(inner_list)
                    writer.writerow(row)
                elif len(value) > 1:
                    for x in range(len(value)):
                        row = [key] if key[-1] != " " else [key[:-1:]]
                        for inner_list in value[x]:
                            if isinstance(inner_list, datetime):
                                tt = inner_list.strftime('%d.%m.%Y')
                                row.append(tt)
                            else:
                                row.append(inner_list)
                        writer.writerow(row)
                else:
                    row = [key] if key[-1] != " " else [key[:-1:]]
                    row[0] = row[0] + ",,"
                    writer.writerow(row)

