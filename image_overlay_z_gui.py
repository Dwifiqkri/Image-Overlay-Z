import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageStat, ImageEnhance
import numpy as np

LANGUAGES = {
    "en": {
        "title": "Image Overlay",
        "select_overlay": "Select the overlay image (with transparent background)",
        "select_targets": "Select the target images to apply the overlay",
        "success": "Overlay applied successfully to all images!",
        "error": "Error applying overlay: ",
        "output_folder": "Select output folder for processed images",
        "done": "Done!",
        "exit": "Press any button to exit",
        "auto_recolor": "Auto-adjust watermark tone based on background brightness?",
        "analyzing": "Analyzing image: ",
        "processing": "Processing: ",
        "yes": "Yes",
        "no": "No"
    },
    "pt": {
        "title": "Sobreposição de Imagem",
        "select_overlay": "Selecione a imagem de sobreposição (com fundo transparente)",
        "select_targets": "Selecione as imagens alvo para aplicar a sobreposição",
        "success": "Sobreposição aplicada com sucesso a todas as imagens!",
        "error": "Erro ao aplicar sobreposição: ",
        "output_folder": "Selecione a pasta de saída para as imagens processadas",
        "done": "Concluído!",
        "exit": "Pressione qualquer botão para sair",
        "auto_recolor": "Ajustar automaticamente o tom da marca d'água com base no brilho do fundo?",
        "analyzing": "Analisando imagem: ",
        "processing": "Processando: ",
        "yes": "Sim",
        "no": "Não"
    }
}

def analyze_brightness(image, bbox):
    # Extract the region where watermark will be placed
    region = image.crop(bbox)
    # Convert to grayscale for brightness analysis
    gray_region = region.convert('L')
    stat = ImageStat.Stat(gray_region)
    mean_brightness = stat.mean[0]
    return mean_brightness / 255.0  # Normalize to 0-1

def adjust_overlay_color(overlay, brightness):
    # Create a new overlay with adjusted color based on background brightness
    # Dark background = VERY LIGHT overlay, Light background = VERY DARK overlay
    # PRESERVES ORIGINAL COLORS - only darkens or lightens them dramatically
    overlay = overlay.convert('RGBA')
    
    # Split into channels
    channels = overlay.split()
    if len(channels) == 4:
        r, g, b, a = channels
    elif len(channels) == 3:
        r, g, b = channels
        a = Image.new('L', r.size, 255)
    else:
        return overlay
    
    # Convert each channel to numpy array for better color preservation
    r_array = np.array(r, dtype=np.float32)
    g_array = np.array(g, dtype=np.float32)
    b_array = np.array(b, dtype=np.float32)
    
    if brightness > 0.5:  # Light background detected - make VERY DARK
        # Extremely aggressive darkening while preserving color ratios
        # The brighter the background, the darker the overlay becomes
        darken_factor = max(0.02, (1.0 - brightness) ** 2.5)
        r_array = r_array * darken_factor
        g_array = g_array * darken_factor
        b_array = b_array * darken_factor
    else:  # Dark background detected - make VERY LIGHT
        # Extremely aggressive lightening while preserving color ratios
        # The darker the background, the lighter the overlay becomes
        # Push colors much closer to white (255) while maintaining their relationships
        lighten_strength = (1.0 - brightness) ** 0.5  # More aggressive for darker backgrounds
        r_array = r_array + (255.0 - r_array) * lighten_strength * 0.95
        g_array = g_array + (255.0 - g_array) * lighten_strength * 0.95
        b_array = b_array + (255.0 - b_array) * lighten_strength * 0.95
    
    # Clip values and convert back to uint8
    r_array = np.clip(r_array, 0, 255).astype(np.uint8)
    g_array = np.clip(g_array, 0, 255).astype(np.uint8)
    b_array = np.clip(b_array, 0, 255).astype(np.uint8)
    
    # Create new image channels
    new_r = Image.fromarray(r_array, mode='L')
    new_g = Image.fromarray(g_array, mode='L')
    new_b = Image.fromarray(b_array, mode='L')
    
    # Recombine channels while preserving original alpha
    try:
        # Ensure all bands are the same size before merging
        size = a.size
        new_r = new_r.resize(size, Image.Resampling.LANCZOS) if new_r.size != size else new_r
        new_g = new_g.resize(size, Image.Resampling.LANCZOS) if new_g.size != size else new_g
        new_b = new_b.resize(size, Image.Resampling.LANCZOS) if new_b.size != size else new_b
        return Image.merge('RGBA', (new_r, new_g, new_b, a))
    except Exception as e:
        print(f"Error merging channels: {e}")
        return overlay

