import os
import shutil
import cairosvg

from PIL import Image, ImageDraw, ImageFont, ImageOps


def add_text_to_icon(icon_file, text, height, font_size, text_color):
    icon = Image.open(icon_file)
    font = ImageFont.truetype("/usr/share/fonts/abattis-cantarell-fonts/Cantarell-Bold.otf", font_size)
    text_width, text_height = font.getbbox(text)[-2:]
    image_width = height + text_width + 5
    image_height = height
    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    icon = icon.resize((height, height), Image.Resampling.LANCZOS)
    icon_pos = (0, int((image_height - height) / 2))
    image.paste(icon, icon_pos)
    draw = ImageDraw.Draw(image)
    text_pos = (height + 5, int((image_height - text_height) / 2 - (text_height / 10)))
    draw.text(text_pos, text, font=font, fill=text_color)
    return image


def image_from_text(text, font_size, text_color):
    font = ImageFont.truetype("/usr/share/fonts/abattis-cantarell-fonts/Cantarell-Bold.otf", font_size)
    text_width, text_height = font.getbbox(text)[-2:]
    image_width = text_width
    image_height = text_height
    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    text_pos = ((image_width - text_width) / 2, (image_height - text_height) / 2 - 5)
    draw.text(text_pos, text, font=font, fill=text_color)
    return image


def logo_export(file, size: tuple, location: str):
    cairosvg.svg2png(
        url=file,
        parent_width=size[0],
        parent_height=size[1],
        write_to=open(location, "wb+")
    )


def invert_image(image_file):
    img = Image.open(image_file)
    r, g, b, a = img.split()
    r, g, b = map(lambda i: ImageOps.invert(i), (r, g, b))
    Image.merge(img.mode, (r, g, b, a)).save(image_file)


class Package:
    def __init__(self, name, version, revision):
        self.name = name
        self.version = version
        self.revision = revision

    def generate(self, location):
        raise NotImplementedError("generate() not implemented")


class DistroLogosPackage(Package):
    def __init__(self, version, revision, distro_id, distro_name, logo, symbolic_logo):
        super().__init__(f"{distro_id}-logos", version, revision)
        self.distro_id = distro_id
        self.distro_name = distro_name
        self.logo = logo
        self.symbolic_logo = symbolic_logo

    def generate(self, location):
        # Making directories
        shutil.rmtree(location, ignore_errors=True)
        shutil.copytree("/rbuild/PackageTemplates/distro-logos", location)

        # Creating anaconda-header.png
        anaconda_header = image_from_text(self.distro_name, 36, (177, 177, 177))
        anaconda_header.save(f"{location}/anaconda/anaconda_header.png")

        # Classic anaconda header
        anaconda_header_classic = image_from_text(self.distro_name, 36, (0, 0, 0))
        anaconda_header_classic.save(f"{location}/anaconda/anaconda_header_classic.png")

        # Symbolic logo exports
        logo_export(self.symbolic_logo, (128, 128), f"{location}/anaconda/sidebar-logo.png")
        logo_export(self.symbolic_logo, (128, 128), f"{location}/anaconda/sidebar-logo_classic.png")
        logo_export(self.symbolic_logo, (48, 48), f"{location}/icons/hicolor/48x48/apps/fedora-logo-icon-symbolic.png")
        logo_export(self.symbolic_logo, (48, 48), f"{location}/icons/hicolor/48x48/apps/{self.distro_id}-logo-icon-symbolic.png")
        logo_export(self.symbolic_logo, (512, 512), f"{location}/pixmaps/system-logo-white.png")

        invert_image(f"{location}/anaconda/sidebar-logo.png")
        invert_image(f"{location}/anaconda/sidebar-logo_classic.png")
        invert_image(f"{location}/pixmaps/system-logo-white.png")

        # Logo exports
        logo_export(self.logo, (512, 512), f"{location}/logo.png")
        logo_export(self.logo, (512, 512), f"{location}/logo-symbolic.png")
        logo_export(self.logo, (128, 128), f"{location}/icons/hicolor/48x48/apps/fedora-logo-icon.png")
        logo_export(self.logo, (128, 128), f"{location}/icons/hicolor/48x48/apps/{self.distro_id}-logo-icon.png")
        logo_export(self.logo, (512, 512), f"{location}/pixmaps/fedora-logo-sprite.png")
        shutil.copy(self.logo, f"{location}/pixmaps/fedora-logo-sprite.svg")

        # Long logo exports
        gdm_logo = add_text_to_icon(f"{location}/logo.png", self.distro_name, 43, 40, (255, 255, 255))
        gdm_logo.save(f"{location}/pixmaps/fedora-gdm-logo.png")
        fedora_logo = add_text_to_icon(f"{location}/logo.png", self.distro_name, 164, 161, (0, 0, 0))
        fedora_logo.save(f"{location}/pixmaps/fedora-logo.png")
        fedora_logo_med = add_text_to_icon(f"{location}/logo.png", self.distro_name, 80, 77, (255, 255, 255))
        fedora_logo_med.save(f"{location}/pixmaps/fedora_logo_med.png")
        fedora_logo_small = add_text_to_icon(f"{location}/logo.png", self.distro_name, 47, 44, (0, 0, 0))
        fedora_logo_small.save(f"{location}/pixmaps/fedora-logo-small.png")
        whitelogo = add_text_to_icon(f"{location}/logo.png", self.distro_name, 164, 161, (255, 255, 255))
        whitelogo.save(f"{location}/pixmaps/fedora_whitelogo.png")
        whitelogo_med = add_text_to_icon(f"{location}/logo.png", self.distro_name, 80, 77, (255, 255, 255))
        whitelogo_med.save(f"{location}/pixmaps/fedora_whitelogo_med.png")
        whitelogo_small = add_text_to_icon(f"{location}/logo.png", self.distro_name, 47, 44, (255, 255, 255))
        whitelogo_small.save(f"{location}/pixmaps/fedora_whitelogo_small.png")

        shutil.copy(self.logo, f"{location}/pixmaps/fedora-logo-sprite.svg")
        shutil.copy(self.logo, f"{location}/icons/hicolor/scalable/apps/fedora-logo-icon.svg")
        shutil.copy(self.logo, f"{location}/icons/hicolor/scalable/apps/{self.distro_id}-logo-icon.svg")
        shutil.copy(self.symbolic_logo, f"{location}/icons/hicolor/symbolic/apps/fedora-logo-icon-symbolic.svg")
        shutil.copy(self.symbolic_logo, f"{location}/icons/hicolor/symbolic/apps/{self.distro_id}-logo-icon-symbolic.svg")
        
        # Replace distro name in spec
        with open(f"{location}/distro-logos.spec", "r") as f:
            spec = f.read()
            spec = spec.replace("{distroname}", self.distro_id)
            spec = spec.replace("{packageversion}", self.version)
            spec = spec.replace("{packagerelease}", self.revision)
        with open(f"{location}/distro-logos.spec", "w") as f:
            f.write(spec)
        # Rename spec
        os.rename(f"{location}/distro-logos.spec", f"{location}/{self.name}.spec")


        #logo = Image.open(self.logo)


test = DistroLogosPackage("18.0.4", "1", "rmakeros", "rMaker", "/home/cameron/Documents/rMaker/PackageTemplates/distro-logos/logo.svg", "/home/cameron/Documents/rMaker/PackageTemplates/distro-logos/logo_symbolic.svg")
test.generate("/home/cameron/Documents/rMaker/PackageTemplates/distro-logos2")