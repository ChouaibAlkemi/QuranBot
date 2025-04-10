"""
UI Controller for Qur'anic Verse Application

This module manages the user interface and mode switching.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import threading
import time

from src.verse_manager import VerseManager
from src.config_manager import ConfigurationManager

class UIController:
    """
    Controller for managing the user interface and mode switching.
    """
    
    def __init__(self, root):
        """
        Initialize the UI controller.
        
        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.verse_manager = VerseManager()
        self.config_manager = ConfigurationManager()
        
        # Load configuration
        self.config = self.config_manager.get_config()
        
        # Set up the UI
        self._setup_ui()
        
        # Current mode
        self.current_mode = "standard"
        
        # Show the standard mode by default
        self._show_standard_mode()
    
    def _setup_ui(self):
        """Set up the main user interface."""
        # Configure the root window
        self.root.title("Qur'anic Verse Application")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Apply theme
        self._apply_theme()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create mode selection tabs
        self.mode_tabs = ttk.Notebook(self.header_frame)
        self.mode_tabs.pack(fill=tk.X)
        
        # Create tab frames
        self.standard_tab = ttk.Frame(self.mode_tabs)
        self.simulation_tab = ttk.Frame(self.mode_tabs)
        self.advanced_tab = ttk.Frame(self.mode_tabs)
        
        # Add tabs to notebook
        self.mode_tabs.add(self.standard_tab, text="Standard Mode")
        self.mode_tabs.add(self.simulation_tab, text="Simulation Mode")
        self.mode_tabs.add(self.advanced_tab, text="Advanced Mode 🔒")
        
        # Bind tab change event
        self.mode_tabs.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
        # Create content frame (will be replaced by mode-specific frames)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create settings button
        self.settings_button = ttk.Button(
            self.header_frame, 
            text="⚙️", 
            width=3,
            command=self._show_settings
        )
        self.settings_button.pack(side=tk.RIGHT, padx=5)
        
        # Create mode-specific frames (will be shown/hidden as needed)
        self._create_standard_mode_frame()
        self._create_simulation_mode_frame()
        self._create_advanced_mode_frame()
    
    def _create_standard_mode_frame(self):
        """Create the standard mode UI frame."""
        self.standard_frame = ttk.Frame(self.main_frame)
        
        # Verse display frame
        self.verse_frame = ttk.Frame(self.standard_frame, relief=tk.GROOVE, borderwidth=2)
        self.verse_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Arabic text
        self.arabic_text = tk.Text(
            self.verse_frame, 
            height=5, 
            wrap=tk.WORD, 
            font=("Arial", 18),
            background="#f8f8f8",
            relief=tk.FLAT
        )
        self.arabic_text.pack(fill=tk.X, padx=20, pady=(20, 10))
        self.arabic_text.tag_configure("center", justify="center")
        self.arabic_text.insert(tk.END, "Press 'New Random Verse' to display a verse")
        self.arabic_text.tag_add("center", "1.0", "end")
        self.arabic_text.config(state=tk.DISABLED)
        
        # Translation text
        self.translation_text = tk.Text(
            self.verse_frame, 
            height=8, 
            wrap=tk.WORD, 
            font=("Arial", 12),
            background="#f8f8f8",
            relief=tk.FLAT
        )
        self.translation_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.translation_text.tag_configure("center", justify="center")
        self.translation_text.config(state=tk.DISABLED)
        
        # Reference label
        self.reference_label = ttk.Label(
            self.verse_frame, 
            text="",
            font=("Arial", 10, "italic")
        )
        self.reference_label.pack(pady=(0, 20), anchor=tk.E, padx=20)
        
        # Controls frame
        self.controls_frame = ttk.Frame(self.standard_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        # New verse button
        self.new_verse_button = ttk.Button(
            self.controls_frame, 
            text="New Random Verse",
            command=self._get_random_verse
        )
        self.new_verse_button.pack(side=tk.LEFT, padx=5)
        
        # Copy button
        self.copy_button = ttk.Button(
            self.controls_frame, 
            text="Copy",
            command=self._copy_verse
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        # Share button
        self.share_button = ttk.Button(
            self.controls_frame, 
            text="Share",
            command=self._share_verse
        )
        self.share_button.pack(side=tk.LEFT, padx=5)
        
        # Settings frame
        self.settings_frame = ttk.Frame(self.standard_frame)
        self.settings_frame.pack(fill=tk.X, pady=10)
        
        # Translation selection
        ttk.Label(self.settings_frame, text="Translation:").pack(side=tk.LEFT, padx=5)
        self.translation_var = tk.StringVar(value=self.config["translation"])
        self.translation_combo = ttk.Combobox(
            self.settings_frame, 
            textvariable=self.translation_var,
            state="readonly",
            width=20
        )
        self.translation_combo.pack(side=tk.LEFT, padx=5)
        
        # Populate translations (async)
        threading.Thread(target=self._load_translations, daemon=True).start()
        
        # Bind translation change
        self.translation_combo.bind("<<ComboboxSelected>>", self._on_translation_changed)
    
    def _create_simulation_mode_frame(self):
        """Create the simulation mode UI frame."""
        self.simulation_frame = ttk.Frame(self.main_frame)
        
        # Placeholder label
        ttk.Label(
            self.simulation_frame, 
            text="Simulation Mode\nThis feature will be implemented in the next phase.",
            font=("Arial", 14),
            justify=tk.CENTER
        ).pack(expand=True)
    
    def _create_advanced_mode_frame(self):
        """Create the advanced mode UI frame."""
        self.advanced_frame = ttk.Frame(self.main_frame)
        
        # Lock frame (shown when advanced mode is locked)
        self.advanced_lock_frame = ttk.Frame(self.advanced_frame)
        self.advanced_lock_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            self.advanced_lock_frame, 
            text="⚠️ Advanced Developer Mode",
            font=("Arial", 16, "bold"),
            foreground="#CC0000"
        ).pack(pady=(50, 10))
        
        ttk.Label(
            self.advanced_lock_frame, 
            text="This mode is for educational purposes only.\nIt provides a local sandbox environment for testing automation concepts.",
            justify=tk.CENTER
        ).pack(pady=10)
        
        ttk.Button(
            self.advanced_lock_frame, 
            text="Unlock Advanced Mode",
            command=self._unlock_advanced_mode
        ).pack(pady=20)
        
        # Content frame (shown when advanced mode is unlocked)
        self.advanced_content_frame = ttk.Frame(self.advanced_frame)
        
        # Placeholder label
        ttk.Label(
            self.advanced_content_frame, 
            text="Advanced Developer Mode\nThis feature will be implemented in the next phase.",
            font=("Arial", 14),
            justify=tk.CENTER
        ).pack(expand=True)
    
    def _show_standard_mode(self):
        """Show the standard mode UI."""
        # Hide other frames
        self.simulation_frame.pack_forget()
        self.advanced_frame.pack_forget()
        
        # Show standard frame
        self.standard_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update current mode
        self.current_mode = "standard"
        
        # Select the standard tab
        self.mode_tabs.select(0)
    
    def _show_simulation_mode(self):
        """Show the simulation mode UI."""
        # Hide other frames
        self.standard_frame.pack_forget()
        self.advanced_frame.pack_forget()
        
        # Show simulation frame
        self.simulation_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update current mode
        self.current_mode = "simulation"
    
    def _show_advanced_mode(self):
        """Show the advanced mode UI."""
        # Hide other frames
        self.standard_frame.pack_forget()
        self.simulation_frame.pack_forget()
        
        # Show advanced frame
        self.advanced_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show lock or content based on advanced mode status
        if self.config_manager.is_advanced_mode_enabled():
            self.advanced_lock_frame.pack_forget()
            self.advanced_content_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.advanced_content_frame.pack_forget()
            self.advanced_lock_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update current mode
        self.current_mode = "advanced"
    
    def _on_tab_changed(self, event):
        """
        Handle tab change events.
        
        Args:
            event: The tab change event.
        """
        selected_tab = self.mode_tabs.index(self.mode_tabs.select())
        
        if selected_tab == 0:
            self._show_standard_mode()
        elif selected_tab == 1:
            self._show_simulation_mode()
        elif selected_tab == 2:
            self._show_advanced_mode()
    
    def _get_random_verse(self):
        """Get and display a random verse."""
        # Show loading state
        self.new_verse_button.config(state=tk.DISABLED)
        self.new_verse_button.config(text="Loading...")
        self.root.update()
        
        # Get translation from config
        translation = self.translation_var.get()
        
        # Get random verse
        verse = self.verse_manager.get_random_verse(translation)
        
        if verse:
            # Update UI with verse
            self._display_verse(verse)
        else:
            messagebox.showerror(
                "Error", 
                "Failed to retrieve verse. Please check your internet connection and try again."
            )
        
        # Reset button state
        self.new_verse_button.config(state=tk.NORMAL)
        self.new_verse_button.config(text="New Random Verse")
    
    def _display_verse(self, verse):
        """
        Display a verse in the UI.
        
        Args:
            verse (dict): The verse data to display.
        """
        # Update Arabic text
        self.arabic_text.config(state=tk.NORMAL)
        self.arabic_text.delete(1.0, tk.END)
        self.arabic_text.insert(tk.END, verse["text"]["arabic"])
        self.arabic_text.tag_add("center", "1.0", "end")
        self.arabic_text.config(state=tk.DISABLED)
        
        # Update translation text
        self.translation_text.config(state=tk.NORMAL)
        self.translation_text.delete(1.0, tk.END)
        self.translation_text.insert(tk.END, verse["text"]["translation"])
        self.translation_text.tag_add("center", "1.0", "end")
        self.translation_text.config(state=tk.DISABLED)
        
        # Update reference
        surah_name = verse["surah"]["englishName"]
        reference = verse["reference"]
        self.reference_label.config(text=f"— Surah {surah_name} ({reference})")
    
    def _copy_verse(self):
        """Copy the current verse to clipboard."""
        if self.verse_manager.current_verse:
            verse_text = self.verse_manager.get_formatted_verse_text()
            self.root.clipboard_clear()
            self.root.clipboard_append(verse_text)
            messagebox.showinfo("Copied", "Verse copied to clipboard.")
        else:
            messagebox.showinfo("No Verse", "Please get a verse first.")
    
    def _share_verse(self):
        """Share the current verse."""
        if self.verse_manager.current_verse:
            verse_text = self.verse_manager.get_formatted_verse_text()
            
            # Create a simple sharing menu
            share_window = tk.Toplevel(self.root)
            share_window.title("Share Verse")
            share_window.geometry("400x300")
            share_window.transient(self.root)
            share_window.grab_set()
            
            ttk.Label(
                share_window, 
                text="Share this verse:",
                font=("Arial", 12, "bold")
            ).pack(pady=(20, 10))
            
            # Verse preview
            preview = tk.Text(
                share_window, 
                height=8, 
                wrap=tk.WORD, 
                font=("Arial", 10)
            )
            preview.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            preview.insert(tk.END, verse_text)
            preview.config(state=tk.DISABLED)
            
            # Sharing options
            options_frame = ttk.Frame(share_window)
            options_frame.pack(fill=tk.X, pady=10)
            
            ttk.Button(
                options_frame, 
                text="Copy to Clipboard",
                command=lambda: [self.root.clipboard_clear(), 
                                self.root.clipboard_append(verse_text),
                                messagebox.showinfo("Copied", "Verse copied to clipboard."),
                                share_window.destroy()]
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            ttk.Button(
                options_frame, 
                text="Cancel",
                command=share_window.destroy
            ).pack(side=tk.RIGHT, padx=10, pady=10)
        else:
            messagebox.showinfo("No Verse", "Please get a verse first.")
    
    def _load_translations(self):
        """Load available translations asynchronously."""
        translations = self.verse_manager.get_available_translations()
        
        if translations:
            # Create a list of translation options
            options = []
            translation_map = {}
            
            for translation in translations:
                identifier = translation["identifier"]
                name = f"{translation['englishName']} ({translation['language']})"
                options.append(name)
                translation_map[name] = identifier
            
            # Update the combobox
            self.root.after(0, lambda: self._update_translation_combo(options, translation_map))
    
    def _update_translation_combo(self, options, translation_map):
        """
        Update the translation combobox with options.
        
        Args:
            options (list): List of translation names.
            translation_map (dict): Mapping of names to identifiers.
        """
        self.translation_combo["values"] = options
        self.translation_map = translation_map
        
        # Set current value
        current_id = self.translation_var.get()
        
        # Find the name for the current ID
        for name, identifier in translation_map.items():
            if identifier == current_id:
                self.translation_combo.set(name)
                break
    
    def _on_translation_changed(self, event):
        """
        Handle translation selection change.
        
        Args:
            event: The combobox selection event.
        """
        selected_name = self.translation_combo.get()
        
        if hasattr(self, "translation_map") and selected_name in self.translation_map:
            # Get the identifier for the selected name
            identifier = self.translation_map[selected_name]
            
            # Update the config
            self.translation_var.set(identifier)
            self.config["translation"] = identifier
            self.config_manager.update_config({"translation": identifier})
            
            # If we have a current verse, refresh it with the new translation
            if self.verse_manager.current_verse:
                reference = self.verse_manager.current_verse["reference"]
                verse = self.verse_manager.get_specific_verse(reference, identifier)
                
                if verse:
                    self._display_verse(verse)
    
    def _show_settings(self):
        """Show the settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Create notebook for settings categories
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        general_tab = ttk.Frame(notebook)
        notebook.add(general_tab, text="General")
        
        # Theme setting
        theme_frame = ttk.Frame(general_tab)
        theme_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=10)
        
        theme_var = tk.StringVar(value=self.config["theme"])
        theme_combo = ttk.Combobox(
            theme_frame, 
            textvariable=theme_var,
            values=["light", "dark"],
            state="readonly",
            width=15
        )
        theme_combo.pack(side=tk.LEFT, padx=5)
        
        # Font size setting
        font_frame = ttk.Frame(general_tab)
        font_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT, padx=10)
        
        font_var = tk.StringVar(value=self.config["fontSize"])
        font_combo = ttk.Combobox(
            font_frame, 
            textvariable=font_var,
            values=["small", "medium", "large"],
            state="readonly",
            width=15
        )
        font_combo.pack(side=tk.LEFT, padx=5)
        
        # Advanced settings tab
        advanced_tab = ttk.Frame(notebook)
        notebook.add(advanced_tab, text="Advanced")
        
        # Advanced mode settings
        advanced_frame = ttk.LabelFrame(advanced_tab, text="Advanced Developer Mode")
        advanced_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Password setting
        password_frame = ttk.Frame(advanced_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            password_frame, 
            text="Set Password:"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            password_frame, 
            text="Change Password",
            command=lambda: self._change_advanced_password(settings_window)
        ).pack(side=tk.LEFT, padx=5)
        
        # Warning label
        ttk.Label(
            advanced_frame, 
            text="⚠️ Advanced mode is for educational purposes only.\nIt provides a local sandbox environment for testing automation concepts.",
            foreground="#CC0000",
            justify=tk.LEFT
        ).pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(settings_window)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            buttons_frame, 
            text="Save",
            command=lambda: self._save_settings(
                settings_window, 
                {
                    "theme": theme_var.get(),
                    "fontSize": font_var.get()
                }
            )
        ).pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(
            buttons_frame, 
            text="Cancel",
            command=settings_window.destroy
        ).pack(side=tk.RIGHT, padx=10)
    
    def _save_settings(self, window, settings):
        """
        Save settings and close the settings window.
        
        Args:
            window (tk.Toplevel): The settings window.
            settings (dict): The settings to save.
        """
        # Update config
        self.config.update(settings)
        self.config_manager.update_config(settings)
        
        # Apply settings
        self._apply_theme()
        
        # Close window
        window.destroy()
    
    def _apply_theme(self):
        """Apply the current theme to the UI."""
        # This is a simple implementation
        # In a real application, you would use a proper theming system
        theme = self.config.get("theme", "light")
        
        if theme == "dark":
            self.root.configure(bg="#333333")
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("TFrame", background="#333333")
            style.configure("TLabel", background="#333333", foreground="#FFFFFF")
            style.configure("TButton", background="#555555", foreground="#FFFFFF")
            
            # Update text widgets
            if hasattr(self, "arabic_text"):
                self.arabic_text.configure(background="#444444", foreground="#FFFFFF")
                self.translation_text.configure(background="#444444", foreground="#FFFFFF")
        else:
            self.root.configure(bg="#F0F0F0")
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("TFrame", background="#F0F0F0")
            style.configure("TLabel", background="#F0F0F0", foreground="#000000")
            style.configure("TButton", background="#E0E0E0", foreground="#000000")
            
            # Update text widgets
            if hasattr(self, "arabic_text"):
                self.arabic_text.configure(background="#F8F8F8", foreground="#000000")
                self.translation_text.configure(background="#F8F8F8", foreground="#000000")
    
    def _change_advanced_password(self, parent_window):
        """
        Show dialog to change the advanced mode password.
        
        Args:
            parent_window (tk.Toplevel): The parent settings window.
        """
        # Simple password dialog
        password = simpledialog.askstring(
            "Advanced Mode Password", 
            "Enter a new password for Advanced Mode:",
            parent=parent_window,
            show="*"
        )
        
        if password:
            if len(password) < 4:
                messagebox.showerror(
                    "Error", 
                    "Password must be at least 4 characters long.",
                    parent=parent_window
                )
            else:
                self.config_manager.set_advanced_mode_password(password)
                messagebox.showinfo(
                    "Password Changed", 
                    "Advanced mode password has been updated.",
                    parent=parent_window
                )
    
    def _unlock_advanced_mode(self):
        """Show dialog to unlock advanced mode."""
        # Check if password is set
        if not self.config["advancedModePassword"]:
            messagebox.showerror(
                "No Password Set", 
                "Please set a password in Settings > Advanced before using Advanced Mode."
            )
            return
        
        # Ask for password
        password = simpledialog.askstring(
            "Advanced Mode", 
            "Enter password to unlock Advanced Mode:",
            show="*"
        )
        
        if password:
            if self.config_manager.verify_advanced_mode_password(password):
                # Enable advanced mode
                self.config_manager.enable_advanced_mode(password)
                
                # Show warning
                result = messagebox.askokcancel(
                    "Advanced Mode Warning", 
                    "⚠️ EDUCATIONAL USE ONLY ⚠️\n\n"
                    "Advanced Developer Mode is for educational purposes only and "
                    "provides a local sandbox environment for testing automation concepts.\n\n"
                    "This mode should not be used to create tools that violate platform "
                    "terms of service or for any malicious purposes.\n\n"
                    "Do you understand and wish to continue?"
                )
                
                if result:
                    # Show advanced content
                    self.advanced_lock_frame.pack_forget()
                    self.advanced_content_frame.pack(fill=tk.BOTH, expand=True)
                else:
                    # Disable advanced mode
                    self.config_manager.disable_advanced_mode()
            else:
                messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = UIController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
