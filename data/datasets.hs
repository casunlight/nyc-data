import Network.HTTP

url = "https://data.cityofnewyork.us/browse?limitTo=datasets&page=1&sortBy=oldest&view_type=table"

main = do
  let text = simpleHTTP (getRequest url)
  putStrLn text
