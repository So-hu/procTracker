import os

def printTable(table):
	width = [max(len(v) for v in col) for col in zip(*table)]
	for n, line in enumerate(table):
		if n == 0:
			print " ",
		else:
			print n,
		i = 0
		for s in line:
			print s, " "*(width[i] - len(s)),
			i+= 1
		print

def pidExists(pid):
	process = {p for p in os.listdir('/proc') if p.isdigit()}
	if pid in process:
		return True
	else:
		return False

def listProcess():
	process = [p for p in os.listdir('/proc') if p.isdigit()]
	res_table = [["PID", "EXE", "STATUS", "TTY"]]

	for pid in process:
		p_info = open(os.path.join('/proc', pid, 'stat'))
		v = p_info.readline()
		res = v.split(' ')
		p_info.close()
		res_table.append([res[0], res[1], res[2], res[6]])
	printTable(res_table)

def getThread(pid):	
	ploc = os.path.join('/proc', pid, 'task')
	if pidExists(pid):
		threads = [t for t in os.listdir(ploc) if t.isdigit()]
		print "ID"
		for t in threads:
			print t
	else:
		print "process " + pid + " does not exist"

def getModules():
	table = [["MODULE", "MEM", "USER"]]
	mod_file = open('/proc/modules', 'r')
	for line in mod_file:
		temp = line.split()
		table.append[temp[0], temp[1], temp[2]]
	printTable(table)

def mapPages(pid):
	if pidExists(pid):
		path = os.path.join('/proc', pid, 'maps')
		mem = open(path, 'r')
		table = [["address", "perms", "offset", "dev", "inode", "path"]]
		for line in mem:
			values = line.split()
			if len(values) == 5:
				values.append("")
			table.append(values)
		printTable(table)
	else:
		print "Process " + pid + " does not exist"

def instructions():
	print "'lp' -- List processes on the system \n'lt [pid]' -- list threads in designated process \n'lm' -- List loaded modules \n'mp [pid]' -- Memory map for executeables in the process \n'exit' -- end the script"
def main():
	print "Welcome to process manager. Type 'help' to get list of available commands"
	while(True):
		user_input = raw_input()
		cmd = user_input.split(" ")
		if cmd[0] == 'exit':
			return 0
		elif cmd[0] == 'help':
			instructions()
		elif cmd[0] == 'lp':
			listProcess()
		elif cmd[0] == 'lt' and len(cmd) == 2:
			getThread(cmd[1])
		elif cmd[0] == 'lm':
			getModules()
		elif cmd[0] == 'mp' and len(cmd) == 2:
			mapPages(cmd[1]) 
		else:
			print "Invalid command. Type 'help' to get list of available commands"
if __name__ == "__main__":
	main()