def overlay_images(overlay_path, target_paths, output_folder, watermark_height=None, watermark_opacity=1.0, watermark_height_percent=None, watermark_position="bottom_right", auto_recolor=False, target_color=None, progress_var=None, status_label=None, L=None):
    try:
        overlay = Image.open(overlay_path).convert("RGBA")
        overlay_w, overlay_h = overlay.size
        total = len(target_paths)
        
        for idx, target_path in enumerate(target_paths):
            try:
                base = Image.open(target_path).convert("RGBA")
                base_w, base_h = base.size
                aspect_ratio = overlay_w / overlay_h
                
                # Watermark size logic
                if watermark_height is not None and watermark_height > 0:
                    new_overlay_h = min(watermark_height, base_h)
                    new_overlay_w = int(new_overlay_h * aspect_ratio)
                    new_overlay_w = min(new_overlay_w, base_w)
                elif watermark_height_percent is not None:
                    new_overlay_h = int(base_h * watermark_height_percent)
                    new_overlay_w = int(new_overlay_h * aspect_ratio)
                    new_overlay_w = min(new_overlay_w, base_w)
                    new_overlay_h = min(new_overlay_h, base_h)
                else:
                    base_area = base_w * base_h
                    target_overlay_area = int(base_area * 0.03)
                    new_overlay_h = int((target_overlay_area / aspect_ratio) ** 0.5)
                    new_overlay_w = int(new_overlay_h * aspect_ratio)
                    new_overlay_w = min(new_overlay_w, base_w)
                    new_overlay_h = min(new_overlay_h, base_h)
                
                overlay_resized = overlay.resize((new_overlay_w, new_overlay_h), Image.Resampling.LANCZOS)
                
                # Calculate position and bbox
                if watermark_position == "top_left":
                    pos_x, pos_y = 0, 0
                    bbox = (0, 0, new_overlay_w, new_overlay_h)
                elif watermark_position == "top_right":
                    pos_x, pos_y = base_w - new_overlay_w, 0
                    bbox = (base_w - new_overlay_w, 0, base_w, new_overlay_h)
                elif watermark_position == "bottom_left":
                    pos_x, pos_y = 0, base_h - new_overlay_h
                    bbox = (0, base_h - new_overlay_h, new_overlay_w, base_h)
                else:  # bottom_right
                    pos_x, pos_y = base_w - new_overlay_w, base_h - new_overlay_h
                    bbox = (base_w - new_overlay_w, base_h - new_overlay_h, base_w, base_h)

                # Recolor if requested (before other adjustments)
                if target_color:
                    if status_label:
                        status_label.config(text=L["analyzing"] + os.path.basename(target_path))
                    overlay_resized = recolor_overlay(overlay_resized, target_color, base, bbox)
                
                # Apply opacity
                if watermark_opacity < 1.0:
                    channels = overlay_resized.split()
                    if len(channels) == 4:
                        alpha = channels[3]
                        alpha = alpha.point(lambda p: int(p * watermark_opacity))
                        overlay_resized.putalpha(alpha)

                # Auto-recolor for contrast if needed
                if auto_recolor:
                    if status_label:
                        status_label.config(text=L["analyzing"] + os.path.basename(target_path))
                    brightness = analyze_brightness(base, bbox)
                    overlay_resized = adjust_overlay_color(overlay_resized, brightness)
                
                # Combine images
                combined = base.copy()
                combined.paste(overlay_resized, (pos_x, pos_y), overlay_resized)
                
                # Save with highest quality for each format
                out_path = os.path.join(output_folder, os.path.basename(target_path))
                ext = os.path.splitext(out_path)[1].lower()
                if ext in [".jpg", ".jpeg"]:
                    combined = combined.convert("RGB")
                    combined.save(out_path, format="JPEG", quality=100, subsampling=0, optimize=True)
                elif ext == ".png":
                    combined.save(out_path, format="PNG", optimize=True, compress_level=0)
                elif ext == ".gif":
                    combined = combined.convert("RGB")
                    combined.save(out_path, format="GIF")
                elif ext == ".bmp":
                    combined = combined.convert("RGB")
                    combined.save(out_path, format="BMP")
                else:
                    combined.save(out_path)
                    
                if progress_var:
                    progress_var.set((idx + 1) / total * 100)
                    
            except Exception as e:
                print(f"Error processing {target_path}: {e}")
                return str(e)
                
        return None
    except Exception as e:
        return str(e)

