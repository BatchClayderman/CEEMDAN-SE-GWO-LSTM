import os
from snownlp import SnowNLP
from wordcloud import WordCloud
from matplotlib import pyplot as plt
os.chdir(os.path.abspath(os.path.dirname(__file__))) # cd into program's locating folder


def get_cut_list(content): # get the list of cut
	s = SnowNLP(content)
	cut = [tag[0] for tag in list(s.tags)]
	return cut

def get_sorted_dicts(cut_list, reverse = True): # print the count of every word
	cut_dicts = {}
	for word in cut_list:
		if word not in cut_dicts:
			cut_dicts.setdefault(word, cut_list.count(word))
	cut_tuples = sorted(cut_dicts.items(), key = lambda x:x[1], reverse = reverse)
	return cut_tuples

def dump_sorted_tuples(sorted_tuples, filepath = None, encoding = "utf-8"): # dump the sorted results
	if filepath is None:
		print(sorted_tuples)
	else:
		to_write = []
		for item in sorted_tuples:
			to_write.append("{0}\t{1}".format(item[0], item[1]))
		try:
			with open(filepath, "w", encoding = encoding) as f:
				f.write("\n".join(to_write))
		except Exception as e:
			print(e)

def draw_wordcloud(cut_list, width = 2000, height = 1000, dpi = 3000, bg_color = "white", filepath = None): # draw wordcloud
	wordcloud = WordCloud(width = width, height = height, background_color = bg_color, collocations = False).generate(" ".join(cut_list))
	plt.imshow(wordcloud, interpolation = "bilinear")
	plt.axis("off")
	plt.rcParams["figure.dpi"] = dpi
	plt.rcParams["savefig.dpi"] = dpi
	if filepath is None:
		plt.show()
	else:
		plt.savefig(filepath)
	plt.close()



if __name__ == "__main__":
	content = """Climate change presents a massive threat to life as we know it. To mitigate the effects of climate change, we need to take drastic action to reduce the amount of greenhouse gases in the atmosphere. Simply reducing greenhouse gas emissions is not enough. We need to make efforts to enhance our stocks of carbon dioxide sequestered out of the atmosphere by the biosphere or by mechanical means. This process is called carbon sequestration. The biosphere sequesters carbon dioxide in plants (especially large plants like trees), soils, and water environments. Thus, forests are integral to any climate change mitigation effort. 
Forests sequester carbon dioxide in living plants and in the products created from their trees including furniture, lumber, plywood, paper, and other wood products. These forest products sequester carbon dioxide for their lifespan. Some products have a short lifespan, while others have a lifespan that may exceed that of the trees from which they are produced. The carbon sequestered in some forest products combined with the carbon sequestered because of the regrowth of younger forests has the potential to allow for more carbon sequestration over time when compared to the carbon sequestration benefits of not cutting forests at all. 
At the global level, forest management strategies that include appropriate harvesting can be beneficial for carbon sequestration. However, overharvesting can limit carbon sequestration. Forest managers must find a balance between the value of forest products derived from harvesting and the value of allowing the forest to continue growing and sequestering carbon as living trees. In doing so, they must consider many factors such as age and types of trees, geography, topography, and benefits and lifespan of forest products. 
The concerns of forest managers are not limited to carbon sequestration and forest products. They must make forest management decisions based on the many ways their forest is valued. These may include, but are not limited to, potential carbon sequestration, conservation and biodiversity aspects, recreational uses, and cultural considerations. """
	cut = get_cut_list(content)
	print(cut)
	dump_sorted_tuples(get_sorted_dicts(cut, True), "splitter.txt")
	draw_wordcloud(cut, filepath = "splitter.png")