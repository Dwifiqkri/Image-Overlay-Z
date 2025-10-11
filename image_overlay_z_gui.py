import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

LANGUAGES = {
    "en": {
        "title": "Image Overlay",
        "select_overlay": "Select the overlay image (with transparent background)",
        "select_targets": "Select the target images to apply the overlay",
        "success": "Overlay applied successfully to all images!",
        "error": "Error applying overlay: {err}",
        "output_folder": "Select output folder for processed images",
        "done": "Done!",
        "exit": "Press any button to exit"
    },
    "pt": {
        "title": "Sobreposição de Imagem",
        "select_overlay": "Selecione a imagem de sobreposição (com fundo transparente)",
        "select_targets": "Selecione as imagens alvo para aplicar a sobreposição",
        "success": "Sobreposição aplicada com sucesso a todas as imagens!",
        "error": "Erro ao aplicar sobreposição: {err}",
        "output_folder": "Selecione a pasta de saída para as imagens processadas",
        "done": "Concluído!",
        "exit": "Pressione qualquer botão para sair"
    }
}

def overlay_images(overlay_path, target_paths, output_folder, watermark_height=None, watermark_opacity=1.0, watermark_height_percent=None, watermark_position="bottom_right"):
    overlay = Image.open(overlay_path).convert("RGBA")
    overlay_w, overlay_h = overlay.size
    for target_path in target_paths:
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
            # Apply opacity
            if watermark_opacity < 1.0:
                alpha = overlay_resized.split()[3]
                alpha = alpha.point(lambda p: int(p * watermark_opacity))
                overlay_resized.putalpha(alpha)
            combined = base.copy()
            # Watermark position logic
            if watermark_position == "top_left":
                pos_x, pos_y = 0, 0
            elif watermark_position == "top_right":
                pos_x, pos_y = base_w - new_overlay_w, 0
            elif watermark_position == "bottom_left":
                pos_x, pos_y = 0, base_h - new_overlay_h
            else:  # bottom_right
                pos_x, pos_y = base_w - new_overlay_w, base_h - new_overlay_h
            combined.paste(overlay_resized, (pos_x, pos_y), overlay_resized)
            out_path = os.path.join(output_folder, os.path.basename(target_path))
            ext = os.path.splitext(out_path)[1].lower()
            # Save with highest quality for each format
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
        except Exception as e:
            print(f"Error processing {target_path}: {e}")
    return None

def run_gui(lang_code):
    L = LANGUAGES[lang_code]
    root = tk.Tk()
    root.withdraw()
    # Create a larger initial window with credits
    splash = tk.Toplevel()
    splash.title(L["title"])
    splash.geometry("500x220")
    splash.resizable(False, False)
    label = tk.Label(splash, text=L["title"], font=("Arial", 18, "bold"))
    label.pack(pady=30)
    credits_text = "Image Overlay Tool by Ium101 - 2025"
    credits_label = tk.Label(splash, text=credits_text, font=("Arial", 9), fg="gray")
    credits_label.pack(side="bottom", pady=10)
    splash.update()
    splash.after(1200, splash.destroy)
    splash.wait_window()
    overlay_path = filedialog.askopenfilename(title=L["select_overlay"], filetypes=[("PNG Images", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not overlay_path:
        messagebox.showinfo(L["title"], L["exit"])
        return
    target_paths = filedialog.askopenfilenames(title=L["select_targets"], filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not target_paths:
        messagebox.showinfo(L["title"], L["exit"])
        return
    output_folder = filedialog.askdirectory(title=L["output_folder"])
    if not output_folder:
        messagebox.showinfo(L["title"], L["exit"])
        return
    # Prompt for watermark height (pixels or percentage)
    height_prompt = {
        "en": "Enter watermark height in pixels or percentage (e.g. 50 for 50px, 10% for 10% of image height, blank for default):",
        "pt": "Digite a altura da marca d'água em pixels ou porcentagem (ex: 50 para 50px, 10% para 10% da altura da imagem, deixe em branco para padrão):"
    }
    root.deiconify()
    height_str = tk.simpledialog.askstring(L["title"], height_prompt[lang_code], parent=root)
    root.withdraw()
    watermark_height = None
    watermark_height_percent = None
    if height_str:
        if height_str.strip().endswith('%'):
            try:
                watermark_height_percent = float(height_str.strip().replace('%','')) / 100.0
            except Exception:
                watermark_height_percent = None
        else:
            try:
                watermark_height = int(height_str)
            except Exception:
                watermark_height = None
    # Prompt for opacity (percentage)
    opacity_prompt = {
        "en": "Choose watermark opacity (0-100%, e.g. 75 for 75%, default is 100):",
        "pt": "Escolha a opacidade da marca d'água (0-100%, por exemplo 75 para 75%, padrão é 100):"
    }
    root.deiconify()
    opacity_str = tk.simpledialog.askstring(L["title"], opacity_prompt[lang_code], parent=root)
    root.withdraw()
    watermark_opacity = 1.0
    if opacity_str:
        try:
            percent = int(opacity_str)
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
        "pt": "Escolha a posição da marca d'água: canto superior esquerdo, superior direito, inferior esquerdo, inferior direito (padrão é inferior direito):"
    }
    root.deiconify()
    position_str = tk.simpledialog.askstring(L["title"], position_prompt[lang_code], parent=root)
    root.withdraw()
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
    watermark_position = position_map.get(position_str.strip().lower(), "bottom_right") if position_str else "bottom_right"
    err = overlay_images(overlay_path, target_paths, output_folder, watermark_height, watermark_opacity, watermark_height_percent, watermark_position)
    if err:
        messagebox.showerror(L["title"], L["error"].format(err=err))
    else:
        messagebox.showinfo(L["title"], L["success"])
        root.destroy()
        import sys
        sys.exit()

    def main_window():
        root = tk.Tk()
        root.title("Image Overlay")
        root.geometry("400x220")
        btn_en = tk.Button(root, text="Proceed in English", command=lambda: [root.destroy(), run_gui("en")], height=2, width=30)
        btn_en.pack(pady=10)
        btn_pt = tk.Button(root, text="Prosseguir em Português Brasileiro", command=lambda: [root.destroy(), run_gui("pt")], height=2, width=30)
        btn_pt.pack(pady=10)
        credits_lbl = tk.Label(root, text="Feito pelo Usuário Ium101 do GitHub / Made by User Ium101 from GitHub", font=("Arial", 8))
        credits_lbl.pack(side="bottom", pady=10)
    err = overlay_images(overlay_path, target_paths, output_folder, watermark_height, watermark_opacity, watermark_height_percent)

    if __name__ == "__main__":
        main_window()

if __name__ == "__main__":
    # Simple language selection
    lang_choice = tk.simpledialog.askstring("Language", "Select language / Selecione o idioma:\n1. Português Brasileiro\n2. English\nEnter 1 or 2:")
    lang_code = "pt" if lang_choice == "1" else "en"
    run_gui(lang_code)
