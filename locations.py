import geocoder

    #test code, we need to return data back from flask after this point
locationDict = {['2333 piedmont ave, Berkeley, CA'], ['Birge Path, Berkeley, CA 94704']}

g = geocoder.bing(locationDict, method='batch')
for results in g:
    print(results.city)
