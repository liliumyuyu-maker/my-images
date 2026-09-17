from pathlib import Path

p = Path('707-shirt/index.html')
t = p.read_text(encoding='utf-8')

old_save = "function save(){localStorage.setItem(KEY,JSON.stringify(state))}"
new_save = """function save(){
  const raw=JSON.stringify(state);
  try{
    const old=localStorage.getItem(KEY);
    if(old&&old!==raw){
      let hist=[];
      try{hist=JSON.parse(localStorage.getItem(KEY+'_history')||'[]')}catch{}
      if(!hist.length||hist[hist.length-1]?.data!==old)hist.push({at:new Date().toISOString(),data:old});
      if(hist.length>12)hist=hist.slice(-12);
      localStorage.setItem(KEY+'_history',JSON.stringify(hist));
    }
    localStorage.setItem(KEY,raw);
  }catch(e){console.error('707 save failed',e)}
}"""
if old_save not in t:
    raise SystemExit('save() pattern not found')
t = t.replace(old_save, new_save, 1)

old_render = "function render(){renderStudents();renderTeachers();renderStats();renderSummary();renderOfficial();renderAnonymous();renderReferencePeople();renderFamilyRows();renderPrintList();save()}"
new_render = "function render(){save();renderStudents();renderTeachers();renderStats();renderSummary();renderOfficial();renderAnonymous();if($('referencePeople'))renderReferencePeople();renderFamilyRows();renderPrintList()}"
if old_render not in t:
    raise SystemExit('render() pattern not found')
t = t.replace(old_render, new_render, 1)

old_refresh = "function refreshStudentDerived(){renderStats();renderSummary();renderAnonymous();renderFamilyRows();renderPrintList();save()}"
new_refresh = "function refreshStudentDerived(){save();renderStats();renderSummary();renderAnonymous();renderFamilyRows();renderPrintList()}"
if old_refresh not in t:
    raise SystemExit('refreshStudentDerived() pattern not found')
t = t.replace(old_refresh, new_refresh, 1)

old_ref = "function renderReferencePeople(){$('referencePeople').innerHTML="
new_ref = "function renderReferencePeople(){const host=$('referencePeople');if(!host)return;host.innerHTML="
if old_ref in t:
    t = t.replace(old_ref, new_ref, 1)

old_student = "function renderStudentOnly(i){\n  const oldEl=$('stu-'+i);"
new_student = "function renderStudentOnly(i){\n  save();\n  const oldEl=$('stu-'+i);"
if old_student not in t:
    raise SystemExit('renderStudentOnly() pattern not found')
t = t.replace(old_student, new_student, 1)

p.write_text(t, encoding='utf-8')
print('patched persistence: save-before-render, guarded removed reference UI, added local history')
