with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_tag = '<main role="main" className={`flex-1 p-3 pb-4 sm:p-6 sm:pb-6 lg:p-8 lg:pb-6 min-w-0 w-full max-w-full overflow-x-hidden ${isPublicGuestRoute ? "pt-20" : ""}`}'
good_tag = '<main role="main" className={`flex-1 p-3 pb-4 sm:p-6 sm:pb-6 lg:p-8 lg:pb-6 min-w-0 w-full max-w-full overflow-x-hidden ${isPublicGuestRoute ? "pt-20" : ""}`}>'

if bad_tag in html:
    html = html.replace(bad_tag, good_tag)
    print("Fixed missing closing bracket > on main tag!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
