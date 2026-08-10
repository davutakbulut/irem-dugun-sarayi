import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the exact duplicate dangling code block between line 7865 and line 8040
dangling_start_marker = "            )}\n          </div>\n        </div>\n      );\n    }\n      const [step, setStep] = useState(1);"
clean_replacement = "            )}\n          </div>\n        </div>\n      );\n    }"

if dangling_start_marker in content:
    # Find the end of the dangling duplicate block right before "// ISOLATED BLOCK ERROR BOUNDARY"
    block_boundary_marker = "    // ISOLATED BLOCK ERROR BOUNDARY"
    start_pos = content.find(dangling_start_marker)
    end_pos = content.find(block_boundary_marker, start_pos)

    if start_pos != -1 and end_pos != -1:
        content = content[:start_pos + len("            )}\n          </div>\n        </div>\n      );\n    }")] + "\n\n" + content[end_pos:]
        print("Successfully removed dangling duplicate LeadModal code block!")
    else:
        print("Could not locate boundaries for dangling block.")
else:
    print("dangling_start_marker not found directly, using string slicing search...")
    # Alternative precise search
    pattern = "      const [step, setStep] = useState(1);\n      const [formData, setFormData] = useState({\n        eventType: defaultEventType,\n        guests: 400,"
    p_pos = content.find(pattern)
    b_pos = content.find("    // ISOLATED BLOCK ERROR BOUNDARY")
    if p_pos != -1 and b_pos != -1 and p_pos < b_pos:
        content = content[:p_pos] + content[b_pos:]
        print("Successfully removed dangling duplicate LeadModal code block via pattern matching!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
