from sec_edgar_downloader import Downloader
import os

tickrs = ["MSFT", "AAPL"]
dl = Downloader("Personal", "foo.bar@baz.com")

for tickr in tickrs:
    dl.get("10-K", tickr)
    dl.get("10-Q", tickr)
print("Finished")
