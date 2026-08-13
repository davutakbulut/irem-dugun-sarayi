with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

bad_route = "app.all(['/api/draft-reservations', '/api/draft-reservations/*', '/api/draft-reservations-delete/*'], (req, res) => {"
good_route = "app.use(['/api/draft-reservations', '/api/draft-reservations-delete'], (req, res) => {"

if bad_route in code:
    code = code.replace(bad_route, good_route)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed express 5 route in server.js!")
else:
    print("bad_route not found!")
