import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, colorchooser
import os
import json
import webbrowser
from datetime import datetime

class WebsiteBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Website Builder - Production Ready")
        self.root.geometry("1000x700")
        
        # Color scheme
        self.primary_color = "#2563eb"
        self.secondary_color = "#1e40af"
        
        # Templates
        self.templates = {
            "Business": self.generate_business_template,
            "Portfolio": self.generate_portfolio_template,
            "E-commerce": self.generate_ecommerce_template,
            "Blog": self.generate_blog_template,
            "Landing Page": self.generate_landing_template,
            "Restaurant": self.generate_restaurant_template
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="🌐 Automatic Website Builder", 
                              font=("Arial", 20, "bold"), fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left Panel - Inputs
        input_frame = ttk.LabelFrame(main_frame, text="Website Configuration", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Website Name
        ttk.Label(input_frame, text="Website Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.website_name = ttk.Entry(input_frame, width=30)
        self.website_name.grid(row=0, column=1, pady=5)
        self.website_name.insert(0, "My Awesome Website")
        
        # Template Selection
        ttk.Label(input_frame, text="Template:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar(value="Business")
        template_combo = ttk.Combobox(input_frame, textvariable=self.template_var, 
                                     values=list(self.templates.keys()), state="readonly", width=28)
        template_combo.grid(row=1, column=1, pady=5)
        
        # Business Description
        ttk.Label(input_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.description = scrolledtext.ScrolledText(input_frame, width=30, height=4)
        self.description.grid(row=2, column=1, pady=5)
        self.description.insert(1.0, "We provide innovative solutions for your business needs.")
        
        # Contact Email
        ttk.Label(input_frame, text="Contact Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email = ttk.Entry(input_frame, width=30)
        self.email.grid(row=3, column=1, pady=5)
        self.email.insert(0, "info@example.com")
        
        # Phone
        ttk.Label(input_frame, text="Phone:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.phone = ttk.Entry(input_frame, width=30)
        self.phone.grid(row=4, column=1, pady=5)
        self.phone.insert(0, "+1 (555) 123-4567")
        
        # Primary Color
        ttk.Label(input_frame, text="Primary Color:").grid(row=5, column=0, sticky=tk.W, pady=5)
        color_frame = ttk.Frame(input_frame)
        color_frame.grid(row=5, column=1, pady=5, sticky=tk.W)
        self.color_display = tk.Label(color_frame, bg=self.primary_color, width=10, relief="solid")
        self.color_display.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(color_frame, text="Choose Color", command=self.choose_color).pack(side=tk.LEFT)
        
        # Features
        ttk.Label(input_frame, text="Features (comma separated):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.features = scrolledtext.ScrolledText(input_frame, width=30, height=3)
        self.features.grid(row=6, column=1, pady=5)
        self.features.insert(1.0, "Fast Delivery, Quality Service, 24/7 Support")
        
        # Social Media
        ttk.Label(input_frame, text="Social Links:").grid(row=7, column=0, sticky=tk.W, pady=5)
        social_frame = ttk.Frame(input_frame)
        social_frame.grid(row=7, column=1, sticky=tk.W)
        
        ttk.Label(social_frame, text="Facebook:").pack(anchor=tk.W)
        self.facebook = ttk.Entry(social_frame, width=30)
        self.facebook.pack(anchor=tk.W)
        
        ttk.Label(social_frame, text="Twitter:").pack(anchor=tk.W)
        self.twitter = ttk.Entry(social_frame, width=30)
        self.twitter.pack(anchor=tk.W)
        
        ttk.Label(social_frame, text="LinkedIn:").pack(anchor=tk.W)
        self.linkedin = ttk.Entry(social_frame, width=30)
        self.linkedin.pack(anchor=tk.W)
        
        # Right Panel - Preview & Actions
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        
        # Preview
        preview_frame = ttk.LabelFrame(right_frame, text="HTML Preview", padding="10")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        
        self.preview = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, width=50, height=20)
        self.preview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(button_frame, text="🔨 Generate Website", 
                  command=self.generate_website).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save to File", 
                  command=self.save_website).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🌐 Preview in Browser", 
                  command=self.preview_in_browser).pack(side=tk.LEFT, padx=5)
        
        # Status Bar
        self.status = tk.Label(main_frame, text="Ready to build your website", 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Primary Color")
        if color[1]:
            self.primary_color = color[1]
            self.color_display.config(bg=self.primary_color)
            
    def get_user_data(self):
        return {
            "name": self.website_name.get(),
            "description": self.description.get(1.0, tk.END).strip(),
            "email": self.email.get(),
            "phone": self.phone.get(),
            "color": self.primary_color,
            "features": [f.strip() for f in self.features.get(1.0, tk.END).strip().split(",")],
            "social": {
                "facebook": self.facebook.get(),
                "twitter": self.twitter.get(),
                "linkedin": self.linkedin.get()
            }
        }
    
    def generate_website(self):
        template = self.template_var.get()
        data = self.get_user_data()
        
        if template in self.templates:
            html_content = self.templates[template](data)
            self.preview.delete(1.0, tk.END)
            self.preview.insert(1.0, html_content)
            self.status.config(text=f"✓ {template} website generated successfully!")
            self.current_html = html_content
        else:
            messagebox.showerror("Error", "Invalid template selected")
    
    def save_website(self):
        if not hasattr(self, 'current_html'):
            messagebox.showwarning("Warning", "Please generate a website first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialfile=f"{self.website_name.get().replace(' ', '_').lower()}.html"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.current_html)
                self.status.config(text=f"✓ Website saved to {file_path}")
                messagebox.showinfo("Success", f"Website saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def preview_in_browser(self):
        if not hasattr(self, 'current_html'):
            messagebox.showwarning("Warning", "Please generate a website first!")
            return
        
        temp_file = "temp_preview.html"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(self.current_html)
        
        webbrowser.open('file://' + os.path.abspath(temp_file))
        self.status.config(text="✓ Website opened in browser")
    
    def generate_business_template(self, data):
        features_html = "\n".join([f'<div class="feature"><div class="feature-icon">✓</div><h3>{feature}</h3></div>' 
                                  for feature in data['features']])
        
        social_html = ""
        if data['social']['facebook']:
            social_html += f'<a href="{data["social"]["facebook"]}" class="social-link">Facebook</a>'
        if data['social']['twitter']:
            social_html += f'<a href="{data["social"]["twitter"]}" class="social-link">Twitter</a>'
        if data['social']['linkedin']:
            social_html += f'<a href="{data["social"]["linkedin"]}" class="social-link">LinkedIn</a>'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, {data['color']} 0%, {data['color']}dd 100%);
            color: white;
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .nav {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }}
        .logo {{
            font-size: 1.8rem;
            font-weight: bold;
        }}
        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}
        .nav-links a {{
            color: white;
            text-decoration: none;
            transition: opacity 0.3s;
        }}
        .nav-links a:hover {{
            opacity: 0.8;
        }}
        .hero {{
            background: linear-gradient(135deg, {data['color']}22 0%, {data['color']}44 100%);
            padding: 5rem 2rem;
            text-align: center;
        }}
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            color: {data['color']};
        }}
        .hero p {{
            font-size: 1.3rem;
            max-width: 800px;
            margin: 0 auto 2rem;
            color: #555;
        }}
        .cta-button {{
            display: inline-block;
            padding: 1rem 2.5rem;
            background: {data['color']};
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.1rem;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        .features {{
            max-width: 1200px;
            margin: 4rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }}
        .feature {{
            text-align: center;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .feature:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        .feature-icon {{
            font-size: 3rem;
            color: {data['color']};
            margin-bottom: 1rem;
        }}
        .about {{
            background: #f8f9fa;
            padding: 4rem 2rem;
            text-align: center;
        }}
        .about-content {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .about h2 {{
            font-size: 2.5rem;
            color: {data['color']};
            margin-bottom: 1.5rem;
        }}
        .contact {{
            max-width: 600px;
            margin: 4rem auto;
            padding: 0 2rem;
        }}
        .contact h2 {{
            text-align: center;
            font-size: 2.5rem;
            color: {data['color']};
            margin-bottom: 2rem;
        }}
        .contact-info {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .contact-item {{
            margin: 1rem 0;
            font-size: 1.1rem;
        }}
        .contact-item strong {{
            color: {data['color']};
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }}
        .social-links {{
            margin: 1rem 0;
        }}
        .social-link {{
            color: white;
            text-decoration: none;
            margin: 0 1rem;
            transition: opacity 0.3s;
        }}
        .social-link:hover {{
            opacity: 0.7;
        }}
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            .nav-links {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">{data['name']}</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <section id="home" class="hero">
        <h1>Welcome to {data['name']}</h1>
        <p>{data['description']}</p>
        <a href="#contact" class="cta-button">Get Started</a>
    </section>

    <section id="features" class="features">
        {features_html}
    </section>

    <section id="about" class="about">
        <div class="about-content">
            <h2>About Us</h2>
            <p>{data['description']}</p>
            <p>We are committed to delivering excellence and exceeding expectations in everything we do.</p>
        </div>
    </section>

    <section id="contact" class="contact">
        <h2>Contact Us</h2>
        <div class="contact-info">
            <div class="contact-item"><strong>Email:</strong> {data['email']}</div>
            <div class="contact-item"><strong>Phone:</strong> {data['phone']}</div>
            <div class="contact-item"><strong>Address:</strong> 123 Business Street, City, Country</div>
        </div>
    </section>

    <footer class="footer">
        <div class="social-links">
            {social_html}
        </div>
        <p>&copy; {datetime.now().year} {data['name']}. All rights reserved.</p>
    </footer>
</body>
</html>'''

    def generate_portfolio_template(self, data):
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} - Portfolio</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Arial', sans-serif;
            background: #0a0a0a;
            color: #fff;
        }}
        .hero {{
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(135deg, {data['color']}33 0%, #0a0a0a 100%);
        }}
        .hero h1 {{
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: fadeInUp 1s ease;
        }}
        .hero p {{
            font-size: 1.5rem;
            opacity: 0.8;
            animation: fadeInUp 1.2s ease;
        }}
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .section {{
            max-width: 1200px;
            margin: 4rem auto;
            padding: 0 2rem;
        }}
        .section h2 {{
            font-size: 2.5rem;
            margin-bottom: 2rem;
            color: {data['color']};
        }}
        .skills {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }}
        .skill {{
            background: #1a1a1a;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s;
        }}
        .skill:hover {{
            transform: scale(1.05);
            background: {data['color']}22;
        }}
        .contact {{
            text-align: center;
            padding: 4rem 2rem;
        }}
        .contact a {{
            display: inline-block;
            margin: 1rem;
            padding: 1rem 2rem;
            background: {data['color']};
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div>
            <h1>{data['name']}</h1>
            <p>{data['description']}</p>
        </div>
    </section>
    
    <section class="section">
        <h2>Skills & Expertise</h2>
        <div class="skills">
            {' '.join([f'<div class="skill"><h3>{skill}</h3></div>' for skill in data['features']])}
        </div>
    </section>
    
    <section class="contact">
        <h2>Let's Work Together</h2>
        <a href="mailto:{data['email']}">Contact Me</a>
    </section>
</body>
</html>'''

    def generate_ecommerce_template(self, data):
        products = [
            {"name": "Product 1", "price": "$99.99"},
            {"name": "Product 2", "price": "$149.99"},
            {"name": "Product 3", "price": "$79.99"},
            {"name": "Product 4", "price": "$199.99"}
        ]
        
        products_html = "\n".join([
            f'''<div class="product">
                <div class="product-image">📦</div>
                <h3>{p['name']}</h3>
                <p class="price">{p['price']}</p>
                <button class="buy-btn">Add to Cart</button>
            </div>''' for p in products
        ])
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} - Shop</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; }}
        .header {{
            background: {data['color']};
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{ font-size: 1.5rem; font-weight: bold; }}
        .cart {{ font-size: 1.5rem; cursor: pointer; }}
        .banner {{
            background: linear-gradient(135deg, {data['color']}44, {data['color']}88);
            padding: 4rem 2rem;
            text-align: center;
        }}
        .banner h1 {{ font-size: 3rem; color: white; margin-bottom: 1rem; }}
        .products {{
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }}
        .product {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .product:hover {{ transform: translateY(-5px); }}
        .product-image {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        .price {{
            font-size: 1.5rem;
            color: {data['color']};
            font-weight: bold;
            margin: 1rem 0;
        }}
        .buy-btn {{
            background: {data['color']};
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
        }}
        .buy-btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <header class="header">
        <div class="logo">{data['name']}</div>
        <div class="cart">🛒 (0)</div>
    </header>
    
    <section class="banner">
        <h1>Welcome to Our Store</h1>
        <p>{data['description']}</p>
    </section>
    
    <section class="products">
        {products_html}
    </section>
</body>
</html>'''

    def generate_blog_template(self, data):
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Georgia, serif; line-height: 1.8; color: #333; }}
        .header {{
            background: white;
            border-bottom: 3px solid {data['color']};
            padding: 2rem;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5rem; color: {data['color']}; }}
        .container {{ max-width: 800px; margin: 3rem auto; padding: 0 2rem; }}
        .post {{
            background: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .post h2 {{ color: {data['color']}; margin-bottom: 0.5rem; }}
        .post-meta {{ color: #888; margin-bottom: 1rem; font-size: 0.9rem; }}
        .read-more {{
            color: {data['color']};
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>{data['name']}</h1>
        <p>{data['description']}</p>
    </header>
    
    <div class="container">
        <article class="post">
            <h2>Welcome to My Blog</h2>
            <div class="post-meta">Posted on {datetime.now().strftime("%B %d, %Y")}</div>
            <p>This is your new blog. Start sharing your thoughts, stories, and expertise with the world. 
            Create engaging content that resonates with your audience and builds a community around your passion.</p>
            <a href="#" class="read-more">Read more →</a>
        </article>
        
        <article class="post">
            <h2>Getting Started</h2>
            <div class="post-meta">Posted on {datetime.now().strftime("%B %d, %Y")}</div>
            <p>Welcome to your blogging journey! This template provides a clean, readable design perfect for 
            sharing your ideas. Customize it to match your style and start publishing amazing content.</p>
            <a href="#" class="read-more">Read more →</a>
        </article>
    </div>
</body>
</html>'''

    def generate_landing_template(self, data):
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica', Arial, sans-serif; }}
        .hero {{
            height: 100vh;
            background: linear-gradient(135deg, {data['color']} 0%, {data['color']}cc 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
        }}
        .hero h1 {{ font-size: 4rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.5rem; margin-bottom: 2rem; max-width: 600px; }}
        .cta {{
            display: inline-block;
            padding: 1.5rem 3rem;
            background: white;
            color: {data['color']};
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        .cta:hover {{ transform: translateY(-3px); }}
        .features {{
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }}
        .feature {{
            text-align: center;
            padding: 2rem;
        }}
        .feature-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <section class="hero">
        <div>
            <h1>{data['name']}</h1>
            <p>{data['description']}</p>
            <a href="#{data['email']}" class="cta">Get Started Now</a>
        </div>
    </section>
    
    <section class="features">
        {' '.join([f'<div class="feature"><div class="feature-icon">⭐</div><h3>{f}</h3></div>' for f in data['features']])}
    </section>
</body>
</html>'''