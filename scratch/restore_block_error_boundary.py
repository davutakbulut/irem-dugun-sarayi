import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

block_error_boundary_code = """
    // ISOLATED BLOCK ERROR BOUNDARY (SINGLE BLOCK FAULT ISOLATION)
    class BlockErrorBoundary extends React.Component {
      constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
      }
      static getDerivedStateFromError(error) {
        return { hasError: true, error };
      }
      componentDidCatch(error, errorInfo) {
        console.warn(`[PublicBlock:${this.props.blockName || 'Block'}] Error isolated:`, error, errorInfo);
      }
      render() {
        if (this.state.hasError) {
          return this.props.fallback || (
            <div className="w-full p-4 my-2 rounded-2xl bg-amber-500/5 border border-amber-500/20 text-center text-xs text-slate-500">
              <span>⚠️ {this.props.blockName || 'Bu Modül'} geçici olarak gösterilemiyor.</span>
            </div>
          );
        }
        return this.props.children;
      }
    }
"""

marker = "    // 3. PUBLIC LAYOUT MODULE (ISOLATED NAVBAR & FOOTER BLOCKS)"
marker_idx = content.find(marker)

if marker_idx != -1:
    content = content[:marker_idx] + block_error_boundary_code + "\n" + content[marker_idx:]
    print("Successfully restored BlockErrorBoundary before PublicLayout!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
