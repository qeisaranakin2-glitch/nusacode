import { useState } from 'react';
import { Activity, Braces, Bug, Check, ChevronDown, CircleHelp, Code2, Command, Cpu, FileCode2, Github, Play, RotateCcw, Terminal, Zap } from 'lucide-react';

const starter = `# Selamat datang di NusaCode Studio
LET nama = "Qeisar";
LET umur = 21;

PRINT "Halo, " + nama;
PRINT "Tahun depan umur kamu:";
PRINT umur + 1;`;

const examples = {
  "Perkenalan": starter,
  "Kalkulator": `LET angka1 = 25;
LET angka2 = 5;
LET hasil = angka1 * angka2 + 10;
PRINT "Hasil perhitungan:";
PRINT hasil;`,
  "Ekspresi": `LET a = 10;
LET b = 3;
PRINT (a + b) * 2;
PRINT a / b;`,
  "Error demo": `PRINT variabelBelumAda;`
};

export default function App() {
  const [code, setCode] = useState(starter);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('output');
  const [busy, setBusy] = useState(false);
  const [example, setExample] = useState('Perkenalan');

  async function compile() {
    setBusy(true);
    setActiveTab('output');
    try {
      const response = await fetch('http://127.0.0.1:5000/api/compile', {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({code})
      });
      const data = await response.json();
      setResult(data);
    } catch {
      setResult({success:false, error:{stage:'Connection', message:'Backend Python tidak terhubung. Jalankan Flask pada port 5000.', line:1, column:1}});
    } finally { setBusy(false); }
  }

  function loadExample(name) { setExample(name); setCode(examples[name]); setResult(null); }
  const tabs = [
    ['output','Output'], ['tokens','Tokens'], ['ast','AST'], ['symbols','Symbol Table'], ['ir','Intermediate Code']
  ];

  return <div className="app-shell">
    <header className="topbar">
      <div className="brand"><div className="brand-mark"><Braces size={21}/></div><div><b>NusaCode<span>.</span></b><small>STUDIO / MINI COMPILER</small></div></div>
      <div className="top-center"><span className="live-dot"/> COMPILER ENVIRONMENT <span className="top-version">v1.0.0</span></div>
      <div className="top-actions"><span className="python-pill"><span/> PYTHON ENGINE</span><a className="icon-link" href="https://github.com" target="_blank" rel="noreferrer"><Github size={17}/></a></div>
    </header>

    <main className="workspace">
      <section className="welcome">
        <div><div className="eyebrow"><Zap size={13}/> YOUR FIRST LANGUAGE, YOUR RULES</div><h1>Build ideas.<br/><span>Compile them.</span></h1><p>Eksperimen dengan NusaLang, bahasa pemrograman mini yang dibangun dengan compiler Python.</p></div>
        <div className="welcome-stats"><div><span>01</span><b>Lexical</b><small>Tokenization</small></div><div><span>02</span><b>Syntax</b><small>AST Parsing</small></div><div><span>03</span><b>Semantic</b><small>Type checking</small></div><div><span>04</span><b>Runtime</b><small>Execution</small></div></div>
      </section>

      <section className="studio-card">
        <div className="studio-head"><div className="file-title"><FileCode2 size={16}/><b>main.nusa</b><span className="unsaved-dot"/></div><div className="head-right"><span className="language-label">NUSALANG</span><button className="run-btn" onClick={compile} disabled={busy}>{busy ? <Activity size={15} className="spin"/> : <Play size={15} fill="currentColor"/>}{busy?'Compiling...':'Compile & Run'} <kbd>Ctrl ↵</kbd></button></div></div>
        <div className="editor-toolbar"><div className="crumb"><span>workspace</span><span>/</span><b>main.nusa</b></div><div className="toolbar-right"><label className="example-select">Examples <ChevronDown size={13}/><select value={example} onChange={e=>loadExample(e.target.value)}>{Object.keys(examples).map(x=><option key={x}>{x}</option>)}</select></label><button className="subtle-btn" onClick={()=>{setCode('');setResult(null)}}><RotateCcw size={13}/> Clear</button><button className="subtle-btn" onClick={()=>{setCode(starter);setResult(null)}}>Reset</button></div></div>
        <div className="editor-wrap"><div className="line-numbers">{code.split('\n').map((_,i)=><div key={i}>{String(i+1).padStart(2,'0')}</div>)}</div><textarea spellCheck="false" aria-label="NusaLang code editor" value={code} onChange={e=>setCode(e.target.value)} onKeyDown={e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();compile()} if(e.key==='Tab'){e.preventDefault();const s=e.target.selectionStart;const end=e.target.selectionEnd;const next=code.slice(0,s)+'  '+code.slice(end);setCode(next);requestAnimationFrame(()=>{e.target.selectionStart=e.target.selectionEnd=s+2})}}} placeholder="Tulis kode NusaLang di sini..."/></div>
        <div className="editor-foot"><span><span className="green-dot"/> Ready</span><span>UTF-8&nbsp;&nbsp; • &nbsp;&nbsp;NusaLang&nbsp;&nbsp; • &nbsp;&nbsp;{code.split('\n').length} lines</span></div>
      </section>

      <section className="result-card">
        <div className="result-heading"><div><Terminal size={17}/><b>Compiler Console</b></div><div className="console-state">{result ? result.success ? <><span className="green-dot"/> COMPILE SUCCESS</> : <><span className="red-dot"/> COMPILE ERROR</> : 'AWAITING EXECUTION'}</div></div>
        <div className="tab-bar">{tabs.map(([id,label])=><button key={id} className={activeTab===id?'active':''} onClick={()=>setActiveTab(id)}>{label}{id==='output'&&result?.success&&<span className="tab-count">{result.output?.length||0}</span>}{id==='tokens'&&result?.success&&<span className="tab-count">{result.tokens?.length||0}</span>}</button>)}</div>
        <div className="console-content">
          {!result && <div className="empty-state"><div className="empty-icon"><Command size={22}/></div><b>Console is ready</b><p>Tekan <strong>Compile & Run</strong> untuk memproses program pertamamu.</p></div>}
          {result && !result.success && <div className="error-panel"><div className="error-icon"><Bug size={17}/></div><div><b>{result.error?.stage || 'Error'} Error</b><p>{result.error?.message}</p><small>Line {result.error?.line} · Column {result.error?.column}</small></div></div>}
          {result?.success && activeTab==='output' && <div className="output-view"><div className="success-line"><Check size={14}/> Program executed successfully</div>{result.output.length ? result.output.map((line,i)=><div className="output-line" key={i}><span>{String(i+1).padStart(2,'0')}</span>{line}</div>) : <div className="muted">Program selesai tanpa output.</div>}</div>}
          {result?.success && activeTab==='tokens' && <div className="table-scroll"><table><thead><tr><th>#</th><th>TYPE</th><th>VALUE</th><th>POSITION</th></tr></thead><tbody>{result.tokens.map((t,i)=><tr key={i}><td>{i+1}</td><td><span className="token-type">{t.type}</span></td><td className="mono">{String(t.value)}</td><td>{t.line}:{t.column}</td></tr>)}</tbody></table></div>}
          {result?.success && activeTab==='ast' && <pre className="json-view">{JSON.stringify(result.ast,null,2)}</pre>}
          {result?.success && activeTab==='symbols' && <div className="table-scroll"><table><thead><tr><th>VARIABLE</th><th>TYPE</th><th>VALUE</th></tr></thead><tbody>{result.symbolTable.map((s,i)=><tr key={i}><td className="mono">{s.name}</td><td><span className="token-type">{s.type}</span></td><td className="mono">{String(s.value)}</td></tr>)}</tbody></table>{!result.symbolTable.length&&<div className="muted">Tidak ada variabel.</div>}</div>}
          {result?.success && activeTab==='ir' && <div className="ir-view">{result.intermediateCode.map((line,i)=><div key={i}><span>{String(i+1).padStart(2,'0')}</span><code>{line}</code></div>)}</div>}
        </div>
      </section>

      <section className="pipeline"><div className="section-title"><div><Cpu size={16}/><b>Compiler Pipeline</b></div><span>HOW NUSACODE WORKS</span></div><div className="pipeline-grid">{[['01','Lexical Analysis','Memecah kode menjadi token.'],['02','Syntax Analysis','Menyusun token menjadi AST.'],['03','Semantic Analysis','Memvalidasi variabel dan tipe.'],['04','Intermediate Code','Membuat instruksi perantara.'],['05','Execution','Menjalankan AST dan mencetak output.']].map(([n,t,d],i)=><div className="pipeline-step" key={n}><span>{n}</span><b>{t}</b><small>{d}</small>{i<4&&<i>→</i>}</div>)}</div></section>
      <footer><div className="footer-brand"><Braces size={15}/> NUSACODE STUDIO</div><span>Built for learning compiler design · Python-powered</span><span>© 2026</span></footer>
    </main>
  </div>;
}
