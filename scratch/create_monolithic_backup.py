import subprocess
import shutil
import os

# 1. Fetch exact working index.html from commit 900f015
html_900f015 = subprocess.check_output(['git', 'show', '900f015:index.html']).decode('utf-8')

# Fix ProfileComponent missing closing brace in 900f015
old_profile_end = """            <div className="pt-2 flex justify-end">
              <button type="submit" className="gold-button font-bold px-6 py-3 rounded-2xl text-xs shadow-lg hover:scale-105 transition">
                Değişiklikleri Kaydet ✓
              </button>
            </div>
          </form>
        </div>
      );
    // --- 10. GÖRÜNÜM & TEMA AYARLARI (MODULAR SETTINGS PAGE) ---"""

new_profile_end = """            <div className="pt-2 flex justify-end">
              <button type="submit" className="gold-button font-bold px-6 py-3 rounded-2xl text-xs shadow-lg hover:scale-105 transition">
                Değişiklikleri Kaydet ✓
              </button>
            </div>
          </form>
        </div>
      );
    }

    // --- 10. GÖRÜNÜM & TEMA AYARLARI (MODULAR SETTINGS PAGE) ---"""

fixed_html = html_900f015.replace(old_profile_end, new_profile_end)

# Save backup to project workspace
backup_path_workspace = "index_monolithic_backup.html"
with open(backup_path_workspace, "w", encoding="utf-8") as f:
    f.write(fixed_html)

print(f"✅ Workspace backup created: {backup_path_workspace} ({len(fixed_html.splitlines())} lines)")

# Save backup to artifact scratch directory as well
artifact_scratch_dir = "/Users/davutakbulut/.gemini/antigravity/brain/f60111cc-5bec-4b99-8da2-93a0a75c00b9/scratch"
os.makedirs(artifact_scratch_dir, exist_ok=True)
backup_path_artifact = os.path.join(artifact_scratch_dir, "index_monolithic_backup.html")
with open(backup_path_artifact, "w", encoding="utf-8") as f:
    f.write(fixed_html)

print(f"✅ Artifact scratch backup created: {backup_path_artifact}")
