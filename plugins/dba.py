targets = [
    {
        'match' : '^servers\.dis.*loadavg\.01$',
        'max' : 10,
        'min' : 0,
        'retry' : 3,
    },
    {
        'match' : '^servers\.dis1.*cpu\.total\.user$',
        'max' : 400,
        'min' : 0,
    },
]

