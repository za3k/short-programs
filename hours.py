def midnight(days_offset=0):
	import time
	etime=int(time.time()) - time.altzone
	midnight = (etime - (etime % 86400)) + time.altzone + 86400*days_offset
	return midnight

def split_by_gap(gap, times):
	i = iter(times)
	first = last = i.next()
	for time in i:
		if time > last + gap:
			yield first, last	
			first = last = time
		else:
			last = time
	yield first, None
			
def readable_time(timestamp):
	from datetime import datetime
	dt = datetime.fromtimestamp(timestamp)
	return dt.strftime('%I:%M%p').lower()

def readable_date(timestamp):
	from datetime import datetime
	dt = datetime.fromtimestamp(timestamp)
	return dt.strftime('%D').lower()

if __name__ == "__main__":
	midnight = midnight()
	import fileinput
	lines = list(int(t) for t in fileinput.input() if t.strip() != '')
	for begin, end in split_by_gap(1*60*60, (time for time in lines if time > midnight)):
		if end is not None:
			print("{0} - {1}\t{2}".format(readable_time(begin), readable_time(end), readable_date(end)))
		else:
			end = lines[-1]
			print("{0} - ({1})\t{2}".format(readable_time(begin), readable_time(end), readable_date(end)))