def get_complementary_color(color):
    """Returns the complementary color with adjusted brightness for better contrast"""
    r, g, b = color
    # Convert to HSV for better color manipulation
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    # Rotate hue by 180 degrees
    h = (h + 0.5) % 1.0
    
    # Adjust saturation and value for better contrast
    s = min(1.0, s * 1.3)  # Increase saturation
    if v > 0.5:
        v = max(0.3, v * 0.7)  # Darken bright colors
    else:
        v = min(1.0, v * 1.8)  # Brighten dark colors
    
    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def get_predominant_color(image, bbox):
    """Analyzes the region where watermark will be placed to find predominant color"""
    region = image.crop(bbox)
    # Convert to RGB to ensure we can get color information
    region = region.convert('RGB')
    # Resize to speed up analysis
    region = region.resize((50, 50))
    
    # Get color data
    pixels = list(region.getdata())
    
    # Calculate average color
    r_total = sum(p[0] for p in pixels)
    g_total = sum(p[1] for p in pixels)
    b_total = sum(p[2] for p in pixels)
    pixel_count = len(pixels)
    
    return (
        r_total // pixel_count,
        g_total // pixel_count,
        b_total // pixel_count
    )

def recolor_overlay(overlay, target_color, base_image=None, bbox=None):
    """Recolors the overlay while preserving transparency and luminance variations."""
    if not target_color:
        return overlay
        
    # Convert to RGBA to ensure we have alpha
    overlay = overlay.convert('RGBA')
    
    # Split into channels
    channels = overlay.split()
    if len(channels) == 4:
        r, g, b, a = channels
    elif len(channels) == 3:
        r, g, b = channels
        a = Image.new('L', r.size, 255)
    else:
        return overlay
    
    # Convert to numpy arrays for better processing
    r_array = np.array(r, dtype=np.float32)
    g_array = np.array(g, dtype=np.float32)
    b_array = np.array(b, dtype=np.float32)
    
    # Calculate luminance for each pixel (preserve brightness variations)
    luminance = 0.299 * r_array + 0.587 * g_array + 0.114 * b_array
    luminance_normalized = luminance / 255.0
    
    # Create the new color base with original alpha
    target_r, target_g, target_b = target_color
    
    # Apply luminance to each channel while preserving the target color
    new_r_array = luminance_normalized * target_r
    new_g_array = luminance_normalized * target_g
    new_b_array = luminance_normalized * target_b
    
    # Clip and convert back
    new_r_array = np.clip(new_r_array, 0, 255).astype(np.uint8)
    new_g_array = np.clip(new_g_array, 0, 255).astype(np.uint8)
    new_b_array = np.clip(new_b_array, 0, 255).astype(np.uint8)
    
    # Create new channels
    new_r = Image.fromarray(new_r_array, mode='L')
    new_g = Image.fromarray(new_g_array, mode='L')
    new_b = Image.fromarray(new_b_array, mode='L')
    
    # Ensure all bands are the same size before merging
    size = a.size
    new_r = new_r.resize(size, Image.Resampling.LANCZOS) if new_r.size != size else new_r
    new_g = new_g.resize(size, Image.Resampling.LANCZOS) if new_g.size != size else new_g
    new_b = new_b.resize(size, Image.Resampling.LANCZOS) if new_b.size != size else new_b
    
    # Merge back with original alpha channel
    return Image.merge('RGBA', (new_r, new_g, new_b, a))

