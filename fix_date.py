import csv
from datetime import datetime
from os import listdir

datetime_format = '%Y-%m-%d %H:%M:%S.%f'

data_from = './data'
data_to = './dist'

def comma_float(num):
	return str(num).replace('.', ',')

for file_name in listdir('./data'):

	with open('{}/{}'.format(data_from, file_name), 'r') as fr:
		csvreader = csv.reader(fr, delimiter=';')

		fw = open('{}/{}'.format(data_to, file_name), 'w', newline='')
		csvwriter = csv.writer(fw, delimiter=';')

		is_first_row = True
		is_second_row = True
		first_timestamp = None
		for row in csvreader:
			if is_first_row:
				is_first_row = False
				csvwriter.writerow(row)
				continue


			timestamp = datetime.strptime(row[0], datetime_format).timestamp()

			if is_second_row:
				is_second_row = False
				first_timestamp = timestamp
				csvwriter.writerow([0] + row[1:])
			else:
				csvwriter.writerow([comma_float(timestamp - first_timestamp)] + row[1:])

		fw.close()
