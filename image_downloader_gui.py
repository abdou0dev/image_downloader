from tkinter import *
import requests, bs4, os, sys
from urllib.parse import urlsplit
from tkinter.ttk import Progressbar

def submit():
    # URL entry user input handling.
    url = url_entry.get()
    if not url:
        stats_label.config(text='Please provide a url first.')
    elif not url.startswith(('https://', 'http://')):
        stats_label.config(text=f"that's not a valid url perhaps you meant: http://{url}")
    else:
        # Getting main url.
        url_split = urlsplit(url)
        main_url = f"{url_split.scheme}://{url_split.netloc}"
        # Creating dirs.
        os.makedirs(f"image_downloader/{url_split.netloc}", exist_ok=True)
        session_path = f"image_downloader/{url_split.netloc}"

        # Setting session.
        stats_label.config(text='Creating session')
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        session = requests.Session()

        # Establishing connection
        stats_label.config(text='Establishing connection...')
        response = session.get(url, headers=headers, stream=True)
        try:
            response.raise_for_status()
        except Exception as err:
            stats_label.config(text="Error: couldn't establish connection.")
            sys.exit()

        # Parsing HTML.
        stats_label.config(text='Parsing HTML')
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        img_elems = soup.select("img")

        info_label.config(text=f"{len(img_elems)} image found.")

        # Looping through every <img> element.
        stats_label.config(text='Locating Images')
        downloaded_images = 0
        for img in img_elems:
            window.update_idletasks()
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
                stats_label.config(text=f'Downloading {filename}...')
                for chunk in img_response.iter_content(100000):
                    f.write(chunk)
                downloaded_images += 1
                info_label.config(text=f"{downloaded_images} of {len(img_elems)}")
        stats_label.config(text='Done.')
        info_label.config(text=f"{downloaded_images} Downloaded of {len(img_elems)}")

window = Tk() # Instantiate an instance of a window.
window.config(padx=10)
# URL entry.
url_entry = Entry(window,
                  width=40,
                  font=('Arial', 15))
url_entry.grid(pady=20)
# Stats label
stats_label = Label(window,
                    font=('Arial', 7),
                    text='')
stats_label.grid(row=1)
# Info label
info_label = Label(window,
                   font=('Arial', 7),
                   text='')
info_label.grid(row=2)
# Submit button.
submit_btn = Button(window,
                    text='Submit',
                    font=('Arial', 10, 'bold'),
                    pady=10,
                    command=submit,)
submit_btn.grid(row=3)

window.mainloop()