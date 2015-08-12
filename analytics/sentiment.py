import csv, collections, re, string

freq = collections.defaultdict(int)

with open("../../pilkada-bpjs.csv") as csvfile:
  dt = csv.reader(csvfile)
  for line in dt:
    text = line[3]
    text = re.sub(r"https?://t\.co/\w{10}", " ", text)
    text = re.sub(r"&\w{1,5};", " ", text)
    text = re.sub(r"[\.,|():?/;~\-\\\"*']+", " ", text)
    for word in filter(lambda x: x in string.printable, text).lower().split():
      freq[word] += 1

items = freq.items()
items.sort(key = lambda (x, y): y, reverse = True)

for i in items: print i
