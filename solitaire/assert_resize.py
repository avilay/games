from pathlib import Path

from PIL import Image

orig_res_root = Path.home() / "projects" / "github" / "games" / "solitaire" / "orig-assets"

native_res_root = Path.home() / "projects" / "github" / "games" / "solitaire" / "native-assets"
native_newsize = (90, 130)

web_res_root = Path.home() / "projects" / "github" / "games" / "solitaire" / "src" / "web-assets"
web_newsize = (135, 194)

for filename in orig_res_root.glob("**/*.png"):
    for new_res_root, newsize in zip((native_res_root, web_res_root), (native_newsize, web_newsize)):
        new_filename = Path(str(filename).replace(str(orig_res_root), str(new_res_root)))
        new_filename.parent.mkdir(parents=True, exist_ok=True)
        img = Image.open(str(filename))
        img = img.resize(
            size=newsize,
            resample=Image.Resampling.LANCZOS
        )
        img.save(str(new_filename))
