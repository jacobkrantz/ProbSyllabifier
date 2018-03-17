from celex import Celex as C

def test():
	c = C()
	transcription_scheme = [
        ['b', 'h', 'z', 'm', '0', 'x', 'Z'],
        ['p', 'C', 'T', '_', 'v'],
        ['k'],
        ['d', 'n'],
        ['$', 'I', 'P', '2', '5', '~'],
        ['@', 'E', 'i', '1', 'u', '7', '8', 'U'],
        ['t', 'N'],
        ['H', '#', 'r', 'c', 'F'],
        ['D', 'j', 'Q', '3', '4', 'V', '9', '{'],
        ['S', 'R', 'l', '6'],
        ['q', 's'],
        ['J', 'w', 'g', 'f']
    ]
	c.load_sets(5000, 200)
	model = c.train_hmm(transcription_scheme)
	results, full = c.test_hmm(model)
	print results




test()
