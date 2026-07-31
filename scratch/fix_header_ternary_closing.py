with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_closing = """                />
              )}
            </header>
          )}"""

good_closing = """                />
              )}
            </header>
          ))}"""

if bad_closing in html:
    html = html.replace(bad_closing, good_closing)
    print("Fixed closing parenthesis for ternary header condition!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
