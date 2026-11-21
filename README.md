# Website Builder

Built by [VisionQuantech](https://visionquantech.com) — AI agents, apps & tools for small businesses.

**Desktop GUI app (tkinter)** — template-based website generator (Business, Portfolio, E-commerce, Blog, Landing Page, Restaurant). Fills in name/description/contact/colors, generates HTML, preview in window or browser, save to file.

## Run

The module has no `__main__` launcher — launch it like this:

```bash
xvfb-run -a python -c "
import tkinter as tk
from website_builder import WebsiteBuilder
root = tk.Tk()
WebsiteBuilder(root)
root.mainloop()
"
```

## Deps

Standard library + tkinter only.

## Notes

- Fixed 2026-09-24: added the missing `generate_restaurant_template` method (was referenced in the template dict but undefined, which crashed the GUI at construction).
- All 6 templates generate valid HTML — verified programmatically.
- Desktop app — needs a display; not a web service.