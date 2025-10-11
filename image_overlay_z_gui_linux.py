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

def overlay_images(overlay_path, target_paths, output_folder):
    overlay = Image.open(overlay_path).convert("RGBA")
    for target_path in target_paths:
        try:
            base = Image.open(target_path).convert("RGBA")
            overlay_resized = overlay.resize(base.size, Image.ANTIALIAS)
            combined = Image.alpha_composite(base, overlay_resized)
            out_path = os.path.join(output_folder, os.path.basename(target_path))
            combined.save(out_path)
        except Exception as e:
            return str(e)
    return None

def run_gui(lang_code):
    L = LANGUAGES[lang_code]
    root = tk.Tk()
    root.withdraw()
    overlay_path = filedialog.askopenfilename(title=L["select_overlay"], filetypes=[("PNG Images", "*.png")])
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
    err = overlay_images(overlay_path, target_paths, output_folder)
    if err:
        messagebox.showerror(L["title"], L["error"].format(err=err))
    else:
        messagebox.showinfo(L["title"], L["success"])
    messagebox.showinfo(L["title"], L["done"])
    root.destroy()

if __name__ == "__main__":
    lang_choice = tk.simpledialog.askstring("Language", "Select language / Selecione o idioma:\n1. Português Brasileiro\n2. English\nEnter 1 or 2:")
    lang_code = "pt" if lang_choice == "1" else "en"
    run_gui(lang_code)
