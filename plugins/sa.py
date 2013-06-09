targets = [
    {
        'match' : '^servers\.dis1.*loadavg\.01$',
        'max' : 10,
        'min' : 0,
        'retry' : 3,
    },
    {
        'match' : '^servers\.dis1.*cpu\.total\.user$',
        'max' : 400,
        'min' : 0,
    },
    {
        'match' : '^servers\.dis1.*memory\.MemFree$',
        'max' : 1024,
        'min' : 0,
    },
]

