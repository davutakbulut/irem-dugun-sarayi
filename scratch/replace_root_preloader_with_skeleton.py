import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_loader_block = """  <div id="root">
    <!-- ELEGANT THEME-AWARE PRE-LOADER (ZERO VISUAL LAYOUT SHIFT OR FOUC) -->
    <div id="initial-app-loader" style="min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background: var(--color-bg, #faf9f6); transition: opacity 0.25s ease-out;">
      <div style="width: 52px; height: 52px; border: 3px solid rgba(217, 119, 6, 0.2); border-top-color: #d97706; border-radius: 50%; animation: spin-loader 0.75s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;"></div>
      <div style="margin-top: 18px; font-weight: 800; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; color: #d97706; font-family: system-ui, -apple-system, sans-serif;">İREM DÜĞÜN SARAYI</div>
      <style>@keyframes spin-loader { to { transform: rotate(360deg); } }</style>
    </div>
  </div>"""

# Instant Skeleton UI Layout for Frame-1 Zero-Flicker Rendering
new_skeleton_block = """  <div id="root">
    <!-- INSTANT SKELETON PRE-RENDER (FRAME-1 INSTANT UI - ZERO BLOCKING SPINNER) -->
    <div style="min-height: 100vh; display: flex; flex-direction: column; background: #faf9f6; font-family: 'Inter', system-ui, sans-serif;">
      <!-- TOP HEADER SKELETON -->
      <div style="height: 64px; border-bottom: 1px solid #e2e8f0; background: #ffffff; display: flex; align-items: center; justify-content: space-between; padding: 0 24px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 36px; height: 36px; border-radius: 12px; background: linear-gradient(135deg, #f59e0b, #d97706);"></div>
          <div style="height: 18px; width: 160px; border-radius: 6px; background: #e2e8f0;" class="skeleton-shimmer"></div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="height: 36px; width: 100px; border-radius: 12px; background: #f1f5f9;" class="skeleton-shimmer"></div>
          <div style="width: 36px; height: 36px; border-radius: 50%; background: #e2e8f0;" class="skeleton-shimmer"></div>
        </div>
      </div>

      <!-- MAIN BODY WITH SIDEBAR & CONTENT SKELETON -->
      <div style="flex: 1; display: flex;">
        <!-- SIDEBAR SKELETON -->
        <div style="width: 240px; border-right: 1px solid #e2e8f0; background: #ffffff; padding: 20px; display: flex; flex-direction: column; gap: 12px;">
          <div style="height: 12px; width: 80px; background: #e2e8f0; border-radius: 4px;" class="skeleton-shimmer"></div>
          <div style="height: 38px; width: 100%; background: #fef3c7; border-radius: 10px;" class="skeleton-shimmer"></div>
          <div style="height: 38px; width: 100%; background: #f8fafc; border-radius: 10px;" class="skeleton-shimmer"></div>
          <div style="height: 38px; width: 100%; background: #f8fafc; border-radius: 10px;" class="skeleton-shimmer"></div>
          <div style="height: 12px; width: 100px; background: #e2e8f0; border-radius: 4px; margin-top: 10px;" class="skeleton-shimmer"></div>
          <div style="height: 38px; width: 100%; background: #f8fafc; border-radius: 10px;" class="skeleton-shimmer"></div>
          <div style="height: 38px; width: 100%; background: #f8fafc; border-radius: 10px;" class="skeleton-shimmer"></div>
        </div>

        <!-- CONTENT SKELETON -->
        <div style="flex: 1; padding: 24px; display: flex; flex-direction: column; gap: 20px;">
          <!-- BANNER SKELETON -->
          <div style="height: 100px; width: 100%; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 20px; display: flex; flex-direction: column; gap: 10px;">
            <div style="height: 22px; width: 220px; background: #e2e8f0; border-radius: 6px;" class="skeleton-shimmer"></div>
            <div style="height: 14px; width: 340px; background: #f1f5f9; border-radius: 4px;" class="skeleton-shimmer"></div>
          </div>

          <!-- CARDS GRID SKELETON -->
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
            <div style="height: 90px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 8px;" class="skeleton-shimmer"></div>
            <div style="height: 90px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 8px;" class="skeleton-shimmer"></div>
            <div style="height: 90px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 8px;" class="skeleton-shimmer"></div>
            <div style="height: 90px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 8px;" class="skeleton-shimmer"></div>
          </div>

          <!-- TABLE SKELETON -->
          <div style="flex: 1; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 20px; display: flex; flex-direction: column; gap: 12px;">
            <div style="height: 40px; width: 100%; background: #f8fafc; border-radius: 10px;" class="skeleton-shimmer"></div>
            <div style="height: 48px; width: 100%; background: #f1f5f9; border-radius: 10px;" class="skeleton-shimmer"></div>
            <div style="height: 48px; width: 100%; background: #f8fafc; border-radius: 10px;" class="skeleton-shimmer"></div>
            <div style="height: 48px; width: 100%; background: #f1f5f9; border-radius: 10px;" class="skeleton-shimmer"></div>
          </div>
        </div>
      </div>
    </div>
  </div>"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_loader_block in content:
        content = content.replace(old_loader_block, new_skeleton_block)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Replaced pre-loader with instant skeleton layout in {h_file}")
    else:
        print(f"old_loader_block not found in {h_file}")

print("Pre-loader spinner successfully replaced across all HTML files!")
