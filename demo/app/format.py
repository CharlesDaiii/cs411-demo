
def format_stock_data(results):
	index = 0
	list = []
	for i in results:
		index+=1
		item = {
			"id":index,
			"ticker":i[0],
			"company_name":i[3],
			"fiftyTwoWeekLow":i[4],
			"fiftyTwoWeekHigh":i[5],
			"forwardPE":i[6],
			"trailingPE":i[7],
            "positive":i[8],
			"negative":i[9],
			"overall":i[10]
		}
		list.append(item)
	return list

def format_company_data(results):
	list = []
	for i in results:
		if len(i) < 5:
			continue
		item = {
			"ticker":i[0],
			"company_name":i[1],
			"category":i[2],
			"region":i[3],
			"CEO_Name":i[4]
		}
		list.append(item)
	return list

def format_toppick_data(results):
	list = []
	for i in results:
		item = {
			"category":i[0],
			"count_status":i[1],
			"avg_sentiment":i[2],
			"avg_PE":i[3]
		}
		list.append(item)
	return list
