import pygsheets

class GSheetsWriter:

	def __init__(self, df, workbook_name):
		self.df = df
		self.workbook_name = workbook_name

	def connect_to_workbook(self):
		self.connector = pygsheets.authorize(service_file='SDDSProject-3c298c43dcbd.json')
		self.workbook = self.connector.open(self.workbook_name)
		#self.sheet = self.workbook

	def write_df_to_sheet(self, sheet_idx):
		self.sheet = self.workbook[sheet_idx]
		self.sheet.set_dataframe(self.df, (1,1))






'''
gc = pygsheets.authorize(service_file='SDDSProject-3c298c43dcbd.json')
sh = gc.open('Covid19PA_DEV')
wks = sh[0]
wks.set_dataframe(df, (1,1))

'''