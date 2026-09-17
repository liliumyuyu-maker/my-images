from pathlib import Path

p = Path('707-shirt/index.html')
t = p.read_text(encoding='utf-8')

# 1) Make the teacher/family purchase area extensible without changing saved data.
old = '<div class="card"><h2>老師自行購買</h2><div id="teachers"></div></div>'
new = '<div class="card"><h2>老師 / 家人自行購買</h2><div class="note">這裡不限兩筆。可新增先生、媽媽、小孩或其他家人；每一筆都依 432 元 / 件計算。</div><div id="teachers"></div><div class="toolbar"><button class="btn secondary" onclick="addTeacherOrder()">＋ 新增老師 / 家人購買</button></div></div>'
if old in t:
    t = t.replace(old, new, 1)

# 2) Remove fixed “2 件” wording from summaries.
t = t.replace('<small>老師另購</small><b id="stTeacher">2</b>', '<small>老師 / 家人另購</small><b id="stTeacher">2</b>', 1)
t = t.replace('<small>老師 2 件</small><b id="mTeacher">$0</b>', '<small>老師 / 家人另購</small><b id="mTeacher">$0</b>', 1)
t = t.replace('<th>老師</th><th>合計</th>', '<th>老師 / 家人</th><th>合計</th>', 1)

# 3) Replace only the teacher-row renderer, adding a delete button and a safe add function.
start = 'function renderTeachers()'
end = 'function renderStats()'
if start in t and end in t:
    a = t.index(start)
    b = t.index(end, a)
    replacement = '''function renderTeachers(){$('teachers').innerHTML=state.teachers.map((e,i)=>`<div class="teacherrow"><div class="grid"><label><span>對象</span><input value="${esc(e.label||'')}" placeholder="例如：老師的媽媽" onchange="state.teachers[${i}].label=this.value;render()"></label><label><span>尺寸</span><select onchange="state.teachers[${i}].size=this.value;render()">${opts(SIZES,e.size)}</select></label><label><span>合身度</span><select onchange="state.teachers[${i}].fit=this.value;render()">${opts(FITS,e.fit)}</select></label><label><span>件數</span><input type="number" min="1" value="${e.qty||1}" onchange="state.teachers[${i}].qty=this.value;render()"></label><button class="btn red" style="align-self:end" onclick="removeTeacherOrder(${i})">刪除這筆</button></div></div>`).join('')||'<div class="note">尚未新增老師 / 家人購買。</div>'}
function addTeacherOrder(){state.teachers.push({id:uid(),label:'',size:'',fit:'',qty:1});render()}
function removeTeacherOrder(i){if(!confirm('確定刪除這筆老師 / 家人購買嗎？'))return;state.teachers.splice(i,1);render()}
'''
    t = t[:a] + replacement + t[b:]

p.write_text(t, encoding='utf-8')
print('patched teacher/family rows')
