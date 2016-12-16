'''

2016-10-21

对应  space.py 代码

将此大程序拆分成几个小程序

'''


#=====================【 结 果 存 储 】==================================
def write(dictionary,filename,conclusion):

	file = open(filename,'w')
	file.truncate()
	for key in dictionary:
		srt = key + ":" + str(dictionary[key])
		file.write(srt)
		file.write("\n")
	file.write(conclusion)

