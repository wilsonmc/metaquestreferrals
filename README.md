I'll admit I didn't spend a whole lot of time looking around for something that does this already, but when I did I couldnt find any script that I could feed it a bunch of Meta referral links and have it spit back out if they were still giving 25% discounts and if they were working as well. So I used ChatGPT to help me write one in Python. I figured it might help me learn a bit of Python in the process :)

I'm sure there is code out there that is way better and does more, but I figured someone might get some benefit from this. Remember I am not a programmer so don't assume I know how to add any features or fix any issues, but if you want to give suggestions I'll certainly listen to them.

With all that out of the way here is what you need to do to use the script:

1. You will need python and pip installed
2. pip install requests
3. pip install beautifulsoup4
4. pip install colorama
5. The file you want to download is metalinkcheck.py
6. Add a urls.txt to the same folder the script is in that contains all your referral links (apps/games only, no device referral links)
7. Run the metalinkcheck.py script and it will show you the status of each link (I hope..lol)
8. The script can be run with the following arguments:
   --date - Adds in the current date and time to the output
   --lb - Adds in line breaks after each result. This should be used as without it, it's all jumbled together. I'll probably fix it at somepoint.

These are probably pretty terrible instructions but hopefully you have some tech knowhow to figure it out since you somehow ended up here in the first place.

Enjoy!
