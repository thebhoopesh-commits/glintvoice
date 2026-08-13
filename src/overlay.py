import tkinter as tk
import ctypes
import pyautogui

# Windows API constants for transparent/click-through window
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GlintVoice Overlay")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        
        # Make the background color transparent
        transparent_color = "black"
        self.root.configure(bg=transparent_color)
        self.root.attributes("-transparentcolor", transparent_color)
        
        # Full screen coverage
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Canvas for drawing the animations
        self.canvas = tk.Canvas(self.root, bg=transparent_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Apply Win32 API styles to make it click-through
        self.root.update()
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(
            hwnd, 
            GWL_EXSTYLE, 
            ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        )

    def trigger_start_ripple(self):
        """Thread-safe trigger for start ripple (Cyan)."""
        x, y = pyautogui.position()
        # root.after schedules this to run on the main Tkinter thread
        self.root.after(0, lambda: self._animate_ripple(x, y, "cyan"))

    def trigger_stop_ripple(self):
        """Thread-safe trigger for stop ripple (Orange)."""
        x, y = pyautogui.position()
        self.root.after(0, lambda: self._animate_ripple(x, y, "orange"))

    def _animate_ripple(self, x, y, color):
        """Animates a single expanding circle."""
        max_radius = 40
        steps = 15
        circle = self.canvas.create_oval(x, y, x, y, outline=color, width=3)
        
        def _step(current_step):
            if current_step > steps:
                self.canvas.delete(circle)
                return
            # Expand radius
            radius = (max_radius / steps) * current_step
            self.canvas.coords(circle, x - radius, y - radius, x + radius, y + radius)
            # Schedule next frame
            self.root.after(15, _step, current_step + 1)
            
        _step(1)

    def run(self):
        """Starts the Tkinter main event loop. This blocks."""
        self.root.mainloop()
