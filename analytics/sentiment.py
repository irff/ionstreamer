import csv, collections, re, string, json

freq = collections.defaultdict(int)

with open("../../classified") as jsonfile:
  tweets = json.load(jsonfile)
  for line in [x for x in tweets if x['class'] == 'positive']:
    # text = line[3]
    # text = re.sub(r"https?://t\.co/\w{10}", " ", text)
    # text = re.sub(r"&\w{1,5};", " ", text)
    # text = re.sub(r"[\.,|():?/;~\-\\\"*']+", " ", text)
    # for word in filter(lambda x: x in string.printable, text).lower().split():
    #   freq[word] += 1
    # print "@%s: %s" % (line['user']['screen_name'], line['text'])
    sumber = line['retweeted_status']['user']['screen_name'] if 'retweeted_status' in line else line['user']['screen_name']
    freq[sumber] += 1

# items = freq.items()
# items.sort(key = lambda (x, y): y, reverse = True)

# for i in items: print i

# for k in freq:
#   print k, freq[k]