def process_image(target_path, overlay_path, output_folder, watermark_position, watermark_height, 
                 watermark_height_percent, watermark_opacity, auto_recolor, target_color=None):
    try:
        # Load images
        base = Image.open(target_path).convert("RGBA")
        overlay = Image.open(overlay_path).convert("RGBA")
        
        # Get dimensions
        base_w, base_h = base.size
        overlay_w, overlay_h = overlay.size

        # Adjust watermark size
        if watermark_height_percent:
            new_height = int(base_h * watermark_height_percent)
            ratio = new_height / overlay_h
            new_width = int(overlay_w * ratio)
            overlay_resized = overlay.resize((new_width, new_height), Image.Resampling.LANCZOS)
        elif watermark_height:
            ratio = watermark_height / overlay_h
            new_width = int(overlay_w * ratio)
            overlay_resized = overlay.resize((new_width, watermark_height), Image.Resampling.LANCZOS)
        else:
            overlay_resized = overlay
            
        new_overlay_w, new_overlay_h = overlay_resized.size
        
        # Recolor if requested
        if target_color:
            # Calculate watermark position for bbox
            if watermark_position == "top_left":
                pos_x, pos_y = 0, 0
            elif watermark_position == "top_right":
                pos_x, pos_y = base_w - new_overlay_w, 0
            elif watermark_position == "bottom_left":
                pos_x, pos_y = 0, base_h - new_overlay_h
            else:  # bottom_right
                pos_x, pos_y = base_w - new_overlay_w, base_h - new_overlay_h
            bbox = (pos_x, pos_y, pos_x + new_overlay_w, pos_y + new_overlay_h)
            overlay_resized = recolor_overlay(overlay_resized, target_color, base, bbox)
            
        # Apply opacity
        if watermark_opacity != 1.0:
            channels = overlay_resized.split()
            if len(channels) == 4:
                alpha = channels[3]
                alpha = alpha.point(lambda p: int(p * watermark_opacity))
                overlay_resized.putalpha(alpha)
        
        # Auto-recolor if needed
        if auto_recolor:
            # Calculate watermark position for analysis
            if watermark_position == "top_left":
                pos_x, pos_y = 0, 0
            elif watermark_position == "top_right":
                pos_x, pos_y = base_w - new_overlay_w, 0
            elif watermark_position == "bottom_left":
                pos_x, pos_y = 0, base_h - new_overlay_h
            else:  # bottom_right
                pos_x, pos_y = base_w - new_overlay_w, base_h - new_overlay_h
                
            # Analyze background brightness where watermark will be placed
            bbox = (pos_x, pos_y, pos_x + new_overlay_w, pos_y + new_overlay_h)
            brightness = analyze_brightness(base, bbox)
            overlay_resized = adjust_overlay_color(overlay_resized, brightness)
        
        # Combine images
        combined = base.copy()
        if watermark_position == "top_left":
            pos_x, pos_y = 0, 0
        elif watermark_position == "top_right":
            pos_x, pos_y = base_w - new_overlay_w, 0
        elif watermark_position == "bottom_left":
            pos_x, pos_y = 0, base_h - new_overlay_h
        else:  # bottom_right
            pos_x, pos_y = base_w - new_overlay_w, base_h - new_overlay_h
        
        combined.paste(overlay_resized, (pos_x, pos_y), overlay_resized)
        
        # Save with proper format and quality
        out_path = os.path.join(output_folder, os.path.basename(target_path))
        ext = os.path.splitext(out_path)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            combined = combined.convert("RGB")
            combined.save(out_path, format="JPEG", quality=100, subsampling=0, optimize=True)
        elif ext == ".png":
            combined.save(out_path, format="PNG", optimize=True, compress_level=0)
        elif ext == ".gif":
            combined = combined.convert("RGB")
            combined.save(out_path, format="GIF")
        elif ext == ".bmp":
            combined = combined.convert("RGB")
            combined.save(out_path, format="BMP")
        else:
            combined.save(out_path)
            
        return None
    except Exception as e:
        return str(e)

