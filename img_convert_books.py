from html2pdf import HTMLToPDF

HTML = """
    <!DOCTYPE html>
    <html>
        <body>
        <h1>Hello World</h1>
        </body>
    </html>
"""

h = HTMLToPDF(HTML, asd.pdf)
