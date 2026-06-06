import requests, bs4, os, sys
from urllib.parse import urlsplit

# Argument handling.
if len(sys.argv) < 2:
	print("No url has been provided.")
	sys.exit()
url = sys.argv[1]
if not url.startswith(("https")):
	print(f"Please enter a valid url, perhaps you meant: http://{url}")
	sys.exit()

# Getting main url.
url_split = urlsplit(url)
main_url = f"{url_split.scheme}://{url_split.netloc}"

# Creating dirs.
os.makedirs(f"image_downloader/{url_split.netloc}", exist_ok=True)
session_path = f"image_downloader/{url_split.netloc}"

# Setting session.
headers = {
	"User-Agent": "Mozilla/5.0"
}
session = requests.Session()

# Establishing connection
response = session.get(url, headers=headers, stream=True)
response.raise_for_status()

# Parsing HTML.
soup = bs4.BeautifulSoup(response.text, 'html.parser')
img_elems = soup.select("img")

print(f"{len(img_elems)} image found.")

# Looping through every <img> element.
for img in img_elems:
	img_url = img.get('src')
	if img_url == None:
		continue
	if img_url.startswith("/"):
		img_url = main_url + img_url
	filename = os.path.basename(img_url)
	try:
		img_response = session.get(img_url, headers=headers, stream=True)
	except Exception as err:
		print(f"Error downloading {filename}.")
		continue
	
	with open(os.path.join(session_path, filename), 'wb') as f:
		print(f"Downloading {filename}...")
		for chunk in img_response.iter_content(100000):
			f.write(chunk)
print("Done.")