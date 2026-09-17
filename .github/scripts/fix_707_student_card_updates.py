from pathlib import Path

p = Path('707-shirt/index.html')
t = p.read_text(encoding='utf-8')

start = 'function renderStudents()'
end = 'function renderTeachers()'
if start not in t or end not in t:
    raise SystemExit('student renderer markers not found')

a = t.index(start)
b = t.index(end, a)

replacement = r'''function studentHTML(s,i){return `<details class="student" id="stu-${i}"><summary><div class="seat">${esc(s.no)}</div><div><div class="name">${esc(s.name||'尚未填姓名')}</div><div class="meta">${s.size?'尺寸 '+esc(s.size):'未選尺寸'}${s.fit?' · '+esc(s.fit):''} · 加購 ${extraCount(s)} 件</div></div><div class="money">${money(studentTotal(s))}</div></summary><div class="body"><div class="grid"><label><span>姓名</span><input value="${esc(s.name)}" onchange="setS(${i},'name',this.value)"></label><label><span>座號</span><input value="${esc(s.no)}" onchange="setS(${i},'no',this.value)"></label><label><span>身高 cm</span><input type="number" step=".1" value="${esc(s.height)}" onchange="setS(${i},'height',this.value)"></label><label><span>體重 kg</span><input type="number" step=".1" value="${esc(s.weight)}" onchange="setS(${i},'weight',this.value)"></label><label><span>學生尺寸</span><select onchange="setS(${i},'size',this.value)">${opts(SIZES,s.size)}</select></label><label><span>量套感受</span><select onchange="setS(${i},'fit',this.value)">${opts(FITS,s.fit)}</select></label></div><div style="margin-top:12px"><b>本人 / 家庭加購</b> <span class="badge">${extraCount(s)} 件</span></div>${s.extras.map((e,j)=>`<div class="extra"><div class="extrahead"><b>${esc(e.relation||'加購')}</b><button class="btn red" style="min-height:34px;padding:6px 9px" onclick="event.preventDefault();removeStudentExtra(${i},${j})">刪除</button></div><div class="grid"><label><span>關係</span><select onchange="setE(${i},${j},'relation',this.value)">${opts(RELS,e.relation)}</select></label><label><span>稱呼（可空白）</span><input value="${esc(e.label||'')}" onchange="setE(${i},${j},'label',this.value)"></label><label><span>尺寸</span><select onchange="setE(${i},${j},'size',this.value)">${opts(SIZES,e.size)}</select></label><label><span>合身度</span><select onchange="setE(${i},${j},'fit',this.value)">${opts(FITS,e.fit)}</select></label><label><span>件數</span><input type="number" min="1" value="${e.qty||1}" onchange="setE(${i},${j},'qty',this.value)"></label></div></div>`).join('')}<div class="toolbar"><button class="btn secondary" onclick="event.preventDefault();addStudentExtra(${i})">＋ 新增加購</button></div></div></details>`}
function renderStudents(){$('students').innerHTML=state.students.map((s,i)=>studentHTML(s,i)).join('')}
function refreshStudentDerived(){renderStats();renderSummary();renderAnonymous();renderFamilyRows();renderPrintList();save()}
function renderStudentOnly(i){
  const oldEl=$('stu-'+i);
  if(!oldEl){renderStudents();refreshStudentDerived();return}
  const y=window.scrollY;
  if(document.activeElement&&typeof document.activeElement.blur==='function')document.activeElement.blur();
  oldEl.outerHTML=studentHTML(state.students[i],i);
  const d=$('stu-'+i);if(d)d.open=true;
  window.scrollTo(0,y);
  requestAnimationFrame(()=>{window.scrollTo(0,y);requestAnimationFrame(()=>window.scrollTo(0,y))});
  refreshStudentDerived();
}
function addStudentExtra(i){state.students[i].extras.push({id:uid(),relation:'本人加購',label:'',size:'',fit:'',qty:1});renderStudentOnly(i)}
function removeStudentExtra(i,j){state.students[i].extras.splice(j,1);renderStudentOnly(i)}
function renderKeep(i){renderStudentOnly(i)}
function setS(i,k,v){state.students[i][k]=v;renderStudentOnly(i)}
function setE(i,j,k,v){state.students[i].extras[j][k]=v;renderStudentOnly(i)}
'''

t = t[:a] + replacement + t[b:]
p.write_text(t, encoding='utf-8')
print('patched student card updates to avoid full-list rerenders')
