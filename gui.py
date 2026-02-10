"""GUI for Ocean Temperature Time Series Pipeline."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import os
from src.data_loader import load_temperature_data, validate_data
from src.analysis import calculate_mean_temperature, calculate_trend


class OceanTemperatureAnalysisGUI:
    """Main GUI application for ocean temperature time series analysis."""

    def __init__(self, root):
        self.root = root
        self.root.title("Ocean Temperature Time Series")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Data storage
        self.df = None
        self.data_path = None

        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

        self._create_header()
        self._create_file_section()
        self._create_stats_section()
        self._create_plot_section()
        self._create_status_section()

        # Set default file path
        default_path = os.path.join(os.path.dirname(__file__), "data", "ocean_temps.csv")
        if os.path.exists(default_path):
            self.file_path_var.set(default_path)

    def _create_header(self):
        """Create the header section with title."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        title_label = ttk.Label(
            header_frame,
            text="Ocean Temperature Time Series",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(anchor="center")

        subtitle_label = ttk.Label(
            header_frame,
            text="Analyze and visualize ocean temperature data",
            font=("Helvetica", 10)
        )
        subtitle_label.pack(anchor="center")

        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=(10, 0))

    def _create_file_section(self):
        """Create the file loading section."""
        file_frame = ttk.LabelFrame(self.main_frame, text="Data File", padding="10")
        file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="File Path:").grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=60)
        file_entry.grid(row=0, column=1, sticky="ew", padx=5)

        browse_btn = ttk.Button(file_frame, text="Browse...", command=self._browse_file)
        browse_btn.grid(row=0, column=2, padx=(5, 0))

        # Action buttons
        btn_frame = ttk.Frame(file_frame)
        btn_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        self.load_btn = ttk.Button(btn_frame, text="Load Data", command=self._load_data)
        self.load_btn.pack(side="left", padx=5)

        self.run_analysis_btn = ttk.Button(
            btn_frame,
            text="Run Full Analysis",
            command=self._run_analysis,
            state="disabled"
        )
        self.run_analysis_btn.pack(side="left", padx=5)

    def _create_stats_section(self):
        """Create the statistics display section."""
        stats_frame = ttk.LabelFrame(self.main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # Create a grid for statistics
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill="x")

        # Data info
        ttk.Label(stats_grid, text="Records:", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.records_var = tk.StringVar(value="--")
        ttk.Label(stats_grid, textvariable=self.records_var).grid(row=0, column=1, sticky="w")

        ttk.Label(stats_grid, text="Date Range:", font=("Helvetica", 10, "bold")).grid(
            row=0, column=2, sticky="w", padx=(30, 10)
        )
        self.date_range_var = tk.StringVar(value="--")
        ttk.Label(stats_grid, textvariable=self.date_range_var).grid(row=0, column=3, sticky="w")

        # Temperature stats
        ttk.Label(stats_grid, text="Mean Temperature:", font=("Helvetica", 10, "bold")).grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0)
        )
        self.mean_temp_var = tk.StringVar(value="--")
        ttk.Label(stats_grid, textvariable=self.mean_temp_var).grid(
            row=1, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(stats_grid, text="Temperature Trend:", font=("Helvetica", 10, "bold")).grid(
            row=1, column=2, sticky="w", padx=(30, 10), pady=(10, 0)
        )
        self.trend_var = tk.StringVar(value="--")
        ttk.Label(stats_grid, textvariable=self.trend_var).grid(
            row=1, column=3, sticky="w", pady=(10, 0)
        )

        # Validation status
        ttk.Label(stats_grid, text="Validation:", font=("Helvetica", 10, "bold")).grid(
            row=2, column=0, sticky="w", padx=(0, 10), pady=(10, 0)
        )
        self.validation_var = tk.StringVar(value="--")
        self.validation_label = ttk.Label(stats_grid, textvariable=self.validation_var)
        self.validation_label.grid(row=2, column=1, columnspan=3, sticky="w", pady=(10, 0))

    def _create_plot_section(self):
        """Create the plot display section."""
        plot_frame = ttk.LabelFrame(self.main_frame, text="Visualization", padding="10")
        plot_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=1)

        # Plot buttons
        plot_btn_frame = ttk.Frame(plot_frame)
        plot_btn_frame.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.plot_timeseries_btn = ttk.Button(
            plot_btn_frame,
            text="Plot Time Series",
            command=self._plot_timeseries,
            state="disabled"
        )
        self.plot_timeseries_btn.pack(side="left", padx=(0, 5))

        self.save_plot_btn = ttk.Button(
            plot_btn_frame,
            text="Save Plot...",
            command=self._save_plot,
            state="disabled"
        )
        self.save_plot_btn.pack(side="left", padx=5)

        self.clear_plot_btn = ttk.Button(
            plot_btn_frame,
            text="Clear Plot",
            command=self._clear_plot,
            state="disabled"
        )
        self.clear_plot_btn.pack(side="left", padx=5)

        # Plot canvas area
        self.canvas_frame = ttk.Frame(plot_frame)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#f0f0f0')
        self.ax.text(
            0.5, 0.5, "Load data and click 'Plot Time Series' to view",
            ha='center', va='center', fontsize=12, color='gray'
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Navigation toolbar
        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.grid(row=2, column=0, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

    def _create_status_section(self):
        """Create the status/log section."""
        status_frame = ttk.LabelFrame(self.main_frame, text="Status Log", padding="10")
        status_frame.grid(row=4, column=0, sticky="ew")
        status_frame.columnconfigure(0, weight=1)

        # Status text with scrollbar
        text_frame = ttk.Frame(status_frame)
        text_frame.pack(fill="x")
        text_frame.columnconfigure(0, weight=1)

        self.status_text = tk.Text(text_frame, height=5, wrap="word", state="disabled")
        self.status_text.grid(row=0, column=0, sticky="ew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)

        # Clear log button
        clear_log_btn = ttk.Button(status_frame, text="Clear Log", command=self._clear_log)
        clear_log_btn.pack(anchor="e", pady=(5, 0))

    def _log(self, message):
        """Add a message to the status log."""
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")
        self.root.update_idletasks()

    def _clear_log(self):
        """Clear the status log."""
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.configure(state="disabled")

    def _browse_file(self):
        """Open file dialog to select a CSV file."""
        filename = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.path.dirname(self.file_path_var.get()) if self.file_path_var.get() else None
        )
        if filename:
            self.file_path_var.set(filename)

    def _load_data(self):
        """Load data from the specified file using src/data_loader.py."""
        filepath = self.file_path_var.get()

        if not filepath:
            messagebox.showerror("Error", "Please specify a file path.")
            return

        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found: {filepath}")
            return

        try:
            self._log(f"Loading data from: {filepath}")
            self.df = load_temperature_data(filepath)
            self.data_path = filepath

            # Update statistics
            self.records_var.set(str(len(self.df)))

            # Try to get date range
            if 'date' in self.df.columns:
                date_min = self.df['date'].min()
                date_max = self.df['date'].max()
                self.date_range_var.set(f"{date_min} to {date_max}")
            else:
                self.date_range_var.set("No date column found")

            # Validate data using src/data_loader.py
            self._log("Validating data...")

            # Get validation message and display in GUI
            validation_message = validate_data(self.df)
            self.validation_var.set(validation_message)

            self._log(f"Loaded {len(self.df)} records successfully!")

            # Enable analysis and plot buttons
            self.run_analysis_btn.configure(state="normal")
            self.plot_timeseries_btn.configure(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self._log(f"Error: {str(e)}")

    def _run_analysis(self):
        """Run the complete analysis pipeline."""
        if self.df is None:
            messagebox.showerror("Error", "Please load data first.")
            return

        try:
            self._log("=" * 40)
            self._log("Running full analysis...")

            # Calculate statistics
            self._log("Calculating mean temperature...")
            mean_temp = calculate_mean_temperature(self.df)
            self.mean_temp_var.set(f"{mean_temp:.2f}°C")
            self._log(f"Mean temperature: {mean_temp:.2f}°C")

            self._log("Calculating temperature trend...")
            trend = calculate_trend(self.df)
            trend_direction = "+" if trend > 0 else ""
            self.trend_var.set(f"{trend_direction}{trend:.4f}°C per year")
            self._log(f"Temperature trend: {trend_direction}{trend:.4f}°C per year")

            self._log("Analysis complete!")
            self._log("=" * 40)

        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self._log(f"Error: {str(e)}")

    def _plot_timeseries(self):
        """Create a time series plot of temperature data."""
        if self.df is None:
            messagebox.showerror("Error", "Please load data first.")
            return

        try:
            self._log("Creating time series plot...")

            # Clear previous plot
            self.figure.clear()
            self.ax = self.figure.add_subplot(111)

            # Create the plot
            if 'date' in self.df.columns:
                x_data = self.df.index
            else:
                x_data = self.df.index

            self.ax.plot(x_data, self.df['temperature'], linewidth=0.8, alpha=0.7, color='#1f77b4')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Temperature (°C)')
            self.ax.set_title('Ocean Temperature Over Time')
            self.ax.grid(True, alpha=0.3)

            # Rotate x-axis labels for better readability
            self.figure.autofmt_xdate()
            self.canvas.draw()

            # Enable save and clear buttons
            self.save_plot_btn.configure(state="normal")
            self.clear_plot_btn.configure(state="normal")

            self._log("Plot created successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create plot: {str(e)}")
            self._log(f"Error: {str(e)}")

    def _save_plot(self):
        """Save the current plot to a file."""
        filename = filedialog.asksaveasfilename(
            title="Save Plot",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                self.figure.savefig(filename, dpi=300, bbox_inches='tight')
                self._log(f"Plot saved to: {filename}")
                messagebox.showinfo("Success", f"Plot saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot: {str(e)}")
                self._log(f"Error saving plot: {str(e)}")

    def _clear_plot(self):
        """Clear the current plot."""
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#f0f0f0')
        self.ax.text(
            0.5, 0.5, "Plot cleared",
            ha='center', va='center', fontsize=12, color='gray'
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

        self.save_plot_btn.configure(state="disabled")
        self.clear_plot_btn.configure(state="disabled")
        self._log("Plot cleared.")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = OceanTemperatureAnalysisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

