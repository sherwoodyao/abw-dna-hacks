from nupack import *
import matplotlib.pyplot as plt
import pandas as pd

# Function from nupack that compares 2 strands
def compare(strand1, strand2, c1, c2, plot=False, save_plot=False, save_results=False,
plot_name='my-figure.png', results_name='tube-results.txt'):
	# specify strands
	a = Strand(strand1, name='a')
	b = Strand(strand2, name='b')
	c = Complex([a, b], name='c')
	storage = []

	# specify tubes
	t1 = Tube({a: c1, b: c2}, complexes=SetSpec(max_size=2), name='t1')
	# t2 = Tube({a: 1e-8, b: 1e-9}, complexes=SetSpec(include=[c]), name='t2')
	
	# analyze tubes
	model1 = Model(material='dna')
	tube_results = tube_analysis([t1], model=model1, compute=['pfunc', 'pairs', 'mfe', 		
	'sample', 'subopt'], options={'num_sample': 2, 'energy_gap': 0.5})
	# print(tube_results)
	for my_complex, conc in tube_results.tubes[t1].complex_concentrations.items():
		if my_complex.name == "(a+b)" or my_complex.name == "(b+a)":
    			storage.append([my_complex.name, conc])
    		
    	# Saves results
	if save_results:
		tube_results.save_text(results_name)
	# print(storage)
	
	# If selected prints tube results
	if plot:
		plt.imshow(tube_results[c].pairs.to_array())
		plt.xlabel('Base index')
		plt.ylabel('Base index')
		plt.title('Pair probabilities for complex c')
		plt.colorbar()
		plt.clim(0, 1)
		if save_plot:
			plt.savefig(plot_name)
			
	return storage[0][1]

# Gets all possible strands from big strand (unmatched)
def matcher(i, length, big_strand):
	ret_list = []
	END = len(big_strand)
	if i <= END-length:
		tryString = big_strand[i:i+length]

	if i > END-length:
		tryString = big_strand[i:] + big_strand[0:length-END+i]

	return tryString
	
# Converts strands from matcher to link and reverses them
def reverse_comp(strand):
	new = ''
	for x in list(strand):
		if x in dict1.keys():
			new += dict1[x]
	# reversed_string = "".join(list(grapheme.graphemes(input_string))[::-1])
	return new[::-1]
	
	
def baseFilter(input_list, bases, selection_mode):
	'''
	selection_mode: begin,end,begin/end, contain
	
	'''
	ret_list = []
	for z in input_list:

		sequence = z[0]
		if selection_mode != "contain":

			if sequence[0] in bases and "begin" == selection_mode:
				ret_list.append(z)

				
			if sequence[-1] in bases and "end" == selection_mode:
				ret_list.append(z)
				
			elif (sequence[0] in bases or sequence[-1] in bases) and "begin/end" == selection_mode:
				ret_list.append(z)
				
		elif selection_mode=="contain":
			for x in sequence:
				if x in bases:
					ret_list.append(z)
				
	ret_list.sort(key=lambda x: x[1], reverse=True)
	return ret_list

# Gets all combinations that link from long strand
def getQuencherStrands(quencher_length,aptamer,binding_sites=None):
	ret_dict = {}
	locked_small_strands = []

	for start_base in range(len(aptamer)):
	
		if binding_sites != None:
			for binding_site in binding_sites:
				if start_base <= binding_site and binding_site <= start_base + quencher_length-1:
					
					quencher = reverse_comp(matcher(start_base,quencher_length,aptamer))
					
					if quencher not in ret_dict.keys():
						ret_dict[quencher] = 0
					ret_dict[quencher] += 1
				
			retValue = ret_dict

		else:
			locked_small_strands.append(reverse_comp(matcher(start_base,quencher_length,aptamer)))

			retValue = locked_small_strands
	return retValue
	
# DNA base match dictionary
dict1 = {
"A": "T",
"C": "G",
"T": "A",
"G": "C"
}

# Other variable storage
locked_small_strands = []
A = 'GCACAAGGTCGG'
B = 'CAGCACCGACCTTGTGCTTTGGGAGTGCTGGTCCAAGGGCGTTAATGGACA'
c1 = 1e-6
c2 = 1e-6
intermediate = []

locked_small_strands = getQuencherStrands(12,B,[3,4,28,29,33,43,42])

# Runs comparison between small and long strand
for x in locked_small_strands:
	intermediate.append([x, round((compare(B, x, c1, c2)/c1)*100, 3),locked_small_strands[x]])


final = baseFilter(intermediate,['A'],'begin/end')

final_df = pd.DataFrame(final)
final_df.to_csv('my_csv.csv', index=False)



