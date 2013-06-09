targets = [
    {
        'match' : '^servers\.dis.*udp\.InDatagrams$',
        'max' : 10,
        'min' : 0,
        'retry' : 2,
    },
    {
        'match' : '^servers\.dis1.*udp\.OutDatagrams$',
        'max' : 5,
        'min' : 0,
    },
]

