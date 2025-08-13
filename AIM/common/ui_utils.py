"""
UI Utilities - Common UI components and styling functions
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import time


class LoadingIndicator:
    """Utility class for showing loading progress in the application."""
    
    def __init__(self, parent_widget, message="Loading..."):
        self.parent = parent_widget
        self.message = message
        self.is_showing = False
        
    def show(self, message=None):
        """Show loading indicator with optional custom message."""
        if message:
            self.message = message
            
        if hasattr(self.parent, 'clear_results'):
            self.parent.clear_results()
        if hasattr(self.parent, 'log_result'):
            self.parent.log_result("=" * 60)
            self.parent.log_result(f"⏳ {self.message}")
            self.parent.log_result("=" * 60)
            self.parent.log_result("Please wait...")
        
        if hasattr(self.parent, 'root'):
            self.parent.root.update_idletasks()
            self.parent.root.update()
        
        self.is_showing = True
        time.sleep(0.1)  # Small delay to ensure visibility
        
    def hide(self):
        """Hide loading indicator."""
        if self.is_showing:
            if hasattr(self.parent, 'clear_results'):
                self.parent.clear_results()
            self.is_showing = False
            
    def update_message(self, new_message):
        """Update the loading message."""
        self.message = new_message
        if self.is_showing:
            self.show(new_message)


class UIUtils:
    """Common UI utility functions and styling"""
    
    # Color palette
    COLORS = {
        'primary_blue': '#3498db',
        'primary_blue_hover': '#2980b9',
        'dark_gray': '#2c3e50',
        'light_gray': '#34495e',
        'background': '#f8f9fa',
        'white': '#ffffff',
        'success_green': '#27ae60',
        'success_green_hover': '#229954',
        'warning_orange': '#e67e22',
        'warning_orange_hover': '#d35400',
        'error_red': '#e74c3c',
        'error_red_hover': '#c0392b',
        'purple': '#8e44ad',
        'purple_hover': '#7d3c98'
    }

    @staticmethod
    def create_dialog_button(parent, text, command, bg_color="#3498db", hover_color="#2980b9"):
        """Create a styled dialog button with hover effects."""
        btn = tk.Button(parent, text=text, command=command,
                       font=("Segoe UI", 9, "bold"), width=20, height=2,
                       bg=bg_color, fg="white", relief="flat", bd=0,
                       cursor="hand2", activebackground=hover_color, activeforeground="white",
                       wraplength=150)
        
        # Add hover effects
        def on_enter(e):
            btn.configure(bg=hover_color)
        def on_leave(e):
            btn.configure(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    @staticmethod
    def create_main_button(parent, text, command, row, col, bg_color="#3498db", hover_color="#2980b9"):
        """Create a styled main page button with hover effects and modern design."""
        btn = tk.Button(parent, text=text, command=command,
                       font=("Segoe UI", 9, "bold"), width=18, height=2,
                       bg=bg_color, fg="white", relief="flat", bd=0,
                       cursor="hand2", activebackground=hover_color, activeforeground="white")
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        # Add hover effects
        def on_enter(e):
            btn.configure(bg=hover_color)
        def on_leave(e):
            btn.configure(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    @staticmethod
    def create_modern_header(parent, title, subtitle=None, bg_color="#2c3e50", height=80):
        """Create a modern header frame with title and optional subtitle."""
        header_frame = tk.Frame(parent, bg=bg_color, height=height)
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text=title, 
                             font=("Segoe UI", 20, "bold"), fg="#ecf0f1", bg=bg_color)
        title_label.pack(expand=True)
        
        if subtitle:
            subtitle_label = tk.Label(header_frame, text=subtitle, 
                                    font=("Segoe UI", 10), fg="#bdc3c7", bg=bg_color)
            subtitle_label.pack()
        
        return header_frame

    @staticmethod
    def create_status_frame(parent, status_var, db_stats_var=None):
        """Create a status display frame with modern styling."""
        status_frame = tk.Frame(parent, bg="#ecf0f1", relief="flat", bd=1)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        status_label = tk.Label(status_frame, textvariable=status_var, 
                              font=("Segoe UI", 11), fg="#2c3e50", bg="#ecf0f1")
        status_label.pack(pady=8)
        
        if db_stats_var:
            db_stats_label = tk.Label(status_frame, textvariable=db_stats_var, 
                                    font=("Segoe UI", 10), fg="#27ae60", bg="#ecf0f1")
            db_stats_label.pack(pady=2)
        
        return status_frame

    @staticmethod
    def create_results_area(parent, height=12, width=80):
        """Create a results display area with modern styling."""
        results_container = tk.Frame(parent, bg="#f0f4f8")
        results_container.pack(padx=20, pady=(5, 15), fill="both", expand=True)
        
        results_header_frame = tk.Frame(results_container, bg="#34495e", height=35)
        results_header_frame.pack(fill="x")
        results_header_frame.pack_propagate(False)
        
        results_label = tk.Label(results_header_frame, text="📄 Results & Output", 
                               font=("Segoe UI", 11, "bold"), fg="#ecf0f1", bg="#34495e")
        results_label.pack(expand=True)
        
        # Results text area with modern styling
        text_frame = tk.Frame(results_container, bg="#ffffff", relief="sunken", bd=1)
        text_frame.pack(fill="both", expand=True)
        
        results_text = scrolledtext.ScrolledText(text_frame, height=height, width=width,
                                               font=("Consolas", 9), bg="#ffffff", fg="#2c3e50",
                                               insertbackground="#2c3e50", selectbackground="#3498db",
                                               relief="flat", bd=5)
        results_text.pack(padx=8, pady=8, fill="both", expand=True)
        
        return results_text

    @staticmethod
    def create_scrollable_dialog(parent, title, width=700, height=650):
        """Create a dialog with scrollable content area."""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(bg="#f8f9fa")
        
        # Header
        header_frame = tk.Frame(dialog, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=title, 
                font=("Segoe UI", 14, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(expand=True)
        
        # Main content frame with scrolling capability
        main_frame = tk.Frame(dialog, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_frame, bg="#f8f9fa")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return dialog, scrollable_frame

    @staticmethod
    def log_to_text_widget(text_widget, message):
        """Add a message to a text widget and scroll to end."""
        text_widget.insert(tk.END, f"{message}\n")
        text_widget.see(tk.END)

    @staticmethod
    def clear_text_widget(text_widget):
        """Clear the contents of a text widget."""
        text_widget.delete(1.0, tk.END)

    @staticmethod
    def show_loading_in_text(text_widget, message="Loading..."):
        """Show loading text in a text widget with enhanced visibility."""
        UIUtils.clear_text_widget(text_widget)
        UIUtils.log_to_text_widget(text_widget, "=" * 60)
        UIUtils.log_to_text_widget(text_widget, f"⏳ {message}")
        UIUtils.log_to_text_widget(text_widget, "=" * 60)
        UIUtils.log_to_text_widget(text_widget, "Please wait...")
        
        # Force update
        text_widget.update_idletasks()
        text_widget.update()
        time.sleep(0.1)
