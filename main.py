import os
import time
import tkinter as tk
import tkinterweb as tkw
import json


def get_settings():
    with open("settings.json") as f:
        return json.load(f)


settings = get_settings()


def make_widgets(win) -> tuple:
    upper_widgets = tk.Frame(win, relief="raised")
    upper_widgets.grid(row=0, column=0, sticky="ew")

    win.grid_columnconfigure(0, weight=1)
    win.grid_rowconfigure(2, weight=1)

    if settings["home_button_enabled"]:
        upper_widgets.grid_columnconfigure(4, weight=1)

        url_box = tk.Entry(upper_widgets, font=("Arial", 9))
        url_box.grid(row=0, column=4, sticky="ew", padx=5)

        reload_button = tk.Button(upper_widgets, text="⟳")
        reload_button.grid(row=0, column=2, sticky="w")

        back_button = tk.Button(upper_widgets, text="🡄")
        back_button.grid(row=0, column=0, sticky="w")

        forward_button = tk.Button(upper_widgets, text="🡆")
        forward_button.grid(row=0, column=1)

        home_button = tk.Button(upper_widgets, text="⌂")
        home_button.grid(row=0, column=3, sticky="w")
    else:
        upper_widgets.grid_columnconfigure(3, weight=1)

        url_box = tk.Entry(upper_widgets, font=("Arial", 9))
        url_box.grid(row=0, column=3, sticky="ew", padx=5)

        reload_button = tk.Button(upper_widgets, text="⟳")
        reload_button.grid(row=0, column=2, sticky="w")

        back_button = tk.Button(upper_widgets, text="🡄")
        back_button.grid(row=0, column=0, sticky="")

        forward_button = tk.Button(upper_widgets, text="🡆")
        forward_button.grid(row=0, column=1)

    site_name = tk.Label(win, bg=settings["bg_color"], fg="white", font=("Arial", 9))
    site_name.grid(row=1, column=0, sticky="w", pady=5)

    html = tkw.HtmlFrame(win, messages_enabled=False, javascript_enabled=True)
    html.grid(row=2, column=0, sticky="nsew")

    if settings["home_button_enabled"]:
        return upper_widgets, url_box, reload_button, back_button, forward_button, home_button, site_name, html
    else:
        return upper_widgets, url_box, reload_button, back_button, forward_button, site_name, html


def main():
    root = tk.Tk()

    root.title("WebBrowse")

    root.configure(bg=settings["bg_color"])

    sites = []

    global site_index
    site_index = 0

    global switching
    switching = False

    upper_widgets: tk.Frame
    url_box: tk.Entry
    reload_button: tk.Button
    back_button: tk.Button
    forward_button: tk.Button
    home_button: tk.Button
    site_name: tk.Label
    html: tkw.HtmlFrame

    if settings["home_button_enabled"]:
        upper_widgets, url_box, reload_button, back_button, forward_button, home_button, site_name, html = (
            make_widgets(root)
        )
    else:
        upper_widgets, url_box, reload_button, back_button, forward_button, site_name, html = make_widgets(root)

    def matching_url_check():
        if url_box.get() != html.current_url and not root.focus_get() == url_box and not switching:
            url_box.delete(0, tk.END)
            url_box.insert(0, html.current_url)
        root.after(10, matching_url_check)

    def add_site_to_sites():
        global site_index
        if html.current_url not in sites:
            sites.append(html.current_url)
            site_index += 1
        root.after(10, add_site_to_sites)

    def go_to_last_site():
        global site_index
        global switching
        switching = True

        if len(sites) > 1:
            site_index -= 1

            url_box.delete(0, tk.END)
            url_box.insert(0, sites[site_index])

            get_new_site(False)
        print(site_index)

        switching = False

    def go_to_later_site():
        global site_index
        global switching
        switching = True

        if len(sites) > 1:
            site_index += 1

            url_box.delete(0, tk.END)
            url_box.insert(0, sites[site_index])

            get_new_site(False)
        print(site_index)

        switching = False

    def go_to_home_page():
        if settings["homepage"] == "homepage.html":
            url_box.delete(0, tk.END)
            url_box.insert(0, f"file://{os.path.abspath('./homepage/homepage.html').replace('\\', '/')}")
        else:
            url_box.delete(0, tk.END)
            url_box.insert(0, settings["homepage"])
        get_new_site(False)

    def get_new_site(protocol_check):
        url = url_box.get()

        if protocol_check:
            for index, value in enumerate(("https://", "http://", "file://")):
                if value not in url:
                    if index + 1 == 3:
                        url = "https://" + url

        html.load_url(url)
        time.sleep(1)
        site_name.configure(text=html.title)

    go_to_home_page()
    matching_url_check()
    add_site_to_sites()

    site_index -= 1

    reload_button.configure(command=lambda: get_new_site(False))
    back_button.configure(command=go_to_last_site)
    forward_button.configure(command=go_to_later_site)

    if settings["home_button_enabled"]:
        home_button.configure(command=go_to_home_page)

    url_box.bind("<Return>", lambda a: get_new_site(True))

    root.mainloop()


main()