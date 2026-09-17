from pathlib import Path

p = Path('707-shirt/index.html')
t = p.read_text(encoding='utf-8')

old = "function renderKeep(i){render();setTimeout(()=>{const d=$('stu-'+i);if(d)d.open=true},0)}"
new = "function renderKeep(i){const oldEl=$('stu-'+i),top=oldEl?oldEl.getBoundingClientRect().top:null;render();const d=$('stu-'+i);if(d)d.open=true;if(d&&top!==null)requestAnimationFrame(()=>{window.scrollBy(0,d.getBoundingClientRect().top-top)})}"

if old not in t and new not in t:
    raise SystemExit('renderKeep pattern not found; refusing unsafe patch')
if old in t:
    t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8')
print('patched student render scroll preservation')
