import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


# For image handling, you might need Pillow (PIL)
# from PIL import Image, ImageTk # Uncomment if you want to use actual images

class MapAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("仿地图应用界面")
        self.root.geometry("380x720")
        self.root.configure(bg="#f0f0f0")

        # --- Style Configuration ---
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Using a theme that allows more customization

        # Define some colors (can be further refined)
        self.colors = {
            "primary": "#007AFF",  # A slightly more vibrant blue
            "secondary_bg": "#FFFFFF",
            "text_dark": "#1c1c1e",  # Darker text for better contrast
            "text_light": "#8e8e93",  # Lighter gray for secondary text
            "active_tab": "#34C759",  # A vibrant green for active elements
            "inactive_tab_bg": "#EFEFF4",  # Lighter, softer inactive background
            "bottom_nav_bg": "#F9F9F9",  # Slightly off-white for bottom nav
            "search_bar_bg": "#E9E9EB",
            "card_border": "#D1D1D6",
            "map_placeholder_bg": "#E0EBF9",  # Softer blue for map
        }

        # Define fonts
        self.default_font = tkfont.Font(family="Helvetica Neue", size=11)  # Changed font
        self.title_font = tkfont.Font(family="Helvetica Neue", size=13, weight="bold")
        self.small_font = tkfont.Font(family="Helvetica Neue", size=10)
        self.button_font = tkfont.Font(family="Helvetica Neue", size=10,
                                       weight="normal")  # Changed "medium" to "normal"

        # --- Custom ttk Styles ---
        self.style.configure("App.TFrame", background=self.colors["secondary_bg"])
        self.style.configure("BottomNav.TFrame", background=self.colors["bottom_nav_bg"])

        # Style for filter buttons
        self.style.configure("Filter.TButton",
                             font=self.button_font,
                             padding=(10, 8),  # Increased padding
                             relief=tk.FLAT,
                             borderwidth=0)
        self.style.map("Filter.TButton",
                       background=[('active', self.colors["active_tab"]),
                                   ('!active', self.colors["inactive_tab_bg"])],
                       foreground=[('active', self.colors["secondary_bg"]),  # White text on active
                                   ('!active', self.colors["text_dark"])])

        # Style for bottom navigation text (using Labels as buttons)
        # We will style Labels directly, ttk.Label styling is less flexible for this case

        # --- Main Structure ---
        self.create_status_bar()
        self.create_top_bar()
        self.create_filter_tabs()
        self.create_map_area()
        self.create_info_panel()
        self.create_bottom_navigation()

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root, style="App.TFrame", height=30)  # Increased height
        status_frame.pack(fill=tk.X, side=tk.TOP)
        status_frame.pack_propagate(False)

        time_label = ttk.Label(status_frame, text="10:00", font=self.small_font, background=self.colors["secondary_bg"],
                               foreground=self.colors["text_dark"])
        time_label.pack(side=tk.LEFT, padx=15, pady=5)  # Increased padding

        icons_label = ttk.Label(status_frame, text="📶  🔋", font=self.small_font, background=self.colors["secondary_bg"],
                                foreground=self.colors["text_dark"])
        icons_label.pack(side=tk.RIGHT, padx=15, pady=5)

    def create_top_bar(self):
        top_bar_frame = ttk.Frame(self.root, style="App.TFrame", height=55)  # Increased height
        top_bar_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 1))
        top_bar_frame.pack_propagate(False)

        # Note: ttk.Button might not look exactly like native iOS/Android back buttons.
        # For a truly custom look, images are often used for such buttons.
        back_button = ttk.Button(top_bar_frame, text="←", command=self.on_back_click,
                                 style="Toolbutton")  # Using a less obtrusive style if available
        try:
            # Attempt to make it less obtrusive, if Toolbutton style doesn't provide enough control
            self.style.configure("Toolbutton", font=self.title_font, padding=5, relief=tk.FLAT,
                                 background=self.colors["secondary_bg"])
        except tk.TclError:
            pass  # Style might not exist on all platforms, or 'clam' theme handles it differently
        back_button.pack(side=tk.LEFT, padx=(10, 0), pady=5)

        # Search bar - achieving perfectly rounded Entry is hard with standard Tkinter/ttk
        # This is a common limitation.
        search_container = ttk.Frame(top_bar_frame, style="App.TFrame")
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)

        search_frame = tk.Frame(search_container, bg=self.colors["search_bar_bg"], relief=tk.SOLID, borderwidth=0)
        # To simulate rounded corners for search_frame, one would typically use a Canvas
        # and draw a rounded rectangle, then place the Entry widget inside it without its own border.
        # For simplicity, we keep it rectangular but with a distinct background.
        search_frame.pack(fill=tk.BOTH, expand=True)

        search_icon = ttk.Label(search_frame, text="🔍", font=self.default_font, background=self.colors["search_bar_bg"],
                                foreground=self.colors["text_light"])
        search_icon.pack(side=tk.LEFT, padx=(8, 2), pady=5)

        self.search_entry = tk.Entry(search_frame, font=self.default_font, relief=tk.FLAT,
                                     bg=self.colors["search_bar_bg"], fg=self.colors["text_dark"],
                                     insertbackground=self.colors["text_dark"],  # Cursor color
                                     borderwidth=0, highlightthickness=0)  # Remove Entry border
        self.search_entry.insert(0, "大学生特种兵 两天一夜 极限游玩")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5, ipady=3)  # ipady for internal padding

        menu_button = ttk.Button(top_bar_frame, text="☰", command=self.on_menu_click, style="Toolbutton")
        menu_button.pack(side=tk.RIGHT, padx=(0, 10), pady=5)

    def create_filter_tabs(self):
        self.filter_buttons = []
        filter_frame = ttk.Frame(self.root, style="App.TFrame", height=50)  # Increased height
        self.filter_tab_frame = filter_frame
        filter_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))  # Added bottom padding
        filter_frame.pack_propagate(False)

        tabs = ["高分路线", "特种兵路线", "文艺游路线", "家庭游路线"]
        self.active_filter_tab = tk.StringVar(value=tabs[1])

        for i, tab_text in enumerate(tabs):
            btn = ttk.Button(
                filter_frame,
                text=tab_text,
                style="Filter.TButton",
                command=lambda t=tab_text: self.on_filter_tab_click(t)
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3 if i > 0 else (8, 3),
                     pady=5)  # More padding on sides
            self.filter_buttons.append(btn)

        self.update_filter_button_states()  # Initial state update

    def update_filter_button_states(self):
        active_tab_name = self.active_filter_tab.get()
        for btn in self.filter_buttons:
            if btn.cget("text") == active_tab_name:
                btn.state(['active'])  # ttk uses states
            else:
                btn.state(['!active'])

    def on_filter_tab_click(self, tab_name):
        self.active_filter_tab.set(tab_name)
        print(f"Filter tab clicked: {tab_name}")
        self.update_filter_button_states()

    def create_map_area(self):
        map_canvas = tk.Canvas(self.root, bg=self.colors["map_placeholder_bg"], relief=tk.FLAT, borderwidth=0,
                               highlightthickness=0)
        map_canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Mock elements (can be styled further if needed)
        map_canvas.create_text(190, 50, text="南京站 (模拟)", font=self.default_font, fill=self.colors["text_dark"])
        map_canvas.create_oval(185, 65, 195, 75, fill=self.colors["primary"],
                               outline=self.colors["primary"])  # Smaller marker

        map_canvas.create_text(100, 150, text="总统府 (模拟)", font=self.default_font, fill=self.colors["text_dark"])
        map_canvas.create_oval(95, 165, 105, 175, fill=self.colors["primary"], outline=self.colors["primary"])

        map_canvas.create_text(280, 200, text="南京博物院 (模拟)", font=self.default_font,
                               fill=self.colors["text_dark"])
        map_canvas.create_oval(275, 215, 285, 225, fill=self.colors["primary"], outline=self.colors["primary"])

        map_canvas.create_line(190, 70, 100, 170, 280, 220, fill=self.colors["primary"], width=2,
                               smooth=True)  # Thinner line

    def create_info_panel(self):
        info_panel_container = ttk.Frame(self.root, style="App.TFrame", height=160)  # Increased height
        info_panel_container.pack(fill=tk.X, side=tk.TOP, pady=(1, 0))
        info_panel_container.pack_propagate(False)

        canvas = tk.Canvas(info_panel_container, bg=self.colors["secondary_bg"], highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))  # Padding for scroll start

        scrollbar = ttk.Scrollbar(info_panel_container, orient=tk.HORIZONTAL, command=canvas.xview)
        # Scrollbar not packed yet, will be placed over canvas if needed or outside
        # For a cleaner look, sometimes scrollbars are hidden until hover, which is complex in Tkinter.

        canvas.configure(xscrollcommand=scrollbar.set)

        self.scrollable_frame = ttk.Frame(canvas, style="App.TFrame")
        self.scrollable_frame_id = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.scrollable_frame_id, height=e.height,
                                                               width=e.width))  # Ensure frame resizes

        # Populate with cards
        cards_data = [
            {"name": "老门东", "image_placeholder": "#FFCA28", "details": "1 · 2.5km", "fav": True},  # Brighter yellow
            {"name": "夫子庙秦淮风光带", "image_placeholder": "#66BB6A", "details": "2 · 2.9km", "fav": False},
            # Softer green
            {"name": "南京艺术学院", "image_placeholder": "#42A5F5", "details": "3 · 3.2km", "fav": True},  # Nice blue
            {"name": "总统府", "image_placeholder": "#EF5350", "details": "4 · 1.8km", "fav": False},  # Softer red
        ]

        for card_data in cards_data:
            self.add_info_card(self.scrollable_frame, card_data)

        # Only show scrollbar if content overflows (this is a bit manual)
        self.root.update_idletasks()  # Ensure widgets are drawn and sizes are calculated
        if self.scrollable_frame.winfo_reqwidth() > canvas.winfo_width():
            scrollbar.pack(side=tk.BOTTOM, fill=tk.X, padx=(8, 0))

    def add_info_card(self, parent, data):
        card_width = 130  # Slightly wider
        card_height = 145  # Slightly taller

        # Using tk.Frame for card to have more control over border if needed, or ttk.Frame
        card_frame = tk.Frame(parent, width=card_width, height=card_height,
                              bg=self.colors["secondary_bg"],
                              relief=tk.SOLID,  # Or tk.FLAT
                              borderwidth=1, highlightbackground=self.colors["card_border"],
                              highlightcolor=self.colors["card_border"], highlightthickness=1)
        # Using highlightthickness for a border that might look better on some systems
        card_frame.pack(side=tk.LEFT, padx=(0, 8), pady=10)  # Spacing between cards
        card_frame.pack_propagate(False)

        # Image placeholder
        img_placeholder = tk.Frame(card_frame, bg=data["image_placeholder"], height=80)  # Taller placeholder
        img_placeholder.pack(fill=tk.X, side=tk.TOP, padx=1, pady=1)  # Small internal border

        if data["fav"]:
            fav_label = tk.Label(img_placeholder, text="★", font=self.title_font, bg=data["image_placeholder"],
                                 fg="gold")
            fav_label.place(relx=0.92, rely=0.1, anchor="ne")

        name_label = tk.Label(card_frame, text=data["name"], font=self.button_font, bg=self.colors["secondary_bg"],
                              fg=self.colors["text_dark"], wraplength=card_width - 15, anchor="w", justify=tk.LEFT)
        name_label.pack(fill=tk.X, pady=(8, 2), padx=8)

        details_label = tk.Label(card_frame, text=data["details"], font=self.small_font, bg=self.colors["secondary_bg"],
                                 fg=self.colors["text_light"], anchor="w", justify=tk.LEFT)
        details_label.pack(fill=tk.X, pady=(0, 8), padx=8)

    def create_bottom_navigation(self):
        self.nav_item_widgets = []
        nav_frame = ttk.Frame(self.root, style="BottomNav.TFrame", height=65)  # Increased height
        self.bottom_nav_frame = nav_frame
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        # Add a thin top border to the nav_frame
        top_border = tk.Frame(nav_frame, height=1, bg=self.colors["card_border"])
        top_border.pack(fill=tk.X, side=tk.TOP)
        nav_frame.pack_propagate(False)

        nav_items_data = [
            {"text": "精选", "icon": "🌟"},
            {"text": "发现", "icon": "💡"},
            {"text": "商城", "icon": "🛒"},
            {"text": "我的", "icon": "👤"}
        ]

        self.active_nav_item = tk.StringVar(value=nav_items_data[1]["text"])

        for item_data in nav_items_data:
            item_frame = ttk.Frame(nav_frame, style="BottomNav.TFrame")  # Use the styled frame
            item_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            item_frame.bind("<Button-1>", lambda e, t=item_data["text"]: self.on_nav_item_click(t))

            # Using tk.Label for more direct fg/bg control if ttk.Label proves tricky for active states
            icon_label = tk.Label(item_frame, text=item_data["icon"],
                                  font=tkfont.Font(family="Helvetica Neue", size=20),
                                  bg=self.colors["bottom_nav_bg"])  # Set bg explicitly
            icon_label.pack(pady=(8, 0))  # Increased padding
            icon_label.bind("<Button-1>", lambda e, t=item_data["text"]: self.on_nav_item_click(t))

            text_label = tk.Label(item_frame, text=item_data["text"], font=self.small_font,
                                  bg=self.colors["bottom_nav_bg"])  # Set bg explicitly
            text_label.pack(pady=(2, 8))  # Increased padding
            text_label.bind("<Button-1>", lambda e, t=item_data["text"]: self.on_nav_item_click(t))

            self.nav_item_widgets.append(
                {"frame": item_frame, "icon_label": icon_label, "text_label": text_label, "name": item_data["text"]})

        self.update_nav_item_states()  # Initial state update

    def update_nav_item_states(self):
        active_name = self.active_nav_item.get()
        for item_widget_set in self.nav_item_widgets:
            is_active = (item_widget_set["name"] == active_name)
            new_fg = self.colors["primary"] if is_active else self.colors[
                "text_light"]  # Using primary color for active
            item_widget_set["icon_label"].config(fg=new_fg)
            item_widget_set["text_label"].config(fg=new_fg)

    def on_nav_item_click(self, item_name):
        self.active_nav_item.set(item_name)
        print(f"Nav item clicked: {item_name}")
        self.update_nav_item_states()

    def on_back_click(self):
        print("Back button clicked")

    def on_menu_click(self):
        print("Menu button clicked")


if __name__ == "__main__":
    root = tk.Tk()
    app = MapAppUI(root)
    root.mainloop()