def run_gui(lang_code):
    L = LANGUAGES[lang_code]
    main_window = tk.Tk()
    main_window.title(L["title"])
    main_window.geometry("600x220")  # Increased height to prevent text cutoff
    main_window.withdraw()  # Hide window immediately and keep it hidden during prompts
    
    # Configure grid weights for centering
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_rowconfigure(0, weight=1)

    # Create main frame with centering
    main_frame = ttk.Frame(main_window, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Add title (centered)
    title_label = ttk.Label(main_frame, text=L["title"], font=("Arial", 18, "bold"), anchor="center")
    title_label.grid(row=0, column=0, pady=(10, 5), sticky="ew")
    
    # Add credits in the middle (centered)
    credits_text = "Made by Ium101 from GitHub" if lang_code == "en" else "Feito por Ium101 do GitHub"
    credits_label = ttk.Label(main_frame, text=credits_text, font=("Arial", 8), anchor="center")
    credits_label.grid(row=1, column=0, pady=(5, 10), sticky="ew")
    
    # Keep window hidden during all prompts
    main_window.withdraw()

    # Select overlay image
    overlay_path = filedialog.askopenfilename(
        title=L["select_overlay"],
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if not overlay_path:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return

    # Select target images
    target_paths = filedialog.askopenfilenames(
        title=L["select_targets"],
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if not target_paths:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return

    # Select output folder
    output_folder = filedialog.askdirectory(title=L["output_folder"])
    if not output_folder:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return

    # Prompt for recoloring (manual color selection only)
    recolor_prompt = {
        "en": "Do you want to change the color of the overlay (preserving transparency and shading)?",
        "pt": "Deseja alterar a cor da sobreposição (preservando transparência e sombreamento)?"
    }
    do_recolor = messagebox.askyesno(L["title"], recolor_prompt[lang_code])
    if do_recolor is None:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return
    
    target_color = None
    if do_recolor:
        from tkinter.colorchooser import askcolor
        color_prompt = {
            "en": "Choose the new base color for the overlay",
            "pt": "Escolha a nova cor base para a sobreposição"
        }
        result = askcolor(title=color_prompt[lang_code])
        if result[0] is None:
            try:
                main_window.destroy()
            except:
                pass
            os._exit(0)
            return
        target_color = result[0]

    # Auto-recolor prompt for tone adjustment (keep this unchanged)
    auto_recolor = messagebox.askyesno(L["title"], L["auto_recolor"])
    if auto_recolor is None:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return

    # Prompt for watermark height
    height_prompt = {
        "en": "Enter watermark height in pixels or percentage (e.g. 50 for 50px, 50% for 50% of image height, blank for default):",
        "pt": "Digite a altura da marca d'água em pixels ou porcentagem (ex: 50 para 50px, 50% para 50% da altura da imagem, deixe em branco para padrão):"
    }
    height_str = tk.simpledialog.askstring(L["title"], height_prompt[lang_code], parent=main_window)
    if height_str is None:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return
    
    # Process height input
    watermark_height = None
    watermark_height_percent = None
    if height_str:
        s = height_str.strip()
        if s.endswith('%'):
            try:
                watermark_height_percent = float(s.replace('%','')) / 100.0
            except Exception:
                watermark_height_percent = None
        else:
            try:
                if '.' in s:
                    watermark_height_percent = float(s) / 100.0
                else:
                    watermark_height = int(s)
            except Exception:
                watermark_height = None
                watermark_height_percent = None
    
    # Prompt for watermark opacity
    opacity_prompt = {
        "en": "Choose watermark opacity (0-100%, e.g. 50 for 50%, default is 100):",
        "pt": "Escolha a opacidade da marca d'água (0-100%, por exemplo 50 para 50%, padrão é 100):"
    }
    opacity_str = tk.simpledialog.askstring(L["title"], opacity_prompt[lang_code], parent=main_window)
    if opacity_str is None:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return
        
    watermark_opacity = 1.0
    if opacity_str:
        s = opacity_str.strip().replace(',', '.')
        try:
            if s.endswith('%'):
                percent = float(s.replace('%',''))
            else:
                percent = float(s)
            if percent < 1:
                percent = 1
            elif percent > 100:
                percent = 100
            watermark_opacity = percent / 100.0
        except Exception:
            watermark_opacity = 1.0
    
    # Prompt for position
    position_prompt = {
        "en": "Choose watermark position: top left, top right, bottom left, bottom right (default is bottom right):",
        "pt": "Escolha a posição da marca d'água para o canto: superior esquerdo, superior direito, inferior esquerdo, inferior direito (padrão é inferior direito):"
    }
    position_str = tk.simpledialog.askstring(L["title"], position_prompt[lang_code], parent=main_window)
    if position_str is None:
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
        return
        
    position_map = {
        "top left": "top_left",
        "superior esquerdo": "top_left",
        "top right": "top_right",
        "superior direito": "top_right",
        "bottom left": "bottom_left",
        "inferior esquerdo": "bottom_left",
        "bottom right": "bottom_right",
        "inferior direito": "bottom_right"
    }
    watermark_position = position_map.get(position_str.strip().lower() if position_str else "", "bottom_right")
            
    # Clear main frame for processing display
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Update progress display
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(main_frame, length=500, mode='determinate', variable=progress_var)
    progress_bar.grid(row=0, column=0, pady=(20, 10), padx=10)
    
    # Status label with wraplength to handle long filenames
    status_label = ttk.Label(main_frame, text="", font=("Arial", 10), wraplength=560, anchor="center", justify="center")
    status_label.grid(row=1, column=0, pady=(10, 10), padx=20, sticky="ew")
    
    # Add credits back at the bottom
    credits_text = "Made by Ium101 from GitHub" if lang_code == "en" else "Feito por Ium101 do GitHub"
    credits_label = ttk.Label(main_frame, text=credits_text, font=("Arial", 8), anchor="center")
    credits_label.grid(row=2, column=0, pady=(10, 20), sticky="ew")
    
    main_window.deiconify()
    main_window.update()
    
    # Process all images automatically
    total = len(target_paths)
    for i, target_path in enumerate(target_paths):
        try:
            # Update status with current file - show full filename
            filename = os.path.basename(target_path)
            status_label.config(text=L["processing"] + filename)
            progress_var.set((i / total) * 100)
            main_window.update()
            
            result = process_image(
                target_path,
                overlay_path,
                output_folder,
                watermark_position,
                watermark_height,
                watermark_height_percent,
                watermark_opacity,
                auto_recolor,
                target_color
            )
            
            if result:
                error_message = L["error"] + str(result)
                messagebox.showerror(L["title"], error_message)
                try:
                    main_window.destroy()
                    main_window.quit()
                except:
                    pass
                return
        except Exception as e:
            messagebox.showerror(L["error"], str(e))
            main_window.destroy()
            return
    
    # Show completion message and close
    try:
        progress_var.set(100)
        status_label.config(text=L["done"])
        main_window.update()
        messagebox.showinfo(L["title"], L["success"])
    finally:
        try:
            # Destroy all widgets first
            for widget in main_window.winfo_children():
                widget.destroy()
        except:
            pass
        try:
            main_window.destroy()
        except:
            pass
        os._exit(0)
    
def show_language_selection():
    root = tk.Tk()
    root.title("Image Overlay / Sobreposição de Imagem")
    root.geometry("500x400")  # Increased height to show all text
    root.resizable(False, False)

    # Configure grid for vertical centering
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    # Create main frame with more padding
    frame = ttk.Frame(root, padding="30")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.grid_columnconfigure(0, weight=1)
    
    # Title (centered)
    title = ttk.Label(frame, text="Image Overlay", font=("Arial", 24, "bold"), anchor="center")
    title.grid(row=0, column=0, pady=(10, 5), sticky="ew")
    
    # Subtitle (centered)
    subtitle = ttk.Label(frame, text="Sobreposição de Imagem", font=("Arial", 24, "bold"), anchor="center")
    subtitle.grid(row=1, column=0, pady=(5, 20), sticky="ew")
    
    # Language buttons with improved style
    style = ttk.Style()
    style.configure("Lang.TButton", padding=10, font=("Arial", 11))
    
    def start_with_language(lang):
        root.destroy()
        run_gui(lang)
    
    btn_en = ttk.Button(frame, text="Continue in English",
                      command=lambda: start_with_language("en"),
                      style="Lang.TButton")
    btn_en.grid(row=2, column=0, pady=(10, 5), sticky=tk.EW, padx=20)
    
    btn_pt = ttk.Button(frame, text="Continuar em Português Brasileiro",
                      command=lambda: start_with_language("pt"),
                      style="Lang.TButton")
    btn_pt.grid(row=3, column=0, pady=(5, 20), sticky=tk.EW, padx=20)
    
    # Credits with separator (centered)
    ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, sticky=tk.EW, pady=(15, 15), padx=20)
    credits = ttk.Label(frame, text="Made by Ium101 from GitHub", font=("Arial", 9), anchor="center")
    credits.grid(row=5, column=0, pady=(5, 5), sticky="ew")
    credits_pt = ttk.Label(frame, text="Feito por Ium101 do GitHub", font=("Arial", 9), anchor="center")
    credits_pt.grid(row=6, column=0, pady=(5, 15), sticky="ew")
    
    root.mainloop()

if __name__ == "__main__":
    try:
        show_language_selection()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            # Clean up any remaining tkinter windows
            root = tk.Tk()
            root.destroy()
        except:
            pass
        # Force exit
        os._exit(0)