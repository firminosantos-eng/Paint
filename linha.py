<!DOCTYPE html>
<!-- saved from url=(0077)https://ayoshiaki.github.io/ufs-disciplinas/programacao-a/2026-1-T05/projeto/ -->
<html lang="pt-BR"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Projeto — Projeto Paint | Material Didático</title>
  <link rel="stylesheet" href="./linha_files/main.css">
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="https://ayoshiaki.github.io/ufs-disciplinas/" class="header-brand">
        <div class="header-avatar">UFS</div>
        <div>
          <div class="header-name">Prof. Dr. André Yoshiaki Kashiwabara</div>
          <div class="header-dept">DCOMP · Universidade Federal de Sergipe</div>
        </div>
      </a>
      <nav class="header-nav">
        <a href="https://ayoshiaki.github.io/ufs-disciplinas/">Disciplinas</a>
      </nav>
    </div>
  </header>

  <div class="yellow-bar"></div>

  <main class="site-main">
    <div class="content-wrapper">
      <nav class="breadcrumb">
  <a href="https://ayoshiaki.github.io/ufs-disciplinas/">Disciplinas</a>
  <span class="breadcrumb-sep">›</span>
  <a href="https://ayoshiaki.github.io/ufs-disciplinas/programacao-a">COMP0496 — Programação A</a>
  <span class="breadcrumb-sep">›</span>
  <a href="https://ayoshiaki.github.io/ufs-disciplinas/programacao-a/2026-1-T05">Turma 5 · 2026/1</a>
  <span class="breadcrumb-sep">›</span>
  <span>Projeto</span>
</nav>

<h1 class="page-title">Projeto — Projeto Paint</h1>
<p class="page-subtitle">Um programa estilo <em>paint</em> em Python com Tkinter, evoluindo de imperativo para OO/MVC ao longo de 7 entregas</p>

<div class="table-card">
  <div class="table-card-header">📋 Enunciado</div>
  <table>
    <tbody>
      <tr>
        <td><strong>Descrição do projeto — entregas, datas e tags Git</strong></td>
        <td class="td-right"><a class="badge-colab" href="https://colab.research.google.com/github/ayoshiaki/ufs-disciplinas/blob/main/programacao-a/2026-1-T05/projeto/descricao.ipynb">▶ Abrir no Colab</a></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="table-card">
  <div class="table-card-header">💻 Código de referência</div>
  <table>
    <tbody>
      <tr>
        <td><strong>01-linha.py</strong> — uma única linha por vez</td>
        <td class="td-right"><a class="badge-code" href="https://github.com/ayoshiaki/ufs-disciplinas/blob/main/programacao-a/2026-1-T05/projeto/01-linha.py">🗂 Ver código</a></td>
      </tr>
      <tr>
        <td><strong>02-linhas.py</strong> — várias linhas acumuladas</td>
        <td class="td-right"><a class="badge-code" href="https://github.com/ayoshiaki/ufs-disciplinas/blob/main/programacao-a/2026-1-T05/projeto/02-linhas.py">🗂 Ver código</a></td>
      </tr>
      <tr>
        <td><strong>03-linhasERabiscos.py</strong> — base entregue aos alunos</td>
        <td class="td-right"><a class="badge-code" href="https://github.com/ayoshiaki/ufs-disciplinas/blob/main/programacao-a/2026-1-T05/projeto/03-linhasERabiscos.py">🗂 Ver código</a></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="prose">

  <h1 id="projeto-paint--programao-a-2026-1">Projeto Paint — Programação A 2026-1</h1>

  <p>Projeto da disciplina <strong>Programação A (2026-1)</strong> — DCOMP/UFS.</p>

  <p>Este exercício foi desenvolvido por Dr. Giovanny Fernando Lucero Palma, e utilizado por docentes desta disciplina.</p>

  <p>Dr. André Yoshiaki Kashiwabara adaptou o exercício para a turma T05 de 2026/01.</p>

  <p>Um programa do tipo <em>paint</em> em Python com Tkinter, no estilo das aplicações
Google Drawings e LibreOffice Draw. O projeto parte de uma implementação
imperativa simples e evolui, ao longo de 7 entregas, para uma arquitetura
Orientada a Objetos com MVC e padrões de projeto.</p>

  <p>O enunciado completo, com as entregas, datas e tags Git,
está em <a href="https://ayoshiaki.github.io/ufs-disciplinas/programacao-a/2026-1-T05/projeto/descricao.ipynb"><code class="language-plaintext highlighter-rouge">descricao.ipynb</code></a>.</p>

  <h2 id="requisitos">Requisitos</h2>

  <ul>
    <li>Python 3.10 ou superior.</li>
    <li>Tkinter (incluído na maioria das instalações de Python; no Linux pode exigir
o pacote <code class="language-plaintext highlighter-rouge">python3-tk</code>).</li>
  </ul>

  <p>Para conferir se o Tkinter está disponível:</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>python <span class="nt">-m</span> tkinter
</code></pre></div>  </div>

  <h2 id="como-executar">Como executar</h2>

  <p>Cada script abre uma janela própria. A partir da raiz do projeto:</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>python 01-linha.py            <span class="c"># desenha uma única linha (apaga a anterior)</span>
python 02-linhas.py           <span class="c"># acumula várias linhas</span>
python 03-linhasERabiscos.py  <span class="c"># linhas e rabiscos, com OptionMenu (base dos alunos)</span>
</code></pre></div>  </div>

  <h2 id="mapa-dos-arquivos">Mapa dos arquivos</h2>

  <table>
    <thead>
      <tr>
        <th>Arquivo</th>
        <th>Descrição</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code class="language-plaintext highlighter-rouge">descricao.ipynb</code></td>
        <td>Enunciado completo do projeto (entregas, datas).</td>
      </tr>
      <tr>
        <td><code class="language-plaintext highlighter-rouge">01-linha.py</code></td>
        <td>Referência imperativa: uma única linha por vez.</td>
      </tr>
      <tr>
        <td><code class="language-plaintext highlighter-rouge">02-linhas.py</code></td>
        <td>Referência imperativa: várias linhas acumuladas.</td>
      </tr>
      <tr>
        <td><code class="language-plaintext highlighter-rouge">03-linhasERabiscos.py</code></td>
        <td><strong>Base entregue aos alunos</strong> — linhas e rabiscos, imperativo.</td>
      </tr>
    </tbody>
  </table>

</div>

    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <span>Universidade Federal de Sergipe · DCOMP</span>
      <span>Publicado com Jekyll · <a href="https://github.com/ayoshiaki/ufs-disciplinas">GitHub</a></span>
    </div>
  </footer>



</body></html>