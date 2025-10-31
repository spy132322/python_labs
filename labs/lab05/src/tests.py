from libs.conver import *

print("Тестим на готовых файлах из лабы")
json_to_csv(json_path="test_files/ready/people.json", csv_path="output/ready/people_out.csv")
csv_to_json(csv_path="test_files/ready/people.csv", json_path="output/ready/people_out.json")
csv_to_xlsx(csv_path="test_files/ready/cities.csv", xlsx_path="output/ready/city_out.xlsx")

print("Тестим мои кейсы")
json_to_csv(json_path="test_files/my/100%_original.json", csv_path="output/my/people_out.csv")
csv_to_json(csv_path="test_files/my/100%_original.csv", json_path="output/my/people_out.json")
csv_to_xlsx(csv_path="test_files/my/100%_original.csv", xlsx_path="output/my/city_out.xlsx")