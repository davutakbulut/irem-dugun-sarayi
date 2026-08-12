import os

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_format_fn = """    function formatPhoneNumber(value) {
      if (!value) return '';
      let digits = value.replace(/\D/g, '');
      if (digits.startsWith('90') && digits.length > 10) {
        digits = digits.substring(2);
      }
      if (digits.length > 0 && !digits.startsWith('0')) {
        digits = '0' + digits;
      }
      digits = digits.substring(0, 11);
      if (digits.length <= 1) return digits;
      if (digits.length <= 4) return `${digits.substring(0, 1)} (${digits.substring(1)}`;
      if (digits.length <= 7) return `${digits.substring(0, 1)} (${digits.substring(1, 4)}) ${digits.substring(4)}`;
      if (digits.length <= 9) return `${digits.substring(0, 1)} (${digits.substring(1, 4)}) ${digits.substring(4, 7)} ${digits.substring(7)}`;
      return `${digits.substring(0, 1)} (${digits.substring(1, 4)}) ${digits.substring(4, 7)} ${digits.substring(7, 9)} ${digits.substring(9, 11)}`;
    }"""

new_format_fn = """    function formatPhoneNumber(value) {
      if (!value) return '';
      let digits = value.replace(/\D/g, '');
      if (digits.startsWith('90') && digits.length >= 11) {
        digits = digits.substring(2);
      }
      if (digits.startsWith('0') && digits.length > 1) {
        digits = digits.substring(1);
      }
      digits = digits.substring(0, 10);
      if (digits.length === 0) return '';
      if (digits.length <= 3) return `0 (${digits}`;
      if (digits.length <= 6) return `0 (${digits.substring(0, 3)}) ${digits.substring(3)}`;
      if (digits.length <= 8) return `0 (${digits.substring(0, 3)}) ${digits.substring(3, 6)} ${digits.substring(6)}`;
      return `0 (${digits.substring(0, 3)}) ${digits.substring(3, 6)} ${digits.substring(6, 8)} ${digits.substring(8, 10)}`;
    }"""

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_format_fn in content:
        content = content.replace(old_format_fn, new_format_fn)
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated formatPhoneNumber in {f_path}!")

print("Phone number formatting update finished!")
